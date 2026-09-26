#!/usr/bin/env python3
"""Rapatrie dans le dépôt les images encore servies par Wix.

Le site ne doit plus rien demander à Wix une fois chez Infomaniak. Ce
script relève les adresses static.wixstatic.com que cite le générateur
(outils/*.py et outils/fragments/*.html), télécharge chaque original
dans assets/images/ sous un nom lisible, puis écrit
outils/images_locales.json : adresse Wix → fichier local, dimensions,
variantes. Le générateur lit cette table pour remplacer les adresses
Wix par les fichiers du dépôt.

    python3 outils/rapatrier_images.py                  # ce qui manque
    python3 outils/rapatrier_images.py --forcer         # tout, à nouveau
    python3 outils/rapatrier_images.py --hote URL       # autre serveur

Il se relance sans risque : ce qui est déjà là n'est pas retéléchargé.
Pillow est facultatif. Présent, il relève les dimensions et ajoute des
variantes WebP de 480, 960 et 1600 px ; absent, on garde les originaux
seuls. Ensuite : python3 outils/construire.py
"""

import argparse
import glob
import html
import http.client
import importlib
import io
import json
import os
import re
import socket
import sys
import time
import unicodedata
import urllib.error
import urllib.request

try:
    from PIL import Image, ImageOps, __version__ as VERSION_PILLOW
except ImportError:  # facultatif : sans Pillow, les originaux seuls
    Image = ImageOps = VERSION_PILLOW = None

OUTILS = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(OUTILS)
sys.path.insert(0, OUTILS)

WIX = "https://static.wixstatic.com"
DOSSIER = "assets/images"
CORRESPONDANCES = os.path.join(OUTILS, "images_locales.json")

AGENT = "DSG-Renovation-rapatriement/1.0 (+https://www.dsg-renov.ch)"
DELAI = 30  # secondes d'attente, par essai
ESSAIS = 3
LARGEURS = (480, 960, 1600)
QUALITE = 80

# Le nom de chaque image, par identifiant Wix : métier, pièce, lieu, tirés
# des textes alternatifs du générateur. Une image citée à plusieurs
# endroits garde un seul nom. Une image absente de la table prend un nom
# tiré de son alt, suivi d'un bout de son identifiant.
NOMS = {
    # Rénovation complète : page, vignette, partage de l'accueil ;
    # réalisation n° 001, appartement Beaulieu.
    "2c1464_593f3a927ebd420ab56d4d306a4e6aa5~mv2.jpg":
        "renovation-appartement-sejour-cuisine-lausanne",
    # Peinture : page, vignette ; réalisation n° 005, villa de Chailly.
    "2c1464_a7cac83b91964ef7b403ba6eb333bd0b~mv2.jpg":
        "peinture-villa-degagement-cuisine-lausanne",
    # Plâtrerie, cloisons et faux plafonds : page, vignette.
    "2c1464_1f332a25fbc5404f8ea0424fc54875d2~mv2.jpg":
        "platrerie-mur-repris-appartement-lausanne",
    # Carrelage et sols : page, vignette ; rénovation de salle de bains ;
    # réalisation n° 002, duplex des Eaux-Vives (l'alt y montre une
    # baignoire : c'est une salle de bains).
    "2c1464_c44b6415607747ff9dccd68b224b3945~mv2.jpg":
        "carrelage-salle-de-bains-duplex-geneve",
    # Nettoyage : page, vignette ; remise en état d'appartement ; lot
    # cloisons ; réalisation n° 006, immeuble Rue de Bourg.
    "2c1464_59c5df800ba245e2b7dff597bb0221a4~mv2.jpg":
        "nettoyage-hall-logement-lausanne",
    # Lot faux plafonds ; chantier signature, immeuble Béthusy.
    "2c1464_a6d8829808714189a920f4d0c39660b9~mv2.jpg":
        "faux-plafond-cuisine-immeuble-bethusy-lausanne",
    # Lot revêtements muraux ; réalisation n° 004, loft de Sévelin.
    "2c1464_ab94350c74604962a66564240516acc5~mv2.jpg":
        "revetement-mural-sejour-loft-sevelin-lausanne",
    # Lot pose de sol ; réalisation n° 003, maison de Pully.
    "2c1464_ce05ed0a65a14673bd0dcfe6d34744e1~mv2.jpg":
        "pose-de-sol-cuisine-gres-cerame-pully",
    # Régies et architectes de fragments/partenaires.html.
    "2c1464_51a61ef883614cd79df85ed6455dc6e3~mv2.png": "logo-vitelli-architectes",
    "2c1464_efbfbae88bc246848f6ef1b5f1eea865~mv2.png": "logo-gerofinance-regie-du-rhone",
    "2c1464_1df3c1502edc4ed39aff38e01f7a9f5c~mv2.png": "logo-patrimonium",
    "2c1464_1557bff3aeef42d1b8c7c3430f45d23f~mv2.png": "logo-regie-privera",
    "2c1464_79208b8bb756457aae973df6e4252ab1~mv2.png": "logo-regie-de-rham",
    "2c1464_816153da3c114f20a00fba61b95b0415~mv2.png": "logo-regie-galland-et-cie",
    "2c1464_e0e4de49acaa4d66adf588419e89c526~mv2.png": "logo-groupe-bernard-nicod",
}

# Déjà remplacé dans le dépôt : signalé, jamais téléchargé, même avec
# --forcer, et absent de la table écrite.
REMPLACES = {
    # L'ancien LOGO de donnees_site.py.
    "2c1464_3db14001d9184097989203ad9a2f559e~mv2.png":
        "assets/images/logo-blanc.avif",
}

# Identifiant d'un média Wix : propriétaire, empreinte, suffixe, extension.
MEDIA = r"[0-9a-z]+_[0-9a-f]{32}(?:~mv2[_0-9a-z]*)?\.[0-9a-z]{3,4}"
# Une adresse complète, avec une éventuelle transformation (/v1/fill/…).
ADRESSE = re.compile(r"https?://static\.wixstatic\.com/media/[^\s\"'<>()\\]+",
                     re.I)
# Un identifiant seul entre guillemets : la forme IMG + "2c1464_…".
IDENTIFIANT = re.compile(r"[\"'](%s)[\"']" % MEDIA, re.I)
BALISE_IMG = re.compile(r"<img\b[^>]*>", re.I)
ATTRIBUT = re.compile(r"""\b(src|alt)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
MOTS_VIDES = {"a", "au", "aux", "avec", "d", "dans", "de", "des", "du", "en",
              "et", "l", "la", "le", "les", "pour", "sur", "un", "une"}


class Echec(Exception):
    """Un fichier qui n'a pas pu être rapatrié ; le message dit pourquoi."""


# Relevé ------------------------------------------------------------------

def inventaire():
    """Les images Wix du générateur : identifiant → adresses citées, alts."""
    images = {}
    for url, alt in (citations_importees() + citations_des_fragments()
                     + citations_du_texte()):
        media = identifiant(url)
        if not media:
            continue
        fiche = images.setdefault(media, {"urls": set(), "alts": []})
        fiche["urls"].add(url)
        if alt and alt not in fiche["alts"]:
            fiche["alts"].append(alt)
    return images


def citations_importees():
    """Les fiches du générateur, telles qu'il les voit : (adresse, alt).

    Importer prestations et services_* donne les adresses finales, IMG
    compris, sans avoir à relire la concaténation.
    """
    try:
        fiches = list(importlib.import_module("prestations").PAGES)
        for module in modules_de_lots():
            fiches += getattr(importlib.import_module(module), "SERVICES", [])
    except Exception as erreur:  # un module en travaux ne bloque pas le relevé
        print("Générateur non importable (%s) : relevé sur le texte seul."
              % erreur)
        return []
    return [(f["image"], f.get("alt")) for f in fiches
            if ADRESSE.match(f.get("image") or "")]


def citations_des_fragments():
    """Les images des fragments HTML, avec l'alt de leur balise."""
    citations = []
    for chemin in sorted(glob.glob(os.path.join(OUTILS, "fragments", "*.html"))):
        texte = lire(chemin)
        for balise in BALISE_IMG.findall(texte):
            attributs = {n.lower(): v1 or v2
                         for n, v1, v2 in ATTRIBUT.findall(balise)}
            if ADRESSE.match(attributs.get("src", "")):
                alt = html.unescape(attributs.get("alt", ""))
                citations.append((attributs["src"], alt))
        # Liens d'agrandissement, srcset : toute autre mention compte.
        citations += [(m.group(0), None) for m in ADRESSE.finditer(texte)]
    return citations


def citations_du_texte():
    """Filet de sécurité : toute adresse ou tout identifiant Wix des .py.

    Rattrape une image citée hors des fiches importées, ou un générateur
    qui ne s'importe plus. Un identifiant seul, comme dans
    IMG + "2c1464_…", est complété par l'adresse de Wix.
    """
    citations = []
    for chemin in sources_python():
        texte = lire(chemin)
        citations += [(m.group(0), None) for m in ADRESSE.finditer(texte)]
        citations += [(WIX + "/media/" + media, None)
                      for media in IDENTIFIANT.findall(texte)]
    return citations


def sources_python():
    """Les modules du générateur, sauf ce script, qui cite toute la table."""
    moi = os.path.abspath(__file__)
    return [p for p in sorted(glob.glob(os.path.join(OUTILS, "*.py")))
            if os.path.abspath(p) != moi]


def modules_de_lots():
    """services_finitions, services_gros_oeuvre… : les fiches de lot."""
    return [os.path.splitext(os.path.basename(p))[0]
            for p in sorted(glob.glob(os.path.join(OUTILS, "services_*.py")))]


def identifiant(url):
    """L'identifiant du média : le premier segment après /media/."""
    trouve = re.match(MEDIA, url.split("/media/", 1)[-1], re.I)
    return trouve.group(0) if trouve else None


def lire(chemin):
    """Le texte d'une source du générateur."""
    with io.open(chemin, encoding="utf-8", errors="replace") as f:
        return f.read()


# Noms --------------------------------------------------------------------

def ordre(images):
    """Celles de la table d'abord, dans son ordre ; les autres ensuite."""
    return ([m for m in NOMS if m in images]
            + sorted(m for m in images if m not in NOMS))


def nommer(medias, images):
    """Un nom de fichier par image, sans collision : la table, sinon l'alt.

    L'unicité se juge sans l'extension : les variantes d'un .jpg et d'un
    .png de même nom se marcheraient dessus.
    """
    noms, pris = {}, set()
    for media in medias:
        base = NOMS.get(media) or nom_de_repli(media, images[media]["alts"])
        nom, n = base, 2
        while nom in pris:
            nom, n = "%s-%d" % (base, n), n + 1
        pris.add(nom)
        noms[media] = nom + extension(media)
    return noms


def nom_de_repli(media, alts):
    """Pour une image hors table : l'alt en six mots, et un bout d'empreinte.

    Le bout d'empreinte garde le nom stable d'un passage à l'autre et
    distinct d'un fichier posé à la main dans assets/images/.
    """
    mots = [m for m in en_mots(alts[0] if alts else "") if m not in MOTS_VIDES]
    empreinte = media.split("_", 1)[1][:6]
    return "-".join((mots[:6] or ["image"]) + [empreinte])


def en_mots(texte):
    """« Salle d'eau carrelée » → salle, d, eau, carrelee."""
    texte = html.unescape(texte).replace("œ", "oe").replace("Œ", "Oe")
    texte = unicodedata.normalize("NFKD", texte.replace("&", " et "))
    return re.findall(r"[a-z0-9]+", texte.encode("ascii", "ignore")
                      .decode("ascii").lower())


def extension(media):
    """L'extension de l'original, en minuscules : .jpg, .png…"""
    ext = os.path.splitext(media)[1].lower()
    return ".jpg" if ext == ".jpeg" else ext


def variante(nom, largeur):
    """assets/images/<nom>-<largeur>.webp"""
    return "%s/%s-%d.webp" % (DOSSIER, os.path.splitext(nom)[0], largeur)


def local(relatif):
    """Chemin sur le disque d'un chemin du site (assets/images/…)."""
    return os.path.join(RACINE, *relatif.split("/"))


# Téléchargement ----------------------------------------------------------

def rapatrier(media, chemin, options):
    """Télécharge l'original s'il manque ; renvoie sa taille, ou None."""
    if not options.forcer and deja_la(chemin):
        return None
    octets, annonce = telecharger("%s/media/%s" % (options.hote, media))
    verifier(octets, annonce)
    ecrire_octets(chemin, octets)
    return len(octets)


def telecharger(url):
    """Le corps d'une réponse et son type annoncé, en trois essais au plus.

    Seules les pannes passagères (réseau, délai, 5xx, 429) sont
    retentées : un 404 ne changera pas d'avis en insistant.
    """
    requete = urllib.request.Request(url, headers={"User-Agent": AGENT})
    derniere = None
    for essai in range(1, ESSAIS + 1):
        try:
            with urllib.request.urlopen(requete, timeout=DELAI) as reponse:
                annonce = reponse.headers.get("Content-Type", "")
                return reponse.read(), annonce.split(";")[0].strip().lower()
        except urllib.error.HTTPError as erreur:
            if erreur.code < 500 and erreur.code not in (408, 429):
                raise Echec(raison(erreur))
            derniere = erreur
        except (urllib.error.URLError, http.client.HTTPException,
                OSError) as erreur:
            derniere = erreur
        if essai < ESSAIS:
            time.sleep(essai)
    raise Echec("%s, après %d essais" % (raison(derniere), ESSAIS))


def raison(erreur):
    """Une panne, dite en quelques mots."""
    if isinstance(erreur, urllib.error.HTTPError):
        return "HTTP %d %s" % (erreur.code, erreur.reason)
    if isinstance(erreur, http.client.IncompleteRead):
        return "réponse tronquée"
    cause = getattr(erreur, "reason", erreur)
    if isinstance(cause, socket.timeout):
        return "pas de réponse en %d s" % DELAI
    return "connexion impossible (%s)" % cause


def verifier(octets, annonce):
    """Refuse ce qui n'est pas une image : page d'erreur, portail, proxy.

    Les premiers octets tranchent ; le type annoncé sert à dire pourquoi.
    """
    if est_une_image(octets):
        return
    if not octets:
        raise Echec("réponse vide")
    if annonce and not annonce.startswith("image/"):
        raise Echec("le serveur a renvoyé %s au lieu d'une image" % annonce)
    raise Echec("reçu %s, mais les premiers octets ne sont pas ceux d'une "
                "image" % (annonce or "un contenu sans type"))


def est_une_image(octets):
    """Vrai si les premiers octets sont ceux d'une image connue."""
    debut = octets[:1024]
    if debut.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n",
                         b"GIF87a", b"GIF89a")):
        return True
    if debut[:4] == b"RIFF" and debut[8:12] == b"WEBP":
        return True
    if debut[4:8] == b"ftyp" and debut[8:12] in (b"avif", b"avis", b"mif1"):
        return True
    return b"<svg" in debut.lower() and b"<html" not in debut.lower()


def deja_la(chemin):
    """Un original présent et bien une image : on n'y touche pas."""
    try:
        with open(chemin, "rb") as f:
            return est_une_image(f.read(1024))
    except OSError:
        return False


def ecrire_octets(chemin, octets):
    """Écrit d'un coup : un fichier interrompu ne passe jamais pour « déjà là »."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    temporaire = chemin + ".part"
    with open(temporaire, "wb") as f:
        f.write(octets)
    os.replace(temporaire, chemin)


# Dimensions et variantes -------------------------------------------------

def completer(entree, chemin, nom, neuf, urls, precedent):
    """Dimensions et variantes ; renvoie les largeurs écrites à l'instant."""
    if Image is not None and not nom.endswith(".svg"):
        return mesurer(entree, chemin, nom, refaire=neuf)
    # Sans Pillow : ce qu'un passage précédent a laissé. Un identifiant Wix
    # désigne toujours le même fichier, ses mesures restent donc justes.
    reprendre(entree, urls, precedent)
    if a_decliner(nom):
        entree["variantes"] = variantes_presentes(nom)
    return []


def mesurer(entree, chemin, nom, refaire):
    """Relève les dimensions et écrit les variantes qui manquent.

    Une largeur visée plus grande que l'original est ramenée à la sienne :
    on n'agrandit jamais, et la plus grande variante existe toujours. Les
    clés de « variantes » sont donc les largeurs réelles, en pixels.
    """
    with Image.open(chemin) as image:
        entree["largeur"], entree["hauteur"] = dimensions(image)
        if not a_decliner(nom):
            return []
        cibles = sorted({min(c, entree["largeur"]) for c in LARGEURS})
        entree["variantes"] = {str(c): variante(nom, c) for c in cibles}
        a_faire = [c for c in cibles
                   if refaire or not os.path.exists(local(variante(nom, c)))]
        if a_faire:
            decliner(image, a_faire, nom)
        return a_faire


def dimensions(image):
    """Largeur et hauteur affichées : une photo tournée par l'EXIF l'est ici."""
    largeur, hauteur = image.size
    if image.getexif().get(0x0112) in (5, 6, 7, 8):
        return hauteur, largeur
    return largeur, hauteur


def decliner(image, largeurs, nom):
    """Écrit les variantes WebP, orientation EXIF appliquée d'abord.

    Les variantes ne portent pas d'EXIF : ni orientation à réappliquer,
    ni coordonnées du chantier.
    """
    profil = image.info.get("icc_profile")
    droite = en_rvb(ImageOps.exif_transpose(image))
    for largeur in largeurs:
        enregistrer_webp(droite, largeur, local(variante(nom, largeur)), profil)


def en_rvb(image):
    """WebP ne connaît que RVB et RVBA : un JPEG CMJN ou une palette y passent."""
    if image.mode in ("RGB", "RGBA"):
        return image
    transparente = image.mode in ("LA", "PA") or "transparency" in image.info
    return image.convert("RGBA" if transparente else "RGB")


def enregistrer_webp(image, largeur, chemin, profil):
    """Une variante à la largeur voulue, écrite d'un coup."""
    if largeur != image.width:
        hauteur = max(1, round(image.height * largeur / image.width))
        filtre = getattr(Image, "Resampling", Image).LANCZOS
        image = image.resize((largeur, hauteur), filtre)
    options = {"quality": QUALITE, "method": 6}
    if profil:
        options["icc_profile"] = profil
    temporaire = chemin + ".part"
    image.save(temporaire, "WEBP", **options)
    os.replace(temporaire, chemin)


def a_decliner(nom):
    """Les photographies seulement : un logo garde son seul original."""
    return (not nom.startswith("logo-")
            and nom.endswith((".jpg", ".png", ".webp")))


def variantes_presentes(nom):
    """Les variantes WebP déjà sur le disque, laissées par un passage avec Pillow."""
    motif = re.compile(re.escape(os.path.splitext(nom)[0]) + r"-(\d+)\.webp$")
    largeurs = sorted(int(m.group(1)) for m in
                      map(motif.match, os.listdir(local(DOSSIER))) if m)
    return {str(largeur): variante(nom, largeur) for largeur in largeurs}


def reprendre(entree, urls, precedent):
    """Reprend les dimensions de la table précédente, si elle les avait."""
    for url in urls:
        ancienne = precedent.get(url)
        if (isinstance(ancienne, dict)
                and ancienne.get("fichier") == entree["fichier"]):
            entree["largeur"] = ancienne.get("largeur")
            entree["hauteur"] = ancienne.get("hauteur")
            return


# Table des correspondances -----------------------------------------------

def lire_correspondances():
    """La table du passage précédent, s'il y en a eu un."""
    try:
        with io.open(CORRESPONDANCES, encoding="utf-8") as f:
            table = json.load(f)
    except (OSError, ValueError):
        return {}
    return table if isinstance(table, dict) else {}


def ecrire_correspondances(table):
    """outils/images_locales.json : adresse Wix → fichier local, trié."""
    texte = json.dumps(dict(sorted(table.items())), ensure_ascii=False,
                       indent=2)
    ecrire_octets(CORRESPONDANCES, (texte + "\n").encode("utf-8"))


# Déroulé -----------------------------------------------------------------

def traiter(media, nom, urls, options, precedent):
    """Une image de bout en bout ; renvoie son statut et son entrée."""
    chemin = local(DOSSIER + "/" + nom)
    try:
        venue = rapatrier(media, chemin, options)
    except Echec as erreur:
        print("  ✘ %s : %s" % (nom, erreur))
        return "echec", None
    entree = {"fichier": DOSSIER + "/" + nom,
              "largeur": None, "hauteur": None, "variantes": {}}
    try:
        faites = completer(entree, chemin, nom, venue is not None, urls,
                           precedent)
    except Exception as erreur:  # Pillow ne sait pas lire ce fichier
        print("  ✘ %s : rapatrié, mais illisible pour Pillow (%s)"
              % (nom, erreur))
        return "echec", entree
    dire(nom, venue, entree, faites)
    return ("deja" if venue is None else "ok"), entree


def dire(nom, venue, entree, faites):
    """Une ligne par fichier : ✔ téléchargé, · déjà là."""
    webp = "WebP " + ", ".join(map(str, faites)) if faites else ""
    if venue is None:
        suite = " — variantes %s créées" % webp if webp else ""
        print("  · déjà là : %s%s" % (nom, suite))
        return
    details = [poids(venue)]
    if entree["largeur"]:
        details.append("%d × %d" % (entree["largeur"], entree["hauteur"]))
    if webp:
        details.append(webp)
    print("  ✔ %s — %s" % (nom, " · ".join(details)))


def signaler_remplace(media):
    """Le logo Wix : déjà remplacé dans le dépôt. Renvoie 1 si c'est faux."""
    fichier = REMPLACES[media]
    if os.path.exists(local(fichier)):
        print("  · déjà remplacé : %s → %s" % (media, fichier))
        return 0
    print("  ✘ %s : devait être remplacé par %s, introuvable" % (media, fichier))
    return 1


def annoncer(nombre, options):
    """L'en-tête : combien d'images, d'où, avec ou sans Pillow."""
    print("Images Wix citées par le générateur : %d, à rapatrier dans %s/."
          % (nombre, DOSSIER))
    print("Source : %s/media/" % options.hote)
    if Image is None:
        print("Pillow absent : originaux seulement, sans dimensions ni variantes.")
    else:
        print("Pillow %s : dimensions et variantes WebP %s px."
              % (VERSION_PILLOW, ", ".join(map(str, LARGEURS))))
    print()


def conclure(comptes, adresses, hors_table):
    """Le bilan, et ce qu'il reste à faire."""
    print()
    print("Bilan : %s, %s, %s." % (accord(comptes["ok"], "téléchargée"),
                                   accord(comptes["deja"], "déjà présente"),
                                   accord(comptes["echec"], "échec")))
    print("Table écrite : outils/images_locales.json (%s)."
          % accord(adresses, "adresse"))
    if hors_table:
        print("Noms tirés de l'alt, hors table : %s. Fixez-les dans NOMS, "
              "en tête de ce script." % ", ".join(hors_table))
    if Image is None:
        print("Installez Pillow pour les tailles réduites : pip install Pillow "
              "(ou python3 -m pip install Pillow), puis relancez ce script.")
    if comptes["echec"]:
        print("Suite : relancez ce script pour reprendre les échecs (le reste "
              "ne sera pas retéléchargé), puis lancez python3 outils/construire.py")
    else:
        print("Suite : vérifiez les images dans assets/images/, "
              "puis lancez python3 outils/construire.py")


def accord(nombre, mot):
    """« 1 échec », « 2 échecs » : le pluriel commence à deux."""
    return "%d %s%s" % (nombre, mot, "s" if nombre > 1 else "")


def poids(octets):
    """« 45 Ko », « 1,2 Mo »."""
    if octets >= 1024 * 1024:
        return ("%.1f Mo" % (octets / 1048576)).replace(".", ",")
    return "%d Ko" % max(1, round(octets / 1024))


def arguments():
    """--hote et --forcer ; l'hôte perd sa barre finale."""
    parseur = argparse.ArgumentParser(
        description="Rapatrie dans assets/images/ les images encore servies "
                    "par Wix, et écrit outils/images_locales.json.")
    parseur.add_argument("--hote", default=WIX, metavar="URL",
                         help="serveur à interroger au lieu de %s "
                              "(essais)" % WIX)
    parseur.add_argument("--forcer", action="store_true",
                         help="retélécharger aussi les images déjà là")
    options = parseur.parse_args()
    if not re.match(r"https?://", options.hote):
        parseur.error("--hote attend une adresse en http:// ou https://")
    options.hote = options.hote.rstrip("/")
    return options


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # console sans « ✔ » : « ? »
    options = arguments()
    images = inventaire()
    if not images:
        print("Aucune image Wix dans le générateur : rien à rapatrier.")
        return 0
    medias = [m for m in ordre(images) if m not in REMPLACES]
    noms = nommer(medias, images)
    annoncer(len(medias), options)
    precedent = lire_correspondances()
    comptes, table = {"ok": 0, "deja": 0, "echec": 0}, {}
    for media in medias:
        urls = sorted(images[media]["urls"])
        statut, entree = traiter(media, noms[media], urls, options, precedent)
        comptes[statut] += 1
        if entree:
            table.update(dict.fromkeys(urls, entree))
    for media in (m for m in ordre(images) if m in REMPLACES):
        comptes["echec"] += signaler_remplace(media)
    ecrire_correspondances(table)
    conclure(comptes, len(table), [noms[m] for m in medias if m not in NOMS])
    return 1 if comptes["echec"] else 0


if __name__ == "__main__":
    sys.exit(main())

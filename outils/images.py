"""Les images de chantier : fichiers du site dès qu'ils existent.

Une partie des photos est encore servie par l'ancien site Wix. Le
script outils/rapatrier_images.py les copie dans assets/images/ et
écrit outils/images_locales.json, qui fait correspondre chaque adresse
Wix à son fichier local. À l'assemblage, chaque adresse Wix dont le
fichier existe est remplacée :
  - par un chemin relatif dans la page (src, href) ;
  - par une adresse absolue là où les robots la lisent (balises
    og:image, balisage structuré), qui exigent une URL complète.
Une image absente reste servie par Wix : le site ne casse jamais.
"""

import io
import json
import os
import re

from donnees_site import SITE

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORRESPONDANCE = os.path.join(RACINE, "outils", "images_locales.json")

_WIX = re.compile(r'https://static\.wixstatic\.com/media/[^"\'\s)<>]+')
# Une vraie image : l'adresse se termine par son extension.
_WIX_FICHIER = re.compile(r'https://static\.wixstatic\.com/media/[^"\'\s)<>]+?\.(?:jpe?g|png|webp|gif|avif)\b')
_JSONLD = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)
_CARTE = None


_VARIANTES = {}

# La largeur d'affichage d'une image, d'après le bloc qui la contient :
# le navigateur choisit alors dans srcset la variante juste assez grande.
_TAILLES = [
    ("metiers__vue", "72px"),
    ("chemise__tirage", "(max-width: 639px) 100vw, (max-width: 1023px) 50vw, 66vw"),
    ("signature__cadre", "100vw"),
    ("ouverture__cadre", "100vw"),
]


def _carte():
    """Adresse Wix → chemin local, pour les seuls fichiers présents."""
    global _CARTE
    if _CARTE is None:
        _CARTE = {}
        if os.path.exists(CORRESPONDANCE):
            with io.open(CORRESPONDANCE, encoding="utf-8") as f:
                for url, fiche in json.load(f).items():
                    chemin = fiche.get("fichier") if isinstance(fiche, dict) else fiche
                    if chemin and os.path.exists(os.path.join(RACINE, chemin)):
                        _CARTE[url] = chemin
                        variantes = fiche.get("variantes") if isinstance(fiche, dict) else None
                        _VARIANTES[url] = sorted(
                            (int(l), v) for l, v in (variantes or {}).items()
                            if os.path.exists(os.path.join(RACINE, v)))
    return _CARTE


def urls_wix_des_sources():
    """Toutes les adresses Wix que citent encore les sources du site."""
    trouvees = set()
    dossier = os.path.join(RACINE, "outils")
    for racine, _, fichiers in os.walk(dossier):
        for nom in fichiers:
            if nom.endswith((".py", ".html")) and nom != "rapatrier_images.py":
                with io.open(os.path.join(racine, nom), encoding="utf-8") as f:
                    texte = f.read()
                # IMG + "2c1464_…" : le préfixe et le nom sont écrits à part.
                texte = re.sub(r'IMG\s*\+\s*["\']', "https://static.wixstatic.com/media/", texte)
                trouvees.update(_WIX_FICHIER.findall(texte))
    return trouvees


def reste_des_images_wix():
    """Vrai tant qu'une image au moins n'a pas été rapatriée."""
    return any(not locale(url) for url in urls_wix_des_sources())


def locale(url):
    """Le chemin local d'une image Wix, ou None si elle n'est pas là."""
    return _carte().get(url)


def absolue(url):
    """L'adresse complète d'une image : locale si possible."""
    chemin = locale(url)
    return "%s/%s" % (SITE, chemin) if chemin else url


def _img_responsive(balise, url, base, contexte):
    """Une balise <img> Wix rapatriée : srcset des variantes WebP,
    src sur la variante moyenne, sizes d'après le bloc qui la contient."""
    variantes = _VARIANTES.get(url) or []
    if not variantes or "srcset=" in balise:
        return balise.replace(url, base + locale(url))
    tailles = next((t for classe, t in _TAILLES if classe in contexte), "100vw")
    moyenne = next((v for l, v in variantes if l >= 900), variantes[-1][1])
    if tailles == "72px":
        moyenne = variantes[0][1]
    srcset = ", ".join("%s%s %dw" % (base, v, l) for l, v in variantes)
    return balise.replace('src="%s"' % url, 'src="%s%s" srcset="%s" sizes="%s"'
                          % (base, moyenne, srcset, tailles))


_IMG = re.compile(r'<img\b[^>]*\bsrc="(https://static\.wixstatic\.com/media/[^"]+)"[^>]*>')


def localiser(html, base):
    """Remplace dans une page chaque image Wix rapatriée."""
    if not _carte():
        return html
    # Les <img> d'abord : elles reçoivent leurs variantes.
    html = _IMG.sub(lambda m: _img_responsive(m.group(0), m.group(1), base,
                                              html[max(0, m.start() - 400):m.start()])
                    if locale(m.group(1)) else m.group(0), html)
    zones_robots = [m.span() for m in _JSONLD.finditer(html)]

    def remplacer(correspondance):
        url = correspondance.group(0)
        chemin = locale(url)
        if not chemin:
            return url
        debut = correspondance.start()
        pour_robots = (html[max(0, debut - 9):debut] == 'content="'
                       or any(a <= debut < b for a, b in zones_robots))
        return "%s/%s" % (SITE, chemin) if pour_robots else base + chemin

    return _WIX.sub(remplacer, html)


def preconnexion(html):
    """Tant qu'une image vient encore de Wix, ouvre la connexion tôt.

    Sans l'attribut crossorigin : les <img> ordinaires se chargent sans
    CORS, et une connexion CORS préparée ne leur servirait à rien.
    """
    tete, sep, corps = html.partition("</head>")
    if "static.wixstatic.com" not in corps:
        return html
    lien = '<link rel="preconnect" href="https://static.wixstatic.com">\n'
    return tete.replace('<link rel="stylesheet"', lien + '<link rel="stylesheet"', 1) + sep + corps

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
_DECLINAISONS = None
_DOSSIER = os.path.join(RACINE, "assets", "images")

# La largeur d'affichage d'une image, d'après le bloc qui la contient,
# mesurée dans la page de 320 à 1920 px : le navigateur choisit alors
# dans srcset la variante juste assez grande pour l'écran et sa densité.
# Des conditions de largeur et calc() seulement : min() dans sizes n'est
# pas lu partout, et un sizes illisible vaut 100vw.
#
# Une photo recadrée dans un cadre plus haut qu'elle (object-fit: cover)
# s'affiche plus large que son cadre : sa largeur utile est la hauteur
# du cadre fois son format (largeur / hauteur). Celles-là reçoivent une
# fonction du format, qui suit les règles de leur cadre.


def _recadree(format_, bureau, tablette, telephone):
    """sizes d'une photo recadrée. `bureau` : la hauteur du cadre dès
    1024 px, (plancher, retrait sous 100vh, plafond) — clamp() de la
    feuille ; `tablette`, `telephone` : (rapport hauteur / largeur du
    cadre, retrait sous 100vw)."""
    plancher, retrait, plafond = bureau

    def large(cadre):
        rapport, marge = cadre
        facteur = max(1, round(rapport * format_, 3))
        if not marge:
            return "%dvw" % round(facteur * 100)
        return ("calc(%s * (100vw - %dpx))" % (facteur, marge) if facteur > 1
                else "calc(100vw - %dpx)" % marge)

    return ("(min-width: 1024px) and (min-height: %dpx) %dpx, "
            "(min-width: 1024px) and (min-height: %dpx) calc(%s * (100vh - %dpx)), "
            "(min-width: 1024px) %dpx, (min-width: 768px) %s, %s" % (
                plafond + retrait, round(plafond * format_),
                plancher + retrait, round(format_, 3), retrait,
                round(plancher * format_), large(tablette), large(telephone)))


_TAILLES = [
    ("metiers__vue", "(min-width: 1024px) 112px, 72px"),
    ("voisin__vue", "64px"),
    # Les fiches alternent grande et petite case : la grande fait foi.
    ("chemise__tirage", "(min-width: 1620px) 1000px, (min-width: 1024px) 62vw, "
                        "(min-width: 640px) 50vw, calc(100vw - 32px)"),
    ("signature__cadre", "(min-width: 1568px) 1504px, 100vw"),
    # 14-document.css : 4/3 au téléphone, 16/10 à la tablette, puis la
    # hauteur de l'écran moins l'en-tête (64 px) et 120 px.
    ("piece__image", lambda f: _recadree(f, (460, 184, 760), (10 / 16, 51), (3 / 4, 32))),
    # 06-haut.css : 4/3 puis 5/4 au téléphone, bord à bord ; 16/9 à la
    # tablette ; puis la hauteur de l'écran moins 200 px.
    ("comparateur__vue", lambda f: _recadree(f, (460, 200, 780), (9 / 16, 51), (4 / 5, 0))),
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


def declinaisons(chemin):
    """Les déclinaisons d'une image locale (outils/optimiser_images.py),
    par format et par largeur croissante : {"avif": [(480, chemin), …],
    "webp": […]}. Trouvées par leur nom, <nom>-<largeur>.<format>."""
    global _DECLINAISONS
    if _DECLINAISONS is None:
        _DECLINAISONS = {}
        motif = re.compile(r"^(.+)-(\d+)\.(avif|webp)$")
        for nom in os.listdir(_DOSSIER) if os.path.isdir(_DOSSIER) else ():
            m = motif.match(nom)
            if m:
                (_DECLINAISONS.setdefault(m.group(1), {})
                 .setdefault(m.group(3), []).append((int(m.group(2)), "assets/images/" + nom)))
        for formats in _DECLINAISONS.values():
            for liste in formats.values():
                liste.sort()
    return _DECLINAISONS.get(os.path.splitext(os.path.basename(chemin))[0], {})


def _tailles(contexte, balise):
    """Le sizes du bloc le plus proche qui précède l'image."""
    position, tailles = max(((contexte.rfind(classe), i) for i, (classe, _) in enumerate(_TAILLES)),
                            default=(-1, None))
    if position < 0:
        return "100vw"
    tailles = _TAILLES[tailles][1]
    if callable(tailles):
        mesures = [re.search(r'\s%s="(\d+)"' % a, balise) for a in ("width", "height")]
        format_ = (int(mesures[0].group(1)) / int(mesures[1].group(1))
                   if all(mesures) else 1.6)
        return tailles(format_)
    return tailles


def _img_responsive(balise, chemin, base, contexte):
    """Une balise <img> d'image locale : ses déclinaisons, servies au
    plus juste. Un seul fichier (les logos) : il remplace l'original.
    Plusieurs : srcset WebP sur l'<img>, et devant, une <source> AVIF que
    prennent tous les navigateurs qui la lisent."""
    formats = declinaisons(chemin)
    webp, avif = formats.get("webp", []), formats.get("avif", [])
    if "srcset=" in balise or not (webp or avif):
        return balise
    if len(webp) == 1 and not avif:
        return balise.replace('src="%s%s"' % (base, chemin), 'src="%s%s"' % (base, webp[0][1]))
    # Un sizes écrit dans la source a le dernier mot.
    ecrit = re.search(r'\ssizes="([^"]*)"', balise)
    tailles = ecrit.group(1) if ecrit else _tailles(contexte, balise)
    if not ecrit:
        balise = re.sub(r"<img\b", '<img sizes="%s"' % tailles, balise, count=1)

    def jeu(liste):
        return ", ".join("%s%s %dw" % (base, v, l) for l, v in liste)

    if webp:
        moyenne = (webp[0][1] if tailles.endswith("72px") or tailles == "64px"
                   else next((v for l, v in webp if l >= 900), webp[-1][1]))
        balise = balise.replace('src="%s%s"' % (base, chemin),
                                'src="%s%s" srcset="%s"' % (base, moyenne, jeu(webp)))
    if not avif:
        return balise
    return ('<picture><source type="image/avif" srcset="%s" sizes="%s">%s</picture>'
            % (jeu(avif), tailles, balise))


_IMG = re.compile(r'<img\b[^>]*\bsrc="(https://static\.wixstatic\.com/media/[^"]+)"[^>]*>')
# Une image locale d'origine (photo .jpg, logo .png), pas encore déclinée.
_IMG_LOCALE = re.compile(r'<img\b[^>]*\bsrc="(?:/|(?:\.\./)*)(assets/images/[\w-]+\.(?:jpg|png))"[^>]*>')


def _decliner(html, base):
    """Chaque <img> d'image locale reçoit ses déclinaisons — sauf dans un
    <picture> écrit à la main, qui a déjà les siennes."""
    def remplacer(m):
        avant = html[max(0, m.start() - 400):m.start()]
        if avant.rfind("<picture") > avant.rfind("</picture>"):
            return m.group(0)
        return _img_responsive(m.group(0), m.group(1), base, avant)
    return _IMG_LOCALE.sub(remplacer, html)


def localiser(html, base):
    """Remplace dans une page chaque image Wix rapatriée, puis sert
    chaque image locale à ses déclinaisons."""
    if not _carte():
        return _decliner(html, base)
    # Les <img> d'abord : leur adresse devient celle du fichier local.
    html = _IMG.sub(lambda m: m.group(0).replace(m.group(1), base + locale(m.group(1)))
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
        if pour_robots:
            return "%s/%s" % (SITE, chemin)
        # Un lien vers la photo (la visionneuse) : sa plus grande variante
        # WebP, cinq à dix fois plus légère que l'original.
        variantes = declinaisons(chemin).get("webp") or _VARIANTES.get(url)
        if variantes and html[max(0, debut - 6):debut] == 'href="':
            return base + variantes[-1][1]
        return base + chemin

    return _decliner(_WIX.sub(remplacer, html), base)


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

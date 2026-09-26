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
_JSONLD = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)
_CARTE = None


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
    return _CARTE


def locale(url):
    """Le chemin local d'une image Wix, ou None si elle n'est pas là."""
    return _carte().get(url)


def absolue(url):
    """L'adresse complète d'une image : locale si possible."""
    chemin = locale(url)
    return "%s/%s" % (SITE, chemin) if chemin else url


def localiser(html, base):
    """Remplace dans une page chaque image Wix rapatriée."""
    if not _carte():
        return html
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

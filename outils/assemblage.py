"""Assemblage d'un document : feuille, scripts, chrome, écriture.

Séparé de construire.py pour que celui-ci ne décrive que les pages.
"""

import hashlib
import io
import os
import re

import accessibilite
import gabarit
import images
import prestations
import rythme
import typographie

SERVICES = prestations.PAGES
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Les feuilles sources, dans l'ordre de leur numéro. On les édite une à
# une ; les pages, elles, ne chargent qu'une feuille : site.css, leur
# concaténation minifiée, écrite par construire.py. Une requête au lieu
# de dix-huit, et aucun commentaire envoyé au visiteur.
FEUILLES = [
    "00-jetons.css", "00-polices.css", "01-socle.css", "02-boutons.css",
    "03-fiches.css", "04-formulaires.css", "05-navigation.css",
    "06-haut.css", "07-chantiers.css", "08-bas.css", "10-comparateur.css",
    "11-lumineuse.css", "12-equipe.css", "13-pile.css", "14-document.css", "15-pages.css",
    "16-composants.css", "17-repli.css", "18-confiance.css",
    "19-impression.css",
]
FEUILLE_SITE = "assets/css/site.css"

BASE_JS = ["nav.js", "motion.js", "onglets.js"]


def ecrire(chemin, contenu):
    """Écrit un fichier du site, chemin relatif à la racine du projet."""
    complet = os.path.join(RACINE, chemin)
    os.makedirs(os.path.dirname(complet) or ".", exist_ok=True)
    with io.open(complet, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def _empreinte(texte):
    """Huit caractères qui changent dès que le fichier change : le
    navigateur peut garder le fichier en cache un an sans risque."""
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()[:8]


def _minifier(css):
    """Retire commentaires et blancs superflus, sans toucher au sens.

    Prudent par construction : les chaînes sont recopiées telles
    quelles, les espaces ne disparaissent qu'autour de { } ; , — jamais
    autour de « : » (« a :hover » n'est pas « a:hover ») ni dans calc(),
    où « - » et « + » exigent leurs espaces.
    """
    sortie, i, n = [], 0, len(css)
    while i < n:
        c = css[i]
        if c in "\"'":
            fin = i + 1
            while fin < n and css[fin] != c:
                fin += 2 if css[fin] == "\\" else 1
            sortie.append(css[i:fin + 1])
            i = fin + 1
        elif css.startswith("/*", i):
            fin = css.find("*/", i + 2)
            i = n if fin == -1 else fin + 2
        elif c.isspace():
            while i < n and css[i].isspace():
                i += 1
            # Un commentaire retiré entre deux blancs en laisserait deux.
            if not sortie or sortie[-1] != " ":
                sortie.append(" ")
        else:
            sortie.append(c)
            i += 1
    texte = "".join(sortie)
    texte = re.sub(r" ?([{};,]) ?", r"\1", texte)
    texte = texte.replace(";}", "}")
    return texte.strip() + "\n"


def feuille_du_site():
    """Écrit site.css et renvoie son chemin versionné."""
    morceaux = []
    for nom in FEUILLES:
        with io.open(os.path.join(RACINE, "assets", "css", nom), encoding="utf-8") as f:
            morceaux.append(f.read())
    css = _minifier("\n".join(morceaux))
    ecrire(FEUILLE_SITE, css)
    return "%s?v=%s" % (FEUILLE_SITE, _empreinte(css))


def version_script(nom):
    """Empreinte d'un module JavaScript, pour son adresse versionnée."""
    with io.open(os.path.join(RACINE, "assets", "js", nom), encoding="utf-8") as f:
        return _empreinte(f.read())


_FEUILLE = None


def _feuille():
    global _FEUILLE
    if _FEUILLE is None:
        _FEUILLE = feuille_du_site()
    return _FEUILLE


def assembler(page, corps, base, modules, schemas):
    """Un document complet : tête, en-tête, corps, pied, scripts."""
    html = accessibilite.lier_titres(
        gabarit.tete(page, base, _feuille(), schemas)
        + gabarit.entete(base, page["courante"], SERVICES)
        + '\n<main id="contenu">\n'
        + corps
        + "</main>\n"
        + gabarit.pied(base, page["courante"], SERVICES)
        + gabarit.scripts(base, modules, version_script)
    )
    # Les textes de contenu écrivent leurs liens internes « {base}… » :
    # ils ignorent à quelle profondeur ils seront publiés.
    html = html.replace("{base}", base)
    html = rythme.rythmer(html)
    html = images.localiser(html, base)
    return typographie.espacer(images.preconnexion(html))

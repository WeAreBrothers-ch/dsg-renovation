"""Assemblage d'un document : feuilles, scripts, chrome, écriture.

Séparé de construire.py pour que celui-ci ne décrive que les pages.
"""

import io
import os

import accessibilite
import gabarit
import prestations

SERVICES = prestations.PAGES
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Toutes les feuilles, dans l'ordre de leur numéro. Les pages riches les
# chargent toutes : le poids total reste sous les cinquante kilo-octets,
# et un jeu par page se serait périmé au premier composant déplacé.
FEUILLES = [
    "00-jetons.css", "01-socle.css", "02-boutons.css", "03-fiches.css",
    "04-formulaires.css", "05-navigation.css", "06-haut.css",
    "07-chantiers.css", "08-bas.css", "09-curseur.css", "10-comparateur.css",
    "11-lumineuse.css", "12-planche.css", "13-pile.css", "14-document.css",
    "15-pages.css", "16-composants.css", "17-repli.css", "18-confiance.css",
    "19-impression.css",
]
FEUILLES_ANNEXE = [
    "00-jetons.css", "01-socle.css", "02-boutons.css", "05-navigation.css",
    "08-bas.css", "09-curseur.css", "14-document.css", "15-pages.css", "16-composants.css", "17-repli.css", "18-confiance.css", "19-impression.css",
]

BASE_JS = ["nav.js", "motion.js", "effets.js", "curseur.js", "onglets.js"]


def ecrire(chemin, contenu):
    """Écrit un fichier du site, chemin relatif à la racine du projet."""
    complet = os.path.join(RACINE, chemin)
    os.makedirs(os.path.dirname(complet) or ".", exist_ok=True)
    with io.open(complet, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def assembler(page, corps, base, feuilles, modules, schemas):
    """Un document complet : tête, en-tête, corps, pied, scripts."""
    return accessibilite.lier_titres(
        gabarit.tete(page, base, feuilles, schemas)
        + gabarit.entete(base, page["courante"])
        + '\n<main id="contenu">\n'
        + corps
        + "</main>\n"
        + gabarit.pied(base, page["courante"], SERVICES)
        + gabarit.scripts(base, modules)
    )

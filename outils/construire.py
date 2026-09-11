#!/usr/bin/env python3
"""Assemble les pages du site à partir des gabarits et du contenu.

Le site livré reste du HTML statique : ce script n'est pas une étape de
compilation, c'est une commodité de maintenance. Il se lance à la main
après une modification du contenu ou du chrome :

    python3 outils/construire.py

Ouvrir index.html suffit toujours pour consulter le site.
"""

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import briques
import catalogue
import gabarit
import page_service
import page_accueil
import pages_contenu
import pages_site
import seo
import prestations
from donnees_site import SITE

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICES = prestations.PAGES

# Toutes les feuilles, dans l'ordre de leur numéro. Les pages riches les
# chargent toutes : le poids total reste sous les cinquante kilo-octets,
# et un jeu par page se serait périmé au premier composant déplacé.
FEUILLES = [
    "00-jetons.css", "01-socle.css", "02-boutons.css", "03-fiches.css",
    "04-formulaires.css", "05-navigation.css", "06-haut.css",
    "07-chantiers.css", "08-bas.css", "09-curseur.css", "10-comparateur.css",
    "11-lumineuse.css", "12-planche.css", "13-pile.css", "14-document.css",
    "15-pages.css", "16-composants.css",
]
FEUILLES_ANNEXE = [
    "00-jetons.css", "01-socle.css", "02-boutons.css", "05-navigation.css",
    "08-bas.css", "09-curseur.css", "14-document.css", "15-pages.css", "16-composants.css",
]

BASE_JS = ["nav.js", "motion.js", "effets.js", "curseur.js"]


def ecrire(chemin, contenu):
    complet = os.path.join(RACINE, chemin)
    os.makedirs(os.path.dirname(complet) or ".", exist_ok=True)
    with io.open(complet, "w", encoding="utf-8") as f:
        f.write(contenu)
    return chemin


def assembler(page, corps, base, feuilles, modules, schemas):
    """Un document complet : tête, en-tête, corps, pied, scripts."""
    return (
        gabarit.tete(page, base, feuilles, schemas)
        + gabarit.entete(base, page["courante"])
        + '\n<main id="contenu">\n'
        + corps
        + "</main>\n"
        + gabarit.pied(base, page["courante"], SERVICES)
        + gabarit.scripts(base, modules)
    )


def page_simple(fichier, titre, description, etiquette, h1, chapo,
                corps_fn, modules, fil_seo, image=None, action=None):
    """Une page de la racine : fil d'Ariane, couverture, corps, pied."""
    page = {
        "titre": titre,
        "description": description,
        "canonique": "%s/%s" % (SITE, fichier),
        "courante": fichier,
        "etiquette": etiquette,
        "h1": h1,
        "chapo": chapo,
    }
    if image:
        page["image_og"] = image
    corps = briques.couverture(
        page, "", [("Accueil", "index.html"), (etiquette, "")], action
    ) + corps_fn(SERVICES, "")
    schemas = [seo.entreprise(), seo.fil([("Accueil", ""), (titre, fichier)])]
    schemas += fil_seo
    return ecrire(fichier, assembler(page, corps, "", FEUILLES, modules, schemas))


def construire_accueil():
    page = {
        "titre": "DSG Rénovation — Entreprise de rénovation à Lausanne",
        "description": (
            "Entreprise de rénovation clé en main à Lausanne et sur l'arc "
            "lémanique : rénovation totale, peinture, plâtrerie, carrelage et "
            "sols. 600 chantiers livrés. Devis gratuit sous 72 h."
        ),
        "canonique": SITE + "/",
        "courante": "index.html",
        "image_og": SERVICES[0]["image"],
    }
    corps = page_accueil.accueil(SERVICES, "")
    schemas = [seo.entreprise()]
    modules = BASE_JS + ["comparateur.js", "vignette.js"]
    return ecrire("index.html", assembler(page, corps, "", FEUILLES, modules, schemas))


def construire_services():
    """La page pilier et les neuf pages de lot."""
    faits = [page_simple(
        "services.html",
        "Nos prestations de rénovation à Lausanne",
        "Les neuf lots de DSG Rénovation à Lausanne : rénovation totale, "
        "peinture, plâtrerie, cloisons, revêtements muraux, faux plafonds, "
        "carrelage, sols et nettoyage de fin de chantier.",
        "Prestations", ["Neuf métiers,", "un seul chantier"],
        "Chaque lot est mené par des salariés de l'entreprise ou par des "
        "partenaires que nous suivons depuis des années.",
        pages_site.savoir_faire, BASE_JS + ["vignette.js"], [])]

    for service in SERVICES:
        fichier = "services/%s.html" % service["slug"]
        page = {
            # Pas de suffixe de marque : « Lausanne » et le métier valent mieux
            # que « DSG Rénovation » dans les soixante caractères affichés.
            "titre": service["titre"],
            "description": service["description"],
            "canonique": "%s/%s" % (SITE, fichier),
            "courante": "services.html",
            "etiquette": service["nom"],
            "h1": service["h1"],
            "chapo": service["chapo"],
            "image_og": service["image"],
        }
        fil = [("Accueil", "index.html"), ("Prestations", "services.html"),
               (service["nom"], "")]
        corps = (briques.couverture(page, "../", fil)
                 + page_service.corps(service, "../"))
        schemas = [
            seo.entreprise(),
            seo.prestation(service, [
                poste
                for _, postes in prestations.prestations_de(service)
                for poste in postes
            ]),
            seo.questions(prestations.questions_de(service)),
            seo.fil([("Accueil", ""), ("Prestations", "services.html"),
                     (service["nom"], fichier)]),
        ]
        faits.append(ecrire(fichier, assembler(
            page, corps, "../", FEUILLES, BASE_JS + ["vignette.js"], schemas)))
    return faits


def construire_pages():
    """Les cinq pages de contenu de la racine, prises au catalogue."""
    balisage = seo.questions(catalogue.LISTE_QUESTIONS)
    return [page_simple(*fiche)
            for fiche in catalogue.pages(BASE_JS, balisage)]


def construire_annexes():
    """Mentions légales et confidentialité : le contenu est déjà rédigé."""
    faits = []
    for fichier, titre, description in [
        ("mentions-legales.html",
         "Mentions légales — DSG Rénovation",
         "Mentions légales du site de DSG Rénovation Sàrl : éditeur, "
         "hébergement, propriété intellectuelle, responsabilité et droit "
         "applicable."),
        ("confidentialite.html",
         "Politique de confidentialité — DSG Rénovation",
         "Comment DSG Rénovation Sàrl traite les données personnelles "
         "transmises depuis son site : données collectées, finalité, "
         "conservation et droits des personnes concernées."),
    ]:
        page = {
            "titre": titre,
            "description": description,
            "canonique": "%s/%s" % (SITE, fichier),
            "courante": fichier,
            "robots": '<meta name="robots" content="noindex, follow">',
        }
        corps = pages_site.fragment("annexe-" + fichier.replace(".html", ""))
        schemas = [seo.entreprise()]
        faits.append(ecrire(fichier, assembler(
            page, corps, "", FEUILLES_ANNEXE, BASE_JS, schemas)))
    return faits


def construire_plan(pages):
    """Plan du site et directives d'exploration."""
    priorites = {"index.html": ("weekly", "1.0"), "devis.html": ("monthly", "0.9"),
                 "services.html": ("monthly", "0.9")}
    urls = []
    for p in pages:
        if p.startswith("mentions") or p.startswith("confidentialite"):
            continue
        freq, prio = priorites.get(p, ("monthly", "0.7"))
        if p.startswith("services/"):
            freq, prio = "monthly", "0.8"
        urls.append(("" if p == "index.html" else p, freq, prio))
    ecrire("sitemap.xml", seo.plan_du_site(urls))
    ecrire("robots.txt", seo.robots())


def main():
    pages = [construire_accueil()]
    pages += construire_services()
    pages += construire_pages()
    pages += construire_annexes()
    construire_plan(pages)
    print("%d pages écrites :" % len(pages))
    for p in sorted(pages):
        print("  ", p)


if __name__ == "__main__":
    main()

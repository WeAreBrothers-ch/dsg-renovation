#!/usr/bin/env python3
"""Assemble les pages du site à partir des gabarits et du contenu.

Le site livré reste du HTML statique : ce script n'est pas une étape de
compilation, c'est une commodité de maintenance. Il se lance à la main
après une modification du contenu ou du chrome :

    python3 outils/construire.py

Il écrit les pages, la feuille unique assets/css/site.css, le plan du
site et robots.txt. Pour consulter le site en local :

    python3 -m http.server   (puis http://localhost:8000)
"""

import datetime
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import briques
import catalogue
import images
import page_service
import page_accueil
import page_prestations
import pages_site
import pages_speciales
import seo
import prestations
from assemblage import BASE_JS, RACINE, assembler, ecrire
from donnees_site import SITE

SERVICES = prestations.PAGES

# Pages utiles au visiteur mais sans valeur pour la recherche : hors du
# plan du site, et marquées noindex.
NOINDEX = '<meta name="robots" content="noindex, follow">'


def _image_partage(url, alt):
    """La photo d'une page pour les réseaux sociaux, si elle est locale.

    Une photo encore servie par Wix disparaîtra avec l'ancien site : on
    lui préfère alors l'image de partage de la marque (gabarit.py).
    """
    if url and images.locale(url):
        return {"image_og": images.absolue(url), "image_og_alt": alt}
    return {}


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
    page.update(_image_partage(image, titre))
    corps = briques.couverture(
        page, "", [("Accueil", "/"), (etiquette, "")], action
    ) + corps_fn(SERVICES, "")
    schemas = [seo.entreprise(), seo.fil([("Accueil", ""), (etiquette, fichier)])]
    schemas += fil_seo
    return ecrire(fichier, assembler(page, corps, "", modules, schemas))


def construire_accueil():
    page = {
        "titre": "Entreprise de rénovation à Lausanne | DSG Rénovation",
        "description": (
            "Rénovation clé en main à Lausanne et sur l'arc lémanique : "
            "peinture, plâtrerie, carrelage, sols. 600 chantiers livrés. "
            "Devis gratuit 72 h après la visite."
        ),
        "canonique": SITE + "/",
        "courante": "index.html",
    }
    corps = page_accueil.accueil(SERVICES, "")
    schemas = [seo.site_web(), seo.entreprise()]
    modules = BASE_JS + ["comparateur.js", "ouverture.js"]
    return ecrire("index.html", assembler(page, corps, "", modules, schemas))


def construire_services():
    """La page pilier et les pages de prestation."""
    faits = [page_simple(
        "services.html",
        "Travaux de rénovation à Lausanne : peinture, plâtrerie, sols",
        "Rénovation complète, peinture, plâtrerie, cloisons, faux plafonds, "
        "carrelage, sols et nettoyage à Lausanne : un seul interlocuteur "
        "pour tout le chantier.",
        "Prestations", ["Travaux de rénovation", "à Lausanne"],
        "Tous nos travaux sont réalisés par des salariés de l'entreprise ou "
        "par des partenaires que nous suivons depuis des années.",
        page_prestations.savoir_faire, BASE_JS, [])]

    for service in SERVICES:
        fichier = "services/%s.html" % service["slug"]
        page = {
            # Pas de suffixe de marque : « Lausanne » et le métier valent mieux
            # que « DSG Rénovation » dans les soixante caractères affichés.
            "titre": service["titre"],
            "description": service["description"],
            "canonique": "%s/%s" % (SITE, fichier),
            "courante": fichier,
            "etiquette": service["nom"],
            "h1": service["h1"],
            "chapo": service["chapo"],
            "travaux": service["slug"],
        }
        page.update(_image_partage(service["image"], service["alt"]))
        fil = [("Accueil", "/"), ("Prestations", "services.html"),
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
            page, corps, "../", BASE_JS + ["ouverture.js"], schemas)))
    return faits


def construire_pages():
    """Les pages de contenu de la racine, prises au catalogue."""
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
            "robots": NOINDEX,
        }
        corps = pages_site.fragment("annexe-" + fichier.replace(".html", ""))
        schemas = [seo.entreprise()]
        faits.append(ecrire(fichier, assembler(page, corps, "", BASE_JS, schemas)))
    return faits


def construire_speciales():
    """Page introuvable et page de remerciement : noindex, hors plan.

    La page 404 est servie par le serveur à n'importe quelle adresse, à
    n'importe quelle profondeur : ses liens partent donc de la racine
    (« / »), pas du dossier courant.
    """
    faits = []
    for fichier, base, titre, description, corps_fn in pages_speciales.PAGES:
        page = {
            "titre": titre,
            "description": description,
            "canonique": "%s/%s" % (SITE, fichier),
            "courante": fichier,
            "robots": NOINDEX,
        }
        faits.append(ecrire(fichier, assembler(
            page, corps_fn(SERVICES, base), base, BASE_JS, [])))
    return faits


def _date_de_modification(fichier):
    """Date de dernière modification réelle d'une page, pour lastmod.

    Si le fichier diffère de sa version enregistrée dans git (ou n'y est
    pas encore), il change aujourd'hui ; sinon, c'est la date du dernier
    commit qui l'a touché. Un lastmod qui bougerait à chaque
    construction ne voudrait plus rien dire, et Google cesserait de le
    lire.
    """
    aujourdhui = datetime.date.today().isoformat()
    try:
        suivi = subprocess.run(["git", "ls-files", "--error-unmatch", fichier],
                               cwd=RACINE, capture_output=True).returncode == 0
        modifie = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", fichier],
                                 cwd=RACINE, capture_output=True).returncode != 0
        if not suivi or modifie:
            return aujourdhui
        date = subprocess.run(["git", "log", "-1", "--format=%cs", "--", fichier],
                              cwd=RACINE, capture_output=True, text=True).stdout.strip()
        return date or aujourdhui
    except OSError:
        return aujourdhui


def construire_plan(pages):
    """Plan du site et directives d'exploration."""
    exclues = ("mentions-legales.html", "confidentialite.html") + tuple(
        fichier for fichier, *_ in pages_speciales.PAGES)
    urls = [("" if p == "index.html" else p, _date_de_modification(p))
            for p in pages if p not in exclues]
    ecrire("sitemap.xml", seo.plan_du_site(urls))
    ecrire("robots.txt", seo.robots())


def main():
    pages = [construire_accueil()]
    pages += construire_services()
    pages += construire_pages()
    pages += construire_annexes()
    pages += construire_speciales()
    construire_plan(pages)
    print("%d pages écrites :" % len(pages))
    for p in sorted(pages):
        print("  ", p)


if __name__ == "__main__":
    main()

"""Balisage structuré, plan du site et directives d'exploration.

Le balisage décrit à Google ce que la page dit déjà en clair. Il ne
promet rien que le texte ne tienne : un horaire faux dans le balisage
est une erreur, pas une optimisation.
"""

import html
import json
import re

import images
from donnees_site import (CODE_POSTAL, COMMUNES, COURRIEL, EFFECTIF,
                          FERMETURE, FONDATION, IMAGE_PARTAGE, ITINERAIRE,
                          JOURS_OUVRES, LOGO_HAUTEUR, LOGO_LARGEUR, LOGO_PNG,
                          MARQUE, OUVERTURE, RUE, SITE, SOCIETE,
                          TELEPHONE_BRUT, VILLE)

ENTREPRISE_ID = SITE + "/#entreprise"
SITE_ID = SITE + "/#site"


def _bloc(donnees):
    return json.dumps(donnees, ensure_ascii=False, indent=2)


def _texte_nu(fragment):
    """Retire balises et entités d'un fragment HTML : le JSON-LD veut du
    texte. Le contenu d'un <script> n'est jamais décodé par le
    navigateur : un « &amp; » laissé ici serait lu tel quel."""
    sans_balises = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(sans_balises)).strip()


def _services():
    """Les prestations, pour décrire ce que l'entreprise sait faire."""
    import prestations
    return [_texte_nu(p["nom"]) for p in prestations.PAGES]


def site_web():
    """Le site lui-même : son nom, sa langue, son éditeur."""
    return _bloc({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": SITE_ID,
        "name": MARQUE,
        "alternateName": SOCIETE,
        "url": SITE + "/",
        "inLanguage": "fr-CH",
        "publisher": {"@id": ENTREPRISE_ID},
    })


def entreprise():
    """Fiche d'établissement, posée une fois et référencée partout.

    GeneralContractor : une entreprise générale, qui coordonne tous les
    corps de métier — c'est exactement la rénovation clé en main. Le
    type hérite de HomeAndConstructionBusiness et de LocalBusiness.
    """
    return _bloc({
        "@context": "https://schema.org",
        "@type": "GeneralContractor",
        "@id": ENTREPRISE_ID,
        "name": SOCIETE,
        "alternateName": MARQUE,
        "description": (
            "Entreprise de rénovation clé en main à Lausanne et sur l'arc "
            "lémanique : rénovation complète, peinture, plâtrerie, cloisons, "
            "faux plafonds, carrelage, sols et nettoyage de fin de chantier."
        ),
        "slogan": "Du sol au plafond, tout en maîtrise.",
        "url": SITE + "/",
        "logo": {
            "@type": "ImageObject",
            "url": "%s/%s" % (SITE, LOGO_PNG),
            "width": LOGO_LARGEUR,
            "height": LOGO_HAUTEUR,
        },
        "image": "%s/%s" % (SITE, IMAGE_PARTAGE),
        "telephone": TELEPHONE_BRUT,
        "email": COURRIEL,
        "foundingDate": FONDATION,
        "numberOfEmployees": {"@type": "QuantitativeValue", "value": EFFECTIF},
        "address": {
            "@type": "PostalAddress",
            "streetAddress": RUE,
            "postalCode": CODE_POSTAL,
            "addressLocality": VILLE,
            "addressRegion": "VD",
            "addressCountry": "CH",
        },
        "hasMap": html.unescape(ITINERAIRE),
        "areaServed": [{"@type": "City", "name": c} for c in COMMUNES],
        "knowsAbout": _services(),
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": JOURS_OUVRES,
            "opens": OUVERTURE,
            "closes": FERMETURE,
        },
    })


def fil(entrees):
    """Fil d'Ariane : la position de la page dans l'arborescence.

    Les noms sont ceux du fil visible, pas les titres de page : Google
    affiche ce chemin dans ses résultats.
    """
    return _bloc({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": _texte_nu(nom),
                "item": SITE + "/" + url if url else SITE + "/",
            }
            for i, (nom, url) in enumerate(entrees)
        ],
    })


def prestation(fiche, offres):
    """Décrit une prestation et la zone où elle est proposée.

    `offres` est la liste à plat des postes couverts par la page, tous
    lots confondus : le catalogue déclaré doit dire ce que la page dit.
    """
    donnees = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": _texte_nu(fiche["nom"]),
        "serviceType": _texte_nu(fiche["nom"]),
        "description": _texte_nu(fiche["description"]),
        "provider": {"@id": ENTREPRISE_ID},
        "areaServed": [{"@type": "City", "name": c} for c in COMMUNES],
        "url": "%s/services/%s.html" % (SITE, fiche["slug"]),
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Prestations — " + _texte_nu(fiche["nom"]),
            "itemListElement": [
                {"@type": "Offer",
                 "itemOffered": {"@type": "Service", "name": _texte_nu(o)}}
                for o in offres
            ],
        },
    }
    # Une photo encore servie par Wix disparaîtra : on ne la déclare
    # qu'une fois rapatriée dans le site.
    if images.locale(fiche.get("image", "")):
        donnees["image"] = images.absolue(fiche["image"])
    return _bloc(donnees)


def questions(paires):
    """Questions fréquentes, telles qu'elles sont écrites sur la page.

    Depuis 2023, Google n'affiche plus ces questions en résultats
    enrichis que pour les sites officiels et de santé : le balisage
    reste valide et décrit la page, sans promettre d'affichage.
    """
    vues, uniques = set(), []
    for q, r in paires:
        nom = _texte_nu(q)
        if nom not in vues:
            vues.add(nom)
            uniques.append((nom, _texte_nu(r)))
    return _bloc({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": r},
            }
            for q, r in uniques
        ],
    })


def plan_du_site(urls):
    """sitemap.xml — une ligne par page indexable, datée.

    Google ignore priority et changefreq ; il lit lastmod, tant qu'il
    reste fidèle (voir construire.py).
    """
    lignes = "\n".join(
        "  <url>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n  </url>"
        % (SITE, url, date)
        for url, date in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "%s\n</urlset>\n" % lignes
    )


def robots():
    """robots.txt — tout est ouvert.

    Les fichiers de fabrication (outils/, documents .md) ne sont pas
    signalés ici — un robots.txt se lit par tous : .htaccess les rend
    tout simplement introuvables.
    """
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Sitemap: %s/sitemap.xml\n" % SITE
    )

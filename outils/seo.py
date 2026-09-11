"""Balisage structuré, plan du site et directives d'exploration.

Le balisage décrit à Google ce que la page dit déjà en clair. Il ne
promet rien que le texte ne tienne : un horaire faux dans le balisage
est une erreur, pas une optimisation.
"""

import json
import re

from donnees_site import (COMMUNES, COURRIEL, LOGO, RUE, SITE, SOCIETE,
                          TELEPHONE_BRUT, VILLE)

ENTREPRISE_ID = SITE + "/#entreprise"


def _bloc(donnees):
    return json.dumps(donnees, ensure_ascii=False, indent=2)


def entreprise():
    """Fiche d'établissement, posée une fois et référencée partout."""
    return _bloc({
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "@id": ENTREPRISE_ID,
        "name": SOCIETE,
        "description": (
            "Entreprise de rénovation clé en main à Lausanne : rénovation "
            "totale, peinture, plâtrerie, cloisons, faux plafonds, carrelage "
            "et sols."
        ),
        "url": SITE + "/",
        "logo": LOGO,
        "image": LOGO,
        "telephone": TELEPHONE_BRUT,
        "email": COURRIEL,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": RUE,
            "postalCode": "1012",
            "addressLocality": VILLE,
            "addressRegion": "VD",
            "addressCountry": "CH",
        },
        "areaServed": [{"@type": "City", "name": c} for c in COMMUNES],
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "08:00",
            "closes": "17:00",
        },
    })


def fil(entrees):
    """Fil d'Ariane : la position de la page dans l'arborescence."""
    return _bloc({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": nom,
                "item": SITE + "/" + url if url else SITE + "/",
            }
            for i, (nom, url) in enumerate(entrees)
        ],
    })


def _texte_nu(html):
    """Retire le balisage d'un fragment : le JSON-LD veut du texte."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def prestation(service):
    """Décrit un lot et la zone où il est proposé."""
    return _bloc({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": _texte_nu(service["nom"]),
        "serviceType": _texte_nu(service["nom"]),
        "description": service["description"],
        "provider": {"@id": ENTREPRISE_ID},
        "areaServed": [{"@type": "City", "name": c} for c in COMMUNES],
        "url": "%s/services/%s.html" % (SITE, service["slug"]),
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Prestations — " + _texte_nu(service["nom"]),
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": p}}
                for p in service["prestations"]
            ],
        },
    })


def questions(paires):
    """Questions fréquentes, telles qu'elles sont écrites sur la page."""
    return _bloc({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": _texte_nu(q),
                "acceptedAnswer": {"@type": "Answer", "text": _texte_nu(r)},
            }
            for q, r in paires
        ],
    })


def plan_du_site(urls):
    """sitemap.xml — une ligne par page, priorité décroissante."""
    lignes = "\n".join(
        "  <url>\n    <loc>%s/%s</loc>\n"
        "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
        % (SITE, url, freq, prio)
        for url, freq, prio in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "%s\n</urlset>\n" % lignes
    )


def robots():
    """robots.txt — tout est ouvert, sauf les outils de fabrication."""
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /outils/\n"
        "\n"
        "Sitemap: %s/sitemap.xml\n" % SITE
    )

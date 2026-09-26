"""Deux pages de prestation : relouer un logement, refaire une salle de bains.

Même structure que prestations.PAGES. Chaque page ne porte qu'une fiche,
de même slug, décrite dans services_solutions.py ; son contenu « sur le
terrain » est dans lausanne_solutions.py.

Branchement, à faire dans le générateur (rien n'est branché ici) :
- prestations.py : ajouter services_solutions.SERVICES à LOTS, PAGES
  ci-dessous à la suite de prestations.PAGES (numéros 06 et 07), et
  INTERTITRES ci-dessous à prestations.INTERTITRES ;
- page_service.py : fusionner lausanne_solutions.LOCAL dans LOCAL ;
Liens internes : les introductions et certaines réponses de
services_solutions.py écrivent leurs liens `<a href="{base}services/….html">`
ou `{base}devis.html`, comme services_finitions.py. C'est
assemblage.assembler() qui remplace `{base}` par le préfixe de la page
dans tout le document ; seo.questions() retire les balises des réponses
pour le balisage FAQPage.

L'image d'ouverture affiche son texte alternatif comme légende visible
(page_service._tirage) : les deux `alt` ci-dessous sont repris tels
quels des pages existantes qui utilisent la même photo.
"""

IMG = "https://static.wixstatic.com/media/"

PAGES = [
    {
        "slug": "remise-en-etat-appartement",
        "numero": "06",
        "nom": "Remise en état entre deux locations",
        "nom_menu": "Remise en état",
        "resume": "Logement remis en état entre deux locataires, rendu à "
                  "date fixe, nettoyage compris.",
        "lots": ["remise-en-etat-appartement"],
        "titre": "Remise en état d'appartement à Lausanne — entre locataires",
        "description": (
            "Remise en état d'appartement à Lausanne entre deux locataires : "
            "peinture, joints, sols, nettoyage, logement rendu à date fixe. "
            "Devis gratuit."
        ),
        "h1": ["Remise en état d'appartement", "à Lausanne"],
        "chapo": "Entre deux locataires, tout se règle sur une date. Nous "
                 "remettons le logement en état et le rendons propre, prêt "
                 "pour l'état des lieux d'entrée.",
        "image": IMG + "2c1464_59c5df800ba245e2b7dff597bb0221a4~mv2.jpg",
        "alt": "Logement nettoyé après travaux, prêt à être occupé",
        "reperes": [
            ("Visite", "Sous une semaine"),
            ("Appartement 100 m²", "1 à 2 semaines de peinture"),
            ("Nettoyage final", "1 à 2 jours pour 100 m²"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "lies": ["peinture", "nettoyage-fin-de-chantier", "carrelage-sols",
                 "platrerie-cloisons"],
    },
    # Sources :
    #   contenu_divers.py:107-114 ; services_finitions.py:82-85 — logement
    #     rendu à date ferme, entre deux baux, nettoyage compris.
    #   prestations.py:152 — logement prêt pour l'état des lieux.
    #   services_finitions.py:196 ; services_finitions.py:260-262 ;
    #     services_finitions.py:49 — joints, sols, peinture entre deux
    #     locations.
    #   prestations.py:160 ; fragments/chantiers.html:160-162 — photo et texte
    #     alternatif repris tels quels de la page nettoyage ; c'est le logement
    #     remis en état de la rue de Bourg (fiche N° 006).
    #   contenu_entreprise.py:45 ; confiance.py:20 ; services_finitions.py:66 ;
    #     services_finitions.py:348 ; services_finitions.py:69 — repères :
    #     visite sous une semaine ; peinture 1 à 2 semaines et nettoyage 1 à 2
    #     jours pour 100 m² ; devis gratuit 72 h après la visite.
    {
        "slug": "renovation-salle-de-bains",
        "numero": "07",
        "nom": "Rénovation de salle de bains",
        "nom_menu": "Salle de bains",
        "resume": "Dépose, étanchéité, carrelage et faïence ; sanitaire et "
                  "électricité coordonnés.",
        "lots": ["renovation-salle-de-bains"],
        "titre": "Rénovation de salle de bains à Lausanne, étanchéité comprise",
        "description": (
            "Rénovation de salle de bains à Lausanne : dépose, étanchéité "
            "sous carrelage, faïence et sol, sanitaire et électricité "
            "coordonnés. Devis gratuit."
        ),
        "h1": ["Rénovation de salle de bains", "à Lausanne"],
        "chapo": "Dépose, support et étanchéité d'abord, carrelage et faïence "
                 "ensuite. Dans une salle de bains, ce qui compte le plus ne "
                 "se voit plus une fois le chantier fini.",
        "image": IMG + "2c1464_c44b6415607747ff9dccd68b224b3945~mv2.jpg",
        "alt": "Salle d'eau carrelée du sol au plafond dans un duplex rénové",
        "reperes": [
            ("Salle de bains", "1 à 2 semaines, étanchéité comprise"),
            ("Dépose et évacuation", "1 à 2 jours selon l'étage"),
            ("Support et étanchéité", "2 jours, séchage compris"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "lies": ["carrelage-sols", "renovation-complete", "platrerie-cloisons",
                 "peinture"],
    },
    # Sources :
    #   services_finitions.py:185-187 ; lausanne_finitions.py:69-73 —
    #     étanchéité posée sous le carrelage, qui protège le logement du
    #     dessous.
    #   contenu_divers.py:12-13 ; contenu_divers.py:24-26 — dépose d'abord,
    #     carrelage et étanchéité ensuite.
    #   services_gros_oeuvre.py:52 ; contenu_divers.py:95-98 — sanitaire et
    #     électricité coordonnés avec les partenaires.
    #   services_finitions.py:190-191 — carrelage de sol et faïence murale.
    #   prestations.py:131 ; fragments/chantiers.html:40-42 — photo et texte
    #     alternatif repris tels quels de la page carrelage ; c'est une salle
    #     d'eau du duplex des Eaux-Vives, à Genève (fiche N° 002).
    #   services_finitions.py:209 ; lausanne_finitions.py:86-88 ;
    #     services_finitions.py:69 — repères : 1 à 2 semaines étanchéité
    #     comprise ; dépose 1 à 2 jours selon l'étage ; support et étanchéité 2
    #     jours séchage compris ; devis gratuit 72 h après la visite.
]


# Les intertitres propres à chaque page, au format de
# prestations.INTERTITRES : sans eux, intertitres_de() retombe sur des
# titres génériques communs à toutes les pages.
INTERTITRES = {
    "remise-en-etat-appartement": {
        "quoi": "Remise en état|entre deux locataires",
        "comment": "Une remise en état,|étape par étape",
        "zone": "Remise en état à Lausanne|et sur l'arc lémanique",
        "questions": "Vos questions sur|la remise en état",
        "voisins": "Souvent réalisé|avec la remise en état",
    },
    "renovation-salle-de-bains": {
        "quoi": "Rénovation de salle de bains,|de la dépose aux joints",
        "comment": "Une salle de bains,|étape par étape",
        "zone": "Rénovation de salle de bains|à Lausanne et sur l'arc lémanique",
        "questions": "Vos questions sur la|rénovation de salle de bains",
        "voisins": "Souvent réalisé|avec la salle de bains",
    },
}
# Sources :
#   prestations.py:176 ; prestations.py:215 — format et repli générique des
#     intertitres. Aucun fait : des intitulés de section.

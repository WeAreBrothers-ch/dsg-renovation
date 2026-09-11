"""Fiche signalétique des pages de la racine.

Titre, description, étiquette et titre affiché de chaque page, plus la
liste des questions fréquentes reprise pour le balisage structuré.
Le point d'entrée se contente ensuite de les assembler.
"""

import pages_contenu
import pages_site

# Reprises telles quelles de la page questions, pour le balisage.
LISTE_QUESTIONS = [
    ("Intervenez-vous en dehors de Lausanne ?",
     "Oui. Nous intervenons sur tout l'arc lémanique : Lausanne et Lavaux, "
     "Genève, Morges, Nyon, Vevey et Montreux."),
    ("Le devis est-il vraiment gratuit ?",
     "Oui, déplacement et relevé compris, sans aucun engagement. Vous recevez "
     "un devis détaillé poste par poste sous 72 heures après la visite."),
    ("Puis-je rester dans le logement pendant les travaux ?",
     "Dans la plupart des cas, oui. Nous organisons le chantier par zones "
     "pour vous laisser une partie du logement utilisable."),
    ("Combien de temps dure une rénovation complète ?",
     "Environ 5 à 8 semaines pour un appartement de 100 m², et 10 à 14 "
     "semaines pour une maison ou un immeuble."),
    ("Travaillez-vous pour les régies et les propriétaires bailleurs ?",
     "Oui, c'est une part importante de notre activité : remises en état "
     "entre deux locations et rénovations d'immeubles en site occupé."),
    ("Qui coordonne les différents corps de métier ?",
     "Nous. Un responsable de chantier unique pilote l'ensemble des lots et "
     "reste votre seul interlocuteur du devis à la remise des clés."),
]

ACTION_BORDEREAU = (
    '<a class="btn btn--plein" href="#bordereau" data-magnetique>'
    'Remplir le bordereau<span class="fleche" aria-hidden="true"></span></a>'
)


def pages(base_js, questions_balisees):
    """Les cinq pages de la racine, prêtes à être assemblées.

    Chaque entrée est le jeu d'arguments de `page_simple` : fichier,
    titre, description, étiquette, titre affiché, chapô, corps, modules,
    balisage supplémentaire, puis l'action de couverture.
    """
    return [
        ("entreprise.html",
         "L'entreprise — DSG Rénovation, rénovation à Lausanne",
         "DSG Rénovation Sàrl, entreprise de rénovation fondée en 2019 à "
         "Lausanne : 11 professionnels salariés, 600 chantiers livrés, "
         "40 ans de savoir-faire transmis.",
         "L'entreprise", ["Quarante ans de métier,", "une entreprise jeune"],
         "Onze professionnels salariés, un réseau de partenaires de la "
         "région, et un seul métier : la rénovation.",
         pages_site.entreprise, base_js + ["vignette.js"], [], None),

        ("realisations.html",
         "Nos réalisations de rénovation à Lausanne",
         "Six chantiers de rénovation livrés à Lausanne, Pully, Genève : "
         "appartements, maisons et immeubles. Surfaces, durées et lots "
         "détaillés fiche par fiche.",
         "Réalisations", ["Six fiches", "de chantier"],
         "Appartements, maisons et immeubles livrés à Lausanne et sur "
         "l'arc lémanique, avec leur relevé complet.",
         pages_contenu.realisations,
         base_js + ["dossier.js", "lumineuse.js"], [], None),

        ("references.html",
         "Références et avis clients — DSG Rénovation Lausanne",
         "Régies, architectes et propriétaires qui confient leurs biens à "
         "DSG Rénovation à Lausanne et Genève, et ce qu'en disent nos "
         "clients.",
         "Références", ["Ils nous confient", "leurs biens"],
         "Régies lausannoises, architectes et propriétaires privés : ceux "
         "qui nous rappellent d'un chantier à l'autre.",
         pages_contenu.references, base_js, [], None),

        ("questions.html",
         "Questions fréquentes — rénovation à Lausanne",
         "Zone d'intervention, gratuité du devis, durée d'une rénovation, "
         "vie dans le logement pendant les travaux : les réponses aux "
         "questions que l'on nous pose avant de signer.",
         "Questions", ["Ce qu'on nous", "demande le plus"],
         "Les réponses aux questions qui reviennent avant la signature "
         "d'un devis.",
         pages_contenu.questions, base_js, [questions_balisees], None),

        ("devis.html",
         "Demander un devis gratuit — DSG Rénovation Lausanne",
         "Devis de rénovation gratuit et détaillé sous 72 heures à "
         "Lausanne et sur l'arc lémanique. Visite et relevé compris, sans "
         "engagement.",
         "Demander un devis", ["Ouvrez", "votre dossier"],
         "Visite, relevé et devis détaillé poste par poste. Gratuit, sous "
         "72 heures, sans engagement.",
         pages_contenu.devis, base_js + ["formulaire.js"], [],
         ACTION_BORDEREAU),
    ]

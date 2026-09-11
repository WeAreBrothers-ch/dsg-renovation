"""Fiche signalétique des pages de la racine.

Titre, description, étiquette et titre affiché de chaque page, plus la
liste des questions fréquentes reprise pour le balisage structuré.
Le point d'entrée se contente ensuite de les assembler.
"""

import pages_contenu
import pages_site

from contenu_questions import toutes as LISTE_QUESTIONS_FN

# Les vingt questions, à plat, pour le balisage structuré.
LISTE_QUESTIONS = LISTE_QUESTIONS_FN()

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

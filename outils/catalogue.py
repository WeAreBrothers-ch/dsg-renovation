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
    """Les trois pages de la racine, prêtes à être assemblées.

    Chaque entrée est le jeu d'arguments de `page_simple` : fichier,
    titre, description, étiquette, titre affiché, chapô, corps, modules,
    balisage supplémentaire, image de partage (None : le logo), puis
    l'action de couverture.
    """
    return [
        ("entreprise.html",
         "L'entreprise — DSG Rénovation, rénovation à Lausanne",
         "DSG Rénovation Sàrl, entreprise de rénovation fondée en 2019 à "
         "Lausanne : 11 professionnels salariés, 600 chantiers livrés, et les "
         "régies qui nous confient leurs biens.",
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

        ("devis.html",
         "Devis rénovation gratuit à Lausanne — DSG Rénovation",
         "Devis de rénovation gratuit et détaillé à Lausanne, 72 h après la visite. "
         "Ce que contient un devis, comment en comparer deux, et les réponses "
         "aux vingt questions qu'on nous pose avant de signer.",
         "Devis gratuit", ["Ouvrez", "votre dossier"],
         "Visite, relevé et devis détaillé poste par poste. Gratuit, remis "
         "72 heures après la visite, sans engagement.",
         pages_contenu.devis, base_js + ["formulaire.js"],
         [questions_balisees], None, ACTION_BORDEREAU),
    ]

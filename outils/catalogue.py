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

ACTION_FORMULAIRE = (
    '<a class="btn btn--plein" href="#formulaire">'
    'Décrire mon projet<span class="fleche" aria-hidden="true"></span></a>'
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
         "L'entreprise DSG Rénovation, à Lausanne depuis 2019",
         "DSG Rénovation Sàrl, fondée en 2019 à Lausanne : 11 professionnels "
         "salariés, 600 chantiers livrés pour les régies et les propriétaires.",
         "L'entreprise", ["Quarante ans de métier,", "une entreprise lausannoise"],
         "Onze professionnels salariés, un réseau de partenaires de la "
         "région, et un seul métier : la rénovation.",
         pages_site.entreprise, base_js, [], None),

        ("realisations.html",
         "Nos réalisations de rénovation à Lausanne",
         "Six chantiers de rénovation livrés à Lausanne, Pully et Genève : "
         "appartements, maisons, immeubles. Surface, durée et travaux "
         "détaillés pour chacun.",
         "Réalisations", ["Nos réalisations", "à Lausanne"],
         "Appartements, maisons et immeubles livrés à Lausanne et sur "
         "l'arc lémanique, avec leur surface, leur durée et les travaux "
         "réalisés.",
         pages_contenu.realisations,
         base_js + ["dossier.js", "lumineuse.js"], [], None),

        ("devis.html",
         "Devis rénovation gratuit à Lausanne — DSG Rénovation",
         "Devis de rénovation gratuit à Lausanne, détaillé poste par poste, "
         "72 h après la visite. Comment le lire, le comparer, et 20 réponses "
         "avant de signer.",
         "Devis gratuit", ["Devis de rénovation gratuit", "à Lausanne"],
         "Visite, mesures et devis détaillé poste par poste. Gratuit, remis "
         "72 heures après la visite, sans engagement.",
         pages_contenu.devis, base_js + ["formulaire.js"],
         [questions_balisees], None, ACTION_FORMULAIRE),
    ]

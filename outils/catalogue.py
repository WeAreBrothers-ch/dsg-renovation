"""Fiche signalétique des pages de la racine.

Titre, description, étiquette et titre affiché de chaque page, plus la
liste des questions fréquentes reprise pour le balisage structuré.
Le point d'entrée se contente ensuite de les assembler.
"""

import pages_contenu
from donnees_site import HORAIRES
import pages_site

from contenu_questions import toutes as LISTE_QUESTIONS_FN

# Les vingt questions, à plat, pour le balisage structuré.
LISTE_QUESTIONS = LISTE_QUESTIONS_FN()

IMG = "https://static.wixstatic.com/media/"

# La photo de couverture de chaque page : un chantier réel, repris des
# fiches de réalisations (fragments/chantiers.html, signature.html).
# Les photos « séjour avant / après » sont celles de l'appartement
# Beaulieu (la cuisine ouverte sur le séjour) : elles portent son nom et
# mènent à sa fiche. Aucune grande photo ne se répète sur une page : la
# page des réalisations, dont la première fiche montre Beaulieu livré,
# s'ouvre sur son état d'avant travaux : toutes les autres photos y ont
# déjà leur fiche.
_BEAULIEU_APRES = {
    "src": "assets/images/sejour-apres.jpg",
    "alt": "Séjour de l'appartement Beaulieu après rénovation complète : cuisine blanche ouverte sur le séjour, parquet chêne et murs repris",
    "lieu": "Appartement Beaulieu, Lausanne",
    "largeur": 1404, "hauteur": 682,
    "ancre": "appartement-beaulieu",
}
_BEAULIEU_AVANT = {
    "src": "assets/images/sejour-avant.jpg",
    "alt": "Séjour de l'appartement Beaulieu avant travaux : cuisine démontée jusqu'au mur, ouverture sur le séjour en cours, gaines et câbles apparents",
    "lieu": "Appartement Beaulieu, avant travaux",
    "largeur": 1404, "hauteur": 682,
    "ancre": "appartement-beaulieu",
}
PHOTO_ENTREPRISE = dict(_BEAULIEU_APRES,
                        quoi="Livré par nos équipes, tous corps de métier")
PHOTO_REALISATIONS = dict(_BEAULIEU_AVANT,
                          quoi="La cuisine s'ouvre sur le séjour : le "
                               "résultat est dans la première fiche")
PHOTO_DEVIS = dict(_BEAULIEU_AVANT,
                   quoi="Ce que nous relevons à la visite, et chiffrons "
                        "poste par poste")
PHOTO_PRESTATIONS = {
    "src": IMG + "2c1464_ab94350c74604962a66564240516acc5~mv2.jpg",
    "alt": "Pièce de vie du loft de Sévelin après travaux : cuisine ouverte "
           "sous un faux plafond éclairé, murs lissés et parquet clair",
    "lieu": "Loft de Sévelin, Lausanne",
    "quoi": "Cloisons, plâtrerie, peinture et parquet : tous les métiers",
    "ancre": "loft-de-sevelin",
}

# Les repères de l'en-tête de chaque page : des faits déjà écrits
# ailleurs sur le site (donnees_site.py, confiance.py, les fiches).
FAITS_PRESTATIONS = [
    ("Prestations", "Sept, un seul interlocuteur"),
    ("Équipe", "11 professionnels salariés"),
    ("Devis", "Gratuit, 72 h après visite"),
    ("Zone", "Lausanne et arc lémanique"),
]
FAITS_ENTREPRISE = [
    ("Atelier", "Lausanne, av. de Béthusy"),
    ("Horaires", HORAIRES),
    ("Zone", "Lausanne et arc lémanique"),
    ("Devis", "Gratuit, 72 h après visite"),
]
FAITS_REALISATIONS = [
    ("Chantiers livrés", "600+ sur l'arc lémanique"),
    ("Sur cette page", "Six chantiers détaillés"),
    ("Biens", "Appartements, maisons, immeubles"),
    ("Lieux", "Lausanne, Pully, Genève"),
]
FAITS_DEVIS = [
    ("Visite", "Sous une semaine"),
    ("Devis", "72 h après la visite"),
    ("Prix", "Gratuit, sans engagement"),
    ("Détail", "Poste par poste"),
]

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
         pages_site.entreprise, base_js, [], None, None, PHOTO_ENTREPRISE,
         FAITS_ENTREPRISE),

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
         base_js + ["dossier.js", "lumineuse.js"], [], None, None,
         PHOTO_REALISATIONS, FAITS_REALISATIONS),

        ("devis.html",
         "Devis rénovation gratuit à Lausanne — DSG Rénovation",
         "Devis de rénovation gratuit à Lausanne, détaillé poste par poste, "
         "72 h après la visite. Comment le lire, le comparer, et 20 réponses "
         "avant de signer.",
         "Devis gratuit", ["Devis de rénovation gratuit", "à Lausanne"],
         "Visite, mesures et devis détaillé poste par poste. Gratuit, remis "
         "72 heures après la visite, sans engagement.",
         pages_contenu.devis, base_js + ["formulaire.js"],
         [questions_balisees], None, ACTION_FORMULAIRE, PHOTO_DEVIS,
         FAITS_DEVIS),
    ]

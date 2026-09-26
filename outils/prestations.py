"""Les pages de prestation, et les lots qu'elles regroupent.

Les fiches de lot restent où elles sont : ce fichier ne fait que dire
lesquels partagent une page, et rédige ce qui leur est commun — titre,
chapô, introduction, repères.

Pourquoi cinq et non neuf : les lots qui se posent ensemble sur un
chantier se cherchent ensemble sur un moteur. Une page dense qui
couvre la plâtrerie, les cloisons et les faux plafonds se positionne
mieux que trois pages moyennes, et elle répond mieux au visiteur, qui
a rarement besoin d'un seul de ces trois lots.

Cinq pages de métier, puis deux pages de situation (pages_solutions.py) :
relouer un logement, refaire une salle de bains. Ce sont les deux
demandes que les clients formulent sans nommer de métier.
"""

import pages_solutions
from services_finitions import SERVICES as FINITIONS
from services_gros_oeuvre import SERVICES as GROS_OEUVRE
from services_solutions import SERVICES as SOLUTIONS

LOTS = {s["slug"]: s for s in GROS_OEUVRE + FINITIONS + SOLUTIONS}

IMG = "https://static.wixstatic.com/media/"

PAGES = [
    {
        "slug": "renovation-complete",
        "numero": "01",
        "nom": "Rénovation complète",
        "nom_menu": "Rénovation complète",
        "resume": "Appartement, maison ou immeuble repris de fond en comble, "
                  "tous corps de métier coordonnés.",
        "lots": ["renovation-complete"],
        "titre": "Rénovation complète d'appartement et de maison à Lausanne",
        "description": (
            "Rénovation complète d'appartement ou de maison à Lausanne : tous "
            "les corps de métier coordonnés, un seul responsable. Devis "
            "gratuit 72 h après visite."
        ),
        "h1": ["Rénovation complète", "à Lausanne"],
        "chapo": "Appartement, maison ou immeuble repris de fond en comble. "
                 "Un seul contrat, un seul responsable de chantier, une seule "
                 "date de livraison.",
        "image": IMG + "2c1464_593f3a927ebd420ab56d4d306a4e6aa5~mv2.jpg",
        "alt": "Séjour et cuisine ouverte après rénovation complète d'un "
               "appartement à Lausanne",
        "reperes": [
            ("Durée type", "5 à 8 semaines pour 100 m²"),
            ("Maison ou immeuble", "10 à 14 semaines"),
            ("Devis", "Gratuit, 72 h après visite"),
            ("Défauts relevés", "Repris sous 10 jours"),
        ],
        "lies": ["platrerie-cloisons", "peinture", "carrelage-sols",
                 "nettoyage-fin-de-chantier"],
    },
    {
        "slug": "peinture",
        "numero": "02",
        "nom": "Peinture &amp; revêtements muraux",
        "nom_menu": "Peinture &amp; revêtements",
        "resume": "Préparation des fonds, mise en teinte, papier peint et "
                  "toile de verre posés sans raccord visible.",
        "lots": ["peinture", "revetements-muraux"],
        "titre": "Peintre à Lausanne — peinture et papier peint",
        "description": (
            "Peintre à Lausanne : préparation des fonds, peinture intérieure "
            "et extérieure, papier peint et toile de verre, teintes testées "
            "sur place. Devis gratuit."
        ),
        "h1": ["Peintre à Lausanne :", "peinture et revêtements muraux"],
        "chapo": "Une belle peinture, c'est quatre-vingts pour cent de "
                 "préparation. Un papier peint se juge à ses raccords. Dans "
                 "les deux cas, tout se joue sur le fond.",
        "image": IMG + "2c1464_a7cac83b91964ef7b403ba6eb333bd0b~mv2.jpg",
        "alt": "Dégagement et cuisine remis en peinture dans une villa "
               "lausannoise",
        "reperes": [
            ("Appartement 100 m²", "1 à 2 semaines"),
            ("Couches de finition", "2 au minimum"),
            ("Teintes", "Essai sur site avant validation"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "lies": ["platrerie-cloisons", "renovation-complete", "carrelage-sols",
                 "remise-en-etat-appartement"],
    },
    {
        "slug": "platrerie-cloisons",
        "numero": "03",
        "nom": "Plâtrerie, cloisons &amp; faux plafonds",
        "nom_menu": "Plâtrerie &amp; cloisons",
        "resume": "Enduits et lissage, création ou suppression de volumes, "
                  "plafonds suspendus et éclairage intégré.",
        "lots": ["platrerie", "cloisons", "faux-plafonds"],
        "titre": "Plâtrier à Lausanne — cloisons, enduits et faux plafonds",
        "description": (
            "Plâtrier à Lausanne : enduits et lissage, cloisons placo ou "
            "alba, faux plafonds avec éclairage intégré. Devis gratuit 72 h "
            "après la visite."
        ),
        "h1": ["Plâtrier à Lausanne :", "plâtrerie, cloisons, faux plafonds"],
        "chapo": "Trois métiers qui dessinent la pièce : ce qui tient les murs, "
                 "ce qui les déplace, et ce qui ferme le dessus. Ils se "
                 "posent presque toujours ensemble.",
        "image": IMG + "2c1464_1f332a25fbc5404f8ea0424fc54875d2~mv2.jpg",
        "alt": "Mur repris en plâtrerie avant mise en peinture dans un "
               "appartement lausannois",
        "reperes": [
            ("Finition des murs", "Prêts à peindre ou lissés parfaits"),
            ("Cloison simple", "2 à 3 jours, finition comprise"),
            ("Perte de hauteur", "8 à 15 cm sous faux plafond"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "lies": ["peinture", "renovation-complete", "carrelage-sols",
                 "nettoyage-fin-de-chantier"],
    },
    {
        "slug": "carrelage-sols",
        "numero": "04",
        "nom": "Carrelage &amp; sols",
        "nom_menu": "Carrelage &amp; sols",
        "resume": "Salles d'eau et cuisines recarrelées, parquet, vinyle et "
                  "linoléum posés sur support préparé.",
        "lots": ["carrelage", "pose-de-sol"],
        "titre": "Carreleur à Lausanne — carrelage, parquet et vinyle",
        "description": (
            "Carreleur à Lausanne : salles de bains, cuisines, grès cérame "
            "grand format, parquet, vinyle et linoléum posés sur un sol "
            "préparé. Devis gratuit."
        ),
        "h1": ["Carreleur à Lausanne :", "carrelage et sols"],
        "chapo": "Ce sur quoi on marche supporte tout le reste. Le plan de "
                 "pose des carreaux et la mise à niveau du sol se décident "
                 "avant la première colle, jamais après.",
        "image": IMG + "2c1464_c44b6415607747ff9dccd68b224b3945~mv2.jpg",
        "alt": "Salle d'eau carrelée du sol au plafond dans un duplex rénové",
        "reperes": [
            ("Salle de bains", "1 à 2 semaines, étanchéité comprise"),
            ("Appartement 100 m²", "3 à 5 jours de sol"),
            ("En immeuble", "Sous-couche acoustique systématique"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "lies": ["renovation-salle-de-bains", "renovation-complete",
                 "platrerie-cloisons", "peinture"],
    },
    {
        "slug": "nettoyage-fin-de-chantier",
        "numero": "05",
        "nom": "Nettoyage de fin de chantier",
        "nom_menu": "Nettoyage de chantier",
        "resume": "Logement rendu habitable immédiatement, vitres et "
                  "sanitaires compris.",
        "lots": ["nettoyage-fin-de-chantier"],
        "titre": "Nettoyage de fin de chantier à Lausanne",
        "description": (
            "Nettoyage de fin de travaux à Lausanne : poussière de chantier, "
            "vitres, sanitaires, sols. Logement habitable, prêt pour l'état "
            "des lieux. Devis gratuit."
        ),
        "h1": ["Nettoyage de fin de chantier", "à Lausanne"],
        "chapo": "La poussière de plâtre se dépose trois fois avant de "
                 "disparaître. Un nettoyage de chantier n'est pas un ménage, "
                 "c'est un métier.",
        "image": IMG + "2c1464_59c5df800ba245e2b7dff597bb0221a4~mv2.jpg",
        "alt": "Logement nettoyé après travaux, prêt à être occupé",
        "reperes": [
            ("Appartement 100 m²", "1 à 2 jours"),
            ("Passages", "2 au minimum, poussière oblige"),
            ("Sur nos chantiers", "Compris dans le devis"),
            ("Seul", "Possible après une autre entreprise"),
        ],
        "lies": ["renovation-complete", "remise-en-etat-appartement",
                 "peinture", "carrelage-sols"],
    },
]

PAGES += pages_solutions.PAGES


# Les intertitres propres à chaque page. Sept pages qui titrent toutes
# « Ce que nous faisons » ou « Où nous intervenons » se ressemblent aux
# yeux d'un moteur ; chacune porte ici son métier et sa ville.
INTERTITRES = {
    "renovation-complete": {
        "quoi": "Une rénovation complète,|tous corps de métier",
        "comment": "Comment se déroule|une rénovation complète",
        "zone": "Rénovation complète à Lausanne|et sur l'arc lémanique",
        "questions": "Vos questions sur|la rénovation complète",
        "voisins": "Les métiers d'une|rénovation complète",
    },
    "peinture": {
        "quoi": "Nos travaux de peinture|et de revêtements",
        "comment": "Un chantier de peinture,|étape par étape",
        "zone": "Peintre à Lausanne|et sur l'arc lémanique",
        "questions": "Vos questions|sur la peinture",
        "voisins": "Souvent réalisé|avec la peinture",
    },
    "platrerie-cloisons": {
        "quoi": "Plâtrerie, cloisons|et faux plafonds",
        "comment": "Un chantier de plâtrerie,|étape par étape",
        "zone": "Plâtrier à Lausanne|et sur l'arc lémanique",
        "questions": "Vos questions sur la|plâtrerie et les cloisons",
        "voisins": "Souvent réalisé|avec la plâtrerie",
    },
    "carrelage-sols": {
        "quoi": "Carrelage, parquet|et sols souples",
        "comment": "Une pose de carrelage,|étape par étape",
        "zone": "Carreleur à Lausanne|et sur l'arc lémanique",
        "questions": "Vos questions sur|le carrelage et les sols",
        "voisins": "Souvent réalisé|avec le carrelage",
    },
    "nettoyage-fin-de-chantier": {
        "quoi": "Un nettoyage de chantier,|pas un ménage",
        "comment": "Un nettoyage de fin de chantier,|étape par étape",
        "zone": "Nettoyage de chantier à Lausanne|et sur l'arc lémanique",
        "questions": "Vos questions sur|le nettoyage de chantier",
        "voisins": "Souvent réalisé|avant le nettoyage",
    },
}


INTERTITRES.update(pages_solutions.INTERTITRES)


def intertitres_de(fiche):
    """Les intertitres d'une page, avec un repli générique pour une page
    qui n'aurait pas encore les siens."""
    return INTERTITRES.get(fiche["slug"], {
        "quoi": "Ce que comprend|la prestation",
        "comment": "Comment|nous procédons",
        "zone": "À Lausanne et|sur l'arc lémanique",
        "questions": "Vos questions|sur cette prestation",
        "voisins": "Souvent réalisé|avec cette prestation",
    })


def page(slug):
    """La fiche d'une page de prestation."""
    return next(p for p in PAGES if p["slug"] == slug)


def lots_de(fiche):
    """Les fiches de lot que cette page regroupe, dans l'ordre."""
    return [LOTS[slug] for slug in fiche["lots"]]


def intro_de(fiche):
    """L'introduction : celle du premier lot, qui porte la page."""
    return LOTS[fiche["lots"][0]]["intro"]


def etapes_de(fiche):
    """La méthode : celle du premier lot, la plus représentative."""
    return LOTS[fiche["lots"][0]]["etapes"]


def questions_de(fiche):
    """Toutes les questions des lots regroupés, sans doublon."""
    vues, sortie = set(), []
    for lot in lots_de(fiche):
        for question, reponse in lot["questions"]:
            if question in vues:
                continue
            vues.add(question)
            sortie.append((question, reponse))
    return sortie


def prestations_de(fiche):
    """Les prestations, groupées par lot quand la page en réunit plusieurs."""
    return [(lot["nom"], lot["prestations"]) for lot in lots_de(fiche)]

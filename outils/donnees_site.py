"""Constantes du site : coordonnées, navigation, zones d'intervention.

Une seule source pour tout ce qui se répète d'une page à l'autre.
Modifier une valeur ici la corrige sur les dix-huit pages.
"""

SITE = "https://www.dsg-renov.ch"
SOCIETE = "DSG Rénovation Sàrl"
MARQUE = "DSG Rénovation"
TELEPHONE = "+41 21 847 02 02"
TELEPHONE_BRUT = "+41218470202"
COURRIEL = "contact@dsg-renov.ch"
RUE = "Avenue de Béthusy 60"
CODE_POSTAL = "1012"
VILLE = "Lausanne"
LOGO = "https://static.wixstatic.com/media/2c1464_3db14001d9184097989203ad9a2f559e~mv2.png"

# Villes citées dans les textes et le balisage. L'ordre va du plus proche
# au plus lointain : c'est celui dans lequel l'entreprise se déplace.
COMMUNES = [
    "Lausanne", "Pully", "Prilly", "Renens", "Ecublens", "Épalinges",
    "Lutry", "Morges", "Nyon", "Vevey", "Montreux", "Genève",
]

ZONES_PIED = [
    "Lausanne &amp; Lavaux",
    "Genève",
    "Morges &amp; Nyon",
    "Vevey &amp; Montreux",
    "Arc lémanique",
]

# Navigation principale : intitulé, fichier, et si l'entrée figure dans
# la barre du haut (les autres n'apparaissent que dans le menu et le pied).
NAVIGATION = [
    {"nom": "L'entreprise", "url": "entreprise.html", "barre": False},
    {"nom": "Savoir-faire", "url": "services.html", "barre": True},
    {"nom": "Réalisations", "url": "realisations.html", "barre": True},
    {"nom": "Références", "url": "references.html", "barre": True},
    {"nom": "Questions", "url": "questions.html", "barre": True},
    {"nom": "Demander un devis", "url": "devis.html", "barre": False},
]

ANNEXES = [
    {"nom": "Mentions légales", "url": "mentions-legales.html"},
    {"nom": "Confidentialité", "url": "confidentialite.html"},
]

# Chiffres du relevé, avec la preuve que chacun porte. Repris tels quels
# du dossier d'origine : intitulé de languette, valeur, signe, texte.
RELEVE = [
    ("Chantiers livrés", "600", "+",
     "Un seul contact du devis à la remise des clés. Nous coordonnons tous "
     "les corps de métier, vous ne gérez rien."),
    ("Ans de savoir-faire", "40", "",
     "Planning de chantier daté, transmis avant le démarrage et tenu semaine "
     "après semaine. Aucun chantier laissé ouvert."),
    ("Professionnels salariés", "11", "",
     "Des professionnels salariés, pas de sous-traitance en cascade : les "
     "mêmes visages du premier au dernier jour."),
    ("Partenaires de la région", "35", "+",
     "Réception de chantier contradictoire, reprise des réserves sous "
     "<span class=\"nb\">10</span> jours et nettoyage complet inclus."),
]

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
# Le logo et ses déclinaisons, servis par le site (chemins depuis la
# racine ; les gabarits y ajoutent le préfixe de la page).
#   logo-blanc.avif  l'original fourni, pour fond clair (12 Ko)
#   logo.webp        le même, pour les navigateurs sans AVIF
#   logo-negatif     lettres blanches, toit rouge : pour le bleu nuit
#   logo.png         pour les robots (balisage, réseaux sociaux)
LOGO_AVIF = "assets/images/logo-blanc.avif"
LOGO_WEBP = "assets/images/logo.webp"
LOGO_NEGATIF = "assets/images/logo-negatif.webp"
LOGO_PNG = "assets/images/logo.png"
LOGO_LARGEUR, LOGO_HAUTEUR = 314, 166

# Image de partage (réseaux sociaux, messageries), 1200 × 630.
IMAGE_PARTAGE = "assets/images/partage.jpg"
IMAGE_PARTAGE_ALT = ("DSG Rénovation, entreprise de rénovation à Lausanne : "
                     "séjour et cuisine après rénovation")

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
# Quatre entrées. Les références ont rejoint la page entreprise, dont
# elles sont la preuve ; les questions ont rejoint la page de devis, où
# elles se posent réellement. Un menu court se lit, un menu long se
# parcourt.
NAVIGATION = [
    {"nom": "Prestations", "url": "services.html", "barre": True},
    {"nom": "Réalisations", "url": "realisations.html", "barre": True},
    {"nom": "L'entreprise", "url": "entreprise.html", "barre": True},
    {"nom": "Devis gratuit", "url": "devis.html", "barre": False},
]

ANNEXES = [
    {"nom": "Mentions légales", "url": "mentions-legales.html"},
    {"nom": "Confidentialité", "url": "confidentialite.html"},
]

# Horaires du bureau. CONTENU À VALIDER : à confirmer avec le client.
# Une seule source : le texte affiché et le balisage structuré en
# découlent tous deux, ils ne peuvent plus diverger.
OUVERTURE, FERMETURE = "08:00", "17:00"
JOURS_OUVRES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
HORAIRES = "Lundi – vendredi, %s – %s" % (OUVERTURE, FERMETURE)

FONDATION = "2019"
EFFECTIF = 11

# Itinéraire vers l'atelier : un lien de recherche, qui ne dépend d'aucune
# fiche d'établissement. À remplacer par le lien de la fiche Google
# Business Profile dès qu'elle existe (À FOURNIR PAR LE CLIENT).
ITINERAIRE = ("https://www.google.com/maps/search/?api=1&amp;query="
              "Avenue+de+B%C3%A9thusy+60%2C+1012+Lausanne")

# Chiffres du relevé, avec la preuve que chacun porte. Chaque texte
# explique le chiffre qu'il accompagne : un chiffre sans explication est
# une vitrine, un chiffre expliqué est une pièce justificative.
RELEVE = [
    ("Chantiers livrés", "600", "+",
     "Appartements, maisons et immeubles, pour des propriétaires privés "
     "comme pour les régies de la place lausannoise."),
    ("Ans de savoir-faire", "40", "",
     "Un métier transmis depuis plus de quarante ans, repris en "
     "<span class=\"nb\">2019</span> sous le nom DSG Rénovation."),
    ("Professionnels salariés", "11", "",
     "Des professionnels salariés, pas de sous-traitance en cascade : les "
     "mêmes visages du premier au dernier jour."),
    ("Partenaires de la région", "35", "+",
     "Des artisans que nous suivons depuis des années. Jamais d'entreprise "
     "inconnue découverte sur place."),
]

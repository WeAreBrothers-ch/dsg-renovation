"""Contenu neuf des pages savoir-faire, réalisations et références.

Trois blocs qui n'existaient pas dans le dossier d'une page : l'ordre
dans lequel les lots s'enchaînent, les trois types de biens que nous
reprenons à Lausanne, et les trois manières de travailler avec nous.
"""

# ---------------------------------------------------------------- services
# L'ordre des lots sur un chantier. C'est la question que tout le monde
# se pose et que personne ne publie.
ENCHAINEMENT = [
    ("Démolition et dépose",
     "Anciens revêtements, cloisons à supprimer, sanitaires déposés. Le "
     "logement revient à son état brut avant qu'on y ajoute quoi que ce soit."),
    ("Cloisons et faux plafonds",
     "Les volumes se dessinent. Tout ce qui touche à la géométrie de la pièce "
     "se décide ici, parce qu'après, tout dépend de ces lignes."),
    ("Lots techniques",
     "Électricité, sanitaire, ventilation : les réseaux passent dans les "
     "cloisons et les plafonds tant qu'ils sont ouverts."),
    ("Plâtrerie",
     "Fermeture, bandes, enduits, lissage. Le support est rendu droit et prêt "
     "à recevoir sa finition."),
    ("Carrelage et étanchéité",
     "Les pièces d'eau se traitent avant les sols secs : elles demandent des "
     "temps de séchage et salissent."),
    ("Sols",
     "Ragréage puis pose. Le sol arrive tard pour ne pas être abîmé par les "
     "lots précédents."),
    ("Peinture et revêtements muraux",
     "L'avant-dernier geste. Les retouches se font après la pose des "
     "plinthes et des portes."),
    ("Nettoyage et réception",
     "Deux passes, un tour du logement avec vous, la liste des réserves, "
     "puis les clés."),
]

# Correspondance entre un besoin exprimé et le lot qui y répond.
BESOINS = [
    ("« Mon appartement est sombre »", "faux-plafonds",
     "Éclairage intégré et teintes claires — souvent avec la peinture."),
    ("« Il me manque une chambre »", "cloisons",
     "Recouper un volume existant, isolation phonique comprise."),
    ("« Les murs sont fissurés »", "platrerie",
     "Traitement des fissures et reprise complète du support."),
    ("« Ma salle de bains a trente ans »", "carrelage",
     "Dépose, étanchéité et recarrelage du sol au plafond."),
    ("« La moquette doit partir »", "pose-de-sol",
     "Dépose, ragréage et pose d'un parquet, d'un vinyle ou d'un linoléum."),
    ("« Je reloue dans six semaines »", "peinture",
     "Remise en état entre deux baux, nettoyage compris."),
    ("« Je viens d'acheter, tout est à faire »", "renovation-complete",
     "Tous les lots coordonnés, un seul devis, une seule date."),
    ("« Les travaux sont finis, c'est inhabitable »", "nettoyage-fin-de-chantier",
     "Nettoyage de fin de chantier, même après une autre entreprise."),
]

# ------------------------------------------------------------ réalisations
# Les trois familles de biens que nous reprenons dans la région.
BIENS = [
    ("L'appartement ancien du centre",
     "Sous-Gare, Chauderon, le Vallon, la Cité",
     "Hauts plafonds, parquets à lames, murs en plâtre sur lattis. On y "
     "gagne des volumes que le neuf ne sait plus produire, et on y trouve "
     "des surprises derrière chaque cloison. Le travail porte d'abord sur "
     "les supports : ce sont eux qui décident du résultat.",
     ["Plâtrerie", "Peinture", "Sols", "Faux plafonds"]),
    ("La villa des hauts",
     "Chailly, Épalinges, Le Mont, Pully",
     "Des maisons des années soixante-dix et quatre-vingt, très cloisonnées, "
     "avec des volumes fermés que l'époque appréciait. L'essentiel du "
     "chantier consiste à rouvrir, à éclaircir et à remplacer des "
     "revêtements qui ont quarante ans.",
     ["Cloisons", "Carrelage", "Peinture", "Sols"]),
    ("L'immeuble de rendement",
     "Toute l'agglomération lausannoise",
     "Des remises en état entre deux locations, souvent logement par "
     "logement, dans un immeuble habité. La contrainte n'est pas technique, "
     "elle est calendaire : une date de libération ferme, cadrée sur "
     "l'entrée du locataire suivant.",
     ["Peinture", "Plâtrerie", "Sols", "Nettoyage"]),
]

# Ce qu'on découvre en ouvrant, et qui n'est jamais dans le devis initial.
SURPRISES = [
    ("Une chape qui n'est pas de niveau",
     "Deux à trois centimètres d'écart sur dix mètres, courant dans les "
     "immeubles d'avant-guerre. Un ragréage règle la question, mais il "
     "s'ajoute au devis s'il n'a pas été anticipé à la visite."),
    ("Un plancher bois sous le revêtement",
     "Sous un vieux linoléum, on trouve souvent des lames sur solives qui "
     "jouent. Un panneau de répartition devient nécessaire avant tout "
     "revêtement collé."),
    ("Des installations électriques d'un autre âge",
     "Fils sous tube métallique, absence de terre, tableau saturé. Nous ne "
     "sommes pas électriciens, mais nous le signalons et nous coordonnons "
     "l'intervention."),
    ("Un mur qui n'est pas celui qu'on croyait",
     "Porteur alors qu'il paraissait léger, ou l'inverse. Seul un relevé sur "
     "place tranche, et il vaut mieux le faire avant de vendre une ouverture."),
]

# -------------------------------------------------------------- références
# Trois manières de travailler avec nous, selon qui commande.
COLLABORATIONS = [
    ("Avec une régie",
     "Remises en état et site occupé",
     "Nous établissons des devis par logement, avec une date de libération "
     "ferme. Sur un immeuble, nous intervenons appartement par appartement "
     "au fil des relocations, sans bloquer les surfaces encore louées. Le "
     "nettoyage est compris : le logement est reloueable le jour de la "
     "réception.",
     ["Devis par logement", "Date de libération ferme", "Chantier en site occupé"]),
    ("Avec un architecte",
     "Exécution sur descriptif",
     "Nous répondons sur descriptif et nous tenons le planning des lots qui "
     "nous sont confiés. Les réunions de chantier sont suivies par le même "
     "responsable du début à la fin, ce qui évite de réexpliquer le dossier "
     "à chaque passage.",
     ["Réponse sur descriptif", "Interlocuteur unique", "Suivi de réunions"]),
    ("Avec un propriétaire",
     "Du premier appel aux clés",
     "C'est le cas le plus fréquent, et celui qui demande le plus de "
     "pédagogie. Nous expliquons ce que chaque poste recouvre, nous montrons "
     "les échantillons sur place et nous validons les teintes avec vous avant "
     "d'appliquer quoi que ce soit.",
     ["Devis expliqué", "Échantillons sur site", "Teintes validées"]),
]

# Ce que nous demandons en retour. Peu d'entreprises l'écrivent.
RECIPROQUE = [
    "Une décision sur les finitions avant le démarrage. Un carrelage choisi "
    "en cours de chantier arrête la pose pendant sa livraison.",
    "Un accès fiable. Une clé, un code, un voisin : l'équipe qui attend "
    "devant une porte fermée facture quand même sa matinée.",
    "Un interlocuteur unique de votre côté aussi. Deux avis contradictoires "
    "dans un couple ou entre associés coûtent plus cher qu'un imprévu "
    "technique.",
    "Le temps de séchage. Un enduit, une chape, une peinture ont leur rythme. "
    "Le seul moyen d'aller plus vite est de commencer plus tôt.",
]

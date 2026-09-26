"""Contenu propre à la page entreprise.

Le déroulé d'un chantier et la liste de ce que nous ne faisons pas sont
les deux blocs qui distinguent une entreprise d'une autre. Le premier
rassure, le second crédibilise : une maison qui sait dire non sait aussi
tenir ce qu'elle promet.
"""

HISTOIRE = [
    "DSG Rénovation a été fondée en 2019 à Lausanne, sur un savoir-faire "
    "transmis depuis plus de quarante ans. L'entreprise est jeune, le métier "
    "ne l'est pas.",
    "Nous avons choisi de rester une structure à taille humaine : onze "
    "professionnels salariés, et un réseau de plus de trente-cinq partenaires de "
    "la région que nous suivons depuis des années. C'est ce qui nous permet "
    "de tenir un planning, parce que nous savons qui vient et quand.",
    "Notre atelier est à l'avenue de Béthusy, sur les hauts de Lausanne. "
    "Cette proximité n'est pas un détail : elle décide de notre zone "
    "d'intervention, et donc de notre capacité à repasser sur un chantier "
    "pour une reprise de deux heures sans que cela ruine la journée.",
]

METIER = [
    "Nous ne faisons que de la rénovation. Pas de construction neuve, pas de "
    "promotion immobilière. Un logement occupé, un immeuble habité, des "
    "voisins à ménager et un calendrier de relocation à tenir : c'est notre "
    "terrain, et c'est un métier différent de celui du gros œuvre.",
    "Concrètement, cela veut dire que nous savons travailler dans trente "
    "mètres carrés avec un ascenseur étroit, que nous protégeons une cage "
    "d'escalier avant d'y monter le premier sac, et que nous rangeons le "
    "chantier chaque soir parce que quelqu'un y vit ou y passe.",
]

# Le déroulé d'un chantier, du premier appel à la remise des clés.
DEROULE = [
    ("Le premier appel",
     "Cinq à dix minutes. Nous cherchons à savoir si le projet entre dans "
     "notre métier et dans notre zone. Si ce n'est pas le cas, nous le disons "
     "tout de suite plutôt que de faire durer.",
     "Le jour même"),
    ("La visite et les mesures",
     "Nous venons sur place, mesurons, sondons les supports et notons les "
     "contraintes : accès, ascenseur, règlement de l'immeuble, horaires. "
     "C'est là que se jouent les trois quarts de la justesse du devis.",
     "Sous une semaine"),
    ("Le devis détaillé",
     "Poste par poste, avec les quantités, les finitions retenues et ce qui "
     "est compris — protections, évacuation, nettoyage. Rien n'est renvoyé à "
     "un « selon besoin ».",
     "72 heures après la visite"),
    ("Le planning daté",
     "Avant le premier jour, vous recevez le calendrier semaine par semaine "
     "de chaque corps de métier, avec la date de livraison.",
     "À la signature"),
    ("Le chantier",
     "Un responsable unique pilote tous les corps de métier et vous rend "
     "compte. Les imprévus "
     "sont signalés et chiffrés avant d'être exécutés, jamais après.",
     "Selon les travaux"),
    ("La réception",
     "Visite de fin de chantier avec vous, pièce par pièce : les défauts "
     "relevés sont repris sous dix jours, le logement est nettoyé, puis "
     "nous vous remettons les clés.",
     "Le dernier jour"),
]

# Ce que nous ne faisons pas. Dire non est un argument de vente.
LIMITES = [
    ("Nous ne faisons pas de construction neuve",
     "Ni de promotion. Notre métier est le bâti existant, avec ses surprises "
     "et ses voisins."),
    ("Nous ne touchons pas à la structure",
     "Ouvrir un mur porteur relève de l'ingénieur civil et d'une "
     "autorisation. Nous vous le disons à la visite et nous vous orientons."),
    ("Nous ne sortons pas de l'arc lémanique",
     "Un chantier à deux heures de route, c'est une équipe qui arrive en "
     "retard et qui ne repasse pas pour une reprise."),
    ("Nous ne sous-traitons pas en cascade",
     "Nos salariés font le travail, ou des partenaires que nous connaissons "
     "et que nous suivons. Pas d'entreprise inconnue découverte sur place."),
]

ENGAGEMENTS = [
    ("Un seul interlocuteur",
     "Un responsable de chantier unique pilote tous les corps de métier, du "
     "devis à la "
     "remise des clés. Vous ne coordonnez personne."),
    ("Un planning daté",
     "Le calendrier des corps de métier vous est transmis avant le démarrage, "
     "semaine par semaine, et tenu."),
    ("Des salariés, pas une cascade",
     "Onze professionnels de l'entreprise sur les chantiers. Les mêmes "
     "visages du premier au dernier jour."),
    ("Une réception en règle",
     "Visite de fin de chantier avec vous, défauts corrigés sous dix jours, "
     "nettoyage complet inclus."),
]

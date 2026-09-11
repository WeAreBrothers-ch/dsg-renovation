"""Les cinq lots de finition : ce que le client voit et touche.

Même structure que les lots de gros œuvre. Voir services_gros_oeuvre.py
pour le détail des champs.
"""

IMG = "https://static.wixstatic.com/media/"

SERVICES = [
    {
        "slug": "peinture",
        "resume": 'Préparation des fonds, mise en teinte intérieure et extérieure, finitions mates ou satinées.',
        "numero": "02",
        "nom": "Travaux de peinture",
        "nom_menu": "Peinture",
        "titre": 'Peintre à Lausanne — peinture intérieure et extérieure',
        "description": (
            "Entreprise de peinture à Lausanne : préparation des fonds, mise "
            "en teinte intérieure et extérieure, finitions mates ou satinées. "
            "Devis gratuit sous 72 heures."
        ),
        "h1": ["Travaux", "de peinture"],
        "chapo": (
            "Une belle peinture, c'est quatre-vingts pour cent de préparation "
            "et vingt pour cent d'application. Nous ne vendons pas la seconde "
            "sans faire la première."
        ),
        "image": IMG + "2c1464_a7cac83b91964ef7b403ba6eb333bd0b~mv2.jpg",
        "alt": "Dégagement et cuisine remis en peinture dans une villa lausannoise",
        "intro": [
            "Remise en peinture d'un appartement avant emménagement, reprise "
            "complète d'une villa, rafraîchissement entre deux locations pour "
            "une régie : la peinture est notre lot le plus demandé à Lausanne "
            "et sur la Riviera.",
            "Nous préparons les fonds avant de peindre, systématiquement. "
            "Rebouchage, ponçage, fixateur adapté au support : c'est ce "
            "travail invisible qui fait qu'une teinte tient dix ans au lieu "
            "de deux.",
            "Les teintes sont validées avec vous sur place, sur une surface "
            "d'essai. Une couleur ne se juge jamais sur un nuancier, elle se "
            "juge sur le mur, à la lumière de la pièce.",
        ],
        "prestations": [
            "Peinture intérieure : murs, plafonds, boiseries et radiateurs",
            "Peinture extérieure : façades, volets, ferronneries, balcons",
            "Préparation des fonds : rebouchage, ponçage, fixateur",
            "Laquage des portes, cadres et plinthes",
            "Peinture de rénovation entre deux locations",
            "Finitions mates, veloutées, satinées ou laquées",
            "Traitement des pièces humides par peinture anti-moisissure",
        ],
        "etapes": [
            ("Choix des teintes", "Essais sur le mur, jugés le matin et le "
             "soir : une teinte change entièrement selon la lumière."),
            ("Protection", "Sols, meubles et menuiseries bâchés avant la "
             "première ouverture de pot."),
            ("Préparation des fonds", "Rebouchage, ponçage, dépoussiérage, "
             "puis primaire adapté au support."),
            ("Application", "Deux couches de finition au minimum, croisées, "
             "avec contrôle sous éclairage rasant."),
            ("Repli", "Dépose des protections, nettoyage et remise en place "
             "du mobilier."),
        ],
        "reperes": [
            ("Appartement 100 m²", "1 à 2 semaines"),
            ("Couches de finition", "2 au minimum"),
            ("Teintes", "Essai sur site avant validation"),
            ("Devis", "Gratuit, remis sous 72 h"),
        ],
        "questions": [
            ("Peut-on repeindre par-dessus du papier peint ?",
             "Techniquement oui, durablement non. Les joints et les motifs "
             "finissent par réapparaître, et le papier se décolle en tirant la "
             "peinture avec lui. Nous déposons, nous reprenons le fond, puis "
             "nous peignons."),
            ("Combien de temps faut-il attendre avant de réemménager ?",
             "Une peinture en phase aqueuse est sèche au toucher en quelques "
             "heures et supporte le mobilier le lendemain. Comptez une "
             "quinzaine de jours pour la dureté finale : évitez de frotter "
             "les murs pendant ce délai."),
            ("Intervenez-vous pour une remise en état entre deux locataires ?",
             "C'est une part importante de notre activité pour les régies "
             "lausannoises. Nous intervenons entre deux baux, avec une date de "
             "libération ferme."),
        ],
        "lies": ["platrerie", "revetements-muraux", "renovation-complete", "nettoyage-fin-de-chantier"],
    },
    {
        "slug": "revetements-muraux",
        "resume": 'Papier peint, toile de verre et revêtements décoratifs posés sans raccord visible.',
        "numero": "05",
        "nom": "Revêtements muraux",
        "nom_menu": "Revêtements muraux",
        "titre": 'Papier peint et toile de verre à Lausanne',
        "description": (
            "Pose de revêtements muraux à Lausanne : papier peint, toile de "
            "verre, revêtements décoratifs, posés sans raccord visible. "
            "Devis gratuit."
        ),
        "h1": ["Revêtements", "muraux"],
        "chapo": (
            "Un papier peint se juge à ses raccords et à ses angles. C'est "
            "là, et nulle part ailleurs, qu'on voit qui l'a posé."
        ),
        "image": IMG + "2c1464_ab94350c74604962a66564240516acc5~mv2.jpg",
        "alt": "Mur habillé d'un revêtement décoratif dans un séjour rénové",
        "intro": [
            "Le papier peint est revenu, et il ne ressemble plus à celui des "
            "années soixante-dix. Panoramiques, intissés texturés, fibres "
            "naturelles : un seul pan de mur suffit souvent à donner un "
            "caractère à une pièce entière.",
            "La toile de verre, elle, répond à un autre besoin : masquer "
            "durablement un support fissuré. Peinte ensuite, elle tient là où "
            "l'enduit seul se rouvrirait.",
            "Dans les deux cas, le fond décide du résultat. Nous préparons le "
            "support avant de poser, comme pour une peinture.",
        ],
        "prestations": [
            "Pose de papier peint intissé, vinyle et traditionnel",
            "Panoramiques et lés numérotés, calepinés avant pose",
            "Toile de verre à peindre sur supports fissurés",
            "Revêtements décoratifs et effets de matière",
            "Dépose des anciens revêtements et reprise du fond",
            "Traitement des angles, tableaux et retours de fenêtre",
        ],
        "etapes": [
            ("Calepinage", "Nous plaçons les raccords aux endroits les moins "
             "visibles et démarrons depuis l'angle le plus vu."),
            ("Préparation du fond", "Dépose, rebouchage, ponçage et primaire "
             "d'accrochage : un intissé ne rattrape aucun défaut."),
            ("Pose", "Lés encollés, marouflés et arasés, avec contrôle du "
             "raccord sur chaque lé posé."),
            ("Finitions", "Angles, tableaux, retours et découpes autour des "
             "prises et des interrupteurs."),
        ],
        "reperes": [
            ("Pièce courante", "1 à 2 jours"),
            ("Panoramique", "Calepinage validé avant commande"),
            ("Toile de verre", "Peinte après pose, 2 couches"),
            ("Devis", "Gratuit, remis sous 72 h"),
        ],
        "questions": [
            ("Le papier peint tient-il dans une salle de bains ?",
             "Un vinyle sur intissé supporte une salle d'eau correctement "
             "ventilée, hors zone de projection directe. En contact avec "
             "l'eau, le carrelage reste la seule réponse durable."),
            ("Peut-on poser un papier peint sur un mur fissuré ?",
             "Pas directement : la fissure travaillera et déchirera le lé. "
             "Nous traitons d'abord la fissure, et nous posons une toile de "
             "verre quand le support bouge encore."),
        ],
        "lies": ["peinture", "platrerie", "renovation-complete", "faux-plafonds"],
    },
    {
        "slug": "carrelage",
        "resume": "Sols et murs, salles d'eau et cuisines, calepinage étudié avant pose.",
        "numero": "07",
        "nom": "Carrelage",
        "nom_menu": "Carrelage",
        "titre": 'Carreleur à Lausanne — pose de carrelage sol et mur',
        "description": (
            "Pose de carrelage à Lausanne : sols et murs, salles de bains et "
            "cuisines, grès cérame grand format, calepinage étudié avant pose. "
            "Devis gratuit."
        ),
        "h1": ["Pose", "de carrelage"],
        "chapo": (
            "Le calepinage se décide avant la première colle. Une fois posé, "
            "un carrelage mal parti se rattrape à la dépose, jamais autrement."
        ),
        "image": IMG + "2c1464_c44b6415607747ff9dccd68b224b3945~mv2.jpg",
        "alt": "Salle d'eau carrelée du sol au plafond dans un duplex rénové",
        "intro": [
            "Salle de bains reprise du sol au plafond, cuisine recarrelée, "
            "grand format posé dans une zone de jour : le carrelage est le "
            "revêtement le plus durable, à condition que le support et le "
            "tracé soient justes.",
            "Nous étudions le calepinage avant de poser : où tombe la coupe, "
            "comment se centre le motif, où passent les joints de "
            "fractionnement. C'est ce travail sur plan qui fait la différence "
            "entre une pose correcte et une pose soignée.",
            "L'étanchéité des zones humides est traitée sous le carrelage, "
            "avant la pose. C'est invisible, et c'est ce qui protège le "
            "logement du dessous.",
        ],
        "prestations": [
            "Carrelage de sol : grès cérame, pierre, grand format",
            "Faïence murale, salles de bains et crédences de cuisine",
            "Étanchéité sous carrelage des zones humides",
            "Ragréage et préparation des supports avant pose",
            "Pose droite, à joints décalés, en chevron ou en diagonale",
            "Plinthes, seuils, profilés d'angle et joints de finition",
            "Réfection de joints et remplacement de carreaux cassés",
        ],
        "etapes": [
            ("Contrôle du support", "Planéité, humidité, tenue : un support "
             "qui bouge fissure le carrelage, quel que soit le collage."),
            ("Calepinage", "Tracé des axes et position des coupes arrêtés "
             "avec vous avant la pose."),
            ("Étanchéité", "Natte ou résine sous les douches, les bacs et "
             "les zones de projection."),
            ("Pose et joints", "Collage au double encollage en grand format, "
             "puis jointoiement et nettoyage du voile de ciment."),
        ],
        "reperes": [
            ("Salle de bains", "1 à 2 semaines, étanchéité comprise"),
            ("Grand format", "Double encollage systématique"),
            ("Étanchéité", "Traitée sous le revêtement"),
            ("Devis", "Gratuit, remis sous 72 h"),
        ],
        "questions": [
            ("Peut-on carreler par-dessus un ancien carrelage ?",
             "Oui si l'ancien est parfaitement adhérent, plan et dégraissé, et "
             "si la surépaisseur ne bloque ni les portes ni les seuils. Sinon "
             "la dépose reste plus sûre, et souvent moins chère que la reprise "
             "d'un sinistre."),
            ("Le grand format convient-il à une petite salle d'eau ?",
             "Oui, et il l'agrandit visuellement en réduisant le nombre de "
             "joints. Il demande en revanche un support très plan : le "
             "ragréage préalable n'est pas optionnel."),
        ],
        "lies": ["pose-de-sol", "renovation-complete", "platrerie", "nettoyage-fin-de-chantier"],
    },
    {
        "slug": "pose-de-sol",
        "resume": 'Parquet, linoléum et vinyle, avec ragréage et plinthes assorties.',
        "numero": "08",
        "nom": "Pose de sol",
        "nom_menu": "Pose de sol",
        "titre": 'Pose de parquet, vinyle et linoléum à Lausanne',
        "description": (
            "Pose de sols à Lausanne : parquet, vinyle, linoléum, avec "
            "ragréage et plinthes assorties. Sols prêts à vivre, livrés "
            "propres. Devis gratuit."
        ),
        "h1": ["Pose", "de sol"],
        "chapo": (
            "Un sol se pose sur ce qu'il y a dessous. Le ragréage n'est pas "
            "une ligne de devis qu'on enlève pour faire baisser le total."
        ),
        "image": IMG + "2c1464_ce05ed0a65a14673bd0dcfe6d34744e1~mv2.jpg",
        "alt": "Sol posé dans une cuisine rénovée, raccords et plinthes ajustés",
        "intro": [
            "Parquet chêne dans un appartement lausannois, vinyle grand "
            "passage dans un logement de rendement, linoléum dans une pièce "
            "d'eau : le choix du revêtement dépend moins du goût que de "
            "l'usage de la pièce.",
            "Nous préparons systématiquement le support : dépose de l'ancien "
            "sol, contrôle de l'humidité de la chape, ragréage autolissant. "
            "Un sol posé sur un support irrégulier s'entend à chaque pas et "
            "s'use en priorité aux points hauts.",
            "Les plinthes et les seuils sont assortis et posés dans la foulée. "
            "C'est le détail qui distingue un chantier fini d'un chantier "
            "arrêté.",
        ],
        "prestations": [
            "Parquet contrecollé et massif, collé ou flottant",
            "Sols vinyle et LVL, lames ou dalles, grand passage",
            "Linoléum et sols souples en lés",
            "Ragréage autolissant et préparation des chapes",
            "Dépose et évacuation des anciens revêtements",
            "Plinthes, seuils, barres de jonction et finitions",
            "Sous-couches acoustiques pour les immeubles",
        ],
        "etapes": [
            ("Contrôle de la chape", "Humidité, planéité, cohésion : mesurés "
             "avant toute commande de revêtement."),
            ("Ragréage", "Autolissant sur primaire, puis séchage complet "
             "avant pose."),
            ("Acclimatation", "Le parquet passe quelques jours dans la pièce "
             "où il sera posé, sans quoi il travaille après la pose."),
            ("Pose et finitions", "Sens de pose arrêté avec vous, puis "
             "plinthes, seuils et nettoyage."),
        ],
        "reperes": [
            ("Appartement 100 m²", "3 à 5 jours, ragréage compris"),
            ("Acclimatation parquet", "48 à 72 h sur place"),
            ("Immeuble", "Sous-couche acoustique systématique"),
            ("Devis", "Gratuit, remis sous 72 h"),
        ],
        "questions": [
            ("Parquet ou vinyle pour un appartement en location ?",
             "Le vinyle grand passage encaisse mieux les rotations de "
             "locataires et se remplace pièce par pièce. Le parquet valorise "
             "davantage le bien à la revente. Le choix dépend de votre horizon, "
             "pas du produit."),
            ("Peut-on poser un sol sur un chauffage au sol ?",
             "Oui, avec un revêtement compatible et une résistance thermique "
             "adaptée. Le collage est alors préférable au flottant, qui isole "
             "le chauffage de la pièce."),
        ],
        "lies": ["carrelage", "renovation-complete", "peinture", "nettoyage-fin-de-chantier"],
    },
    {
        "slug": "nettoyage-fin-de-chantier",
        "resume": 'Logement rendu habitable immédiatement, vitres et sanitaires compris.',
        "numero": "09",
        "nom": "Nettoyage de fin de travaux",
        "nom_menu": "Nettoyage de fin de chantier",
        "titre": 'Nettoyage de fin de chantier à Lausanne',
        "description": (
            "Nettoyage de fin de travaux à Lausanne : poussière de chantier, "
            "vitres, sanitaires et sols. Logement rendu immédiatement "
            "habitable. Inclus dans nos rénovations."
        ),
        "h1": ["Nettoyage", "de fin de chantier"],
        "chapo": (
            "La poussière de plâtre se dépose trois fois avant de disparaître. "
            "Un nettoyage de chantier n'est pas un ménage, c'est un lot."
        ),
        "image": IMG + "2c1464_59c5df800ba245e2b7dff597bb0221a4~mv2.jpg",
        "alt": "Logement nettoyé après travaux, prêt à être occupé",
        "intro": [
            "Un chantier propre le dernier jour n'est pas un chantier fini. La "
            "poussière fine reste en suspension, retombe sur les plinthes, "
            "dans les rails de fenêtre, sur le dessus des portes.",
            "Nous traitons le nettoyage comme un lot à part entière, avec ses "
            "passes successives : décapage des traces de colle et de peinture, "
            "dépoussiérage complet, vitres et encadrements, sanitaires et "
            "robinetterie, puis sols.",
            "Sur nos rénovations, ce lot est compris dans le devis. Nous "
            "intervenons aussi seuls, après les travaux d'une autre "
            "entreprise ou avant un état des lieux de sortie.",
        ],
        "prestations": [
            "Dépoussiérage complet, plinthes et dessus de portes compris",
            "Décapage des traces de peinture, colle, ciment et adhésif",
            "Vitres, encadrements, rails et appuis de fenêtre",
            "Sanitaires, robinetterie et parois de douche détartrés",
            "Cuisine : façades, plans de travail, intérieur des placards",
            "Sols lavés selon la nature du revêtement posé",
            "Évacuation des derniers déchets et protections",
        ],
        "etapes": [
            ("Repli du chantier", "Dépose des protections et évacuation des "
             "derniers déchets et emballages."),
            ("Première passe", "Décapage des points durs et dépoussiérage "
             "descendant, du plafond vers le sol."),
            ("Seconde passe", "Rattrapage de la poussière retombée, vitres, "
             "sanitaires et cuisine."),
            ("Contrôle", "Tour du logement avec vous, pièce par pièce, avant "
             "remise des clés."),
        ],
        "reperes": [
            ("Appartement 100 m²", "1 à 2 jours"),
            ("Passes", "2 au minimum, poussière oblige"),
            ("Sur nos chantiers", "Compris dans le devis"),
            ("Seul", "Possible après une autre entreprise"),
        ],
        "questions": [
            ("Le nettoyage est-il compris dans vos devis de rénovation ?",
             "Oui, systématiquement. Nous ne rendons pas un logement à "
             "nettoyer : c'est la dernière image que vous gardez du chantier."),
            ("Intervenez-vous pour un état des lieux de sortie ?",
             "Oui, y compris sans avoir réalisé les travaux. C'est une demande "
             "fréquente des régies lausannoises entre deux locations."),
        ],
        "lies": ["renovation-complete", "peinture", "pose-de-sol", "carrelage"],
    },
]

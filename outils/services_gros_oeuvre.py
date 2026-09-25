"""Les quatre lots qui touchent à la structure et aux volumes.

Chaque service porte son propre contenu rédactionnel et ses mots-clés
de recherche locale. Rien n'est dupliqué d'un service à l'autre : deux
pages identiques à 80 % se pénalisent l'une l'autre dans les résultats
de recherche.
"""

IMG = "https://static.wixstatic.com/media/"

SERVICES = [
    {
        "slug": "renovation-complete",
        "resume": 'Appartement, maison ou immeuble repris de fond en comble, tous lots coordonnés.',
        "numero": "01",
        "nom": "Rénovation totale",
        "nom_menu": "Rénovation totale",
        "titre": "Rénovation complète d'appartement et de maison à Lausanne",
        "description": (
            "Rénovation totale clé en main à Lausanne et dans l'arc lémanique : "
            "tous les corps de métier coordonnés par un seul interlocuteur. "
            "Devis gratuit 72 h après la visite."
        ),
        "h1": ["Rénovation complète", "à Lausanne"],
        "chapo": (
            "Appartement, maison ou immeuble repris de fond en comble. Un seul "
            "contrat, un seul responsable de chantier, une seule date de "
            "livraison."
        ),
        "image": IMG + "2c1464_593f3a927ebd420ab56d4d306a4e6aa5~mv2.jpg",
        "alt": "Séjour et cuisine ouverte après rénovation complète d'un appartement à Lausanne",
        "intro": [
            "Une rénovation totale, c'est dix métiers qui doivent se succéder "
            "dans le bon ordre, sans se marcher dessus. Le carreleur ne peut "
            "pas passer avant le plâtrier, le peintre ne peut pas finir avant "
            "que les sols soient posés. C'est cette coordination qui fait "
            "tenir ou déraper un chantier.",
            "Nous prenons l'ensemble en charge. Vous signez un devis unique, "
            "vous recevez un planning daté avant le démarrage, et vous avez un "
            "seul numéro à appeler pendant toute la durée des travaux.",
            "Nous intervenons sur des appartements de Lausanne et de ses "
            "communes voisines, sur des villas de Pully, Lutry ou Épalinges, "
            "et sur des immeubles de rendement pour le compte de régies "
            "lausannoises.",
        ],
        "prestations": [
            "Dépose des revêtements, cloisons et équipements existants",
            "Ouverture ou création de volumes, cloisons et faux plafonds",
            "Reprise complète des murs et des plafonds, enduits et lissage",
            "Pose des sols : parquet, carrelage, vinyle, linoléum",
            "Mise en peinture de l'ensemble des surfaces et des boiseries",
            "Coordination des lots techniques : électricité, sanitaire, cuisine",
            "Nettoyage de fin de chantier et remise des clés",
        ],
        "etapes": [
            ("Visite et relevé", "Nous nous déplaçons, mesurons et relevons "
             "l'état existant. La visite est gratuite et sans engagement."),
            ("Devis détaillé", "72 heures après la visite, vous recevez un devis poste "
             "par poste, avec les quantités et les finitions retenues."),
            ("Planning daté", "Avant le premier coup de marteau, vous avez "
             "le calendrier semaine par semaine de tous les corps de métier."),
            ("Chantier suivi", "Un responsable unique pilote les lots et "
             "vous rend compte. Le chantier est rangé chaque soir."),
            ("Réception", "Visite contradictoire, liste des réserves, "
             "reprise sous dix jours, puis remise des clés."),
        ],
        "reperes": [
            ("Durée type", "5 à 8 semaines pour 100 m²"),
            ("Maison ou immeuble", "10 à 14 semaines"),
            ("Devis", "Gratuit, 72 h après visite"),
            ("Réserves", "Reprises sous 10 jours"),
        ],
        "questions": [
            ("Puis-je rester dans le logement pendant une rénovation totale ?",
             "C'est possible sur un chantier mené par zones, mais rarement "
             "souhaitable : une rénovation totale touche l'eau, l'électricité "
             "et les sols en même temps. Libérer les lieux raccourcit le "
             "chantier et réduit la facture."),
            ("Gérez-vous les autorisations et les demandes à la régie ?",
             "Nous préparons les descriptifs techniques que la régie ou la "
             "copropriété réclame, et nous nous adaptons aux horaires imposés "
             "par le règlement de l'immeuble."),
        ],
        "lies": ["platrerie", "peinture", "carrelage", "pose-de-sol"],
    },
    {
        "slug": "platrerie",
        "resume": 'Enduits, rebouchage, lissage et reprise complète de supports abîmés.',
        "numero": "03",
        "nom": "Plâtrerie",
        "nom_menu": "Plâtrerie",
        "titre": 'Plâtrerie à Lausanne — enduits, lissage et reprises',
        "description": (
            "Travaux de plâtrerie à Lausanne et sur l'arc lémanique : enduits, "
            "rebouchage, lissage et reprise de supports abîmés avant peinture. "
            "Devis gratuit."
        ),
        "h1": ["Plâtrerie", "et enduits"],
        "chapo": (
            "Un mur mal préparé se voit sous n'importe quelle peinture. La "
            "plâtrerie est le lot qui décide de la qualité de toutes les "
            "finitions qui suivent."
        ),
        "image": IMG + "2c1464_1f332a25fbc5404f8ea0424fc54875d2~mv2.jpg",
        "alt": "Mur repris en plâtrerie avant mise en peinture dans un appartement lausannois",
        "intro": [
            "Fissures, anciens papiers peints arrachés, trous de chevilles, "
            "angles épaufrés, plafonds fatigués : la plupart des logements "
            "anciens de Lausanne demandent une reprise sérieuse des supports "
            "avant toute mise en teinte.",
            "Nous travaillons les fonds jusqu'à obtenir une surface plane et "
            "régulière. Selon l'état du support et la finition visée, cela va "
            "du simple rebouchage au ratissage complet en pâte à lisser.",
            "Ce lot est presque toujours couplé à la peinture. Le confier à la "
            "même entreprise évite la discussion classique de fin de chantier, "
            "où le peintre reproche au plâtrier un fond mal dressé.",
        ],
        "prestations": [
            "Rebouchage des fissures, trous et saignées",
            "Ratissage et lissage intégral des murs et plafonds",
            "Reprise des angles, arêtes et tableaux de fenêtre",
            "Enduits de finition, du grain fin au lissé miroir",
            "Traitement des supports après dépose de papier peint",
            "Reprise des plafonds avant mise en peinture",
        ],
        "etapes": [
            ("Diagnostic du support", "Nous sondons les fonds : un enduit qui "
             "ne tient pas se voit au son, pas à l'œil."),
            ("Préparation", "Dépose de ce qui ne tient plus, dépoussiérage, "
             "application du fixateur adapté au support."),
            ("Enduit et ponçage", "Passes successives puis ponçage sous "
             "éclairage rasant, le seul qui révèle les défauts."),
            ("Contrôle avant peinture", "Le fond est validé avec vous avant "
             "que la première couche ne soit appliquée."),
        ],
        "reperes": [
            ("Finitions", "Q2 à Q4 selon l'exigence"),
            ("Pièce courante", "1 à 3 jours"),
            ("Couplage", "Le plus souvent avec la peinture"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "questions": [
            ("Faut-il lisser tous les murs avant de repeindre ?",
             "Non. Un mur sain et déjà lisse demande un simple rebouchage. Le "
             "ratissage complet se justifie sur un support marqué, après "
             "dépose de papier peint, ou pour une finition très tendue en "
             "lumière rasante."),
            ("Combien de temps faut-il attendre avant de peindre ?",
             "Compter vingt-quatre à quarante-huit heures de séchage selon "
             "l'épaisseur, la saison et la ventilation. Peindre sur un enduit "
             "encore humide se paie plus tard par des auréoles."),
        ],
        "lies": ["peinture", "renovation-complete", "faux-plafonds", "cloisons"],
    },
    {
        "slug": "cloisons",
        "resume": 'Création ou suppression de volumes, isolation phonique intégrée.',
        "numero": "04",
        "nom": "Cloisons placo &amp; alba",
        "nom_menu": "Cloisons",
        "titre": 'Pose de cloisons placo et alba à Lausanne',
        "description": (
            "Création et suppression de cloisons à Lausanne : placo, alba, "
            "isolation phonique intégrée. Gagner une chambre sans toucher au "
            "gros œuvre. Devis gratuit."
        ),
        "h1": ["Cloisons placo", "et alba"],
        "chapo": (
            "Créer une chambre, fermer un bureau, supprimer un couloir inutile. "
            "Redessiner un logement coûte bien moins cher que d'en changer."
        ),
        "image": IMG + "2c1464_59c5df800ba245e2b7dff597bb0221a4~mv2.jpg",
        "alt": "Cloison en plaques de plâtre montée pour créer une chambre dans un appartement",
        "intro": [
            "Beaucoup d'appartements lausannois ont de beaux volumes mal "
            "découpés : un séjour immense et deux chambres trop petites, ou un "
            "couloir qui mange dix mètres carrés utiles.",
            "Une cloison montée en plaques de plâtre sur ossature se pose en "
            "quelques jours, ne charge pas la structure et s'enlève aussi "
            "facilement qu'elle s'est montée. C'est le geste le plus rentable "
            "d'une rénovation.",
            "Nous intégrons systématiquement une isolation phonique dans "
            "l'ossature : une cloison sèche sans laine est un tambour, et le "
            "surcoût de la laine est dérisoire au regard du confort gagné.",
        ],
        "prestations": [
            "Montage de cloisons sur ossature métallique, placo ou alba",
            "Isolation phonique en laine minérale intégrée",
            "Doublage de murs existants, thermique ou acoustique",
            "Création de gaines techniques et de coffrages",
            "Dépose de cloisons non porteuses et reprise des sols et plafonds",
            "Habillage des tableaux, angles et raccords",
        ],
        "etapes": [
            ("Repérage", "Nous vérifions ce qui est porteur et ce qui ne "
             "l'est pas, et relevons le passage des gaines existantes."),
            ("Tracé au sol", "L'implantation est tracée et validée avec vous "
             "sur place : une cloison se juge mieux au sol que sur un plan."),
            ("Ossature et isolant", "Rails, montants, laine minérale, puis "
             "réservations pour les prises et les interrupteurs."),
            ("Plaques et bandes", "Vissage, bandes à joint, enduit et ponçage "
             "jusqu'au fond prêt à peindre."),
        ],
        "reperes": [
            ("Cloison simple", "2 à 3 jours, finition comprise"),
            ("Isolation", "Laine minérale systématique"),
            ("Épaisseur courante", "de 7 à 10 cm"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "questions": [
            ("Puis-je abattre un mur pour ouvrir la cuisine ?",
             "Seulement s'il n'est pas porteur. Nous le vérifions lors de la "
             "visite. Sur un mur porteur, l'ouverture reste possible mais "
             "exige un ingénieur civil et une autorisation : nous vous le "
             "disons franchement avant d'aller plus loin."),
            ("Une cloison en plaques isole-t-elle vraiment du bruit ?",
             "Correctement montée, avec laine minérale et joints traités, elle "
             "isole souvent mieux qu'une cloison maçonnée mince. Le point "
             "faible n'est jamais la plaque, c'est le raccord mal fait."),
        ],
        "lies": ["platrerie", "faux-plafonds", "renovation-complete", "peinture"],
    },
    {
        "slug": "faux-plafonds",
        "resume": 'Plafonds suspendus, intégration des éclairages et des gaines techniques.',
        "numero": "06",
        "nom": "Faux plafonds",
        "nom_menu": "Faux plafonds",
        "titre": 'Faux plafonds à Lausanne — éclairage intégré',
        "description": (
            "Pose de faux plafonds à Lausanne et en région lémanique : "
            "plafonds suspendus, spots encastrés, gaines techniques masquées, "
            "correction acoustique. Devis gratuit."
        ),
        "h1": ["Faux plafonds", "et éclairage"],
        "chapo": (
            "Le plafond est la seule surface que personne ne regarde et que "
            "tout le monde voit. C'est aussi le meilleur endroit pour faire "
            "disparaître ce qui doit l'être."
        ),
        "image": IMG + "2c1464_a6d8829808714189a920f4d0c39660b9~mv2.jpg",
        "alt": "Faux plafond avec éclairage intégré dans un appartement rénové à Lausanne",
        "intro": [
            "Un faux plafond résout en une fois trois problèmes courants : un "
            "plafond ancien trop abîmé pour être repris, des gaines de "
            "ventilation ou d'électricité qui courent en apparent, et un "
            "éclairage central unique qui écrase la pièce.",
            "Nous posons des plafonds suspendus sur ossature, avec les "
            "réservations des spots percées avant montage et le cheminement "
            "des câbles préparé en amont.",
            "Dans les logements anciens de Lausanne, c'est souvent le geste "
            "qui transforme le plus une pièce pour le budget le plus "
            "raisonnable.",
        ],
        "prestations": [
            "Plafonds suspendus sur ossature métallique",
            "Intégration de spots encastrés et de bandeaux lumineux",
            "Masquage des gaines de ventilation et des chemins de câbles",
            "Correction acoustique par plaques perforées ou laine",
            "Retombées, décaissés et gorges d'éclairage indirect",
            "Trappes de visite pour les organes techniques",
        ],
        "etapes": [
            ("Relevé des contraintes", "Hauteur disponible, position des "
             "gaines, points d'alimentation : tout se décide avant la pose."),
            ("Plan de calepinage", "Position des spots arrêtée avec vous, "
             "sur plan, avant le premier perçage."),
            ("Ossature et isolant", "Suspentes, fourrures, laine acoustique "
             "si la pièce le demande."),
            ("Plaques et finitions", "Vissage, bandes, enduit, ponçage, puis "
             "pose des luminaires."),
        ],
        "reperes": [
            ("Perte de hauteur", "de 8 à 15 cm selon le cas"),
            ("Pièce courante", "3 à 5 jours"),
            ("Éclairage", "Calepinage validé avant pose"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "questions": [
            ("Combien de hauteur sous plafond vais-je perdre ?",
             "Entre huit et quinze centimètres dans la plupart des cas. Si la "
             "hauteur est déjà juste, une retombée partielle sur le seul "
             "passage des gaines préserve le reste de la pièce."),
            ("Peut-on encore accéder aux gaines une fois le plafond fermé ?",
             "Oui, par des trappes de visite que nous posons face aux organes "
             "qui peuvent demander une intervention. Fermer un plafond sans "
             "trappe est une faute qui se paie au premier incident."),
        ],
        "lies": ["platrerie", "cloisons", "peinture", "renovation-complete"],
    },
]

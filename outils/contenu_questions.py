"""Les questions fréquentes, groupées par moment du projet.

Vingt questions au lieu de six. Ce n'est pas du remplissage : chacune
répond à une recherche réelle, et les réponses sont assez précises pour
être reprises telles quelles par un moteur. Une réponse évasive ne sert
ni le visiteur ni le référencement.
"""

GROUPES = [
    {
        "nom": "Avant le devis",
        "cote": "Zone, gratuité, délais",
        "titre": "Avant de|nous appeler",
        "questions": [
            ("Intervenez-vous en dehors de Lausanne ?",
             "Oui. Nous travaillons sur tout l'arc lémanique : Lausanne et "
             "ses communes voisines — Pully, Prilly, Renens, Ecublens, "
             "Épalinges, Lutry —, ainsi que Morges, Nyon, Vevey, Montreux et "
             "Genève. Au-delà, appelez-nous : nous étudions la demande au cas "
             "par cas, en fonction de la taille du chantier."),
            ("Le devis est-il vraiment gratuit ?",
             "Oui, visite et relevé compris, sans aucun engagement. Vous "
             "recevez un devis détaillé poste par poste sous 72 heures "
             "ouvrables après le passage. Nous ne facturons pas l'étude, "
             "même si vous ne donnez pas suite."),
            ("Sous quel délai pouvez-vous démarrer ?",
             "Comptez généralement quatre à huit semaines entre la signature "
             "et le premier jour de chantier, selon la saison et la taille "
             "du lot. Les remises en état entre deux locations se calent plus "
             "vite, parce qu'elles sont courtes."),
            ("Intervenez-vous pour un seul poste, ou seulement en rénovation complète ?",
             "Les deux. Une remise en peinture seule, un sol à changer, une "
             "salle de bains à recarreler : ce sont des demandes courantes. "
             "Nous disons franchement quand un chantier est trop petit pour "
             "qu'un déplacement ait du sens."),
            ("Faut-il vider le logement avant votre visite ?",
             "Non. La visite sert à relever et à comprendre, pas à commencer. "
             "Nous avons seulement besoin d'accéder aux pièces concernées et, "
             "si possible, de voir un angle de mur dégagé pour juger l'état "
             "des supports."),
        ],
    },
    {
        "nom": "Pendant le chantier",
        "cote": "Organisation, nuisances, présence",
        "titre": "Pendant|les travaux",
        "questions": [
            ("Puis-je rester dans le logement pendant les travaux ?",
             "Sur un lot isolé — peinture d'une pièce, changement de sol —, "
             "oui sans difficulté. Sur une rénovation complète, c'est "
             "possible en travaillant par zones, mais le chantier dure plus "
             "longtemps et coûte davantage. Libérer les lieux reste la "
             "solution la plus économique."),
            ("Qui coordonne les différents corps de métier ?",
             "Nous. Un responsable de chantier unique pilote l'ensemble des "
             "lots et reste votre seul interlocuteur, du devis à la remise "
             "des clés. Vous n'avez aucun planning à faire coïncider."),
            ("Quels sont vos horaires de chantier ?",
             "En règle générale de 8 h à 17 h, du lundi au vendredi. En "
             "immeuble, nous nous alignons sur le règlement de la "
             "copropriété, qui encadre souvent les travaux bruyants et "
             "l'usage de l'ascenseur."),
            ("Comment protégez-vous le logement et les parties communes ?",
             "Sols bâchés, mobilier restant protégé et filmé, cage d'escalier "
             "et ascenseur protégés sur le trajet emprunté. Le chantier est "
             "rangé chaque soir : c'est une règle interne, pas une faveur."),
            ("Que se passe-t-il si vous découvrez un problème imprévu ?",
             "Nous arrêtons, nous vous appelons et nous chiffrons l'écart "
             "avant de reprendre. Une chape hors niveau, une gaine non "
             "conforme ou un mur porteur mal identifié se traitent par un "
             "avenant écrit, jamais par une facture de fin de chantier."),
        ],
    },
    {
        "nom": "Prix et paiement",
        "cote": "Devis, avenants, échéances",
        "titre": "Ce que ça|coûte",
        "questions": [
            ("Combien coûte une rénovation complète à Lausanne ?",
             "Le prix dépend de l'état existant bien plus que de la surface. "
             "Deux appartements de cent mètres carrés peuvent varier du "
             "simple au double selon que les sols sont récupérables ou non, "
             "que les cloisons bougent, que la salle de bains est reprise. "
             "C'est pourquoi nous ne publions pas de prix au mètre carré : "
             "il serait faux dans un cas sur deux."),
            ("Votre devis peut-il augmenter en cours de chantier ?",
             "Pas sans votre accord écrit. Le devis signé fixe les postes et "
             "les quantités. Seuls un imprévu constaté ou une modification "
             "que vous demandez donnent lieu à un avenant, chiffré et validé "
             "avant exécution."),
            ("Comment se déroulent les paiements ?",
             "Un acompte à la signature, des situations intermédiaires sur "
             "les chantiers longs, et le solde à la réception une fois les "
             "réserves levées. Les modalités exactes figurent sur le devis."),
            ("Faut-il vous fournir les matériaux ?",
             "Non, nous les fournissons et ils figurent au devis. Si vous "
             "préférez acheter vous-même un carrelage ou un parquet précis, "
             "c'est possible : nous le posons, et nous vous indiquons "
             "auparavant les quantités et les contraintes de pose."),
            ("Comment comparer votre devis à un autre ?",
             "Poste par poste, pas au total. Vérifiez si la préparation des "
             "supports, l'évacuation des déchets, les protections et le "
             "nettoyage final y figurent : ce sont les lignes que l'on retire "
             "pour faire baisser un total, et celles qui réapparaissent en "
             "cours de chantier."),
        ],
    },
    {
        "nom": "Après la livraison",
        "cote": "Réception, réserves, régies",
        "titre": "Une fois|le chantier livré",
        "questions": [
            ("Comment se passe la réception du chantier ?",
             "Par une visite contradictoire, pièce par pièce, avec vous. Ce "
             "qui ne va pas est noté sur une liste de réserves, que nous "
             "reprenons sous dix jours. Les clés sont remises une fois les "
             "réserves levées."),
            ("Le nettoyage est-il compris ?",
             "Oui, systématiquement, sur tous nos chantiers. Nous ne rendons "
             "pas un logement à nettoyer : c'est la dernière image que vous "
             "gardez du travail."),
            ("Que faire si un défaut apparaît après la livraison ?",
             "Appelez-nous. Une fissure de retrait, un joint qui se rétracte "
             "ou une porte qui travaille dans les premiers mois relèvent du "
             "comportement normal des matériaux, et nous revenons les "
             "reprendre. Les garanties légales du droit suisse s'appliquent "
             "par ailleurs."),
            ("Travaillez-vous pour les régies et les propriétaires bailleurs ?",
             "C'est une part importante de notre activité à Lausanne : "
             "remises en état entre deux locations, rénovations d'immeubles "
             "en site occupé, interventions planifiées au fil des "
             "relocations, avec une date de libération ferme."),
            ("Pouvez-vous intervenir sur un logement que vous n'avez pas rénové ?",
             "Oui, notamment pour un nettoyage de fin de travaux ou une "
             "remise en état avant état des lieux de sortie, après le passage "
             "d'une autre entreprise."),
        ],
    },
]


def toutes():
    """La liste à plat, pour le balisage structuré."""
    return [q for g in GROUPES for q in g["questions"]]

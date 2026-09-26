"""Ce que Lausanne impose aux deux prestations de situation.

Même principe que lausanne_gros_oeuvre.py et lausanne_finitions.py : ce
que le bâti et le marché locatif lausannois changent concrètement au
chantier. Les clés sont les slugs des fiches de services_solutions.py.
Les faits viennent des pages existantes ; la source de chacun est notée
sous son entrée.
"""

LOCAL = {
    "remise-en-etat-appartement": {
        "titre": "Relouer|à Lausanne",
        "cote": "Calendrier, immeuble habité",
        "paragraphes": [
            "À Lausanne, un appartement libéré trouve vite preneur, et la "
            "remise en état doit souvent être terminée quelques jours à peine "
            "avant l'arrivée du locataire suivant. La difficulté tient donc "
            "au calendrier plus qu'à la technique. Et pour le propriétaire, "
            "rendre le logement en retard coûte un mois de loyer.",
            "Le chantier se tient au milieu d'un immeuble où l'on vit. Le "
            "règlement de l'immeuble fixe les heures où le bruit est permis "
            "et l'usage de l'ascenseur ; nous protégeons la cage d'escalier "
            "sur le trajet emprunté et nous rangeons chaque soir, parce que "
            "les voisins, eux, restent chez eux pendant tout le chantier.",
            "Changer le sol d'un logement loué pose deux questions. La "
            "première est ce qu'il y a dessous : sous une moquette des années "
            "soixante dort souvent un parquet d'origine, qu'il est parfois "
            "possible de sauver. La seconde concerne les voisins : une "
            "sous-couche acoustique sous le sol neuf évite la plainte la plus "
            "courante après des travaux, le bruit des pas.",
        ],
        "encadre": {
            "titre": "Ce qui fait tenir la date",
            "points": [
                "Une date de remise ferme, écrite dans le devis de chaque "
                "logement.",
                "Des teintes et un sol choisis avant le premier jour, pas en "
                "cours de chantier.",
                "Un accès fiable dès le premier matin : une clé, un code ou "
                "un voisin.",
            ],
        },
    },
    # Sources :
    #   lausanne_finitions.py:125-128 — logement qui se reloue vite, date calée
    #     à quelques jours près sur l'entrée du locataire suivant.
    #   contenu_divers.py:75-81 — contrainte calendaire plutôt que technique,
    #     immeuble habité.
    #   pages_site.py:131-137 — un logement rendu en retard coûte un mois de
    #     loyer au propriétaire.
    #   contenu_questions.py:64-68 ; contenu_questions.py:69-72 ;
    #     contenu_devis.py:66-68 ; lausanne_gros_oeuvre.py:82-85 ;
    #     contenu_entreprise.py:28-31 — règlement de l'immeuble (travaux
    #     bruyants, ascenseur) ; cage d'escalier protégée sur le trajet
    #     emprunté ; chantier rangé chaque soir parce que quelqu'un y vit.
    #   lausanne_finitions.py:98-100 ; lausanne_finitions.py:106-108 — parquet
    #     d'origine parfois récupérable sous la moquette des années soixante ;
    #     sous-couche acoustique, principale source de conflit entre voisins :
    #     les bruits de pas.
    #   contenu_divers.py:107-114 ; contenu_divers.py:133-136 — date de remise
    #     ferme et devis par logement ; finitions décidées avant le démarrage ;
    #     accès fiable : une clé, un code, un voisin.
    "renovation-salle-de-bains": {
        "titre": "Derrière|la faïence",
        "cote": "Chapes, planchers bois, conduites",
        "paragraphes": [
            "Dans un immeuble ancien de Sous-Gare, de Chauderon ou du Vallon, "
            "la vieille faïence peut cacher une chape posée sur du sable, un "
            "plancher bois ou d'anciennes conduites en plomb. Nous les "
            "repérons à la visite, pour que le devis les prévoie au lieu de "
            "les découvrir le jour de la dépose.",
            "Un plancher bois ne reçoit pas un carrelage tel quel. Il faut "
            "d'abord le couvrir d'un panneau de répartition, sans quoi le "
            "mouvement des lames se transmet au carrelage et finit par le "
            "fissurer. Une chape hors niveau se rattrape, elle, par une mise "
            "à niveau du sol (ragréage) avant la pose.",
            "Les conduites en plomb et l'électricité ancienne, avec ses fils "
            "sous tube métallique et sans mise à la terre, relèvent de nos "
            "partenaires : nous signalons ce que la dépose met au jour et nous "
            "les faisons intervenir avant de refermer.",
        ],
        "encadre": {
            "titre": "Ce que nous notons aussi",
            "points": [
                "L'étage et l'ascenseur, qui décident de la durée de la dépose.",
                "Le règlement de l'immeuble : heures des travaux bruyants, "
                "usage de l'ascenseur.",
                "La cage d'escalier et le stationnement, pour planifier les "
                "livraisons et l'évacuation.",
            ],
        },
    },
    # Sources :
    #   lausanne_gros_oeuvre.py:14-18 — Sous-Gare, Chauderon, Vallon :
    #     immeubles du premier tiers du vingtième siècle.
    #   lausanne_finitions.py:74-77 — chapes sur sable, canalisations en plomb,
    #     planchers bois sous la faïence, relevés à la visite.
    #   lausanne_finitions.py:102-105 ; contenu_divers.py:91-94 ;
    #     services_finitions.py:199-200 — plancher bois : panneau de
    #     répartition avant tout revêtement collé, sinon le jeu des lames se
    #     retransmet ; un support qui bouge fissure le carrelage.
    #   contenu_divers.py:86-90 ; lausanne_gros_oeuvre.py:32 — chape hors
    #     niveau rattrapée par une mise à niveau (ragréage).
    #   contenu_divers.py:95-98 ; services_gros_oeuvre.py:52 ;
    #     lausanne_gros_oeuvre.py:34 — fils sous tube métallique, absence de
    #     terre ; signalés, intervention coordonnée ; coordination de
    #     l'électricité et du sanitaire avec les partenaires.
    #   lausanne_finitions.py:78-81 ; lausanne_finitions.py:86-87 ;
    #     contenu_questions.py:64-68 ; contenu_entreprise.py:41-44 — cages
    #     d'escalier serrées, stationnement limité, livraisons planifiées ;
    #     dépose selon l'étage et l'ascenseur ; règlement de l'immeuble ; accès
    #     noté à la visite.
}

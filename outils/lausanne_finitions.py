"""Ce que chaque métier de finition rencontre dans le bâti lausannois.

Voir lausanne_gros_oeuvre.py pour le principe : du contenu que seule
une entreprise qui travaille ici peut écrire.
"""

LOCAL = {
    "peinture": {
        "titre": "Peindre|à Lausanne",
        "cote": "Lumière du lac, supports anciens",
        "paragraphes": [
            "L'orientation change tout. Un appartement de Sous-Gare ouvert "
            "plein sud sur le lac reçoit une lumière franche et froide qui "
            "durcit les gris ; le même gris posé dans un logement du Vallon, "
            "orienté nord, vire au bleu. C'est la raison pour laquelle nous "
            "peignons toujours une surface d'essai sur place.",
            "Les supports anciens demandent un fixateur. Le plâtre sur "
            "lattis des immeubles d'avant-guerre boit énormément : sans "
            "primaire adapté, la première couche disparaît dans le mur et la "
            "teinte finit inégale.",
            "Dans les logements locatifs remis en état entre deux baux, "
            "nous travaillons en blanc cassé ou en teintes claires : elles "
            "supportent les retouches localisées, là où une teinte soutenue "
            "impose de refaire le pan entier au premier choc.",
        ],
        "encadre": {
            "titre": "Trois erreurs qui coûtent cher",
            "points": [
                "Choisir une teinte sur nuancier en magasin, sous un "
                "éclairage qui n'a rien à voir avec celui de la pièce.",
                "Peindre par-dessus un papier peint pour gagner deux jours, "
                "et le voir se décoller six mois plus tard.",
                "Appliquer une seule couche sur un changement de teinte "
                "marqué : le fond réapparaît en séchant.",
            ],
        },
    },
    "revetements-muraux": {
        "titre": "Poser|dans l'ancien",
        "cote": "Murs qui ne sont jamais droits",
        "paragraphes": [
            "Dans un immeuble lausannois ancien, aucun angle n'est à "
            "quatre-vingt-dix degrés et aucun mur n'est d'aplomb sur toute sa "
            "hauteur. Un lé posé au fil à plomb dérive visiblement en trois "
            "mètres si le plan de pose n'a pas été pensé avant.",
            "C'est pourquoi nous partons de l'angle le plus vu de la pièce, "
            "généralement celui qu'on découvre en entrant, et nous reportons "
            "le rattrapage dans l'angle le plus discret, souvent derrière la "
            "porte.",
            "La toile de verre trouve ici son meilleur usage : sur un mur "
            "ancien qui travaille encore, elle ponte les microfissures et "
            "tient là où l'enduit seul se rouvrirait au premier hiver.",
        ],
        "encadre": {
            "titre": "Ce qui se décide avant la commande",
            "points": [
                "Le métrage réel, relevé sur place : un panoramique se "
                "commande au lé près, il ne se rattrape pas.",
                "Le sens du raccord et le mur de départ.",
                "L'état du fond : un intissé ne masque aucun défaut, il les "
                "révèle en lumière rasante.",
            ],
        },
    },
    "carrelage": {
        "titre": "Carreler|en immeuble",
        "cote": "Étanchéité, voisins, accès",
        "paragraphes": [
            "Une salle de bains d'immeuble lausannois se refait presque "
            "toujours au-dessus d'un logement occupé. L'étanchéité posée sous "
            "le carrelage n'est donc pas un supplément de confort : c'est ce "
            "qui protège le plafond du voisin, et c'est le poste sur lequel "
            "nous ne transigeons jamais.",
            "Dans l'ancien, la dépose réserve son lot d'imprévus : anciennes "
            "chapes sur sable, canalisations en plomb, planchers bois sous la "
            "faïence. Nous relevons ces points à la visite plutôt que de les "
            "découvrir la semaine du chantier.",
            "L'accès compte autant que la pose. En vieille ville et dans les "
            "rues étroites de Sous-Gare, les cages d'escalier sont serrées et "
            "le stationnement limité : les livraisons se planifient, et les "
            "parties communes se protègent avant le premier carton.",
        ],
        "encadre": {
            "titre": "Une salle de bains, poste par poste",
            "points": [
                "Dépose et évacuation : un à deux jours selon l'étage et "
                "l'ascenseur.",
                "Reprise du support et étanchéité : deux jours, séchage "
                "compris.",
                "Pose, jointoiement et sanitaires : le reste de la semaine.",
            ],
        },
    },
    "pose-de-sol": {
        "titre": "Des sols|qui ont vécu",
        "cote": "Planchers bois, chapes anciennes",
        "paragraphes": [
            "Sous la moquette d'un appartement lausannois des années "
            "soixante, on trouve souvent un parquet à lames d'origine, parfois "
            "récupérable. Sous un vieux linoléum d'immeuble d'avant-guerre, "
            "on trouve un plancher bois sur solives, qui bouge et qui grince.",
            "Ces supports ne se ragréent pas comme une chape béton. Un "
            "plancher bois demande un panneau de répartition avant tout "
            "revêtement collé, sans quoi le jeu des lames se retransmet au "
            "sol neuf en quelques mois.",
            "En immeuble, la sous-couche acoustique n'est pas négociable. "
            "Elle coûte peu et règle la principale source de conflit entre "
            "voisins après une rénovation : les bruits de pas.",
        ],
        "encadre": {
            "titre": "Ce que nous vérifions avant de poser",
            "points": [
                "L'humidité résiduelle de la chape, mesurée et non estimée.",
                "La planéité : deux millimètres sous une règle de deux "
                "mètres, pas davantage.",
                "La hauteur disponible sous les portes et au droit des "
                "seuils.",
            ],
        },
    },
    "nettoyage-fin-de-chantier": {
        "titre": "Rendre|les clés",
        "cote": "État des lieux et relocation",
        "paragraphes": [
            "Sur le marché lausannois, un logement se reloue vite : la date "
            "de remise du logement est souvent calée sur l'entrée du locataire "
            "suivant, à quelques jours près. Le nettoyage n'est pas la "
            "dernière ligne du devis, c'est ce qui rend la date tenable.",
            "Un état des lieux de sortie se joue sur des détails que la "
            "poussière de chantier masque : rails de fenêtre, dessus de "
            "portes, joints de faïence, intérieur des placards. Ce sont "
            "précisément les points que nous reprenons en seconde passe.",
            "Nous intervenons aussi pour des régies sur des logements que "
            "nous n'avons pas rénovés, entre deux baux, avec un tour du "
            "logement en commun avant la remise des clés.",
        ],
        "encadre": {
            "titre": "Ce que regarde un état des lieux",
            "points": [
                "Les rails et les gonds de fenêtre, jamais nettoyés en cours "
                "de chantier.",
                "Le détartrage complet de la robinetterie et des parois de "
                "douche.",
                "L'intérieur des placards et le dessus des portes, hors du "
                "champ de vision courant.",
            ],
        },
    },
}

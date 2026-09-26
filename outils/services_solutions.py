"""Deux fiches tournées vers une situation plutôt que vers un métier.

La remise en état entre deux locations et la rénovation d'une salle de
bains mobilisent des métiers déjà décrits dans services_finitions.py :
peinture, plâtrerie, carrelage, sols, nettoyage. Ces fiches ne répètent
pas ces pages. Elles partent de la situation du client — un logement à
relouer à date fixe, une salle de bains à refaire au-dessus d'un voisin —
et renvoient vers la page du métier quand le détail est utile.

Même structure que services_finitions.py ; voir services_gros_oeuvre.py
pour le principe. Aucun fait n'est nouveau : durées, délais et façons de
faire figurent déjà ailleurs dans outils/, et la source de chacun est
notée sous sa fiche.

Sur une page qui ne porte qu'une fiche, le générateur n'affiche de la
fiche que `intro`, `prestations`, `etapes` et `questions` (et lit `nom`
pour le balisage) : titre, description, chapô, image et repères sont
ceux de l'entrée correspondante de pages_solutions.py, recopiés ici à
l'identique comme pour les fiches existantes.

Les introductions et certaines réponses portent des liens écrits
`<a href="{base}services/….html">` : assemblage.assembler() y remplace
`{base}` par le préfixe de la page, comme pour services_finitions.py.
"""

IMG = "https://static.wixstatic.com/media/"

SERVICES = [
    {
        "slug": "remise-en-etat-appartement",
        "resume": "Logement remis en état entre deux locataires, rendu à "
                  "date fixe, nettoyage compris.",
        "numero": "06",
        "nom": "Remise en état entre deux locations",
        "nom_menu": "Remise en état",
        "titre": "Remise en état d'appartement à Lausanne — entre locataires",
        "description": (
            "Remise en état d'appartement à Lausanne entre deux locataires : "
            "peinture, joints, sols, nettoyage, logement rendu à date fixe. "
            "Devis gratuit."
        ),
        "h1": ["Remise en état d'appartement", "à Lausanne"],
        "chapo": (
            "Entre deux locataires, tout se règle sur une date. Nous "
            "remettons le logement en état et le rendons propre, prêt pour "
            "l'état des lieux d'entrée."
        ),
        "image": IMG + "2c1464_59c5df800ba245e2b7dff597bb0221a4~mv2.jpg",
        "alt": "Logement nettoyé après travaux, prêt à être occupé",
        "intro": [
            "Une remise en état d'appartement entre deux locations part d'une "
            "date plutôt que d'un plan : celle où le locataire suivant reçoit "
            "les clés. À Lausanne, ce travail pour les régies, les gérances "
            "et les propriétaires bailleurs occupe une place importante dans "
            "notre activité. Chaque logement a son propre devis et une date "
            "de remise ferme.",
            "Le travail porte sur ce que les années de location ont marqué : "
            "trous de chevilles, fissures, murs et plafonds défraîchis, joints "
            "de faïence, carreaux cassés, sol usé. Du simple rafraîchissement "
            "au changement de sol, chaque poste est chiffré à part, et vous "
            "décidez de ce qui se refait maintenant ou au prochain départ. "
            "Sur les murs, la "
            '<a href="{base}services/peinture.html">remise en peinture</a> '
            "commence toujours par la préparation des fonds.",
            "Le "
            '<a href="{base}services/nettoyage-fin-de-chantier.html">nettoyage '
            "de fin de chantier</a> est compris, vitres, placards et "
            "robinetterie inclus : le logement peut être reloué dès la fin "
            "des travaux. Nous intervenons aussi avant un état des lieux de "
            "sortie, y compris dans un appartement que nous n'avons pas "
            "rénové.",
        ],
        "prestations": [
            "Rebouchage des trous de chevilles, des fissures et des angles abîmés",
            "Murs et plafonds repeints en blanc cassé ou en teinte claire",
            "Portes, cadres et plinthes relaqués",
            "Peinture anti-moisissure dans les pièces humides",
            "Joints de faïence refaits, carreaux cassés remplacés",
            "Changement de sol : vinyle grand passage, linoléum ou parquet, "
            "sur sous-couche acoustique en immeuble",
            "Nettoyage complet : vitres, rails de fenêtre, placards et sols",
            "Robinetterie et parois de douche détartrées",
            "Évacuation des anciens revêtements et des déchets de chantier",
        ],
        "etapes": [
            ("Visite du logement", "Sous une semaine, nous passons mesurer et "
             "noter l'état de chaque pièce ; le logement n'a pas besoin "
             "d'être vidé."),
            ("Devis par logement", "Chaque appartement reçoit son devis poste "
             "par poste, 72 heures après la visite."),
            ("Date de remise", "Fixée au devis et calée sur l'entrée du "
             "locataire suivant : c'est une date ferme."),
            ("Travaux dans l'ordre", "Rebouchage, joints et sols d'abord, "
             "peinture ensuite : aucun métier ne défait le travail du "
             "précédent."),
            ("Nettoyage et clés", "Le logement est nettoyé en deux passages, "
             "puis nous le parcourons avec vous avant de rendre les clés."),
        ],
        "reperes": [
            ("Visite", "Sous une semaine"),
            ("Appartement 100 m²", "1 à 2 semaines de peinture"),
            ("Nettoyage final", "1 à 2 jours pour 100 m²"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "questions": [
            ("Combien de temps dure une remise en état entre deux locataires ?",
             "Tout dépend de ce que le logement demande. Pour un appartement "
             "de 100 m², comptez une à deux semaines de peinture, trois à "
             "cinq jours pour la "
             '<a href="{base}services/carrelage-sols.html">pose '
             "d'un sol neuf</a> et un à deux jours de nettoyage. La durée et "
             "la date de remise figurent sur le devis de chaque logement."),
            ("Quand faut-il vous appeler avant une relocation ?",
             "Dès que la fin du bail est connue : c'est l'entrée du locataire "
             "suivant qui fixe le calendrier. Nous passons sous une semaine, "
             "et le devis suit 72 heures après la visite. Comme elle est "
             "courte, une remise en état se cale plus vite que les quatre à "
             "huit semaines habituelles entre la signature et le démarrage."),
            ("Pouvez-vous reprendre plusieurs logements du même immeuble ?",
             "Oui. Nous avançons appartement par appartement, au rythme des "
             "départs, sans bloquer les logements encore loués. Chaque "
             "logement garde son devis et sa date. Certaines régies nous "
             "confient ainsi plusieurs appartements d'un même immeuble au "
             "cours d'une année."),
            ("Faut-il tout repeindre à chaque changement de locataire ?",
             "Pas forcément. Un rafraîchissement peut se limiter aux murs "
             "marqués : un blanc cassé ou une teinte claire se retouche "
             "localement, alors qu'une teinte soutenue oblige à reprendre "
             "tout le pan au premier choc. Nous vous disons à la visite ce "
             "qui se retouche et ce qui se repeint, et le devis le détaille "
             "poste par poste."),
            ("Le logement sera-t-il prêt pour l'état des lieux d'entrée ?",
             "Oui. Le nettoyage est compris et se fait en deux passages, "
             "jusque dans les rails de fenêtre, les placards et le haut des "
             "portes. Nous faisons ensuite le tour du logement avec vous : "
             "un défaut relevé à ce moment est corrigé sous dix jours."),
        ],
        "lies": ["peinture", "platrerie", "pose-de-sol", "nettoyage-fin-de-chantier"],
    },
    # Sources :
    #   contenu_divers.py:107-114 — devis par logement, date de remise ferme,
    #     appartement par appartement sans bloquer les logements encore loués,
    #     nettoyage compris, logement relouable le jour de la réception.
    #   contenu_divers.py:75-81 ; lausanne_finitions.py:125-128 — contrainte
    #     calendaire, date calée sur l'entrée du locataire suivant.
    #   contenu_questions.py:138-143 ; services_finitions.py:82-85 — part
    #     importante de l'activité pour les régies et les propriétaires
    #     bailleurs (« gérances » : synonyme romand de régie, ajouté pour la
    #     recherche, à valider).
    #   pages_site.py:131-137 — plusieurs logements d'un même immeuble sur une
    #     même année.
    #   services_finitions.py:31-35 — rafraîchissement de logements entre deux
    #     locations pour les régies.
    #   services_gros_oeuvre.py:107-110 ; services_gros_oeuvre.py:119 — trous
    #     de chevilles, fissures, angles abîmés, rebouchage.
    #   services_finitions.py:36 — préparation des fonds systématique avant
    #     peinture.
    #   services_finitions.py:45 ; services_finitions.py:48 ;
    #     services_finitions.py:49 ; services_finitions.py:51 — murs, plafonds
    #     et boiseries ; laquage des portes, cadres et plinthes ; peinture
    #     entre deux locations ; peinture anti-moisissure des pièces humides.
    #   lausanne_finitions.py:21-24 — blanc cassé ou teintes claires entre deux
    #     baux, retouches localisées ; une teinte soutenue impose de refaire le
    #     pan entier.
    #   services_finitions.py:196 — joints refaits, carreaux cassés remplacés.
    #   services_finitions.py:260-262 ; services_finitions.py:264 ;
    #     services_finitions.py:266 ; services_finitions.py:281 — parquet,
    #     vinyle grand passage, linoléum ; dépose et évacuation ; sous-couche
    #     acoustique systématique en immeuble.
    #   services_finitions.py:329-335 ; services_finitions.py:349 ;
    #     services_finitions.py:344-345 ; lausanne_finitions.py:129-142 —
    #     nettoyage : dessus des portes, vitres et rails, placards,
    #     robinetterie et parois de douche détartrées, sols, évacuation ; deux
    #     passages au minimum ; tour du logement avec vous avant la remise des
    #     clés ; points regardés à l'état des lieux.
    #   services_finitions.py:324-326 ; services_finitions.py:357-359 ;
    #     contenu_questions.py:144-147 — intervention avant un état des lieux
    #     de sortie, y compris sur un logement que l'entreprise n'a pas rénové.
    #   prestations.py:152 ; contenu_questions.py:126-129 — logement prêt pour
    #     l'état des lieux ; nettoyage compris.
    #   contenu_entreprise.py:41-45 ; confiance.py:17-20 ;
    #     contenu_questions.py:39-43 — visite sous une semaine, mesures et état
    #     des supports ; logement non vidé pour la visite.
    #   services_gros_oeuvre.py:58-59 ; contenu_questions.py:21-25 ;
    #     contenu_devis.py:9-13 — devis gratuit, poste par poste, 72 h après la
    #     visite.
    #   contenu_divers.py:21-35 ; page_prestations.py:43-44 — ordre plâtrerie,
    #     carrelage, sols, peinture, nettoyage ; inverser deux étapes oblige à
    #     refaire la première.
    #   services_finitions.py:66 ; services_finitions.py:279 ;
    #     services_finitions.py:348 — pour 100 m² : peinture 1 à 2 semaines,
    #     sol 3 à 5 jours, nettoyage 1 à 2 jours.
    #   contenu_questions.py:26-31 — quatre à huit semaines entre signature et
    #     démarrage ; les remises en état se calent plus vite.
    #   contenu_devis.py:26-28 ; contenu_devis.py:63-65 — durée et date écrites
    #     au devis ; fin de bail et entrée de locataire dictent le calendrier.
    #   contenu_questions.py:121-125 ; contenu_entreprise.py:60-63 — tour du
    #     logement avec vous, défauts corrigés sous dix jours.
    {
        "slug": "renovation-salle-de-bains",
        "resume": "Dépose, étanchéité, carrelage et faïence ; sanitaire et "
                  "électricité coordonnés.",
        "numero": "07",
        "nom": "Rénovation de salle de bains",
        "nom_menu": "Salle de bains",
        "titre": "Rénovation de salle de bains à Lausanne, étanchéité comprise",
        "description": (
            "Rénovation de salle de bains à Lausanne : dépose, étanchéité "
            "sous carrelage, faïence et sol, sanitaire et électricité "
            "coordonnés. Devis gratuit."
        ),
        "h1": ["Rénovation de salle de bains", "à Lausanne"],
        "chapo": (
            "Dépose, support et étanchéité d'abord, carrelage et faïence "
            "ensuite. Dans une salle de bains, ce qui compte le plus ne se "
            "voit plus une fois le chantier fini."
        ),
        "image": IMG + "2c1464_c44b6415607747ff9dccd68b224b3945~mv2.jpg",
        "alt": "Salle d'eau carrelée du sol au plafond dans un duplex rénové",
        "intro": [
            "La rénovation d'une salle de bains à Lausanne se fait le plus "
            "souvent au-dessus d'un logement habité. L'étanchéité, posée sous "
            "le carrelage et invisible une fois la faïence en place, protège "
            "le plafond du voisin : c'est le poste que nous ne réduisons "
            "jamais pour tenir un budget.",
            "Nous prenons en charge tout ce qui touche aux murs, au sol et au "
            "plafond de la pièce : dépose des anciens revêtements, reprise du "
            "support, étanchéité, "
            '<a href="{base}services/carrelage-sols.html">pose de la faïence '
            "et du carrelage de sol</a>, joints, puis plafond et peinture. Le "
            "sanitaire et l'électricité sont confiés à des partenaires que "
            "nous suivons depuis des années ; nous coordonnons leurs "
            "interventions, et vous gardez un seul interlocuteur.",
            "Tout se décide avant le premier jour : le choix des carreaux, "
            "l'emplacement des coupes et un planning daté. Comptez ensuite une à deux semaines de travaux. "
            "Si la salle de bains fait partie d'une "
            '<a href="{base}services/renovation-complete.html">rénovation '
            "complète</a>, elle passe avant les sols des autres pièces : elle "
            "demande du séchage et elle salit.",
        ],
        "prestations": [
            "Dépose de l'ancien carrelage et de la faïence, évacuation comprise",
            "Contrôle du support et mise à niveau du sol (ragréage)",
            "Étanchéité sous carrelage, en natte ou en résine, sous la douche, "
            "le bac et les zones de projection",
            "Faïence murale, jusqu'au plafond si vous le souhaitez",
            "Carrelage de sol en grès cérame, en pierre ou en grand format",
            "Pose droite, décalée, en chevron ou en diagonale",
            "Joints, profilés d'angle, seuils et finitions",
            "Plafond repris et peint en peinture anti-moisissure",
            "Coordination du sanitaire et de l'électricité avec nos partenaires",
            "Nettoyage final, robinetterie et parois de douche détartrées",
        ],
        "etapes": [
            ("Visite et mesures", "Nous mesurons la pièce, sondons les murs et "
             "le sol, et notons l'accès avant d'établir le devis."),
            ("Choix et tracé", "Carreaux choisis sur échantillons, axes et "
             "coupes arrêtés avec vous avant le démarrage."),
            ("Dépose et support", "Un à deux jours de dépose et d'évacuation, "
             "puis contrôle et mise à niveau du support."),
            ("Étanchéité", "Natte ou résine sous la douche et les zones de "
             "projection, séchage compris, avant le premier carreau."),
            ("Pose et finitions", "Carrelage et joints, raccordement des "
             "sanitaires par notre partenaire, nettoyage, puis tour de la "
             "pièce avec vous."),
        ],
        "reperes": [
            ("Salle de bains", "1 à 2 semaines, étanchéité comprise"),
            ("Dépose et évacuation", "1 à 2 jours selon l'étage"),
            ("Support et étanchéité", "2 jours, séchage compris"),
            ("Devis", "Gratuit, 72 h après visite"),
        ],
        "questions": [
            ("Combien de temps faut-il pour refaire une salle de bains ?",
             "Une à deux semaines, étanchéité comprise. La dépose et "
             "l'évacuation comptent un à deux jours, suivant l'étage et la "
             "présence d'un ascenseur ; la reprise du support et l'étanchéité, "
             "deux jours avec le séchage. La pose, les joints et les "
             "sanitaires occupent la fin de la semaine."),
            ("Qui s'occupe de la plomberie et de l'électricité ?",
             "Des partenaires que nous suivons depuis des années, dont nous "
             "coordonnons les interventions. Les conduites et les câbles passent tant "
             "que les murs sont ouverts, avant l'étanchéité et le carrelage. "
             "Vous n'avez qu'un interlocuteur, notre responsable de chantier."),
            ("Puis-je acheter moi-même mon carrelage ?",
             "Oui. Nous fournissons normalement les matériaux, compris dans "
             "le devis, mais nous posons aussi un carrelage choisi ailleurs ; "
             "nous vous indiquons avant l'achat les quantités et les "
             "contraintes de pose. Le choix doit simplement être arrêté avant "
             "le démarrage : un carreau commandé trop tard bloque la pose "
             "jusqu'à sa livraison."),
            ("Combien coûte la rénovation d'une salle de bains ?",
             "Nous ne publions pas de prix : il dépend de l'état existant et "
             "de ce que révèle la dépose bien plus que de la surface. Vous "
             "pouvez "
             '<a href="{base}devis.html">demander un devis gratuit</a> : '
             "la visite ne vous engage à rien, et le devis détaillé poste par "
             "poste vous parvient 72 heures après."),
            ("Pouvez-vous refaire seulement les joints ou quelques carreaux ?",
             "Oui, la réfection des joints et le remplacement de carreaux "
             "cassés font partie de nos travaux de carrelage. Si "
             "l'intervention est trop petite pour qu'un déplacement ait du "
             "sens, nous vous le disons franchement dès le premier appel."),
        ],
        "lies": ["carrelage", "platrerie", "peinture", "renovation-complete"],
    },
    # Sources :
    #   lausanne_finitions.py:69-73 — salle de bains refaite au-dessus d'un
    #     logement occupé ; l'étanchéité protège le plafond du voisin, poste
    #     sur lequel l'entreprise ne transige jamais.
    #   services_finitions.py:185-187 — étanchéité sous le carrelage, avant la
    #     pose, invisible.
    #   services_finitions.py:190-196 — grès cérame, pierre, grand format ;
    #     faïence murale ; étanchéité des zones humides ; mise à niveau
    #     (ragréage) ; poses droite, décalée, chevron, diagonale ; profilés,
    #     seuils, joints ; réfection de joints et carreaux cassés.
    #   services_finitions.py:199-204 — contrôle du support ; axes et coupes
    #     arrêtés avec vous ; natte ou résine sous les douches, les bacs et les
    #     zones de projection.
    #   services_finitions.py:177 ; contenu_divers.py:47 — salles de bains
    #     recarrelées du sol au plafond.
    #   services_finitions.py:209 ; prestations.py:133 — salle de bains : 1 à 2
    #     semaines, étanchéité comprise.
    #   lausanne_finitions.py:74-77 ; lausanne_finitions.py:84-90 — chapes sur
    #     sable, canalisations en plomb, planchers bois sous la faïence,
    #     relevés à la visite ; dépose et évacuation 1 à 2 jours selon l'étage
    #     et l'ascenseur ; support et étanchéité 2 jours séchage compris ;
    #     « pose, jointoiement et sanitaires : le reste de la semaine » (une
    #     durée : ce texte ne dit pas qui pose les sanitaires).
    #   services_gros_oeuvre.py:52 ; contenu_divers.py:18-20 ;
    #     contenu_divers.py:95-98 ; construire.py:102 ;
    #     contenu_entreprise.py:14-15 — coordination de l'électricité et du
    #     sanitaire avec les partenaires ; réseaux posés tant que les cloisons
    #     sont ouvertes ; « nous ne sommes pas électriciens, mais nous le
    #     signalons et nous coordonnons » ; partenaires suivis depuis des
    #     années ; « coordination de l'électricité et du sanitaire avec nos
    #     partenaires » (services_gros_oeuvre.py). CONTENU À VALIDER : que le
    #     partenaire raccorde les sanitaires (étape « Pose et finitions »).
    #   contenu_questions.py:58-61 — un responsable de chantier unique, seul
    #     interlocuteur.
    #   services_gros_oeuvre.py:124 ; services_finitions.py:51 — plafond repris
    #     avant peinture ; peinture anti-moisissure des pièces humides.
    #   services_finitions.py:264 ; services_finitions.py:332 — dépose et
    #     évacuation ; robinetterie et parois de douche détartrées.
    #   contenu_divers.py:24-26 — les pièces d'eau passent avant les sols
    #     secs : séchage et salissures.
    #   contenu_divers.py:122-126 ; contenu_divers.py:133-134 — échantillons
    #     montrés sur place ; finitions décidées avant le démarrage, un
    #     carrelage choisi en cours de chantier arrête la pose.
    #   services_gros_oeuvre.py:60-61 — planning daté avant le démarrage.
    #   contenu_questions.py:103-107 — matériaux fournis et au devis ;
    #     carrelage acheté par le client possible, quantités et contraintes de
    #     pose indiquées avant.
    #   contenu_questions.py:86-92 ; contenu_questions.py:21-25 — prix selon
    #     l'état existant plus que la surface, aucun prix publié ; visite et
    #     devis gratuits, sans engagement, 72 h.
    #   contenu_questions.py:32-38 ; contenu_entreprise.py:36-39 — salle de
    #     bains à refaire, demande courante ; chantier trop petit dit
    #     franchement, dès le premier appel.
    #   contenu_entreprise.py:41-44 — visite : mesures, sondage des supports,
    #     accès.
]

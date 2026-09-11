# DSG Rénovation — site vitrine

Site de **DSG Rénovation Sàrl**, entreprise de rénovation clé en main à
Lausanne (arc lémanique). Dix-huit pages, dont une par prestation.

HTML, CSS et JavaScript natifs — aucun framework, aucune étape de build.
Ouvrir `index.html` suffit.

## Structure

```
index.html            accueil : la preuve, les chiffres, les renvois
entreprise.html       histoire, engagements, savoir-faire
services.html         page pilier des neuf lots
services/*.html       une page par prestation — neuf fichiers
realisations.html     registre des chantiers, filtres et visionneuse
references.html       partenaires, témoignages, travail avec les régies
questions.html        questions fréquentes
devis.html            bordereau de demande et coordonnées
mentions-legales.html pièce annexe A — éditeur, droits, responsabilité
confidentialite.html  pièce annexe B — traitement des données
sitemap.xml           plan du site, régénéré avec les pages
robots.txt            exploration ouverte, sauf outils/
assets/css/           feuilles numérotées, chargées dans l'ordre
assets/js/            un module par comportement
assets/images/        tirages du comparateur avant / après
outils/               générateur de pages — voir plus bas
```

Toutes les pages partagent le même en-tête, le même menu et le même
pied. `14-document.css` porte la mise en page des annexes légales,
`15-pages.css` celle des pages intérieures et des pages de prestation,
`16-composants.css` la frise d'étapes, les cartes, le tableau des
besoins et les autres blocs de contenu.

## Le générateur

Les dix-huit pages sont assemblées par un script, puis livrées en HTML
statique. **Ce n'est pas une étape de build** : le site fonctionne sans
lui, et ouvrir `index.html` suffit toujours. C'est une commodité de
maintenance, qui évite de corriger un numéro de téléphone dans dix-huit
fichiers.

Après une modification du contenu ou du chrome :

```
python3 outils/construire.py
```

| Fichier | Contenu |
|---|---|
| `donnees_site.py` | coordonnées, navigation, communes, relevé chiffré |
| `services_gros_oeuvre.py` | rénovation totale, plâtrerie, cloisons, faux plafonds |
| `services_finitions.py` | peinture, revêtements, carrelage, sols, nettoyage |
| `lausanne_gros_oeuvre.py` | ce que le bâti lausannois impose à ces quatre lots |
| `lausanne_finitions.py` | idem pour les cinq lots de finition |
| `contenu_entreprise.py` | histoire, déroulé d'un chantier, limites, engagements |
| `contenu_devis.py` | ce que contient un devis, comment le comparer |
| `contenu_questions.py` | vingt questions, groupées par moment du projet |
| `contenu_divers.py` | enchaînement des lots, besoins, familles de biens |
| `gabarit.py` | tête du document, en-tête, menu, pied, scripts |
| `briques.py` | couverture, intercalaire, relevé, appel à l'action |
| `briques_bis.py` | frise, cartes, besoins, limites, conseils |
| `page_service.py` | corps d'une page de prestation |
| `page_accueil.py` | corps de l'accueil |
| `pages_site.py` | entreprise, savoir-faire |
| `pages_contenu.py` | réalisations, références, questions, devis |
| `catalogue.py` | fiche signalétique des pages de la racine |
| `seo.py` | balisage structuré, `sitemap.xml`, `robots.txt` |
| `fragments/` | blocs repris du dossier d'origine, tels quels |

Pour modifier un texte de prestation, éditer le fichier de service
correspondant puis relancer le script. Pour modifier une adresse ou un
numéro, éditer `donnees_site.py` : la correction se propage partout.

Les feuilles de style se lisent dans l'ordre de leur numéro :
`00-jetons.css` porte **toutes** les valeurs du site (couleurs,
typographie, espacements, durées). Les autres n'y puisent que des
jetons — aucune valeur n'est écrite en dur ailleurs, hors cas commenté.

## Référencement local

Chaque page porte un titre et une description qui lui sont propres, un
lien canonique et un balisage `schema.org` : fiche d'établissement sur
toutes les pages, `Service` et `FAQPage` sur les pages de prestation,
fil d'Ariane partout.

Les pages de prestation visent les recherches de la région lausannoise
(« peintre à Lausanne », « carreleur à Lausanne »…). Elles ne se
répètent pas : deux pages qui disent la même chose se concurrencent au
lieu de s'additionner. L'accueil donne l'accroche de chaque sujet et
renvoie vers la page qui le traite.

Chaque page de prestation porte une section **« sur le terrain »** qui
décrit ce que le bâti lausannois impose à ce lot : plâtre sur lattis
des immeubles d'avant-guerre, hauteurs sous plafond du centre, accès
des rues de Sous-Gare, contraintes des immeubles de rendement. C'est
le contenu qu'aucun concurrent ne peut copier, et celui qui distingue
une page « plâtrier à Lausanne » d'une page « plâtrier ».

Les quartiers et communes cités sont ceux où l'entreprise travaille
réellement : Sous-Gare, Chauderon, le Vallon, la Cité, Bellevaux,
Montoie, Vennes, Sévelin, Chailly, puis Pully, Prilly, Renens,
Ecublens, Épalinges, Lutry, Morges, Nyon, Vevey, Montreux et Genève.

La page questions porte vingt questions groupées par moment du projet,
toutes reprises dans le balisage `FAQPage`.

Les deux annexes légales portent `noindex, follow` : utiles au visiteur,
sans valeur pour la recherche.

## Direction artistique

Papier blanc, encre noire, rouge de marque, répartis 60 / 30 / 10.
Le rouge n'est pas une matière : il ne sert qu'à l'action — boutons
d'appel, repère de la section lue, surlignage du titre.

Les blocs sombres redéfinissent la gamme d'encres localement
(`.sur-sombre`) : aucun composant n'a à connaître la couleur de son
fond, il demande `--c-encre` et obtient la bonne.

Chaque couleur de texte porte son rapport de contraste en commentaire.
Le plancher du site est de 4,5:1 — seuil AA.

## Comportements

| Fichier | Rôle |
|---|---|
| `nav.js` | navigation, section courante, menu plein écran |
| `motion.js` | révélations au défilement, compteurs du relevé |
| `effets.js` | jauge de lecture, accord des éléments fixes au fond, parallaxe |
| `vignette.js` | tirage qui suit le pointeur dans la liste des savoir-faire |
| `comparateur.js` | glissière avant / après (souris, tactile, clavier) |
| `lumineuse.js` | visionneuse plein écran des réalisations |
| `formulaire.js` | validation de la demande de devis |
| `dossier.js` | filtres des réalisations |

Chaque page ne charge que les modules dont elle a besoin. Les quatre
modules communs sont `nav.js`, `motion.js`, `effets.js` et `curseur.js` ;
`comparateur.js` ne sert qu'à l'accueil, `dossier.js` et `lumineuse.js`
qu'aux réalisations, `formulaire.js` qu'à la page de devis.

Tout est neutralisé si le visiteur demande moins de mouvement
(`prefers-reduced-motion`), et le contenu reste lisible sans
JavaScript.

## À compléter avant mise en ligne

Les annexes signalent visiblement les informations qui n'appartiennent
qu'au client, au moyen de la classe `.a-valider` — un fond gris et un
soulignement tireté, jamais de rouge. À obtenir puis à remplacer :

- le numéro IDE de la société et l'identité du gérant responsable ;
- le nom et l'adresse de l'hébergeur, une fois celui-ci choisi ;
- l'auteur des prises de vue des chantiers.

Chaque emplacement porte un commentaire `CONTENU À VALIDER` dans le
HTML. Une recherche sur ce mot suffit à les retrouver tous.

## Documents de travail

`DA-MOMDESIGN.md` — analyse de référence et direction corrective.
`DIRECTION-ARTISTIQUE.md` et `dsg-renov-claude.md` décrivent des états
antérieurs du projet : ils sont conservés pour mémoire mais **ne
correspondent plus au site actuel**.

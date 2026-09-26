# DSG Rénovation — site vitrine

Site de **DSG Rénovation Sàrl**, entreprise de rénovation clé en main à
Lausanne (arc lémanique). Douze pages, dont cinq de prestation.

HTML, CSS et JavaScript natifs — aucun framework, aucune étape de build.
Ouvrir `index.html` suffit.

## Structure

```
index.html            accueil : la preuve, les chiffres, les renvois
services.html         page pilier des cinq prestations
services/*.html       une page par prestation — cinq fichiers
realisations.html     registre des chantiers, familles de biens, imprévus
entreprise.html       histoire, déroulé, limites, références, témoignages
devis.html            bordereau, lecture d'un devis, vingt questions
mentions-legales.html pièce annexe A — éditeur, droits, responsabilité
confidentialite.html  pièce annexe B — traitement des données
sitemap.xml           plan du site, régénéré avec les pages
robots.txt            exploration ouverte, sauf outils/
assets/css/           feuilles numérotées, chargées dans l'ordre
assets/js/            un module par comportement
assets/images/        tirages du comparateur avant / après
outils/               générateur de pages — voir plus bas
```

**Douze pages, quatre entrées de menu.** Les références vivent dans la
page entreprise, dont elles sont la preuve ; les questions dans la page
de devis, où elles se posent réellement. Les neuf métiers se répartissent
sur cinq pages : ceux qui se posent ensemble sur un chantier partagent
la leur, ce qui donne des pages denses plutôt que nombreuses.

Toutes les pages partagent le même en-tête, le même menu et le même
pied. `14-document.css` porte la mise en page des annexes légales,
`15-pages.css` celle des pages intérieures et des pages de prestation,
`16-composants.css` les cartes et le tableau des besoins,
`17-repli.css` les onglets et les dépliants, `18-confiance.css` les
blocs de réassurance : logos sous la couverture, déroulé en quatre
temps, « après l'envoi ». `10-comparateur.css` porte l'image
d'ouverture et le comparateur avant / après, `19-impression.css` la
version papier.

## Le générateur

Les douze pages sont assemblées par un script, puis livrées en HTML
statique. **Ce n'est pas une étape de build** : le site fonctionne sans
lui, et ouvrir `index.html` suffit toujours. C'est une commodité de
maintenance, qui évite de corriger un numéro de téléphone dans douze
fichiers.

Après une modification du contenu ou du chrome :

```
python3 outils/construire.py
```

| Fichier | Contenu |
|---|---|
| `donnees_site.py` | coordonnées, navigation, communes, relevé chiffré |
| `services_gros_oeuvre.py` | fiches de lot : rénovation, plâtrerie, cloisons, faux plafonds |
| `services_finitions.py` | fiches de lot : peinture, revêtements, carrelage, sols, nettoyage |
| `prestations.py` | quelles fiches de lot partagent une page, et ce qui leur est commun |
| `lausanne_gros_oeuvre.py` | ce que le bâti lausannois impose à ces quatre lots |
| `lausanne_finitions.py` | idem pour les cinq lots de finition |
| `contenu_entreprise.py` | histoire, déroulé d'un chantier, limites, engagements |
| `contenu_devis.py` | ce que contient un devis, comment le comparer |
| `contenu_questions.py` | vingt questions, groupées par moment du projet |
| `contenu_divers.py` | enchaînement des lots, besoins, familles de biens |
| `assemblage.py` | liste des feuilles et scripts, assemblage et écriture d'une page |
| `gabarit.py` | tête du document, en-tête, menu, scripts |
| `gabarit_pied.py` | pied de page : coordonnées, horaires, itinéraire |
| `gabarit_liens.py` | liens du chrome qui dépendent de la page consultée |
| `confiance.py` | déroulé en quatre temps, logos sous la couverture, témoignages |
| `accessibilite.py` | relie chaque section à son titre (lecteurs d'écran) |
| `briques.py` | couverture, intercalaire, relevé, appel à l'action |
| `briques_bis.py` | cartes à filet, tableau des besoins |
| `repli.py` | onglets et dépliants — voir « Ce qui se replie » |
| `page_service.py` | corps d'une page de prestation |
| `service_liens.py` | zone d'intervention et lots voisins d'une page de prestation |
| `ouverture.py` | l'image d'ouverture cadrée qui s'élargit au défilement |
| `page_accueil.py` | corps de l'accueil |
| `pages_site.py` | entreprise |
| `page_prestations.py` | page pilier des prestations |
| `pages_contenu.py` | réalisations, devis |
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

## Ce qui se replie

Une page de chantier se feuillette, elle ne se déroule pas. Les listes
longues, les méthodes en cinq étapes et les questions ne s'affichent
donc pas d'un bloc : **on voit les intitulés, on ouvre ce qu'on veut
lire.**

Deux composants portent cela, tous deux dans `repli.py` :

- **les onglets** — une languette par lot sur les pages qui en réunissent
  plusieurs, et sur la section « sur le terrain » ;
- **les dépliants** — une ligne de bordereau qui porte son numéro, son
  intitulé et sa cote, et qui s'ouvre sur un paragraphe.

Cela ne coûte rien au référencement : le contenu replié est dans le
document, Google le lit. Sans JavaScript, les onglets affichent tous
leurs panneaux et les dépliants restent ouvrables — rien n'est jamais
inaccessible. Le module `onglets.js` ne fait qu'en masquer une partie
quand il s'exécute.

## Référencement local

Chaque page porte un titre et une description qui lui sont propres, un
lien canonique et un balisage `schema.org` : fiche d'établissement sur
toutes les pages, `Service` et `FAQPage` sur les pages de prestation,
fil d'Ariane partout.

Les pages de prestation visent les recherches de la région lausannoise
(« peintre à Lausanne », « carreleur à Lausanne »…). Cinq pages denses
plutôt que neuf moyennes : la profondeur d'une page pèse davantage que
leur nombre, et un visiteur qui cherche des cloisons cherche souvent
aussi la plâtrerie qui va avec. Elles ne se
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

Version du 25/09/2026, « Le plan d'implantation », inspirée de
tekt.com.au ; palette révisée le 26/09/2026, « bleu de travail, jaune
de chantier » — tout est décrit dans `DIRECTION-ARTISTIQUE.md`.

Blanc de chantier, encre bleu nuit, jaune de chantier réservé à
l'action. Une bande de nuit par page, où les repères d'angle passent au
jaune, et le renvoi final sur une bande de bleu de travail. Des
cadres d'un pixel marqués d'un repère carré à chaque angle, une
grotesque (Archivo) pour les titres et une sérif de lecture
(Newsreader) pour les phrases. Chaque section range son intitulé dans
la marge gauche, qui reste accroché pendant la lecture.

L'image d'ouverture n'arrive pas en plein écran : elle est cadrée dans
la colonne de la page, puis s'élargit jusqu'aux bords à mesure qu'on
descend. Sur l'accueil, c'est le comparateur avant / après.

Les blocs sombres redéfinissent la gamme d'encres localement
(`.sur-sombre`) : aucun composant n'a à connaître la couleur de son
fond, il demande `--c-encre` et obtient la bonne. La classe pose aussi
le fond : pour passer une section en bande de nuit, il suffit de
l'ajouter à la `<section>` dans le générateur. `.sur-bleu`, ajoutée à
`.sur-sombre`, en fait la bande bleue du renvoi final.

Chaque couleur de texte porte son rapport de contraste en commentaire.
Le plancher du site est de 4,5:1 — seuil AA.

## Comportements

| Fichier | Rôle |
|---|---|
| `nav.js` | menu plein écran, barre d'action mobile |
| `motion.js` | révélations au défilement, vignettes des métiers sur téléphone |
| `effets.js` | boutons d'appel légèrement magnétiques |
| `ouverture.js` | l'image d'ouverture s'élargit au défilement |
| `curseur.js` | pastille « Glisser » / « Agrandir » qui remplace le pointeur |
| `vignette.js` | tirage qui suit le pointeur dans la liste des savoir-faire |
| `comparateur.js` | glissière avant / après (souris, tactile, clavier), démonstration à la première vue |
| `lumineuse.js` | visionneuse plein écran des réalisations |
| `formulaire.js` | validation et envoi de la demande de devis |
| `dossier.js` | filtres des réalisations |
| `onglets.js` | jeux d'onglets des pages de prestation |

Chaque page ne charge que les modules dont elle a besoin. Les cinq
modules communs sont `nav.js`, `motion.js`, `effets.js`, `curseur.js`
et `onglets.js` ;
`comparateur.js` ne sert qu'à l'accueil, `ouverture.js` à l'accueil et
aux pages de prestation, `dossier.js` et `lumineuse.js`
qu'aux réalisations, `formulaire.js` qu'à la page de devis.

Tout est neutralisé si le visiteur demande moins de mouvement
(`prefers-reduced-motion`), et le contenu reste lisible sans
JavaScript.

## À compléter avant mise en ligne

Les annexes signalent visiblement les informations qui n'appartiennent
qu'au client, au moyen de la classe `.a-valider` — un fond bleuté et un
soulignement tireté, jamais de rouge. À obtenir puis à remplacer :

- le numéro IDE de la société et l'identité du gérant responsable ;
- le nom et l'adresse de l'hébergeur, une fois celui-ci choisi ;
- l'auteur des prises de vue des chantiers ;
- **les témoignages** : les trois textes actuels sont provisoires et
  s'affichent comme tels. Les remplacer par de vrais avis (accord écrit
  de chaque client) dans `outils/confiance.py`, puis passer
  `PROVISOIRES` à `False` ;
- **l'adresse du service d'envoi du formulaire** (Formspree, Web3Forms,
  formulaire Infomaniak…) dans l'attribut `data-envoi` de
  `outils/fragments/formulaire.html`. Sans elle, la demande part par le
  logiciel de messagerie du visiteur, ce qui échoue chez ceux qui n'en
  ont pas configuré ;
- les horaires du bureau (`HORAIRES` dans `donnees_site.py`) ;
- le détail des six fiches de chantier et du chantier signature
  (noms, surfaces, durées, années) ;
- le lien de la fiche Google Business Profile, une fois créée
  (`ITINERAIRE` dans `donnees_site.py`, et l'emplacement réservé sous
  les témoignages).

Chaque emplacement porte un commentaire `CONTENU À VALIDER` ou
`À FOURNIR` dans le HTML ou le script. Une recherche sur ces mots
suffit à les retrouver tous.

## Documents de travail

`DIRECTION-ARTISTIQUE.md` — direction actuelle (v2, 25/09/2026).
`DA-MOMDESIGN.md` et `dsg-renov-claude.md` décrivent des états
antérieurs du projet : ils sont conservés pour mémoire mais **ne
correspondent plus au site actuel**.

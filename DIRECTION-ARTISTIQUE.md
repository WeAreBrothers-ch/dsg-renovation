# DIRECTION ARTISTIQUE — DSG Rénovation Sàrl

Document de référence unique. Il doit permettre de coder le site **sans avoir vu les images d'inspiration**.
Toutes les valeurs sont normatives : si une valeur n'est pas listée ici, elle ne doit pas apparaître dans le code.
Les valeurs vivent dans `assets/css/00-jetons.css` ; ce document en donne la raison.

Date : 05/10/2026 — Statut : **v4**, en production.
La v1 du 29/07/2026 (« La preuve par la matière », six références hors BTP) reste lisible dans l'historique git
(commit `1fd70a6`). Elle est remplacée intégralement.

**Noir nacré & rouge DSG, 05/10/2026 (v4).** À la demande du client, le site prend les couleurs du logo, et
elles seules : son noir (`#1B1B1B`, ramené au noir nacré `#121214`), le rouge du toit (`#DD0022`), le gris
d'ombre des lettres (`#A6A4A5`), le blanc. Pour que le noir ne fasse pas « basique », il est **nacré** sur les
bandes sombres, le pied et la barre mobile : trois reflets à peine teintés (bleu froid, rose, vert d'eau) sur
un noir qui tourne d'un rien, comme l'intérieur d'une coquille. Le survol des boutons rouges passe au noir
nacré ; l'enseigne du pied s'écrit en lettres nacrées. La chaux chaude devient un blanc perle neutre
(`#F3F3F4`). Le même jour, le sommaire collant du téléphone est retiré : le client le trouvait lourd (§ 4).
La palette « Chaux & brique » reste lisible dans l'historique git (`d148c82`).

**Retour aux couleurs d'origine, 27/09/2026 (v2.5) — « Plâtre & brique ».** Après quatre autres palettes
(bleu de travail et jaune de chantier, couleurs du logo, bleu de plan et safran, chocolat et ciel), le client a
demandé les couleurs de départ du site : le plâtre, la terre d'ombre et la brique de la v2 (`0a45b44`). Elles
reviennent à l'identique. Ce qui a été gagné depuis reste : quatre fonds rythment la page (§ 2 bis), l'action et
l'accent écrit ont chacun leur jeton, les ouvriers du site prennent la brique (§ 8). Les palettes essayées restent
lisibles dans l'historique git (« bleu de travail, jaune de chantier » : `9fbd8d8` ; « le toit rouge », tirée du
logo : `d604530` ; « bleu de plan & safran » : `c322a78` ; « chocolat & ciel » : `0d52c52`).

**Architecture du téléphone repensée, 27/09/2026 (v2.7).** Au téléphone, le site se lisait comme un long
document : tout déplié, du texte d'un bout à l'autre, rien pour aller droit à une information. Une page s'y
parcourt désormais par ses intitulés (§ 4, « Au téléphone ») : sommaire collant, premier paragraphe seul,
suites à faire glisser, pied de page court, titres plus marqués. Le bureau n'a pas changé.

**Un site qui vit, 30/09/2026 (v3) — « Chaux & brique ».** Retour du client : le site « fait mort ». La
couverture n'était que du texte sur un fond gris-beige, l'image n'arrivait qu'au défilement ; les légendes
reprenaient le texte alternatif, en petit gris, sur une bande étroite ; les numéros « N° 005 » posés sur les
photos faisaient registre administratif. La v3 garde l'encre et la brique (les couleurs du logo), la
typographie, les cadres et leurs repères ; elle change le reste :
- **le fond s'éclaircit** : la chaux (`#F5F2EC`) remplace le plâtre, une section sur deux passe au blanc franc,
  et le renvoi final prend la brique (§ 2, § 2 bis) ;
- **la couverture montre le chantier** : le titre à gauche, le comparateur avant / après à droite, à la hauteur
  de l'écran, avec deux boutons « Avant » / « Après » (§ 7) ;
- **les légendes parlent en deux voix** : le lieu, puis ce qu'on voit, et le lien vers la fiche du chantier
  (§ 6) ;
- **plus de numéros qui ne comptent rien** : ni « N° 005 » sur les réalisations, ni « 01 … 07 » devant les
  prestations — une photo les remplace (§ 9). Les numéros restent aux vraies suites (étapes, méthode,
  articles).
Les inspirations de cette version sont au § 0 bis.

**Signature et mouvement, 30/09/2026 (v3.3).** Les ouvriers animés disparaissent ; les photos et les
chiffres prennent le relais (§ 8). Le toit du logo tracé en grand a été essayé puis retiré à la demande du
client : il reste le petit chevron devant les intitulés. Une photo par prestation, aucune grande photo
répétée sur une page ; `BRIEF-PHOTOS.md` pour la suite.

**Brique plus vive, 30/09/2026 (v3.4).** À la demande du client, la brique passe de `#9A3324` à `#B2341F`
(texte blanc dessus : 6.2), la brique écrite à `#962C1C` (7.0 sur la chaux), la brique claire à `#EF8F74`.

**Finition, 30/09/2026 (v3.1).** Deuxième retour du client : le bandeau brique avant le pied « n'est pas joli »,
et les pages de prestation gardaient une photo pleine largeur avec une bande de légende dessous. Revue page par
page, au bureau et au téléphone :
- **plus aucun fond brique** : le renvoi final devient un cadre à repères sur le fond de la section — la question
  et les deux boutons à gauche, comment nous joindre (téléphone, courriel, horaires, atelier) à droite (§ 7) ;
- **toutes les pages principales s'ouvrent comme l'accueil** : le texte à gauche, un chantier réel à droite, à la
  hauteur de l'écran ; sous le chapô, quatre repères de la page (durées, conditions, horaires) (§ 7) ;
- **la légende vit dans la photo**, en bas, sur un voile d'encre (`briques.vue`) : plus de bande de texte entre
  l'image et la section suivante (§ 6) ;
- l'image d'ouverture à rideaux, le cartouche d'identité de l'accueil (redit plus bas) et la bande de repères des
  prestations (montés dans l'en-tête) disparaissent ; les communes deviennent une liste à deux colonnes, les
  étiquettes de travaux des pastilles pleines sans trait, les prestations voisines deux par ligne.

---

## 0. Référence : Tekt (tekt.com.au)

Constructeur australien de maisons modulaires. Onze captures fournies par le client
(`inspirations/tekt/`), complétées par une lecture du site en ligne (accueil, `/process/`).

- **Ambiance** : architecturale, calme, sûre d'elle. Un bureau d'études plus qu'une agence de pub.
  Rien ne crie ; tout est aligné.
- **Couleurs** : fond gris-bleu très pâle (`#ECF1F4`), encre brun très sombre (`#2D2012`, lu dans l'inspecteur),
  un bleu-gris pâle pour le bouton flottant « Get in touch → ». Aucun accent saturé : la couleur vient des photos.
- **Typographie** : une grotesque néo-suisse (type Neue Haas) en graisse moyenne pour titres, intitulés et
  commandes ; une **sérif de lecture** (type Tiempos) pour tous les paragraphes. Casse normale partout, aucune
  capitale décorative. Les grands paragraphes d'intention sont composés dans la grotesque, en gros.
- **Grille** : deux colonnes asymétriques — un intitulé court dans le tiers gauche (« Our Process: A Narrative
  of Assembly »), le contenu dans les deux tiers droits. Beaucoup d'air vertical entre les sections.
- **Signature graphique** : des **cadres d'un pixel** autour de chaque bloc (navigation, listes, formulaire),
  avec un **petit carré plein à chaque angle** — comme les poignées d'un objet sélectionné dans un logiciel de
  plan. C'est l'élément le plus reconnaissable du site.
- **Composants** : liste en accordéon « 01 Groundwork / 02 Concept Design… » où la ligne ouverte grandit et
  montre texte + photo ; formulaire en **cases jointives** (petit intitulé, grande réponse) ; panneau dépoli posé
  sur une grande photo (« Urban Series ») ; frise horizontale d'étapes ; bouton « Get in touch → » collé en bas
  à gauche de l'écran.
- **Images** : photos chaudes, désaturées, lumière naturelle, angles vifs, jamais arrondies.
- **Animations** : défilement lissé (Lenis), apparitions discrètes. Rien de spectaculaire.
- **Ouverture** : une photo plein écran avec le titre posé dessus.

### Ce qu'on garde
La grille « intitulé à gauche / contenu à droite », les cadres d'un pixel et leurs repères d'angle, le duo
grotesque + sérif de lecture, la casse normale, l'accordéon numéroté, le formulaire en cases, le panneau posé
sur la photo, la retenue générale.

### Ce qu'on écarte
- **La photo plein écran d'emblée** (demande explicite du client). Remplacée à l'accueil par la couverture
  côte à côte — le titre, l'image cadrée dans la grille (§ 7) —, reprise par toutes les pages principales.
- Le gris-bleu froid : DSG rénove des intérieurs, sa matière est le plâtre et le bois, pas l'acier.
- Le bouton flottant sur grand écran : l'en-tête porte déjà « Devis gratuit ».
- Le défilement lissé par librairie : poids de script et sensation de latence, sans bénéfice pour le visiteur.

## 0 bis. Références Awwwards (v3, 30/09/2026)

Recherche menée sur awwwards.com : sites de rénovation, de construction, d'artisans et d'architectes primés
(mention d'honneur ou site du jour). Le navigateur de l'environnement de travail n'avait pas accès au domaine :
les fiches ont été repérées par la recherche web, **sans être feuilletées écran par écran**. Le tableau ne dit
donc que ce qu'en disent leur fiche et, pour RS.D, l'agence qui l'a conçu ; à regarder de près avant
d'en tirer davantage.

| Référence | Distinction | Ce qu'on en sait (fiche Awwwards, agence) |
|---|---|---|
| RS.D Agencements & Rénovation (Lyon) | mention d'honneur | rénovation d'appartements, cuisines, salles de bains ; chantiers racontés jusqu'au résultat, mise en page aérée, animations discrètes — le métier le plus proche de DSG |
| Apex Transformations | mention d'honneur | entreprise de rénovation et de construction |
| GM Construction (Écosse, Studio Form) | mention d'honneur | entreprise générale et spécialiste du bois, fondée en 1989 |
| Siegesmund | mention d'honneur | menuiserie, mobilier fait main |
| a-rr architecture (Lausanne) | mention d'honneur | bureau d'architecture lausannois |
| Kononenko Architectural Bureau | site du jour | minimalisme, typographie franche, structure réfléchie |

Ce qu'on en tire, et que la v3 applique — une lecture de ce qui revient chez les meilleurs sites du métier,
pas la copie de l'un d'eux : **la preuve dans le premier écran** (le comparateur à côté du titre), **des
légendes courtes qui nomment un lieu** plutôt qu'un numéro, **un fond clair qui laisse la couleur aux
photos**, **une seule couleur forte**, gardée pour l'action. Ce qu'on écarte : le plein écran vidéo, les
défilements scénarisés, les curseurs personnalisés — beaux sur Awwwards, lents et déroutants pour quelqu'un
qui cherche un artisan.

---

## 1. Concept

# « LE PLAN D'IMPLANTATION »

Un chantier de rénovation commence par un relevé : on reporte la pièce sur le plan, on plante des repères aux
angles, puis on ouvre. Le site en reprend la matière et le geste :

- un **fond perle**, clair et neutre — le blanc du logo à peine voilé de gris —, relayé une section sur
  deux par le **blanc franc** ;
- une **encre noire**, celle des lettres du logo ;
- des **cadres d'un pixel marqués aux angles** — les piquets du géomètre ;
- des **bandes de noir nacré** qui rythment la page : un noir à reflets, jamais un aplat mort ;
- **la preuve dès le premier écran** : à l'accueil, le chantier avant / après à côté du titre ; sur les autres
  pages principales, un chantier réel à côté du titre, sa légende posée dans l'image ;
- **un seul accent, le rouge du toit** : réservé à l'action — les boutons d'appel — et à ce qui s'écrit en couleur : liens, numéros d'étape, et devant chaque intitulé de section un
  chevron dessiné comme le toit du logo.

Ce qui reste propre à DSG et n'existe pas chez Tekt : l'Archivo (police historique de la marque), le rouge
DSG, le noir nacré, le logo et son toit rouge, le comparateur avant / après mis au centre de l'accueil, les
repères d'angle qui voyagent avec l'image d'ouverture.

---

## 2. Palette — « Noir nacré & rouge DSG » (v4)

Les couleurs du logo, et elles seules : son noir, son rouge, son gris d'ombre, le blanc. Le noir est nacré
partout où il fait fond. Répartition : **70 % perle et blanc · 25 % noir · 5 % rouge.** Le logo garde ses
propres couleurs. Contrastes mesurés (WCAG 2.1), plancher du site 4.5:1.

Les feuilles de composants ne nomment jamais une couleur : elles demandent un rôle (`--c-encre`, `--c-signal`,
`--c-accent`…). Changer de palette, c'est changer `00-jetons.css` et ce paragraphe.

### Les couleurs
| Jeton | Valeur | Rôle |
|---|---|---|
| `--c-perle` | `#F3F3F4` | le fond, blanc perle |
| `--c-blanc` | `#FFFFFF` | une section sur deux, les cases du formulaire |
| `--c-noir` | `#121214` | noir nacré : l'encre, et la nuit des bandes sombres |
| `--c-noir-2` | `#1E1E23` | noir élevé : cases posées sur la nuit |
| `--c-gris` | `#A6A4A5` | gris d'ombre du logo : le texte secondaire de la nuit |
| `--c-rouge` | `#DD0022` | rouge du toit : aplat des boutons d'appel, poignée du comparateur |
| `--c-rouge-sombre` | `#B3001B` | le rouge écrit sur le clair |
| `--c-rouge-clair` | `#FF6B78` | le rouge écrit sur la nuit |

### Le nacré
`--nacre` : trois dégradés radiaux à peine teintés — bleu froid `rgba(196,206,255,.11)` en haut à gauche, rose
`rgba(255,196,226,.08)` au pied à droite, vert d'eau `rgba(190,245,235,.06)` en haut à droite — sur un dégradé
de noir (`#19191E` → `#121214` → `#16151A`, 155°). Il couvre le fond de `.sur-sombre` (bandes, pied, barre
mobile) et le survol des boutons rouges. Au plus clair, il atteint `#2C2D37` : chaque texte de la nuit y garde
son seuil (troisième valeur ci-dessous). Les cases posées sur la nuit restent d'un noir mat, comme des pièces
sur une table laquée ; celles du pied sont transparentes, le nacré passe dessous.

`--nacre-texte` : le même nacré en lettres (`#73737E` → `#A3A0B4` → `#86989A` → `#AA97A6`), pour l'enseigne du
pied (4.0 au plus sombre, seuil des grands textes 3:1).

### Surfaces
| Jeton | Valeur | Usage |
|---|---|---|
| `--c-papier` | `#F3F3F4` | fond dominant, le perle (le blanc dans `.sur-pale`) |
| `--c-papier-2` | `#E7E7EA` | creux : survols, onglet ouvert, emplacement d'une image qui charge |
| `--c-fiche` | `#FFFFFF` | relief : cases du formulaire, sous-menu (le perle sur le blanc) |
| `--c-bitume` | `#121214` | nuit : bandes sombres, pied de page, visionneuse, barre mobile (nacrée) |
| `--c-bitume-2` | `#1E1E23` | surface élevée dans la nuit |

### Texte (perle / blanc / creux)
| Jeton | Valeur | Contrastes |
|---|---|---|
| `--c-encre` | `#121214` | 16.9 / 18.7 / 15.2 |
| `--c-encre-60` | `#505057` | 7.2 / 8.0 / 6.5 |
| `--c-encre-40` | `#64646B` | 5.3 / 5.9 / 4.8 |
| `--c-craie` | `#F3F3F4` | 16.9 sur la nuit, 12.3 au reflet le plus clair |
| `--c-craie-60` | `#A6A4A5` | 7.6 sur la nuit, 6.7 sur la nuit élevée, 5.5 au reflet |
| `--c-filigrane` | `#73737E` | l'enseigne du pied sans nacré en lettres : 4.0 sur la nuit |

### Rouge — l'action et l'accent écrit
| Jeton | Valeur | Usage | Contraste |
|---|---|---|---|
| `--c-signal` | = rouge | aplat des boutons d'appel, poignée du comparateur, sélection de texte | texte blanc dessus : 5.1 |
| `--c-signal-fonce` | = noir | survol des boutons d'appel : le noir nacré (`--fond-survol-signal`) recouvre le rouge | texte blanc dessus : 18.7 |
| `--c-accent` | = rouge sombre | liens, numéros d'étape (01, 02…), chevrons des intitulés, puces, astérisques, « + » des chiffres, repère « vous êtes ici » | 6.5 / 7.2 / 5.8 |

Dans la nuit, le rouge clair devient la couleur écrite (6.8, 5.0 au reflet) et le bouton d'appel garde son
aplat rouge ; au survol, c'est le perle qui le recouvre, texte noir (16.9). Le rouge ne s'écrit jamais en
titre.

### États
`--c-valide` `#2F6B4A` (5.7) · `--c-alerte` `#8E3B12` (6.8) · `--c-focus` = encre. Chaque fond redéfinit
localement ces jetons : un composant demande `--c-encre` et obtient la bonne.

### Filets
`--c-cadre` = l'encre pleine (trait de plan, 1 px) · `--c-ligne` encre à 14 % · `--c-ligne-forte` encre à 50 %
(3.5). Dans la nuit, le cadre est un perle à 40 % (3.6, au-dessus du seuil 3:1 des contours).

### Voiles
Les fonds translucides (en-tête dépoli, panneau du chantier à la une, visionneuse, étiquettes « Avant » /
« Après », ombres) s'écrivent `rgba(var(--c-papier-rgb), …)`, `rgba(var(--c-encre-rgb), …)`,
`rgba(var(--c-sombre-rgb), …)` : aucune composante n'est écrite en dur hors de `00-jetons.css`. L'en-tête est
à 93 %.

## 2 bis. Rythme des fonds

Trois fonds se relaient ; jamais deux fois le même à la suite. Le rouge ne couvre jamais un fond.

| Fond | Classe | Où |
|---|---|---|
| **Perle** `#F3F3F4` | — | couverture, et une section sur deux |
| **Blanc** `#FFFFFF` | `.sur-pale` | posé automatiquement une section sur deux par `outils/rythme.py` ; c'est aussi le fond de la bande des références (page entreprise) |
| **Noir nacré** `#121214` + `--nacre` | `.sur-sombre` | **une bande par page**, choisie à la main : l'entreprise en chiffres (accueil), la méthode et ses repères (prestations), l'ordre des travaux (page pilier), le déroulé (entreprise), les familles de biens (réalisations), ce que contient le devis (devis) ; et le pied de page, la barre mobile |

Une section pose elle-même son fond : ajouter la classe suffit, tous les composants suivent. Une suite de
sections libres qui finirait sur le fond de la section imposée qui la suit part de l'autre fond (`rythme.py`) :
ainsi la bande des références ne suit jamais une section blanche. On ne place jamais de logos de partenaires
(multipliés sur le fond) ni de formulaire dans la nuit. Dans la nuit, on emploie la déclinaison
négative du logo (`logo-negatif.webp` : lettres blanches, toit rouge).

---

## 3. Typographie

### Familles (Google Fonts, `display=swap`)
| Rôle | Famille | Graisses | Jeton |
|---|---|---|---|
| Titres, intitulés, commandes, données | **Archivo** | 400, 500, 600 | `--f-titre`, `--f-texte` |
| Phrases : chapôs, paragraphes, réponses, citations | **Newsreader** (axe optique) | 400 | `--f-lecture` |

L'Archivo est la police historique de DSG : elle garde la continuité de la marque, et sa graisse 500 donne
exactement la voix calme d'une néo-grotesque. La Newsreader est une romaine de lecture à axe optique : elle
s'ajuste seule à la taille (plus ouverte en petit, plus fine en grand).

**Polices de secours calibrées** : l'Arial a la même chasse que l'Archivo (écart mesuré 0,2 %) ; la Georgia,
8 à 10 % plus large que la Newsreader aux tailles de lecture, est réduite par `size-adjust: 91.5 %`. Résultat
mesuré : aucun texte ne se recompose à l'arrivée des polices, décalage de mise en page nul.

### Échelle (fluide, `clamp`)
| Jeton | Valeur | Usage |
|---|---|---|
| `--t-couverture` | 2.5 → 5.25 rem | h1 de l'accueil, interlignage 1, crénage −0.035 em ; dès 1024 px, 3 → 5 rem, à la mesure de sa colonne |
| `--t-piece` | 2.25 → 4.25 rem | h1 des pages intérieures, titre du renvoi final |
| `--t-h2` | 1.875 → 2.875 rem | titres de section (30 px au téléphone, pour qu'ils dominent le texte) |
| `--t-h3` | 1.375 → 1.75 rem | titres de fiche, dépliant ouvert |
| `--t-h4` | 1.125 → 1.3125 rem | lignes de dépliant, cartouche |
| `--t-declaration` | 1.375 → 2 rem | paragraphe d'intention (grotesque), citations (sérif) |
| `--t-chapo` | 1.1875 → 1.375 rem | chapô en sérif |
| `--t-texte` | 1.0625 → 1.1875 rem | paragraphes en sérif |
| `--t-champ` | 1.1875 → 1.5 rem | réponses du formulaire |
| `--t-ui` / `--t-nav` / `--t-petit` / `--t-etiquette` | 1 / 0.9375 / 0.9375 / 0.875 rem | interface |

### Règles
- Casse normale partout. **Aucune capitale décorative, aucun italique, aucun titre bicolore.**
- Titres en Archivo 500, jamais en gras : la hiérarchie vient de la taille et du crénage.
- Les largeurs maximales des titres s'expriment en `em`, pas en `ch` : le `ch` change d'une police à l'autre
  et ferait passer un titre de deux à trois lignes pendant le chargement.
- Chiffres tabulaires pour toute donnée (`font-variant-numeric: tabular-nums`).
- Guillemets français soudés par des espaces insécables.

---

## 4. Grille, espacement, rayons, ombres

- **Mobile d'abord** (v2.6, 27/09/2026) : chaque feuille décrit d'abord le téléphone ; les écrans plus larges
  s'ajoutent par `min-width`, jamais l'inverse (aucune requête `max-width` pour la mise en page). Paliers :
  400, 480, 600, 640, 768, 1024, 1280, 1440 px. Le bureau n'a pas bougé d'un pixel dans la réécriture.
- **Grille** : 4 colonnes au téléphone, 8 dès 768 px, 12 dès 1024 px ; gouttière 16 / 20 / 24 px (768, 1280) ;
  contenu 1600 px max ; marge `clamp(16px, 3.3vw, 48px)`, élargie s'il le faut pour que rien ne passe sous
  l'encoche d'un téléphone couché (`env(safe-area-inset-*)`, `viewport-fit=cover`).
- **Section type** (≥ 1024 px) : l'intitulé et sa cote dans les colonnes 1–4, **accrochés** pendant la lecture
  de la section ; titre et contenu dans les colonnes 5–12. Les blocs larges (registre, chantier signature,
  déroulé, formulaire) reprennent les 12 colonnes (`.pleine-largeur`). Sous 1024 px, tout s'empile.
- **Rythme vertical** : `--y-bloc` `clamp(52px, 7.6vw, 128px)` en haut et en bas de chaque section (52 px au
  téléphone, inchangé sur grand écran).
- **Espacement** : échelle de 4 px (`--sp-1` 4 → `--sp-9` 96).
- **Rayons** : **zéro**, images comprises.
- **Ombres** : quasi absentes. `--om-1` sur la poignée du comparateur et la liste des prestations qui s'ouvre
  sous « Prestations ». Rien d'autre ne flotte.
- **Au doigt** : toute cible qui se touche seule (hors d'un lien pris dans une phrase) mesure **44 px** de
  haut au moins sur un écran tactile ; avec une souris, les listes reprennent leur espacement serré. Au
  toucher, un voile de l'encre du fond répond (`-webkit-tap-highlight-color`) ; les lignes qui se creusent au
  survol se creusent aussi sous le doigt.
- **Au téléphone** : l'en-tête reste visible pendant toute la lecture, qu'on descende ou qu'on remonte (il
  s'effaçait à la descente jusqu'au 05/10/2026, à la demande du client il ne bouge plus) ; la barre d'action
  (Appeler, Devis gratuit) reste sous le pouce : un bandeau de noir nacré collé au bas de l'écran, d'un bord
  à l'autre, sous un trait d'un pixel ; les deux boutons (46 px, 44 px couché) y sont posés dans les marges de
  la page, 10 px d'air au-dessus et au-dessous (6 px couché), et la barre descend sous eux jusqu'au bas de
  l'écran (encoche, barre du navigateur). Une version flottante, décollée des bords, a été essayée puis
  retirée à la demande du client (05/10/2026). On ouvre ce qu'on veut lire — sans script, tout reste ouvert :
  - **Pas de sommaire collant** (retiré le 05/10/2026) : aucune rangée ne s'accroche en haut de l'écran
    pendant la lecture, en plus de l'en-tête.
  - **Lire la suite** : un texte courant de plusieurs paragraphes montre le premier ; le reste vient d'une
    touche, et le focus passe au paragraphe révélé (`outils/lecture.py`). Dès la tablette, tout est déplié.
  - **Suites à faire glisser** (sous 600 px) : le déroulé, les cartes et les besoins défilent de côté dans
    leur cadre, chaque case calée à gauche, la suivante dépassant à droite ; les repères d'angle ne s'y
    posent pas.
  - **Compacité** : les chiffres gardent leur intitulé et leur valeur, sans phrase ; les réalisations passent
    à deux par ligne ; les références à quatre logos par ligne ; le cartouche d'identité de la couverture,
    qui répète les garanties et les chiffres, attend la tablette. Les étapes d'une méthode, sauf la première,
    et le détail de chaque réalisation partent fermés.
  - **Titres** : titre de section à 30 px, chapô à la taille du texte, paragraphe d'intention à celle du
    chapô ; intitulé et titre plus proches, sections plus serrées.
  - **Couverture de l'accueil (v3.4)** : l'accroche, le titre, une seule phrase de chapô (la suite attend la
    tablette), puis l'avant / après **bord à bord**, sur toute la largeur de l'écran (4/3 sous 400 px, 5/4
    au-delà) ; l'appel pleine largeur, le renvoi, puis les trois garanties en bandeau de trois cases. La
    barre du bas n'apparaît qu'une fois cet appel sorti de l'écran : jamais deux « Devis gratuit » à la fois.
  - **Lire la suite** se replie : le bouton devient « Réduire » une fois le texte ouvert.
  - **Pied** : l'enseigne se lit entière au-dessus de la barre d'action.
  - **Haut de page (v3.2)** : un seul fil — accroche ou chemin, titre, chapô, **puis la photo tout de suite**,
    les repères et l'appel pleine largeur. Le premier écran montre un chantier et le bouton. Le bouton
    téléphone de l'en-tête de page s'efface : « Appeler » est déjà dans l'en-tête du site.
  - **Comparateur** : légende sur une ligne (le lieu, les boutons « Avant » / « Après ») ; ce qu'on voit
    attend la tablette.
  - **Réalisations** : une fiche par ligne, photo 3/2 pleine largeur, surface et durée côte à côte.
  - **Fin de page** : la question et ses deux boutons ; les coordonnées sont dans le pied qui suit.
  - **Communes** en trois colonnes serrées ; **photos du formulaire** : un bouton du site « Ajouter des
    photos » et une ligne d'état en français à la place du sélecteur natif ; **barre du bas** : le combiné
    devant « Appeler ».
  - **Pied de page** : logo, adresse, téléphone et courriel en boutons, horaires, itinéraire ; les trois
    listes (le site, les prestations, les zones) repliées sous leur intitulé. Il tient en moins d'un écran.
  - Le formulaire montre les photos choisies en vignettes, et la touche Entrée du clavier mène au champ
    suivant.
- **Retirés en v2.2** (audit d'ergonomie) : le curseur personnalisé qui remplaçait le pointeur, les boutons
  « magnétiques », la vignette qui suivait la souris et masquait les descriptions. Les prestations montrent à
  la place une photo fixe, en tête de ligne depuis la v3.

---

## 5. Le cadre et ses repères — signature du site

- Tout bloc structurant est **cadré d'un pixel d'encre** : en-tête (une case par rubrique), cartouche
  d'identité, relevé chiffré, déroulé, dépliants, formulaire, coordonnées, lots voisins, pied de page. L'image
  de la couverture porte les repères sans le trait : ses quatre angles suffisent à la poser sur le plan.
- Les grilles de cases se tracent par **interstice d'un pixel sur fond d'encre** (`gap: 1px`) quand le nombre
  de cases est fixe ; par **contour propre à chaque case** (`outline`) quand une rangée peut rester incomplète
  (cartes, lots voisins) — jamais de case vide noire.
- Aux quatre angles d'un bloc cadré : un **carré plein de 5 px** (`--repere`) **posé au-dessus de son trait**
  — sa base contre le trait horizontal, en haut comme en bas du cadre — et centré sur le trait vertical, au
  premier plan devant les photos. Une seule règle, la même partout (05/10/2026 : selon le bloc, les carrés
  tombaient sur le trait, au-dessus ou en dessous). Elle suppose que tous les cadres sont tracés en bordure
  (`border`), jamais en ombre intérieure. La liste des blocs concernés est unique, dans `01-socle.css`.
- Le même carré sert de puce (listes de postes, garanties) et, en rouge, de marque « vous êtes ici »
  (rubrique consultée, onglet actif).
- Les repères d'angle prennent la couleur du cadre (`--c-repere`) : l'encre sur les fonds clairs, dans la nuit
  un gris plein (`#6C6C6E`, le perle à 40 % sur le noir), net là où il chevauche un trait.
- Chaque intitulé de section est précédé du **toit** : un chevron dessiné comme la ligne du logo, en rouge
  sombre (rouge clair dans la nuit).

---

## 6. Imagerie

- Angles vifs, aucun arrondi, aucun filtre de couleur : les photos de chantier sont montrées telles quelles.
- Formats : 16/9 et 16/8 (ouverture, chantier signature), 3/2 et 1/1 (fiches alternées), 4/3 (téléphone,
  photos des prestations) ; la couverture de l'accueil prend la hauteur de l'écran.
- **Rien n'est posé sur une photo au repos.** Deux exceptions, qui ont une fonction : les états « Avant » /
  « Après » du comparateur (un voile d'encre à 66 %, texte blanc : 5.0 au pire, sur un mur blanc), et, au
  survol d'une souris, le **viseur** d'une photo de réalisation — quatre angles blancs sur un voile d'encre,
  les repères du site — qui dit qu'elle s'agrandit. Plus de numéro de registre, plus de tampon.
- **Légende en deux voix, dans la photo** (`.vue`, `briques.vue`, `10-comparateur.css`) : en bas de l'image,
  sur un voile d'encre qui monte du pied (78 % → 0, texte blanc lisible sur un mur blanc), le **lieu** en
  grotesque (« Villa de Chailly, Lausanne ») puis **ce qu'on voit** en romain de lecture (« Dégagement et
  cuisine remis en peinture ») ; à droite, **« Voir le chantier »** vers la fiche de la réalisation quand la
  photo en a une (ancre `realisations.html#villa-de-chailly`). Aucune bande de légende sous une photo. Jamais
  un texte alternatif recopié. La visionneuse des réalisations parle de la même façon.
- Le panneau d'un chantier signature est un **perle dépoli** (à 78 % + flou 14 px), cadrée, repères aux
  angles. C'est le seul verre du site, et il a une fonction : garder la photo visible sous la fiche.
- Toutes les images portent `alt`, `width`, `height`. L'image principale de chaque page est en
  `fetchpriority="high"`, toutes les autres en `loading="lazy"`.

---

## 7. Structure de l'accueil

1. **Couverture : la promesse et la preuve dans le même écran.** Dès 1024 px, deux colonnes :
   - à gauche (cinq colonnes), le slogan coiffé du toit (« Du sol au plafond, tout en maîtrise. »), le h1
     « Entreprise de rénovation à Lausanne » (Archivo 500, jusqu'à 80 px), le chapô en sérif ; au pied, calés
     sur le bas de l'image, les trois garanties en liste (visite et devis gratuits, devis 72 h après la visite,
     sans engagement) puis l'appel en rouge et un renvoi souligné « Voir nos réalisations » ;
   - à droite (sept colonnes), le **comparateur avant / après**, repères aux angles, à la hauteur de l'écran
     (460 à 780 px). À l'arrivée, la poignée fait seule un aller-retour lent. Sous l'image, la légende en deux
     voix (« Appartement Beaulieu — La cuisine ouverte sur le séjour, parquet chêne posé ») et deux cases jointives **« Avant » /
     « Après »** qui montrent un état entier d'un geste — au doigt, c'est plus sûr qu'une poignée ; l'étiquette
     de l'état caché s'efface.
   Au téléphone et sur tablette, le texte puis l'image, l'appel pleine largeur, le renvoi dessous.
2. Cartouche d'identité en quatre cases (dès 768 px), puis bande des références (logos multipliés sur le
   perle).
3. Sections à intitulé accroché : l'entreprise, **en bande de noir nacré** (paragraphe d'intention + chiffres en
   quatre cases, « + » en rouge clair), les prestations (une ligne par prestation, sa photo en tête, sans
   numéro), le chantier à la une (panneau dépoli sur photo pleine largeur), la zone, le déroulé en quatre
   cases — perle et blanc en alternance.
4. Renvoi final : un **cadre à repères** en relief (blanc), la question, l'appel en rouge et le téléphone à
   gauche ; à droite, téléphone, courriel, horaires et atelier. Puis pied de page en noir nacré (logo négatif)
   et le nom de l'entreprise en enseigne, en lettres nacrées.

**Pages intérieures principales** (prestations, entreprise, réalisations, devis, et chaque page de métier) :
la composition de l'accueil. Dès 1024 px, à gauche le chemin, le h1 (`--t-piece-colonne`), le chapô, quatre
repères propres à la page (`.piece__faits` : durées, conditions, horaires, zone — tirés des données du site)
et les deux boutons, calés au pied ; à droite, un chantier réel à la hauteur de l'écran, sa légende posée
dedans. Au téléphone, la photo suit les boutons. Les annexes (mentions, confidentialité, merci, 404) gardent
l'en-tête sans photo.

---

## 8. Mouvement

Une seule idée, reprise partout : **ce qui s'ouvre se révèle depuis son cadre.**

| Geste | Propriétés | Durée / courbe |
|---|---|---|
| Démonstration du comparateur (une fois) | `transform` des calques | 3 × 700 ms, entrée-sortie |
| Boutons « Avant » / « Après » | `transform` des calques, jusqu'à l'état entier | 650 ms, entrée-sortie |
| Comparateur | double translation `transform` (calque + image) | instantané, suit le doigt |
| Boutons : seconde encre qui glisse | `transform: scaleX` | 420 ms |
| Pression | `scale: .97` | 160 ms |

- **Rien ne bouge au défilement** (05/10/2026) : ni apparitions, ni titres qui montent, ni photos qui se
  dévoilent, ni chiffres qui défilent, ni photos qui glissent. Au téléphone, ces effets laissaient des zones
  vides et des photos à moitié découvertes pendant qu'on faisait défiler : tout s'affiche d'emblée. Le
  mouvement ne répond plus qu'à un geste (boutons, comparateur, onglets).
- Aucune courbe d'entrée (ease-in). `--e-sortie` `cubic-bezier(.23,1,.32,1)`.
- **Mouvement réduit** : plus aucun déplacement ; l'image d'ouverture reste cadrée, la poignée ne se déplace pas
  seule, les boutons « Avant » / « Après » la placent d'un coup, le reste ne bouge pas.
- **Sans JavaScript** : tout le contenu est visible, les onglets affichent tous leurs panneaux, l'image reste
  cadrée, le comparateur est coupé à 50 % et les boutons « Avant » / « Après », sans effet, n'apparaissent pas.
- Aucune librairie d'animation ni de défilement.
- **Plus de dessins animés** (v3.3) : les ouvriers du site, jugés bas de gamme par le client, sont retirés.
---

## 9. Interdits

- Photo plein écran brute en ouverture.
- Capitales décoratives, italique, titre bicolore, dégradé de texte (seule exception : l'enseigne nacrée du
  pied).
- Un aplat de noir mort en fond de section (la nuit est nacrée) ; une couleur hors de la palette du logo.
- Le rouge en titre ou en fond de section : il reste aux boutons d'appel, aux marques et aux liens.
- Le logo clair dans la nuit (utiliser le négatif).
- Une bande de légende sous une photo : la légende se pose dans l'image.
- Un nom de couleur dans une feuille de composant : demander un rôle (`--c-encre`, `--c-signal`…).
- Une requête `max-width` pour la mise en page : le téléphone est la base, les écrans plus larges s'ajoutent.
- Une cible tactile de moins de 44 px de haut, hors d'un lien pris dans une phrase.
- Une barre de navigation collée en haut de l'écran au téléphone, en plus de l'en-tête.
- Au téléphone, un élément qui change de largeur ou de hauteur pendant la lecture sans qu'on l'ait touché.
- Coins arrondis, ombres décoratives, filet coloré épais sur un côté d'un bloc.
- Un numéro qui ne compte rien : numéro de section (« N° 01 »), de registre sur une photo (« N° 005 »), de
  rang devant une prestation (« 01 … 07 »). Les numéros sont réservés aux séquences réelles (étapes, articles,
  méthode en cinq temps, rang d'une vue dans la visionneuse).
- Une étiquette posée sur une photo au repos (hors états du comparateur) ; un texte alternatif recopié en
  légende.
- Défilant perpétuel (marquee) : il a été retiré avec cette version.
- Toute animation qui touche à la taille ou à la position dans la mise en page.

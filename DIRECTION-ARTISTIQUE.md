# DIRECTION ARTISTIQUE — DSG Rénovation Sàrl

Document de référence unique. Il doit permettre de coder le site **sans avoir vu les images d'inspiration**.
Toutes les valeurs sont normatives : si une valeur n'est pas listée ici, elle ne doit pas apparaître dans le code.
Les valeurs vivent dans `assets/css/00-jetons.css` ; ce document en donne la raison.

Date : 25/09/2026 — Statut : **v2**, en production.
La v1 du 29/07/2026 (« La preuve par la matière », six références hors BTP) reste lisible dans l'historique git
(commit `1fd70a6`). Elle est remplacée intégralement.

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
- **La photo plein écran d'emblée** (demande explicite du client). Remplacée par l'ouverture cadrée (§ 7).
- Le gris-bleu froid : DSG rénove des intérieurs, sa matière est le plâtre et le bois, pas l'acier.
- Le bouton flottant sur grand écran : l'en-tête porte déjà « Devis gratuit ».
- Le défilement lissé par librairie : poids de script et sensation de latence, sans bénéfice pour le visiteur.

---

## 1. Concept

# « LE PLAN D'IMPLANTATION »

Un chantier de rénovation commence par un relevé : on reporte la pièce sur le plan, on plante des repères aux
angles, puis on ouvre. Le site en reprend la matière et le geste :

- un **fond de plâtre frais**, chaud et mat, relayé par un **creux** d'un ton plus bas ;
- une **encre terre d'ombre**, jamais un noir pur ;
- des **cadres d'un pixel marqués aux angles** — les piquets du géomètre ;
- des **bandes de nuit**, la terre d'ombre en fond, qui rythment la page ;
- une **image d'ouverture qui s'élargit** du cadre de la colonne jusqu'aux bords de l'écran, comme une pièce
  qu'on ouvre après l'avoir relevée ;
- **un seul accent, la brique** : rare, sourd, réservé à l'action — les boutons d'appel — et à ce qui s'écrit en
  couleur : liens, numéros, et devant chaque intitulé de section un chevron dessiné comme le toit du logo.

Ce qui reste propre à DSG et n'existe pas chez Tekt : l'Archivo (police historique de la marque), la brique
(héritière du rouge DSG), le logo et son toit rouge, le comparateur avant / après mis au centre de l'accueil, les
repères d'angle qui voyagent avec l'image d'ouverture.

---

## 2. Palette — « Plâtre & brique » (v2.5, les couleurs d'origine)

Répartition : **70 % plâtre · 25 % encre · 5 % brique.** Le logo garde ses propres couleurs. Contrastes mesurés
(WCAG 2.1), plancher du site 4.5:1.

Les feuilles de composants ne nomment jamais une couleur : elles demandent un rôle (`--c-encre`, `--c-signal`,
`--c-accent`…). Changer de palette, c'est changer `00-jetons.css` et ce paragraphe.

### Les couleurs
| Jeton | Valeur | Rôle |
|---|---|---|
| `--c-platre` | `#EEEBE5` | le fond, plâtre frais |
| `--c-terre` | `#27211C` | terre d'ombre : l'encre, et la nuit des bandes sombres |
| `--c-brique` | `#9A3324` | l'action : aplat des boutons d'appel, poignée du comparateur |
| `--c-brique-sombre` | `#86291C` | la brique écrite sur le plâtre, et le survol des boutons |
| `--c-brique-claire` | `#E29A86` | la brique écrite sur la nuit ; terre cuite des dessins |

### Surfaces
| Jeton | Valeur | Usage |
|---|---|---|
| `--c-papier` | `#EEEBE5` | fond dominant, plâtre frais |
| `--c-papier-2` | `#E3DFD7` | creux : sections en retrait, bande des références, survols, onglet ouvert |
| `--c-fiche` | `#F7F5F1` | relief : cases du formulaire, étiquettes posées sur photo |
| `--c-teinte` | `#DAD4C9` | aplat d'action : le renvoi final de chaque page |
| `--c-bitume` | `#27211C` | nuit : bandes sombres, pied de page, visionneuse, barre mobile |
| `--c-bitume-2` | `#342C26` | surface élevée dans la nuit |

### Texte (plâtre / creux / fiche / teinte)
| Jeton | Valeur | Contrastes |
|---|---|---|
| `--c-encre` | `#27211C` | 13.4 / 12.0 / 14.6 / 10.8 |
| `--c-encre-60` | `#574F47` | 6.8 / 6.0 / 7.4 / 5.5 |
| `--c-encre-40` | `#6A6158` | 5.1 / 4.6 / 5.6 — **jamais sur la teinte (4.1)** |
| `--c-craie` | `#EEEBE5` | 13.4 sur la nuit |
| `--c-craie-60` | `#B8AFA4` | 7.4 sur la nuit, 6.3 sur la nuit élevée |
| `--c-filigrane` | `#7E7368` | l'enseigne du pied, grand texte décoratif : 3.4 sur la nuit |

### Brique — l'action et l'accent écrit
| Jeton | Valeur | Usage | Contraste |
|---|---|---|---|
| `--c-signal` | = brique | aplat des boutons d'appel, poignée du comparateur, sélection de texte | texte clair dessus : 6.7 |
| `--c-signal-fonce` | = brique sombre | survol des boutons d'appel : la brique sombre recouvre la brique | texte clair dessus : 8.2 |
| `--c-accent` | = brique sombre | liens, numéros de séquence (01, 02…), chevrons des intitulés, puces, astérisques, « + » des chiffres, repère « vous êtes ici », outils des ouvriers | 7.5 / 6.7 / 8.2 / 6.1 |

Dans la nuit, la brique claire devient la couleur écrite (7.0) et le bouton d'appel garde son aplat de brique ;
au survol, c'est le plâtre qui le recouvre, texte terre d'ombre (13.4). La brique **ne couvre jamais un fond de
section** et ne s'écrit jamais en titre : elle reste aux boutons, aux marques et aux liens.

### États
`--c-valide` `#2F6B4A` (5.3) · `--c-alerte` `#8E3B12` (6.3) · `--c-focus` = encre. Chaque fond redéfinit
localement ces jetons : un composant demande `--c-encre` et obtient la bonne.

### Filets
`--c-cadre` = l'encre pleine (trait de plan, 1 px) · `--c-ligne` encre à 16 % · `--c-ligne-forte` encre à 50 %
(3.0). Dans la nuit, le cadre est un plâtre à 40 % (3.3, au-dessus du seuil 3:1 des contours).

### Voiles
Les fonds translucides (en-tête dépoli, panneau du chantier à la une, visionneuse, ombres) s'écrivent
`rgba(var(--c-papier-rgb), …)`, `rgba(var(--c-encre-rgb), …)`, `rgba(var(--c-sombre-rgb), …)` : aucune
composante n'est écrite en dur hors de `00-jetons.css`. L'en-tête est à 93 %.

## 2 bis. Rythme des fonds

Quatre fonds se relaient ; jamais deux fois le même à la suite.

| Fond | Classe | Où |
|---|---|---|
| **Plâtre** `#EEEBE5` | — | couverture, et une section sur deux |
| **Creux** `#E3DFD7` | `.sur-pale` | posé automatiquement une section sur deux par `outils/rythme.py` ; c'est aussi le fond de la bande des références |
| **Nuit** `#27211C` | `.sur-sombre` | **une bande par page**, choisie à la main : l'entreprise en chiffres (accueil), la méthode et ses repères (prestations), l'ordre des travaux (page pilier), le déroulé (entreprise), les familles de biens (réalisations), ce que contient le devis (devis) ; et le pied de page, la barre mobile |
| **Teinte** `#DAD4C9` | `.sur-vif` | le renvoi final de chaque page : un cran sous le creux, texte encre, bouton d'appel en brique |

Une section pose elle-même son fond : ajouter la classe suffit, tous les composants suivent. Une suite de
sections libres qui finirait sur le fond de la section imposée qui la suit part de l'autre fond (`rythme.py`) :
ainsi la bande des références ne suit jamais un creux. On ne place jamais de logos de partenaires (multipliés sur
le fond) ni de formulaire dans la nuit. Dans la nuit, on emploie la déclinaison négative du logo
(`logo-negatif.webp` : lettres blanches, toit rouge).

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
| `--t-couverture` | 2.5 → 5.25 rem | h1 de l'accueil, interlignage 1, crénage −0.035 em |
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
- **Au téléphone** : l'en-tête s'efface quand on descend et revient dès qu'on remonte ; la barre d'action
  (Appeler, Devis gratuit) reste sous le pouce, 52 px de haut sur un téléphone couché. Une page se parcourt
  par ses intitulés, on ouvre ce qu'on veut lire — sans script, tout reste ouvert :
  - **Sommaire de page** : sous l'en-tête de toute page de trois sections ou plus (à l'accueil, sous le texte
    de la couverture, avant l'image), une rangée de cases jointives reprend l'intitulé de marge de chaque
    section. Elle colle en haut de l'écran, se loge sous l'en-tête quand il revient (un décalage, jamais un
    changement de mise en page), porte le repère de brique sur la section en cours et mène droit à une
    section. Chaque case a son repère, gris au repos : marquer une case ne change pas sa largeur. Elle se
    déduit des intitulés (`outils/sommaire.py`) ; dès 1024 px, l'intitulé accroché dans la marge la remplace.
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
  - **Pied de page** : logo, adresse, téléphone et courriel en boutons, horaires, itinéraire ; les trois
    listes (le site, les prestations, les zones) repliées sous leur intitulé. Il tient en moins d'un écran.
  - Le formulaire montre les photos choisies en vignettes, et la touche Entrée du clavier mène au champ
    suivant.
- **Retirés en v2.2** (audit d'ergonomie) : le curseur personnalisé qui remplaçait le pointeur, les boutons
  « magnétiques », la vignette qui suivait la souris et masquait les descriptions. Les prestations montrent à
  la place une miniature fixe.

---

## 5. Le cadre et ses repères — signature du site

- Tout bloc structurant est **cadré d'un pixel d'encre** : en-tête (une case par rubrique), cartouche
  d'identité, relevé chiffré, déroulé, dépliants, formulaire, coordonnées, lots voisins, pied de page.
- Les grilles de cases se tracent par **interstice d'un pixel sur fond d'encre** (`gap: 1px`) quand le nombre
  de cases est fixe ; par **contour propre à chaque case** (`outline`) quand une rangée peut rester incomplète
  (cartes, lots voisins) — jamais de case vide noire.
- Aux quatre angles d'un bloc cadré : un **carré plein de 5 px** (`--repere`) posé à cheval sur le trait.
  La liste des blocs concernés est unique, dans `01-socle.css`.
- Le même carré sert de puce (listes de postes, garanties) et, en brique, de marque « vous êtes ici »
  (rubrique consultée, onglet actif).
- Les repères d'angle prennent la couleur du cadre (`--c-repere`) : l'encre sur les fonds clairs, le plâtre à
  40 % dans la nuit.
- Chaque intitulé de section est précédé du **toit** : un chevron dessiné comme la ligne du logo, en brique
  sombre (brique claire dans la nuit).

---

## 6. Imagerie

- Angles vifs, aucun arrondi, aucun filtre de couleur : les photos de chantier sont montrées telles quelles.
- Formats : 16/9 et 16/8 (ouverture, chantier signature), 3/2 et 1/1 (fiches alternées), 4/3 (téléphone).
- Étiquettes posées sur photo : case claire `--c-fiche`, texte encre, sans ombre.
- Le panneau d'un chantier signature est un **plâtre dépoli** (plâtre à 78 % + flou 14 px), cadré, repères aux
  angles. C'est le seul verre du site, et il a une fonction : garder la photo visible sous la fiche.
- Toutes les images portent `alt`, `width`, `height`. L'image principale de chaque page est en
  `fetchpriority="high"`, toutes les autres en `loading="lazy"`.

---

## 7. Structure de l'accueil

1. **Couverture** — dans la marge, le slogan « Du sol au plafond, tout en maîtrise. ». À droite : le h1
   « Entreprise de rénovation à Lausanne » (Archivo 500, jusqu'à 84 px), le chapô en sérif, les deux boutons
   empilés et trois garanties (visite et devis gratuits, devis 72 h après la visite, sans engagement).
2. **L'ouverture** — le comparateur avant / après arrive **cadré dans la colonne de la page**, ses angles marqués
   de repères, visible dès le premier écran, l'état avant travaux à gauche. En descendant, deux rideaux couleur
   du fond s'écartent et l'image
   s'élargit jusqu'aux bords de l'écran. À sa première apparition, la poignée fait seule un aller-retour lent
   pour montrer qu'elle se déplace. Légende sous l'image.
3. Cartouche d'identité en quatre cases (dès 768 px), puis bande des références (logos multipliés sur le
   plâtre). Au téléphone, le sommaire de page se glisse entre le texte de la couverture et l'image.
4. Sections à intitulé accroché : l'entreprise, **en bande de nuit** (paragraphe d'intention + chiffres en
   quatre cases, « + » en brique claire), les prestations
   (une ligne par prestation, avec sa miniature fixe), le chantier à la une (panneau dépoli sur photo pleine
   largeur), la zone, le déroulé en quatre cases — creux et plâtre en alternance.
5. Renvoi final sur la teinte, bouton d'appel en brique, puis pied de page de nuit (logo négatif) et le nom de
   l'entreprise en enseigne, en filigrane.

Les pages de métier s'ouvrent de la même façon, autour du tirage de chaque métier. Les pages intérieures
reprennent la couverture : chemin et nature dans la marge, h1 à droite.

---

## 8. Mouvement

Une seule idée, reprise partout : **ce qui s'ouvre se révèle depuis son cadre.**

| Geste | Propriétés | Durée / courbe |
|---|---|---|
| Ouverture de l'image au défilement | `transform` des rideaux et des étiquettes | liée au défilement, adoucie (cubique) |
| Démonstration du comparateur (une fois) | `transform` des calques | 3 × 700 ms, entrée-sortie |
| Comparateur | double translation `transform` (calque + image) | instantané, suit le doigt |
| Apparitions au défilement | `opacity` + `translateY(16px)` | 800 ms `--e-sortie` |
| Lignes des titres de section | `translateY` derrière un masque | 800 ms, décalage 80 ms |
| Boutons : seconde encre qui glisse | `transform: scaleX` | 420 ms |
| Pression | `scale: .97` | 160 ms |
| Ouvriers du site | attributs `transform` du dessin SVG, image par image | passages de 8 à 10 s, puis 3 à 7 s d'absence |

- Uniquement `transform` et `opacity` pendant le défilement : aucune mise en page recalculée.
- Aucune courbe d'entrée (ease-in). `--e-sortie` `cubic-bezier(.23,1,.32,1)`.
- **Mouvement réduit** : plus aucun déplacement ; l'image d'ouverture reste cadrée, la poignée ne se déplace pas
  seule, les apparitions deviennent de simples fondus courts.
- **Sans JavaScript** : tout le contenu est visible, les onglets affichent tous leurs panneaux, l'image reste
  cadrée, le comparateur est coupé à 50 %.
- Aucune librairie d'animation ni de défilement.
- **Les ouvriers du site** : des silhouettes pleines (grosse tête ronde, membres épais aux bouts arrondis,
  sans casque), posées çà et là, chacune seule dans le bas d'une section, sur la limite avec la suivante qui
  lui sert de sol. Quatre sur l'accueil (le peintre dans la bande de l'entreprise, le poseur de sol sous les
  prestations, l'électricien sous la zone, le charpentier sous le déroulé), deux ou trois sur les autres pages,
  une section sur deux, le métier de la page d'abord ; aucune sur les pages légales. Au départ, un sur deux
  vient de la droite. Chacun vit à son rythme, sans attendre le défilement : il arrive en quelques pas,
  travaille, repart en quelques pas et disparaît ; son ouvrage reste un instant, puis s'efface. Il revient 3 à
  7 s plus tard, jamais à la même place : sur un autre sol libre à l'écran s'il y en a un, sinon ailleurs sur
  le même, pour que la page vive sans qu'on défile ; souvent, c'est un collègue resté hors de l'écran qui vient
  à sa place. Jamais deux ouvriers dans une section. Le peintre tient son rouleau à l'horizontale, contre le
  mur. Le poseur de sol, penché, pousse à petits pas un gros rouleau de revêtement : le rouleau roule, maigrit
  à mesure qu'il se déroule, et la bande posée s'allonge derrière lui, d'un seul mouvement continu (il ne pose
  plus de carreaux un à un). Le poseur, l'électricien et le charpentier se retournent pour repartir (le
  rouleau, l'ampoule, le tréteau sont devant eux).
  Un bouton du pied de page met toutes les animations en pause et le site s'en souvient (WCAG 2.2.2) ; rien
  ne bouge hors de l'écran ni onglet caché. Décor seul
  (`aria-hidden`) ; mouvement réduit ou sans JavaScript : chacun saisi au milieu de sa tâche. Silhouette à
  l'encre du fond (claire dans la nuit) ; peinture, revêtement et ampoule allumée en `--c-aplat`, une terre
  cuite (brique claire, plus sourde dans la nuit pour que la peinture se détache du rouleau) ; outils et
  spirale du rouleau en `--c-accent`, la brique. Aucun bleu.

---

## 9. Interdits

- Photo plein écran brute en ouverture.
- Capitales décoratives, italique, titre bicolore, dégradé de texte.
- Noir pur ; une couleur hors de la palette ; le rouge du logo ailleurs que dans le logo.
- La brique en fond de section ou en titre : elle reste aux boutons d'appel, aux marques et aux liens.
- Le logo clair dans la nuit (utiliser le négatif).
- Plus d'une bande de teinte par page : elle est réservée au renvoi final.
- Un nom de couleur dans une feuille de composant : demander un rôle (`--c-encre`, `--c-signal`…).
- Une requête `max-width` pour la mise en page : le téléphone est la base, les écrans plus larges s'ajoutent.
- Une cible tactile de moins de 44 px de haut, hors d'un lien pris dans une phrase.
- Un sommaire de page écrit à la main : il se déduit des intitulés de section.
- Au téléphone, un élément qui change de largeur ou de hauteur pendant la lecture sans qu'on l'ait touché.
- Coins arrondis, ombres décoratives, filet coloré épais sur un côté d'un bloc.
- Numérotation de sections (« N° 01 ») : les numéros sont réservés aux séquences réelles (étapes, articles,
  méthode en cinq temps).
- Défilant perpétuel (marquee) : il a été retiré avec cette version.
- Toute animation qui touche à la taille ou à la position dans la mise en page.

# DIRECTION ARTISTIQUE — DSG Rénovation Sàrl

Document de référence unique. Il doit permettre de coder le site **sans avoir vu les images d'inspiration**.
Toutes les valeurs sont normatives : si une valeur n'est pas listée ici, elle ne doit pas apparaître dans le code.
Les valeurs vivent dans `assets/css/00-jetons.css` ; ce document en donne la raison.

Date : 25/09/2026 — Statut : **v2**, en production.
La v1 du 29/07/2026 (« La preuve par la matière », six références hors BTP) reste lisible dans l'historique git
(commit `1fd70a6`). Elle est remplacée intégralement.

**Révision de palette, 26/09/2026 (v2.2) — « Le toit rouge », tirée du logo.** Le client a jugé le plâtre beige
et la brique ternes, puis a fourni son logo (`assets/images/logo-blanc.avif`) : les couleurs sont désormais celles
du logo, mesurées au pixel. La structure, la typographie, les cadres et le mouvement ne changent pas ; les
couleurs, le rythme des fonds, la navigation et quelques composants changent (§ 2, § 2 bis, § 7). Les palettes
précédentes restent lisibles dans l'historique git (« plâtre et brique » : `0a45b44` ; « bleu de travail, jaune
de chantier », sans le logo : `9fbd8d8`).

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
- Le gris-bleu froid, et désormais aussi le plâtre beige (v2.2) : le fond est blanc, relayé par le gris de l'ombre
  du logo ; la chaleur vient des photos de chantier et du rouge.
- Le bouton flottant sur grand écran : l'en-tête porte déjà « Devis gratuit ».
- Le défilement lissé par librairie : poids de script et sensation de latence, sans bénéfice pour le visiteur.

---

## 1. Concept

# « LE PLAN D'IMPLANTATION »

Un chantier de rénovation commence par un relevé : on reporte la pièce sur le plan, on plante des repères aux
angles, puis on ouvre. Le site en reprend la matière et le geste :

- un **fond blanc**, relayé par le **gris clair** de l'ombre portée des lettres du logo ;
- une **encre noire**, celle des lettres DSG, jamais un noir pur ;
- des **cadres d'un pixel marqués aux angles** — les piquets du géomètre ;
- des **bandes anthracite** qui rythment la page ; les piquets y passent au rouge ;
- une **image d'ouverture qui s'élargit** du cadre de la colonne jusqu'aux bords de l'écran, comme une pièce
  qu'on ouvre après l'avoir relevée ;
- **le rouge du toit**, la ligne qui coiffe « DSG » dans le logo : il porte l'action, les repères, et un chevron
  devant chaque intitulé de section.

Ce qui reste propre à DSG et n'existe pas chez Tekt : l'Archivo (police historique de la marque), le logo et son
toit rouge, le comparateur avant / après mis au centre de l'accueil, les repères d'angle qui voyagent avec
l'image d'ouverture.

---

## 2. Palette — « Le toit rouge » (v2.2)

Toutes les couleurs viennent du logo, mesurées au pixel sur `assets/images/logo-blanc.avif` : le rouge de la
ligne de toit, le noir des lettres, le gris de leur ombre portée. Contrastes mesurés (WCAG 2.1), plancher du
site 4.5:1.

### Couleurs du logo
| Jeton | Valeur | Origine |
|---|---|---|
| `--c-rouge` | `#DE0022` | la ligne de toit |
| `--c-rouge-fonce` | `#A8001A` | le même, une ombre plus bas (survol) |
| `--c-noir` | `#1A1A1C` | les lettres DSG |
| `--c-gris-logo` | `#A8A8A8` | l'ombre portée des lettres (décor seulement : 2.3 sur le blanc) |

### Surfaces
| Jeton | Valeur | Usage |
|---|---|---|
| `--c-papier` | `#FFFFFF` | fond dominant |
| `--c-papier-2` | `#F2F2F3` | creux : survols, onglet ouvert, légendes du formulaire |
| `--c-fiche` | `#FFFFFF` | relief : cases du formulaire, étiquettes posées sur photo |
| `--c-bitume` | `#1C1C1F` | anthracite : bandes sombres, pied de page, visionneuse, barre mobile |
| `--c-bitume-2` | `#29292E` | surface élevée dans l'anthracite |

### Texte (blanc / creux / gris clair / gris élevé)
| Jeton | Valeur | Contrastes |
|---|---|---|
| `--c-encre` | `#1A1A1C` | 17.4 / 15.5 / 15.7 / 14.2 |
| `--c-encre-60` | `#4B4B52` | 8.7 / 7.7 / 7.8 / 7.1 |
| `--c-encre-40` | `#66666D` | 5.7 / 5.1 / 5.1 / 4.7 |
| `--c-craie` | `#F4F4F5` | 15.5 sur l'anthracite |
| `--c-craie-60` | `#B9B9BF` | 8.7 sur l'anthracite, 7.4 élevé |

### Rouge — l'action et l'accent écrit
| Jeton | Valeur | Usage | Contraste |
|---|---|---|---|
| `--c-signal` | = rouge du logo | aplat des boutons d'appel, poignée du comparateur, sélection de texte | blanc dessus : 5.1 |
| `--c-signal-fonce` | `#A8001A` | survol des boutons d'appel | blanc dessus : 7.8 |
| `--c-accent` | `#C4001E` | liens, numéros de séquence (01, 02…), chevrons des intitulés, puces, astérisques, « + » des chiffres, repère « vous êtes ici » | 6.2 / 5.6 / 5.6 / 5.1 |

`--c-accent` est un cran plus sombre que le rouge du logo, qui ne tiendrait pas 4.5 sur le gris clair (4.2).
Sur l'anthracite, il devient un rouge clair `#FF6B79` (6.2) ; sur la bande rouge, il devient blanc.

### États
`--c-valide` `#1D7048` (6.1) · `--c-alerte` `#B42318` (6.6) · `--c-focus` = encre. Chaque fond redéfinit
localement ces jetons : un composant demande `--c-encre` et obtient la bonne.

### Filets
`--c-cadre` = l'encre pleine (trait de plan, 1 px) · `--c-ligne` encre à 16 % · `--c-ligne-forte` encre à 50 %.
Sur l'anthracite, le cadre est un blanc à 40 % (3.8, au-dessus du seuil 3:1 des contours) ; sur le rouge, blanc
plein (5.1).

### Voiles
Les fonds translucides (en-tête dépoli, panneau du chantier à la une, visionneuse, ombres) s'écrivent
`rgba(var(--c-papier-rgb), …)`, `rgba(var(--c-encre-rgb), …)`, `rgba(var(--c-nuit-rgb), …)` : aucune
composante n'est écrite en dur hors de `00-jetons.css`. L'en-tête est à 93 %.

## 2 bis. Rythme des fonds

Quatre fonds se relaient ; jamais deux fois le même à la suite.

| Fond | Classe | Où |
|---|---|---|
| **Blanc** | — | couverture, et une section sur deux |
| **Gris clair** `#F3F3F4` | `.sur-gris` | posé automatiquement une section sur deux par `outils/rythme.py` |
| **Anthracite** | `.sur-sombre` | **une bande par page**, choisie à la main : l'entreprise en chiffres (accueil), la méthode et ses repères (prestations), l'ordre des travaux (page pilier), le déroulé (entreprise), les familles de biens (réalisations), ce que contient le devis (devis) ; et le pied de page, la barre mobile |
| **Rouge DSG** | `.sur-rouge` | le renvoi final de chaque page : texte blanc, bouton d'appel inversé (blanc, texte noir, noir au survol) |

Une section pose elle-même son fond : ajouter la classe suffit, tous les composants suivent. On ne place jamais
de logos de partenaires (multipliés sur le fond) ni de formulaire sur l'anthracite ou le rouge. Le logo ne va
jamais sur le rouge : son toit y disparaîtrait. Sur l'anthracite, on emploie sa déclinaison négative
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
| `--t-h2` | 1.75 → 2.875 rem | titres de section |
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

- **Grille** : 12 colonnes, gouttière 24 / 20 / 16 px, contenu 1600 px max, marge `clamp(16px, 3.3vw, 48px)`.
- **Section type** (≥ 1024 px) : l'intitulé et sa cote dans les colonnes 1–4, **accrochés** pendant la lecture
  de la section ; titre et contenu dans les colonnes 5–12. Les blocs larges (registre, chantier signature,
  déroulé, formulaire) reprennent les 12 colonnes (`.pleine-largeur`). Sous 1024 px, tout s'empile.
- **Rythme vertical** : `--y-bloc` `clamp(64px, 7.6vw, 128px)` en haut et en bas de chaque section.
- **Espacement** : échelle de 4 px (`--sp-1` 4 → `--sp-9` 96).
- **Rayons** : **zéro**, images comprises.
- **Ombres** : quasi absentes. `--om-1` sur la poignée du comparateur et la liste des prestations qui s'ouvre
  sous « Prestations ». Rien d'autre ne flotte.
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
- Le même carré sert de puce (listes de postes, garanties) et, en rouge, de marque « vous êtes ici »
  (rubrique consultée, onglet actif).
- Sur l'anthracite, les repères d'angle passent au **rouge** (`--c-repere`), sur la bande rouge au blanc.
- Chaque intitulé de section est précédé du **toit** : un chevron rouge dessiné comme la ligne du logo.

---

## 6. Imagerie

- Angles vifs, aucun arrondi, aucun filtre de couleur : les photos de chantier sont montrées telles quelles.
- Formats : 16/9 et 16/8 (ouverture, chantier signature), 3/2 et 1/1 (fiches alternées), 4/3 (téléphone).
- Étiquettes posées sur photo : case blanche `--c-fiche`, texte encre, sans ombre.
- Le panneau d'un chantier signature est un **blanc dépoli** (blanc à 78 % + flou 14 px), cadré, repères aux
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
3. Cartouche d'identité en quatre cases, puis bande des références (logos multipliés sur le fond blanc).
4. Sections à intitulé accroché : l'entreprise, **en bande anthracite** (paragraphe d'intention + chiffres en
   quatre cases, piquets et « + » en rouge), les prestations
   (une ligne par prestation, avec sa miniature fixe), le chantier à la une (panneau dépoli sur photo pleine
   largeur), la zone, le déroulé en quatre cases — gris et blanc en alternance.
5. Renvoi final sur une bande rouge, bouton blanc, puis pied de page anthracite (logo négatif) et le nom de
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

- Uniquement `transform` et `opacity` pendant le défilement : aucune mise en page recalculée.
- Aucune courbe d'entrée (ease-in). `--e-sortie` `cubic-bezier(.23,1,.32,1)`.
- **Mouvement réduit** : plus aucun déplacement ; l'image d'ouverture reste cadrée, la poignée ne se déplace pas
  seule, les apparitions deviennent de simples fondus courts.
- **Sans JavaScript** : tout le contenu est visible, les onglets affichent tous leurs panneaux, l'image reste
  cadrée, le comparateur est coupé à 50 %.
- Aucune librairie d'animation ni de défilement.

---

## 9. Interdits

- Photo plein écran brute en ouverture.
- Capitales décoratives, italique, titre bicolore, dégradé de texte.
- Noir pur, une couleur étrangère au logo, le rouge du logo écrit sur le gris (utiliser `--c-accent`).
- Le logo posé sur le rouge (son toit y disparaît) ; le logo clair sur l'anthracite (utiliser le négatif).
- Plus d'une bande rouge par page : elle est réservée au renvoi final.
- Coins arrondis, ombres décoratives, filet coloré épais sur un côté d'un bloc.
- Numérotation de sections (« N° 01 ») : les numéros sont réservés aux séquences réelles (étapes, articles,
  méthode en cinq temps).
- Défilant perpétuel (marquee) : il a été retiré avec cette version.
- Toute animation qui touche à la taille ou à la position dans la mise en page.

# DIRECTION ARTISTIQUE — DSG Rénovation Sàrl

Document de référence unique. Il doit permettre de coder le site **sans avoir vu les images d'inspiration**.
Toutes les valeurs sont normatives : si une valeur n'est pas listée ici, elle ne doit pas apparaître dans le code.
Les valeurs vivent dans `assets/css/00-jetons.css` ; ce document en donne la raison.

Date : 25/09/2026 — Statut : **v2**, en production.
La v1 du 29/07/2026 (« La preuve par la matière », six références hors BTP) reste lisible dans l'historique git
(commit `1fd70a6`). Elle est remplacée intégralement.

**Révision de palette, 26/09/2026 (v2.4) — « Chocolat & ciel ».** Le client a jugé les couleurs du logo trop
basiques, puis le bleu nuit et safran trop vus ; il a choisi cette palette parmi quatre ambiances rendues sur
le site (outremer, patine vert-de-gris, chocolat et ciel, graphite et fluo). Le logo garde ses couleurs ; le
site ne les reprend plus. La structure, la typographie, les cadres et le mouvement ne changent pas ; les
couleurs et les noms des fonds changent (§ 2, § 2 bis, § 5, § 7). Les palettes précédentes restent lisibles
dans l'historique git (« plâtre et brique » : `0a45b44` ; « bleu de travail, jaune de chantier » : `9fbd8d8` ;
« le toit rouge », tirée du logo : `d604530` ; « bleu de plan & safran » : `c322a78`).

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
- Le plâtre beige : le fond est blanc, relayé par un bleu ciel très pâle, proche du gris-bleu de Tekt ; la
  chaleur vient des photos de chantier et du brun chocolat.
- Le bouton flottant sur grand écran : l'en-tête porte déjà « Devis gratuit ».
- Le défilement lissé par librairie : poids de script et sensation de latence, sans bénéfice pour le visiteur.

---

## 1. Concept

# « LE PLAN D'IMPLANTATION »

Un chantier de rénovation commence par un relevé : on reporte la pièce sur le plan, on plante des repères aux
angles, puis on ouvre. Le site en reprend la matière et le geste :

- un **fond blanc**, relayé par un **ciel très pâle** ;
- une **encre brun chocolat**, celle du bois, jamais un noir pur ;
- des **cadres d'un pixel marqués aux angles** — les piquets du géomètre ;
- des **bandes chocolat** qui rythment la page ; les piquets y passent au bleu ciel ;
- une **image d'ouverture qui s'élargit** du cadre de la colonne jusqu'aux bords de l'écran, comme une pièce
  qu'on ouvre après l'avoir relevée ;
- **le bleu ciel** d'une pièce rendue à la lumière : il porte l'action, boutons d'appel et renvoi final ;
- **un bleu profond** pour ce qui s'écrit en couleur : liens, numéros, et devant chaque intitulé de section un
  chevron dessiné comme le toit du logo.

Ce qui reste propre à DSG et n'existe pas chez Tekt : l'Archivo (police historique de la marque), le logo et son
toit rouge, le comparateur avant / après mis au centre de l'accueil, les repères d'angle qui voyagent avec
l'image d'ouverture.

---

## 2. Palette — « Chocolat & ciel » (v2.4)

Trois couleurs, choisies par le client parmi quatre ambiances rendues sur le site : le **brun chocolat** du bois
pour l'encre et les bandes sombres, le **bleu ciel** d'une pièce rendue à la lumière pour l'action, un **bleu
profond** pour ce qui s'écrit en couleur. Le logo garde ses propres couleurs ; le site ne les reprend pas.
Contrastes mesurés (WCAG 2.1), plancher du site 4.5:1.

Les feuilles de composants ne nomment jamais une couleur : elles demandent un rôle (`--c-encre`, `--c-signal`,
`--c-accent`…). Changer de palette, c'est changer `00-jetons.css` et ce paragraphe.

### Les trois couleurs
| Jeton | Valeur | Rôle |
|---|---|---|
| `--c-chocolat` | `#2B1B14` | l'encre du texte et des cadres |
| `--c-bleu` | `#1D64A8` | l'accent écrit : liens, numéros, puces, chevrons |
| `--c-ciel` | `#9ACDF5` | l'action : boutons d'appel, poignée du comparateur, renvoi final |
| `--c-ciel-fonce` | `#86C0EE` | le même, une ombre plus bas : surface élevée sur la bande ciel |

### Surfaces
| Jeton | Valeur | Usage |
|---|---|---|
| `--c-papier` | `#FFFFFF` | fond dominant |
| `--c-papier-2` | `#F3F8FD` | creux : survols, onglet ouvert, légendes du formulaire |
| `--c-fiche` | `#FFFFFF` | relief : cases du formulaire, étiquettes posées sur photo |
| `--c-teinte` | `#D9E9F8` | aplat secondaire |
| `--c-bitume` | `#3B2419` | chocolat : bandes sombres, pied de page, visionneuse, barre mobile |
| `--c-bitume-2` | `#4B3125` | surface élevée dans le chocolat |

### Texte (blanc / creux / ciel pâle / pâle élevé)
| Jeton | Valeur | Contrastes |
|---|---|---|
| `--c-encre` | `#2B1B14` | 16.5 / 15.5 / 14.7 / 13.4 |
| `--c-encre-60` | `#5A4840` | 8.6 / 8.1 / 7.7 / 7.0 |
| `--c-encre-40` | `#6E5C54` | 6.3 / 5.9 / 5.6 / 5.1 |
| `--c-craie` | `#FFF7F2` | 13.7 sur le chocolat |
| `--c-craie-60` | `#DCC8BB` | 9.0 sur le chocolat, 7.4 élevé |

### Bleu ciel — l'action ; bleu profond — l'accent écrit
| Jeton | Valeur | Usage | Contraste |
|---|---|---|---|
| `--c-signal` | = ciel | aplat des boutons d'appel, poignée du comparateur, sélection de texte | chocolat dessus : 9.8 |
| `--c-signal-fonce` | = chocolat | survol des boutons d'appel : le chocolat recouvre le ciel | blanc dessus : 16.5 |
| `--c-accent` | = bleu profond | liens, numéros de séquence (01, 02…), chevrons des intitulés, puces, astérisques, « + » des chiffres, repère « vous êtes ici » | 6.1 / 5.7 / 5.4 / 4.9 |

Le ciel ne s'écrit jamais sur un fond clair (1.7) : il s'y pose en aplat, texte chocolat dessus. Sur le
chocolat, un ciel à peine plus clair (`#A8D4F7`) devient la couleur écrite (9.2) et le bouton d'appel garde son
aplat ; au survol, c'est le blanc qui le recouvre. Sur la bande ciel, tout est chocolat et le bouton s'inverse :
chocolat, texte blanc.

### États
`--c-valide` `#1D7048` (6.1) · `--c-alerte` `#B42318` (6.6) · `--c-focus` = encre. Chaque fond redéfinit
localement ces jetons : un composant demande `--c-encre` et obtient la bonne.

### Filets
`--c-cadre` = l'encre pleine (trait de plan, 1 px) · `--c-ligne` encre à 16 % · `--c-ligne-forte` encre à 50 %
(3.3). Sur le chocolat, le cadre est un blanc à 40 % (3.6, au-dessus du seuil 3:1 des contours) ; sur le ciel,
chocolat plein (9.8).

### Voiles
Les fonds translucides (en-tête dépoli, panneau du chantier à la une, visionneuse, ombres) s'écrivent
`rgba(var(--c-papier-rgb), …)`, `rgba(var(--c-encre-rgb), …)`, `rgba(var(--c-nuit-rgb), …)` : aucune
composante n'est écrite en dur hors de `00-jetons.css`. L'en-tête est à 93 %.

## 2 bis. Rythme des fonds

Quatre fonds se relaient ; jamais deux fois le même à la suite.

| Fond | Classe | Où |
|---|---|---|
| **Blanc** | — | couverture, et une section sur deux |
| **Ciel pâle** `#EAF3FC` | `.sur-pale` | posé automatiquement une section sur deux par `outils/rythme.py` |
| **Chocolat** `#3B2419` | `.sur-sombre` | **une bande par page**, choisie à la main : l'entreprise en chiffres (accueil), la méthode et ses repères (prestations), l'ordre des travaux (page pilier), le déroulé (entreprise), les familles de biens (réalisations), ce que contient le devis (devis) ; et le pied de page, la barre mobile |
| **Bleu ciel** `#9ACDF5` | `.sur-vif` | le renvoi final de chaque page : texte chocolat, bouton d'appel inversé (chocolat, texte blanc ; blanc au survol) |

Une section pose elle-même son fond : ajouter la classe suffit, tous les composants suivent. On ne place jamais
de logos de partenaires (multipliés sur le fond) ni de formulaire sur le chocolat ou le ciel. Le logo ne va
jamais sur le ciel : son toit rouge y jurerait. Sur le chocolat, on emploie sa déclinaison négative
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
- Le même carré sert de puce (listes de postes, garanties) et, en bleu profond, de marque « vous êtes ici »
  (rubrique consultée, onglet actif).
- Sur le chocolat, les repères d'angle passent au **bleu ciel** (`--c-repere`), sur la bande ciel au chocolat.
- Chaque intitulé de section est précédé du **toit** : un chevron dessiné comme la ligne du logo, en bleu
  profond (bleu ciel sur le chocolat).

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
4. Sections à intitulé accroché : l'entreprise, **en bande chocolat** (paragraphe d'intention + chiffres en
   quatre cases, piquets et « + » en bleu ciel), les prestations
   (une ligne par prestation, avec sa miniature fixe), le chantier à la une (panneau dépoli sur photo pleine
   largeur), la zone, le déroulé en quatre cases — ciel pâle et blanc en alternance.
5. Renvoi final sur une bande bleu ciel, bouton chocolat, puis pied de page chocolat (logo négatif) et le nom de
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
| Ouvriers du site | attributs `transform` du dessin SVG, image par image | boucles indépendantes de 9 à 14 s |

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
  une section sur deux, le métier de la page d'abord ; aucune sur les pages légales. Un sur deux vient de la
  droite. Chacun vit à son rythme, sans attendre le défilement : il arrive en marchant, travaille, repart,
  revient ; son ouvrage s'efface avant son retour. Un bouton du pied de page met toutes les animations en
  pause et le site s'en souvient (WCAG 2.2.2) ; rien ne bouge hors de l'écran ni onglet caché. Décor seul
  (`aria-hidden`) ; mouvement réduit ou sans JavaScript : chacun saisi au milieu de sa tâche. Silhouette à
  l'encre du fond (claire sur la bande sombre), carreaux, peinture et ampoule en `--c-aplat`, outils en
  `--c-accent`.

---

## 9. Interdits

- Photo plein écran brute en ouverture.
- Capitales décoratives, italique, titre bicolore, dégradé de texte.
- Noir pur ; une couleur hors de la palette ; le rouge du logo ailleurs que dans le logo.
- Le bleu ciel écrit sur un fond clair (1.7) : il s'y pose en aplat, jamais en texte (utiliser `--c-accent`).
- Le logo posé sur le ciel (son toit rouge y jure) ; le logo clair sur le chocolat (utiliser le négatif).
- Plus d'une bande ciel par page : elle est réservée au renvoi final.
- Un nom de couleur dans une feuille de composant : demander un rôle (`--c-encre`, `--c-signal`…).
- Coins arrondis, ombres décoratives, filet coloré épais sur un côté d'un bloc.
- Numérotation de sections (« N° 01 ») : les numéros sont réservés aux séquences réelles (étapes, articles,
  méthode en cinq temps).
- Défilant perpétuel (marquee) : il a été retiré avec cette version.
- Toute animation qui touche à la taille ou à la position dans la mise en page.

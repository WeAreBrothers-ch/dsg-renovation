# DSG Rénovation — site vitrine

Site d'une page pour **DSG Rénovation Sàrl**, entreprise de rénovation
clé en main à Lausanne (arc lémanique).

HTML, CSS et JavaScript natifs — aucun framework, aucune étape de build.
Ouvrir `index.html` suffit.

## Structure

```
index.html            le dossier complet, en sept pièces
mentions-legales.html pièce annexe A — éditeur, droits, responsabilité
confidentialite.html  pièce annexe B — traitement des données
assets/css/           feuilles numérotées, chargées dans l'ordre
assets/js/            un module par comportement
assets/images/        tirages du comparateur avant / après
```

Les deux annexes partagent l'en-tête, le menu et le pied du dossier,
mais n'en chargent que les feuilles utiles. Leur mise en page tient
dans `14-document.css`.

Les feuilles de style se lisent dans l'ordre de leur numéro :
`00-jetons.css` porte **toutes** les valeurs du site (couleurs,
typographie, espacements, durées). Les autres n'y puisent que des
jetons — aucune valeur n'est écrite en dur ailleurs, hors cas commenté.

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

Les annexes ne chargent que `nav.js`, `motion.js`, `effets.js` et
`curseur.js` : elles n'ont ni comparateur, ni visionneuse, ni
formulaire.

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

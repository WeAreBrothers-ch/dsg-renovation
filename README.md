# DSG Rénovation — site vitrine

Site de **DSG Rénovation Sàrl**, entreprise de rénovation clé en main à
Lausanne (arc lémanique). HTML, CSS et JavaScript natifs, aucun
framework ; un petit script PHP pour le formulaire. Hébergement prévu :
**Infomaniak** (Apache + PHP).

## Structure

```
index.html            accueil : la preuve, les chiffres, les prestations
services.html         page pilier des prestations
services/*.html       une page par prestation — sept fichiers
realisations.html     nos chantiers, familles de biens, imprévus
entreprise.html       histoire, déroulé, limites, références
devis.html            formulaire de demande, lecture d'un devis, vingt questions
mentions-legales.html éditeur, hébergeur, droits, responsabilité (noindex)
confidentialite.html  traitement des données (noindex)
404.html              page introuvable, servie par le serveur (noindex)
merci.html            après l'envoi du formulaire (noindex)
envoi.php             reçoit le formulaire et l'envoie par e-mail, photos jointes
.htaccess             HTTPS, www, redirections, cache, 404, fichiers internes bloqués
favicon.ico, apple-touch-icon.png   icônes du site
site.webmanifest      nom et icône quand on ajoute le site à l'écran d'accueil
sitemap.xml, robots.txt             régénérés avec les pages
assets/css/           feuilles sources numérotées ; site.css = leur version livrée
assets/js/            un module par comportement
assets/fonts/         Archivo et Newsreader, servies par le site
assets/images/        logo et déclinaisons, image de partage, photos locales
outils/               générateur de pages — voir plus bas
```

**Quatre entrées de menu, une liste des prestations sous la première.**
Les références vivent dans la page entreprise, dont elles sont la
preuve ; les questions dans la page de devis, où elles se posent.

## Le générateur

Les pages sont assemblées par un script, puis livrées en HTML
statique. C'est une commodité de maintenance : un numéro de téléphone
ne se corrige qu'à un endroit.

Après une modification du contenu, des feuilles de style ou du chrome :

```
python3 outils/construire.py
```

Le script écrit les pages, `assets/css/site.css` (les vingt et une feuilles
sources concaténées et minifiées, avec une empreinte de version dans
l'adresse), le plan du site daté et `robots.txt`.

Pour consulter le site en local, servir le dossier (les liens vers
l'accueil pointent sur « / », qu'un simple fichier ouvert ne résout
pas) :

```
python3 -m http.server     # puis http://localhost:8000
```

| Fichier | Contenu |
|---|---|
| `donnees_site.py` | coordonnées, horaires, logo, navigation, communes, chiffres |
| `services_gros_oeuvre.py` | rénovation, plâtrerie, cloisons, faux plafonds |
| `services_finitions.py` | peinture, revêtements, carrelage, sols, nettoyage |
| `services_solutions.py` | remise en état entre deux locations, salle de bains |
| `prestations.py` | quels métiers partagent une page, titres, intertitres, repères |
| `pages_solutions.py` | les deux pages de prestation transverses |
| `lausanne_*.py` | ce que le bâti lausannois impose à chaque métier (« sur le terrain ») |
| `contenu_entreprise.py` | histoire, déroulé d'un chantier, limites, engagements |
| `contenu_devis.py` | ce que contient un devis, comment le comparer |
| `contenu_questions.py` | vingt questions, groupées par moment du projet |
| `contenu_divers.py` | ordre des travaux, besoins, familles de biens, collaborations |
| `assemblage.py` | feuille unique, versions, assemblage et écriture d'une page |
| `rythme.py` | alternance automatique des fonds blanc / pâle |
| `lecture.py` | « Lire la suite » : au téléphone, un texte long montre son premier paragraphe |
| `typographie.py` | espaces insécables avant « : ; ? ! » et dans les guillemets |
| `images.py` | remplace les images Wix par leurs copies locales (srcset compris) |
| `rapatrier_images.py` | télécharge les images encore chez Wix — voir « Mise en ligne » |
| `gabarit.py` | tête du document, en-tête, liste des prestations, menu |
| `gabarit_pied.py` | pied de page, barre d'action mobile |
| `gabarit_liens.py` | lien vers l'accueil, liens « Devis gratuit » (prestation pré-cochée) |
| `carte.py` | le plan du Léman de l'accueil : contour du lac, repères des communes, carton de Lausanne |
| `confiance.py` | déroulés en cases (accueil, entreprise, méthode des prestations), logos, témoignages (masqués tant qu'ils sont provisoires) |
| `accessibilite.py` | relie chaque section à son titre (lecteurs d'écran) |
| `briques.py`, `briques_bis.py` | couverture, intercalaire, chiffres, renvoi final, cartes, besoins, postes (liste ouverte), glissière (suites à faire glisser au téléphone, et leur rangée de repères) |
| `repli.py` | onglets et dépliants |
| `page_service.py`, `service_liens.py` | corps d'une page de prestation, zone, prestations voisines |
| `page_accueil.py`, `page_prestations.py`, `pages_site.py`, `pages_contenu.py` | corps des pages |
| `pages_speciales.py` | 404 et merci |
| `catalogue.py` | titres, descriptions et H1 des pages de la racine |
| `seo.py` | balisage structuré, `sitemap.xml`, `robots.txt` |
| `fragments/` | blocs HTML ; les coordonnées s'y écrivent `{{TELEPHONE}}`, `{{RUE}}`… |

Pour modifier une adresse, un numéro ou les horaires, éditer
`donnees_site.py` : la correction se propage partout, balisage compris.

Les feuilles de style se lisent dans l'ordre de leur numéro :
`00-jetons.css` porte **toutes** les valeurs du site (couleurs,
typographie, espacements, durées). Les autres n'y puisent que des
jetons. On n'édite jamais `site.css`, qui est réécrit à chaque
construction.

## Référencement

- **Chaque page** : un titre de 60 caractères au plus avec le métier et
  « Lausanne », une description de 155 au plus, un seul H1 qui dit le
  métier et la ville, des intertitres propres à la page, une adresse
  canonique, une image de partage (1200 × 630).
- **Balisage** `schema.org` : fiche d'établissement `GeneralContractor`
  (adresse, horaires, zone, date de fondation, effectif, carte) sur
  toutes les pages, `WebSite` sur l'accueil, `Service` et `FAQPage` sur
  les pages de prestation, fil d'Ariane partout. Aucun avis ni note
  n'est balisé : seuls de vrais avis vérifiables pourraient l'être.
- **Maillage** : chaque chantier des réalisations renvoie vers ses
  prestations, et chaque prestation vers le chantier que montre sa
  photo d'en-tête (« Voir le chantier », ancre de la fiche) ; les
  réponses de la page devis vers les pages qu'elles évoquent, chaque
  prestation vers ses voisines.
- **Contenu local** : la section « sur le terrain » de chaque prestation
  décrit ce que le bâti lausannois impose (plâtre sur lattis, hauteurs
  sous plafond, accès de Sous-Gare, immeubles locatifs habités). C'est le
  contenu qu'aucun concurrent ne peut copier.
- **Pas de pages par commune** : des pages « rénovation à Pully /
  Morges… » sur un même modèle seraient traitées par Google comme des
  pages satellites. La zone est couverte par la fiche d'établissement,
  les réalisations et le texte.
- **Vitesse** : une seule feuille de style, polices servies par le site
  et préchargées, scripts différés, images en `srcset` une fois
  rapatriées, cache long (`.htaccess`).

## Couleurs et direction artistique

Palette « Blanc, chaux & rouge DSG » (v6, 07/10/2026) — tout est
décrit dans `DIRECTION-ARTISTIQUE.md`. Le noir, le rouge du toit et le
gris d'ombre du logo, sur un **blanc** franc ; la **chaux** chaude
(`#F4F1EC`) une section sur deux, une bande de noir par page. Ce noir
est **nacré** (`--nacre`) : de légers reflets ivoire, champagne et
vieux rose — sur les bandes sombres, le pied, la barre mobile et le
survol des boutons ; l'enseigne du pied s'écrit en lettres nacrées,
d'un bord à l'autre de la grille. Une seule couleur, le **rouge** du
toit, qui ne couvre jamais un fond : à plat sur les boutons d'appel,
écrit pour les liens, astérisques, erreurs, « vous êtes ici », les
chevrons, numéros et puces, en grand pour les chiffres de
l'entreprise, et en filet au-dessus du pied de page. Le logo garde ses
propres couleurs. Changer de palette, c'est changer
`assets/css/00-jetons.css` : les autres feuilles ne demandent que des
rôles (`--c-encre`, `--c-signal`, `--c-accent`, `--c-eclat`…).
Des cadres d'un pixel ; le repère carré d'angle ne marque que
l'ouverture de l'accueil et le renvoi final (`01-socle.css`) ; un
chevron devant chaque intitulé, une grotesque (Archivo) pour les
titres et une sérif de lecture (Newsreader) pour les phrases.

Ce que la v6.4 a ajouté (07/10/2026) : deux composants de 21st.dev,
réécrits sans dépendance. **L'enseigne du pied s'allume** en rouge sous
la souris ou le doigt (« Text Hover Effect ») ; **la marque des onglets et
des filtres glisse** d'une case à l'autre (« Animated Tabs »). Rien
d'ajouté à l'écran : ils animent ce qui existait.

Ce que la v6.3 a ajouté (07/10/2026) : **le plan se trace**. Quand un
bloc arrive à l'écran, ses traits se tracent : le toit de l'intitulé se
dessine, les filets des listes se tirent à la règle un par un, le plan
du Léman se relève depuis l'atelier et ses piquets se plantent. Seuls les
traits bougent — texte, chiffres et photos sont là d'emblée (`09-trace.css`,
`motion.js`). Rien sans script ni en mouvement réduit.

Ce que la v6.2 a ajouté (07/10/2026) : la section « Zone » de
l'accueil montre un **plan du Léman**, tracé comme un plan
d'implantation — la rive au trait, l'eau hachurée, un carré rouge par
commune, l'atelier en piquet maître, une échelle de 10 km. Les sept
communes serrées autour de Lausanne sont nommées dans un carton agrandi :
sous le plan au téléphone, logé dans son angle dès la tablette. Survoler une commune, sur le plan ou dans la
liste, la marque des deux côtés. Idée reprise du « Location Map » de
21st.dev, dessinée sans photo ni dépendance (`carte.py`, `13-carte.css`,
`carte.js`) ; contours OFS / swisstopo (paquet npm `swiss-maps`, 2026),
crédités dans les mentions légales.

Ce que la v6.1 a ajouté (07/10/2026) : la bande de noir de chaque page
porte la **trame du relevé**, un quadrillage de points à peine visible ;
un toucher ou un clic y fait partir une onde carrée au rouge du toit, et
la bande en montre une fois deux à son arrivée, puis se tient immobile.
Idée reprise du « Sonar Grid » de 21st.dev, réécrite sans React ni
dépendance (`trame.js`, `12-trame.css`).

Ce que la v6 a changé, en bref (07/10/2026, « les mêmes couleurs, moins
mort ») : le blanc devient le fond et la chaux passe une section sur
deux ; les chiffres de l'entreprise s'écrivent au rouge du toit ; un
filet rouge coiffe le pied de page ; le chêne sort de la palette, les
marques prennent le rouge écrit.

Ce que la v5 a changé, en bref (audit de design du 07/10/2026) :

- **Palette réchauffée** et second accent, le chêne ; les gris de
  texte foncés (la sérif pâlissait) ; douze neutres ramenés à neuf.
- **Six défauts corrigés** : « facultatif » en rouge, filets coupés
  des fiches de réalisations, légendes illisibles sur photo au
  téléphone, focus invisible sur la poignée du comparateur, enseigne
  du pied rognée, suites à faire glisser coupées par leur cadre.
- **Moins de monotonie** : deux compositions de section qui alternent
  (marge accrochée pour ce qui se lit, en-tête posé dès qu'un bloc
  prend toute la largeur) ; déroulé, limites, contenu du devis et
  méthode des prestations se lisent ouverts ; les vingt questions du
  devis tiennent en un bloc à onglets ; les repères d'angle sont
  réservés à deux blocs.

Ce que la v3 a changé, en bref :

- **Rien ne s'anime au défilement** (05/10/2026) : ni bonshommes, ni
  photos qui se dévoilent, ni chiffres qui défilent. Tout s'affiche
  d'emblée — au téléphone, ces effets laissaient des vides pendant
  qu'on faisait défiler. (Depuis la v6.3, seuls les traits du plan se
  tracent à l'arrivée de leur bloc ; rien de ce qui se lit n'attend.)
- **Photos** : une par prestation, aucune grande photo répétée sur une
  page ; `BRIEF-PHOTOS.md` dit quoi faire photographier.

- **Couverture de l'accueil** : le titre à gauche, le chantier avant /
  après à droite, à la hauteur de l'écran ; deux boutons « Avant » /
  « Après » sous l'image montrent un état entier d'un geste.
- **En-têtes des pages** : comme l'accueil, le texte et quatre repères
  à gauche, un chantier réel à droite.
- **Légendes dans la photo** : le lieu (« Villa de Chailly, Lausanne »),
  puis ce qu'on voit, et « Voir le chantier » vers sa fiche — posés en
  bas de l'image, plus de bande de texte dessous.
- **Fin de page** : un cadre à repères, l'appel et comment nous joindre
  (plus de bandeau de couleur).
- **Plus de numéros qui ne comptent rien** : ni « N° 005 » sur les
  photos des réalisations, ni « 01 … 07 » devant les prestations, qui
  montrent leur photo à la place.

Chaque couleur de texte porte son rapport de contraste en commentaire
dans `00-jetons.css`. Le plancher du site est de 4,5:1 — seuil AA.

## Mobile d'abord

Les feuilles de style décrivent d'abord le téléphone ; tablette et
bureau s'ajoutent par `min-width` (400, 480, 600, 640, 768, 1024, 1280,
1440 px). Sur écran tactile, toute cible fait 44 px de haut au moins ;
l'en-tête reste en haut de l'écran et la barre d'action reste sous
le pouce, collée au bas de l'écran, ses boutons de 46 px posés dans
les marges de la page ; les marges évitent l'encoche (`viewport-fit=cover`). Le site
s'ajoute à l'écran d'accueil avec son icône (`site.webmanifest`).
Vérifié à 320, 360, 390, 414 px, en paysage et sur tablette : aucun
débordement, décalage de mise en page nul, accessibilité et
référencement à 100 dans Lighthouse (mobile).

Au téléphone, une page reste simple à parcourir. L'en-tête (logo,
Appeler, Menu) reste visible pendant toute la lecture, qu'on descende
ou qu'on remonte ; aucune autre barre ne s'accroche en haut de l'écran.

- **Lire la suite** (`lecture.py`, `onglets.js`) : un texte de plusieurs
  paragraphes montre le premier ; le reste vient d'une touche. Tout le
  texte reste dans la page, pour Google comme sans script.
- **Suites à faire glisser** (`.glissiere`) : les déroulés, la méthode
  des prestations, les cartes et les besoins défilent de côté jusqu'au
  bord de l'écran, une rangée de repères sous eux ; les réalisations passent à deux par ligne, les
  références à quatre logos par ligne, les chiffres à leur seul
  intitulé.
- **Pied de page court** : coordonnées en boutons, les trois listes
  repliées sous leur intitulé (`nav.js`).
- **Titres plus marqués** : titres de section à 30 px, chapô à la
  taille du texte, sections plus serrées.
- **La photo dès le premier écran** : sur chaque page, titre, chapô,
  photo, puis l'appel ; réalisations une par ligne ; formulaire en
  français jusqu'au bouton des photos.

Les pages ont raccourci d'un quart à deux cinquièmes à 390 px de
large (accueil 8 874 → 6 704 px, prestations 7 027 → 4 867,
réalisations 9 526 → 5 751, pied de page 1 179 → 708) ; le bureau n'a
pas bougé d'un pixel.

## Comportements

| Fichier | Rôle |
|---|---|
| `nav.js` | liste des prestations (survol, clavier, Échap), menu plein écran (focus piégé), barre d'action mobile, volets du pied de page |
| `motion.js` | année du pied de page ; l'enseigne qui s'allume ; le plan se trace : à l'arrivée de chaque bloc, ses filets, son toit, le plan du Léman (une fois) |
| `onglets.js` | jeux d'onglets des pages de prestation ; marque qui glisse sous l'onglet ouvert et sous le filtre choisi ; au téléphone, referme les dépliants secondaires (`data-replie-telephone`), déplie « Lire la suite », rend les suites à faire glisser accessibles au clavier |
| `comparateur.js` | glissière avant / après (souris, tactile, clavier), boutons « Avant » / « Après » qui montrent un état entier |
| `lumineuse.js` | visionneuse plein écran des réalisations |
| `dossier.js` | filtres des réalisations |
| `formulaire.js` | vérification, prestation pré-cochée, photos (vignettes), touche Entrée « Suivant », envoi vers `envoi.php` |
| `carte.js` | plan du Léman : une commune survolée, sur le plan ou dans la liste, se marque des deux côtés |
| `trame.js` | trame du relevé sous la bande de noir : onde carrée au toucher, deux ondes une seule fois à l'arrivée, onde figée en mouvement réduit |

Tout est neutralisé si le visiteur demande moins de mouvement
(`prefers-reduced-motion`), et le contenu reste lisible sans
JavaScript.

## Aperçu sur GitHub Pages

Chaque push sur `main` met le site en ligne à
`https://wearebrothers-ch.github.io/dsg-renovation/` (aperçu pour le
client ; la page 404 n'y trouve pas ses fichiers, le site étant servi
dans un sous-dossier). `.github/workflows/pages.yml` le publie en un
seul passage, sans jamais couper une mise en ligne commencée ; il
s'active quand la source de Pages est « GitHub Actions » (Settings →
Pages → Source). `.nojekyll` : le dépôt est publié tel quel, sans
Jekyll. Quand GitHub Actions est ralenti (githubstatus.com), une mise
en ligne peut attendre plusieurs minutes : la dernière version passe
quand même, inutile de pousser à nouveau. Quand GitHub n'attribue plus
de machines du tout, lancer la mise en ligne à la main depuis le Mac de
l'agence : Actions → Mise en ligne → Run workflow → machine « mac » (le
Mac doit être enregistré comme machine de déploiement : Settings →
Actions → Runners → New self-hosted runner, macOS ARM64).

## Mise en ligne chez Infomaniak

1. **Images.** Fait le 05/10/2026 : les quinze images sont dans
   `assets/images/` (originaux et variantes WebP 480, 960, 1600 px),
   plus rien n'est demandé à Wix. Si une image Wix est ajoutée au
   générateur, tant que le site Wix existe, relancer :
   ```
   python3 -m pip install Pillow      # facultatif : variantes WebP légères
   python3 outils/rapatrier_images.py
   python3 outils/construire.py
   ```
   puis commiter `assets/images/` et `outils/images_locales.json`. Sans
   cela, les photos disparaîtront avec le site Wix. La politique de
   confidentialité cesse d'elle-même de mentionner Wix une fois toutes
   les images rapatriées.
2. **Envoyer les fichiers** à la racine de l'hébergement : tout le
   dossier peut partir, `.htaccess` rend introuvables `outils/`, `.git/`
   et les `.md`. Ne pas oublier `.htaccess`, fichier caché.
3. **PHP** (Manager Infomaniak) : version 8.0 ou plus, extension
   fileinfo active, `upload_max_filesize` ≥ 8M, `post_max_size` ≥ 21M,
   `max_file_uploads` ≥ 6, `memory_limit` ≥ 128M.
4. **Courriel** : l'adresse `contact@dsg-renov.ch` doit exister (elle
   expédie les demandes) ; SPF (`include:spf.infomaniak.ch`) et DKIM
   actifs sur le domaine. Faire une vraie demande avec une photo et
   vérifier qu'elle n'arrive pas en indésirables.
5. **Anciennes adresses Wix** : relever les URL de l'ancien site et
   compléter la section 5 de `.htaccess` (redirections 301), avant la
   bascule du domaine.
6. **Après la bascule** : vérifier `https://dsg-renov.ch` →
   `https://www.dsg-renov.ch`, puis activer HSTS dans `.htaccess` ;
   déclarer le site dans Google Search Console et Bing Webmaster Tools,
   soumettre `sitemap.xml`.

## À compléter

Les informations qui n'appartiennent qu'au client sont signalées par un
commentaire `CONTENU À VALIDER` ou `À FOURNIR` (une recherche suffit à
les retrouver) et, dans les annexes, par la classe `.a-valider`.

- le numéro IDE de la société, le gérant responsable, l'auteur des
  photos ;
- **les témoignages** : la section est masquée tant que
  `PROVISOIRES = True` dans `outils/confiance.py`. La remplir de vrais
  avis (accord écrit de chaque client), puis passer la valeur à
  `False` ;
- les horaires du bureau (`OUVERTURE`, `FERMETURE` dans
  `donnees_site.py`) ;
- le détail des six chantiers et du chantier à la une (noms, surfaces,
  durées, années) ;
- la fiche Google Business Profile, puis son lien (`ITINERAIRE` dans
  `donnees_site.py`, et l'emplacement réservé sous les témoignages) ;
- la raison sociale de l'hébergeur, à vérifier sur le contrat.

## Documents de travail

`DIRECTION-ARTISTIQUE.md` — direction actuelle. `DA-MOMDESIGN.md` et
`dsg-renov-claude.md` décrivent des états antérieurs du projet : ils
sont conservés pour mémoire mais **ne correspondent plus au site
actuel**, et ne sont pas servis en ligne.

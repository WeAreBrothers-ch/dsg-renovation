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

Le script écrit les pages, `assets/css/site.css` (les dix-neuf feuilles
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
| `rythme.py` | alternance automatique des fonds blanc / bleu pâle |
| `typographie.py` | espaces insécables avant « : ; ? ! » et dans les guillemets |
| `images.py` | remplace les images Wix par leurs copies locales (srcset compris) |
| `rapatrier_images.py` | télécharge les images encore chez Wix — voir « Mise en ligne » |
| `gabarit.py` | tête du document, en-tête, liste des prestations, menu |
| `gabarit_pied.py` | pied de page, barre d'action mobile |
| `gabarit_liens.py` | lien vers l'accueil, liens « Devis gratuit » (prestation pré-cochée) |
| `confiance.py` | déroulé en quatre temps, logos, témoignages (masqués tant qu'ils sont provisoires) |
| `accessibilite.py` | relie chaque section à son titre (lecteurs d'écran) |
| `briques.py`, `briques_bis.py` | couverture, intercalaire, chiffres, renvoi final, cartes, besoins |
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
  prestations, les réponses de la page devis vers les pages qu'elles
  évoquent, chaque prestation vers ses voisines.
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

Palette « Bleu de plan & safran » (26/09/2026), choisie par le client
parmi trois ambiances — tout est décrit dans `DIRECTION-ARTISTIQUE.md`.
Le bleu nuit d'un tirage de plan pour l'encre, le bleu de plan pour les
liens et les repères écrits, le jaune safran pour l'action. Le logo
garde ses propres couleurs. Quatre fonds alternent : blanc, bleu pâle,
une bande bleu nuit par page, et le renvoi final en safran. Des cadres
d'un pixel marqués d'un repère carré à chaque angle, un chevron devant
chaque intitulé, une grotesque (Archivo) pour les titres et une sérif de
lecture (Newsreader) pour les phrases.

Chaque couleur de texte porte son rapport de contraste en commentaire
dans `00-jetons.css`. Le plancher du site est de 4,5:1 — seuil AA.

## Comportements

| Fichier | Rôle |
|---|---|
| `nav.js` | liste des prestations (survol, clavier, Échap), menu plein écran (focus piégé), barre d'action mobile |
| `motion.js` | révélations au défilement ; sans lui, la page s'affiche quand même |
| `onglets.js` | jeux d'onglets des pages de prestation |
| `ouverture.js` | l'image d'ouverture s'élargit au défilement |
| `comparateur.js` | glissière avant / après (souris, tactile, clavier) |
| `lumineuse.js` | visionneuse plein écran des réalisations |
| `dossier.js` | filtres des réalisations |
| `formulaire.js` | vérification, prestation pré-cochée, photos, envoi vers `envoi.php` |

Tout est neutralisé si le visiteur demande moins de mouvement
(`prefers-reduced-motion`), et le contenu reste lisible sans
JavaScript.

## Mise en ligne chez Infomaniak

1. **Images.** Tant que le site Wix existe, lancer une fois :
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

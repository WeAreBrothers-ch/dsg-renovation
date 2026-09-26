"""Le chrome commun à toutes les pages : tête, en-tête, menu, pied.

Les pages du dossier `services/` sont d'un niveau plus bas que celles de
la racine : `base` porte le préfixe à appliquer aux liens et aux
ressources (« » ou « ../ »). Aucun chemin n'est écrit en dur ailleurs.
"""

from donnees_site import (COURRIEL, IMAGE_PARTAGE, IMAGE_PARTAGE_ALT,
                          LOGO_AVIF, LOGO_HAUTEUR, LOGO_LARGEUR, LOGO_WEBP,
                          MARQUE, NAVIGATION, SITE, TELEPHONE, TELEPHONE_BRUT)
from gabarit_liens import accueil, vers_devis
from gabarit_pied import pied  # noqa: F401 — réexporté pour construire.py

# La classe « js » est posée avant le premier rendu, pour que les blocs
# à révéler soient masqués d'emblée, sans clignotement. Si motion.js ne
# s'exécute pas (fichier bloqué, erreur), il ne pose jamais la classe
# « motion » : au chargement complet, on retire alors « js » et tout le
# contenu redevient visible. Une page ne peut plus rester blanche.
SCRIPT_JS = (
    '<script>document.documentElement.className+=" js";'
    'addEventListener("load",function(){var h=document.documentElement;'
    'if(!h.classList.contains("motion")){h.classList.remove("js")}});</script>'
)


def logo(base):
    """Le logo pour fond clair : l'AVIF fourni, le WebP en secours."""
    return (
        '<picture><source type="image/avif" srcset="%s%s">'
        '<img src="%s%s" alt="%s" width="%d" height="%d"></picture>'
        % (base, LOGO_AVIF, base, LOGO_WEBP, MARQUE, LOGO_LARGEUR, LOGO_HAUTEUR)
    )


def tete(page, base, feuille, schemas):
    """En-tête du document : métadonnées, polices, feuille, balisage."""
    jsonld = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % s for s in schemas
    )
    image = page.get("image_og") or (SITE + "/" + IMAGE_PARTAGE)
    image_alt = page.get("image_og_alt") or IMAGE_PARTAGE_ALT
    dimensions = "" if page.get("image_og") else (
        '<meta property="og:image:width" content="1200">\n'
        '<meta property="og:image:height" content="630">\n'
    )
    return f"""<!DOCTYPE html>
<html lang="fr-CH">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['titre']}</title>
<meta name="description" content="{page['description']}">
<link rel="canonical" href="{page['canonique']}">
{page.get('robots', '')}
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{base}favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" href="{base}assets/images/icone-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CH">
<meta property="og:site_name" content="{MARQUE}">
<meta property="og:title" content="{page['titre']}">
<meta property="og:description" content="{page['description']}">
<meta property="og:url" content="{page['canonique']}">
<meta property="og:image" content="{image}">
{dimensions}<meta property="og:image:alt" content="{image_alt}">
<meta name="twitter:card" content="summary_large_image">

<link rel="preload" href="{base}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{base}{feuille}">
{SCRIPT_JS}

{jsonld}
</head>

<body>
<a class="saut" href="#contenu">Aller au contenu principal</a>
"""


def _lien_nav(entree, base, courante):
    """Une entrée de navigation, marquée si c'est la page consultée."""
    marque = ' aria-current="page"' if entree["url"] == courante else ""
    return '<a href="%s%s"%s>%s</a>' % (base, entree["url"], marque, entree["nom"])


def _sous_menu(base, services, courante):
    """Les prestations, une par ligne, sous l'entrée « Prestations »."""
    lignes = "\n            ".join(
        '<li><a href="%sservices/%s.html"%s><span class="sous-menu__n">%s</span>%s</a></li>'
        % (base, s["slug"], ' aria-current="page"'
           if courante == "services/%s.html" % s["slug"] else "",
           s["numero"], s["nom_menu"])
        for s in services
    )
    return f"""<div class="sous-menu" id="sousMenu">
          <ul class="sous-menu__liste">
            {lignes}
          </ul>
          <a class="sous-menu__tout" href="{base}services.html">Toutes nos prestations<span class="fleche" aria-hidden="true"></span></a>
        </div>"""


def entete(base, courante, services):
    """Barre fixe du haut, identique sur toutes les pages.

    Dès 1024 px : la marque, les trois rubriques (« Prestations » ouvre
    la liste des prestations), le téléphone et le devis. En dessous :
    la marque, « Appeler » et « Menu » — le téléphone reste à un geste.
    """
    dans_prestations = courante == "services.html" or courante.startswith("services/")
    marque_prestations = ' aria-current="page"' if dans_prestations else ""
    autres = "\n      ".join(
        _lien_nav(e, base, courante) for e in NAVIGATION
        if e["barre"] and e["url"] != "services.html"
    )
    menu = "\n    ".join(_entree_menu(e, base, services) for e in NAVIGATION)
    return f"""
<header class="entete" id="entete">
  <div class="zone entete__inner">
    <a class="marque" href="{accueil(base)}" aria-label="{MARQUE}, retour à l'accueil">
      {logo(base)}
    </a>

    <nav class="nav" aria-label="Navigation principale">
      <div class="nav__groupe" id="navPrestations">
        <a href="{base}services.html"{marque_prestations}>Prestations</a>
        <button class="nav__deplier" type="button" aria-expanded="false" aria-controls="sousMenu"><span class="visuellement-cache">Afficher la liste des prestations</span></button>
        {_sous_menu(base, services, courante)}
      </div>
      {autres}
    </nav>

    <div class="entete__actions">
      <a class="entete__tel" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
      <a class="btn btn--plein btn--compact" href="{vers_devis(base, courante)}">Devis gratuit<span class="fleche" aria-hidden="true"></span></a>
    </div>

    <a class="entete__appel" href="tel:{TELEPHONE_BRUT}"><span class="entete__combine" aria-hidden="true"></span>Appeler</a>
    <button class="burger" type="button" id="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">Menu</button>
  </div>
</header>

<div class="menu" id="menu" data-ouvert="false" role="dialog" aria-modal="true" aria-label="Menu de navigation">
  <div class="menu__haut">
    <span class="menu__marque">{logo(base)}</span>
    <button class="menu__fermer" type="button" id="menuFermer" aria-label="Fermer le menu">Fermer</button>
  </div>
  <ul class="menu__liste">
    {menu}
  </ul>
  <div class="menu__pied">
    <a class="donnee" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
    <a class="donnee" href="mailto:{COURRIEL}">{COURRIEL}</a>
    <a class="btn btn--plein" href="{vers_devis(base, courante)}">Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
  </div>
</div>
"""


def _entree_menu(entree, base, services):
    """Une ligne du menu plein écran ; les prestations y sont dépliées."""
    lien = '<a href="%s%s">%s</a>' % (base, entree["url"], entree["nom"])
    if entree["url"] != "services.html":
        return "<li>%s</li>" % lien
    sous = "".join(
        '<li><a href="%sservices/%s.html">%s</a></li>' % (base, s["slug"], s["nom_menu"])
        for s in services
    )
    return '<li>%s<ul class="menu__sous">%s</ul></li>' % (lien, sous)


def scripts(base, modules, version):
    """Modules de comportement, chargés en fin de document."""
    return "\n".join(
        '<script src="%sassets/js/%s?v=%s" defer></script>' % (base, m, version(m))
        for m in modules
    ) + "\n</body>\n</html>\n"

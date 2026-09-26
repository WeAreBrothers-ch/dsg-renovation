"""Le chrome commun à toutes les pages : tête, en-tête, menu, pied.

Les pages du dossier `services/` sont d'un niveau plus bas que celles de
la racine : `base` porte le préfixe à appliquer aux liens et aux
ressources (« » ou « ../ »). Aucun chemin n'est écrit en dur ailleurs.
"""

from donnees_site import (COURRIEL, LOGO, MARQUE, NAVIGATION, TELEPHONE,
                          TELEPHONE_BRUT)
from gabarit_liens import vers_devis
from gabarit_pied import pied  # noqa: F401 — réexporté pour construire.py

# Les esperluettes sont échappées : dans un attribut HTML, « &family »
# est une référence d'entité mal formée. Les navigateurs la corrigent,
# les validateurs la signalent.
POLICES = (
    "https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600"
    "&amp;family=Newsreader:opsz,wght@6..72,400"
    "&amp;display=swap"
)


def tete(page, base, feuilles, schemas):
    """En-tête du document : métadonnées, polices, feuilles, balisage."""
    liens = "\n".join(
        '<link rel="stylesheet" href="%sassets/css/%s">' % (base, f)
        for f in feuilles
    )
    jsonld = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % s for s in schemas
    )
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['titre']}</title>
<meta name="description" content="{page['description']}">
<meta name="theme-color" content="#F5F7FA">
<link rel="canonical" href="{page['canonique']}">
<link rel="icon" href="{LOGO}" type="image/png">
<link rel="apple-touch-icon" href="{LOGO}">
{page.get('robots', '')}
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_CH">
<meta property="og:site_name" content="{MARQUE}">
<meta property="og:title" content="{page['titre']}">
<meta property="og:description" content="{page['description']}">
<meta property="og:url" content="{page['canonique']}">
<meta property="og:image" content="{page.get('image_og', LOGO)}">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://static.wixstatic.com" crossorigin>
<link href="{POLICES}" rel="stylesheet">

{liens}

<!-- Marque la présence du JavaScript avant le premier rendu : évite tout clignotement. -->
<script>document.documentElement.className += " js";</script>

{jsonld}
</head>

<body>
<a class="saut" href="#contenu">Aller au contenu principal</a>
"""


def _lien_nav(entree, base, courante):
    """Une entrée de navigation, marquée si c'est la page consultée."""
    marque = ' aria-current="page"' if entree["url"] == courante else ""
    return '<a href="%s%s"%s>%s</a>' % (base, entree["url"], marque, entree["nom"])


def entete(base, courante):
    """Barre fixe du haut, identique sur toutes les pages."""
    barre = "\n      ".join(
        _lien_nav(e, base, courante) for e in NAVIGATION if e["barre"]
    )
    menu = "\n    ".join(
        '<li><a href="%s%s">%s</a></li>' % (base, e["url"], e["nom"])
        for e in NAVIGATION
    )
    return f"""
<header class="entete" id="entete">
  <div class="zone entete__inner">
    <a class="marque" href="{base}index.html" aria-label="{MARQUE}, retour à l'accueil">
      <img src="{LOGO}" alt="{MARQUE}" width="73" height="38">
    </a>

    <nav class="nav" aria-label="Navigation principale">
      {barre}
    </nav>

    <div class="entete__actions">
      <a class="entete__tel" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
      <a class="btn btn--plein btn--compact" href="{vers_devis(base, courante)}">Devis gratuit<span class="fleche" aria-hidden="true"></span></a>
    </div>

    <button class="burger" type="button" id="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">Menu</button>
  </div>
</header>

<div class="menu" id="menu" data-ouvert="false" role="dialog" aria-modal="true" aria-label="Menu de navigation">
  <div class="menu__haut">
    <span class="menu__marque"><img src="{LOGO}" alt="{MARQUE}" width="54" height="28"></span>
    <button class="menu__fermer" type="button" id="menuFermer" aria-label="Fermer le menu">Fermer</button>
  </div>
  <ul class="menu__liste">
    {menu}
  </ul>
  <div class="menu__pied">
    <a class="donnee" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
    <a class="donnee" href="mailto:{COURRIEL}">{COURRIEL}</a>
    <a class="btn btn--plein" href="{base}devis.html">Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
  </div>
</div>
"""


def scripts(base, modules):
    """Modules de comportement, chargés en fin de document."""
    return "\n".join(
        '<script src="%sassets/js/%s" defer></script>' % (base, m) for m in modules
    ) + "\n</body>\n</html>\n"

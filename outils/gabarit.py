"""Le chrome commun à toutes les pages : tête, en-tête, menu, pied.

Les pages du dossier `services/` sont d'un niveau plus bas que celles de
la racine : `base` porte le préfixe à appliquer aux liens et aux
ressources (« » ou « ../ »). Aucun chemin n'est écrit en dur ailleurs.
"""

from donnees_site import (ANNEXES, COURRIEL, LOGO, MARQUE, NAVIGATION, RUE,
                          TELEPHONE, TELEPHONE_BRUT, VILLE, ZONES_PIED)

POLICES = (
    "https://fonts.googleapis.com/css2?family=Archivo:wght@500;800"
    "&family=IBM+Plex+Mono:wght@400;500"
    "&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap"
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
<meta name="theme-color" content="#F7F7F5">
<link rel="canonical" href="{page['canonique']}">
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
        '<li><a href="%s%s"><span class="n">%02d</span>%s</a></li>'
        % (base, e["url"], i + 1, e["nom"])
        for i, e in enumerate(NAVIGATION)
    )
    return f"""
<header class="entete entete--posee" id="entete">
  <div class="zone entete__inner">
    <a class="marque" href="{base}index.html" aria-label="{MARQUE}, retour à l'accueil">
      <img src="{LOGO}" alt="{MARQUE}" width="73" height="38">
    </a>

    <nav class="nav" aria-label="Navigation principale">
      {barre}
    </nav>

    <div class="entete__actions">
      <a class="entete__tel" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
      <a class="btn btn--plein btn--compact" href="{base}devis.html">Devis gratuit</a>
    </div>

    <button class="burger" type="button" id="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">
      <span></span>
    </button>
  </div>
</header>

<div class="menu sur-sombre" id="menu" data-ouvert="false" role="dialog" aria-modal="true" aria-label="Menu de navigation">
  <div class="zone menu__haut" style="padding-inline:0">
    <img src="{LOGO}" alt="{MARQUE}" width="54" height="28">
    <button class="menu__fermer" type="button" id="menuFermer" aria-label="Fermer le menu">&times;</button>
  </div>
  <ul class="menu__liste">
    {menu}
  </ul>
  <div class="menu__pied">
    <a class="donnee" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
    <a class="donnee" href="mailto:{COURRIEL}">{COURRIEL}</a>
    <a class="btn btn--sombre" href="{base}devis.html">Demander un devis gratuit</a>
  </div>
</div>
"""


def pied(base, courante, services):
    """Bordereau de fin : coordonnées, sommaire, services, zones, légal."""
    sommaire = "\n          ".join(
        '<li><a href="%s%s">%s</a></li>' % (base, e["url"], e["nom"])
        for e in NAVIGATION
    )
    lots = "\n          ".join(
        '<li><a href="%sservices/%s.html">%s</a></li>'
        % (base, s["slug"], s["nom_menu"])
        for s in services
    )
    zones = "\n          ".join("<li>%s</li>" % z for z in ZONES_PIED)
    legal = "\n      ".join(
        '<a href="%s%s"%s>%s</a>'
        % (base, a["url"], ' aria-current="page"' if a["url"] == courante else "", a["nom"])
        for a in ANNEXES
    )
    return f"""
<footer class="pied sur-sombre">
  <div class="zone">
    <div class="pied__grille pied__grille--large">
      <div class="pied__marque">
        <img src="{LOGO}" alt="{MARQUE}" width="73" height="38" loading="lazy" decoding="async">
        <address class="donnee">
          <span>{RUE}<br>1012 {VILLE}, Suisse</span>
          <a href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
          <a href="mailto:{COURRIEL}">{COURRIEL}</a>
        </address>
      </div>

      <nav class="pied__col" aria-labelledby="piedNav">
        <h3 id="piedNav">Le site</h3>
        <ul>
          {sommaire}
        </ul>
      </nav>

      <nav class="pied__col" aria-labelledby="piedLots">
        <h3 id="piedLots">Nos prestations</h3>
        <ul>
          {lots}
        </ul>
      </nav>

      <div class="pied__col">
        <h3>Zone d'intervention</h3>
        <ul>
          {zones}
        </ul>
      </div>
    </div>

    <div class="pied__legal">
      <span>© <span class="nb" id="annee">2026</span> {MARQUE} Sàrl — {VILLE}</span>
      <span>Professionnalisme, fiabilité et passion</span>
      {legal}
    </div>
  </div>
  <p class="pied__logotype" aria-hidden="true">{MARQUE}</p>
</footer>

<div class="barre-mobile" id="barreMobile" data-visible="false">
  <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">Appeler</a>
  <a class="btn btn--plein" href="{base}devis.html">Devis gratuit</a>
</div>
"""


def scripts(base, modules):
    """Modules de comportement, chargés en fin de document."""
    return "\n".join(
        '<script src="%sassets/js/%s" defer></script>' % (base, m) for m in modules
    ) + "\n</body>\n</html>\n"

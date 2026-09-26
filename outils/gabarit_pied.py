"""Le pied de page commun : coordonnées, sommaire, prestations, zones.

Séparé du gabarit pour que chaque fichier reste lisible d'une traite.
Le pied porte ce qu'un visiteur cherche en dernier recours avant
d'appeler : l'adresse, les horaires et le chemin jusqu'à l'atelier.
"""

from gabarit_liens import vers_devis
from donnees_site import (ANNEXES, CODE_POSTAL, COURRIEL, HORAIRES,
                          ITINERAIRE, LOGO_HAUTEUR, LOGO_LARGEUR,
                          LOGO_NEGATIF, MARQUE, NAVIGATION, RUE, TELEPHONE,
                          TELEPHONE_BRUT, VILLE, ZONES_PIED)


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
    <div class="pied__grille">
      <div class="pied__marque">
        <img src="{base}{LOGO_NEGATIF}" alt="{MARQUE}" width="{LOGO_LARGEUR}" height="{LOGO_HAUTEUR}" loading="lazy" decoding="async">
        <address class="donnee">
          <span>{RUE}<br>{CODE_POSTAL} {VILLE}, Suisse</span>
          <a href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
          <a href="mailto:{COURRIEL}">{COURRIEL}</a>
        </address>
        <!-- CONTENU À VALIDER : horaires à confirmer avec le client -->
        <p class="donnee pied__horaires">{HORAIRES}</p>
        <a class="pied__itineraire" href="{ITINERAIRE}" target="_blank" rel="noopener">Itinéraire vers l'atelier<span class="visuellement-cache"> (nouvel onglet)</span><span class="fleche" aria-hidden="true"></span></a>
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

<div class="barre-mobile sur-sombre" id="barreMobile" data-visible="false">
  <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">Appeler</a>
  <a class="btn btn--plein" href="{vers_devis(base, courante)}">Devis gratuit<span class="fleche" aria-hidden="true"></span></a>
</div>
"""

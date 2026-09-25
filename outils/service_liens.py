"""Ce qui relie une page de prestation au reste du site.

La zone d'intervention et les lots voisins sont les mêmes blocs d'une
page de métier à l'autre : ils vivent ici pour que page_service.py ne
porte que ce qui est propre à chaque métier.
"""

import briques
import prestations
from donnees_site import COMMUNES


def zone(base):
    """Où nous intervenons : l'atelier, la ville, les communes."""
    villes = "".join("<li>%s</li>" % c for c in COMMUNES)
    return f"""
  <section class="section" aria-labelledby="ou">
    <div class="zone">
{briques.intercalaire("Zone", "Arc lémanique",
                      "Où nous|intervenons")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Notre atelier est à Lausanne, avenue de Béthusy. Nous
          intervenons chaque semaine en ville — des immeubles anciens de
          Sous-Gare et du Vallon aux villas de Chailly et d'Épalinges — et
          dans les communes de l'agglomération, ainsi que sur La Côte, à
          Lavaux et jusqu'à Genève.</p>
          <p>Un chantier proche, c'est une équipe qui arrive à l'heure et
          qui repasse sans compter quand une reprise est nécessaire. C'est
          la raison pour laquelle nous ne nous éloignons pas de l'arc
          lémanique.</p>
          <p><a href="{base}realisations.html">Voir nos chantiers livrés</a>
          dans la région.</p>
        </div>
        <ul class="lots service__villes">{villes}</ul>
      </div>
    </div>
  </section>
"""


def voisins(fiche, base):
    """Le maillage : les pages des lots souvent menés avec celui-ci."""
    fiches = "\n".join(
        f"""        <li>
          <a class="voisin revele" href="{base}services/{slug}.html">
            <span class="voisin__n">{prestations.page(slug)['numero']}</span>
            <span class="voisin__nom">{prestations.page(slug)['nom']}</span>
            <span class="voisin__chev" aria-hidden="true"></span>
          </a>
        </li>"""
        for slug in fiche["lies"]
    )
    return f"""
  <section class="section" aria-labelledby="voisins">
    <div class="zone">
{briques.intercalaire("Autres prestations", "Souvent menées ensemble",
                      "Ce qui va|avec ce lot")}
      <ul class="voisins">
{fiches}
      </ul>
    </div>
  </section>
"""

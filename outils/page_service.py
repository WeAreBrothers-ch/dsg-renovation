"""Le corps d'une page de prestation.

Une page par lot : ce que nous faisons, comment nous procédons, les
repères chiffrés, les questions propres au métier, et les lots voisins.
Le maillage entre services se fait par la section « lots voisins » :
c'est lui qui donne du poids à chaque page auprès des moteurs.
"""

import briques
from donnees_site import COMMUNES


def _prestations(service):
    items = "\n".join("          <li>%s</li>" % p for p in service["prestations"])
    return f"""
  <section class="section" aria-labelledby="quoi">
    <div class="zone">
{briques.intercalaire("N° 01", "Prestations", "Ce que couvre le lot",
                      "Ce que nous|faisons")}
      <div class="service__deux revele">
        <div class="service__texte">
          {"".join('<p>%s</p>' % p for p in service["intro"])}
        </div>
        <ul class="service__liste">
{items}
        </ul>
      </div>
    </div>
  </section>
"""


def _methode(service):
    etapes = "\n".join(
        f"""        <li class="etape revele trace">
          <span class="etape__n">{i + 1:02d}</span>
          <div>
            <h3 class="h4">{titre}</h3>
            <p class="etape__texte">{texte}</p>
          </div>
        </li>"""
        for i, (titre, texte) in enumerate(service["etapes"])
    )
    return f"""
  <section class="section" aria-labelledby="comment">
    <div class="zone">
{briques.intercalaire("N° 02", "Méthode", "Du premier appel à la réception",
                      "Comment nous|procédons")}
      <ol class="etapes">
{etapes}
      </ol>
    </div>
  </section>
"""


def _reperes(service):
    """Quatre repères du lot, dans la chemise du relevé général.

    La chemise porte ici une mention et non un chiffre : le repère d'un
    lot est une durée ou une pratique, pas une quantité à faire défiler.
    """
    cellules = "\n".join(
        f"""        <li class="preuve revele">
          <span class="preuve__onglet etiquette">{nom}</span>
          <p class="preuve__note">{valeur}</p>
        </li>"""
        for nom, valeur in service["reperes"]
    )
    return f"""
  <section class="section section--serre" aria-label="Repères du lot">
    <div class="zone">
      <ul class="preuves preuves--quatre">
{cellules}
      </ul>
    </div>
  </section>
"""


def _zone(service, base):
    villes = "".join("<li>%s</li>" % c for c in COMMUNES)
    return f"""
  <section class="section" aria-labelledby="ou">
    <div class="zone">
{briques.intercalaire("N° 03", "Zone", "Arc lémanique",
                      "Où nous|intervenons")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Notre atelier est à Lausanne, avenue de Béthusy. Nous
          intervenons chaque semaine en ville et dans les communes de
          l'agglomération, ainsi que sur la Côte, à Lavaux et jusqu'à
          Genève.</p>
          <p>Un chantier proche, c'est une équipe qui arrive à l'heure et
          qui repasse sans compter quand une reprise est nécessaire.
          C'est la raison pour laquelle nous ne nous éloignons pas de
          l'arc lémanique.</p>
          <p><a href="{base}realisations.html">Voir nos chantiers
          livrés</a> dans la région.</p>
        </div>
        <ul class="lots service__villes">{villes}</ul>
      </div>
    </div>
  </section>
"""


def _voisins(service, tous, base):
    index = {s["slug"]: s for s in tous}
    fiches = "\n".join(
        f"""        <li>
          <a class="voisin revele trace" href="{base}services/{slug}.html">
            <span class="voisin__n">{index[slug]['numero']}</span>
            <span class="voisin__nom">{index[slug]['nom']}</span>
            <span class="voisin__chev" aria-hidden="true"></span>
          </a>
        </li>"""
        for slug in service["lies"] if slug in index
    )
    return f"""
  <section class="section" aria-labelledby="voisins">
    <div class="zone">
{briques.intercalaire("N° 05", "Lots voisins", "Souvent menés ensemble",
                      "Ce qui va|avec ce lot")}
      <ul class="voisins">
{fiches}
      </ul>
    </div>
  </section>
"""


def corps(service, tous, base):
    """Assemble la page complète d'un lot."""
    questions = f"""
  <section class="section" aria-labelledby="questions">
    <div class="zone">
{briques.intercalaire("N° 04", "Questions", "Sur ce lot précisément",
                      "Ce qu'on nous|demande")}
{briques.questions_liste(service["questions"])}
    </div>
  </section>
"""
    return (
        _prestations(service)
        + _methode(service)
        + _reperes(service)
        + _zone(service, base)
        + questions
        + _voisins(service, tous, base)
        + briques.appel(
            base,
            "Un projet de " + service["nom_menu"].lower() + " ?",
            "Nous nous déplaçons, mesurons et vous remettons un devis "
            "détaillé et gratuit sous 72 heures.",
        )
    )

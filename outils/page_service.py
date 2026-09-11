"""Le corps d'une page de prestation.

Une page peut réunir plusieurs lots — plâtrerie, cloisons et faux
plafonds se posent ensemble. Les prestations et le contenu local sont
alors groupés par lot, chacun sous son propre intitulé : la page reste
lisible, et chaque métier garde ses mots-clés.
"""

import briques
import prestations
from donnees_site import COMMUNES
from lausanne_finitions import LOCAL as LOCAL_FINITIONS
from lausanne_gros_oeuvre import LOCAL as LOCAL_GROS_OEUVRE

LOCAL = dict(LOCAL_GROS_OEUVRE, **LOCAL_FINITIONS)


def _tirage(fiche):
    """Le tirage d'ouverture : une page de métier se montre d'abord."""
    return f"""
  <figure class="tirage revele-img">
    <img src="{fiche['image']}" alt="{fiche['alt']}"
         width="1600" height="900" fetchpriority="high" decoding="async">
    <figcaption class="etiquette tirage__legende">Lausanne &amp; arc lémanique</figcaption>
  </figure>
"""


def _prestations(fiche):
    """Ce que couvre la page : un bloc par lot, texte et liste en regard.

    Sur une page qui réunit plusieurs lots, chacun garde son intitulé,
    son introduction et sa liste : le visiteur venu pour les cloisons
    trouve les cloisons, et chaque métier garde ses mots-clés.
    """
    lots = prestations.lots_de(fiche)
    multiple = len(lots) > 1
    blocs = []
    for lot in lots:
        titre = ('<h3 class="h3 local__titre">%s</h3>' % lot["nom"]) if multiple else ""
        textes = "".join("<p>%s</p>" % t for t in lot["intro"])
        lignes = "\n".join("            <li>%s</li>" % p for p in lot["prestations"])
        blocs.append(f"""      <div class="local revele">
        {titre}
        <div class="service__deux">
          <div class="service__texte">
            {textes}
          </div>
          <ul class="service__liste">
{lignes}
          </ul>
        </div>
      </div>""")
    return f"""
  <section class="section" aria-labelledby="quoi">
    <div class="zone">
{briques.intercalaire("N° 01", "Prestations", "Ce que couvre la page",
                      "Ce que nous|faisons")}
{chr(10).join(blocs)}
    </div>
  </section>
"""


def _methode(fiche):
    etapes = "\n".join(
        f"""        <li class="etape revele trace">
          <span class="etape__n">{i + 1:02d}</span>
          <div>
            <h3 class="h4">{titre}</h3>
            <p class="etape__texte">{texte}</p>
          </div>
        </li>"""
        for i, (titre, texte) in enumerate(prestations.etapes_de(fiche))
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


def _reperes(fiche):
    """Quatre repères de la page, dans la chemise du relevé général."""
    cellules = "\n".join(
        f"""        <li class="preuve revele">
          <span class="preuve__onglet etiquette">{nom}</span>
          <p class="preuve__note">{valeur}</p>
        </li>"""
        for nom, valeur in fiche["reperes"]
    )
    return f"""
  <section class="section section--serre" aria-label="Repères de la prestation">
    <div class="zone">
      <ul class="preuves preuves--quatre">
{cellules}
      </ul>
    </div>
  </section>
"""


def _zone(base):
    villes = "".join("<li>%s</li>" % c for c in COMMUNES)
    return f"""
  <section class="section" aria-labelledby="ou">
    <div class="zone">
{briques.intercalaire("N° 03", "Zone", "Arc lémanique",
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


def _local(fiche):
    """Ce que le bâti lausannois impose, lot par lot."""
    blocs = []
    for rang, slug in enumerate(fiche["lots"]):
        bloc = LOCAL[slug]
        points = "\n".join(
            "            <li>%s</li>" % pt for pt in bloc["encadre"]["points"]
        )
        textes = "".join("<p>%s</p>" % t for t in bloc["paragraphes"])
        titre = ""
        if len(fiche["lots"]) > 1:
            titre = ('<h3 class="h3 local__titre">%s</h3>'
                     % bloc["titre"].replace("|", " "))
        blocs.append(f"""      <div class="local revele">
        {titre}
        <div class="service__deux">
          <div class="service__texte">
            {textes}
          </div>
          <aside class="encadre trace">
            <p class="etiquette encadre__titre">{bloc['encadre']['titre']}</p>
            <ul class="encadre__liste">
{points}
            </ul>
          </aside>
        </div>
      </div>""")
    premier = LOCAL[fiche["lots"][0]]
    titre = (premier["titre"] if len(fiche["lots"]) == 1
             else "Ce que le bâti|lausannois impose")
    cote = (premier["cote"] if len(fiche["lots"]) == 1
            else "Lot par lot")
    return f"""
  <section class="section" aria-labelledby="local">
    <div class="zone">
{briques.intercalaire("N° 04", "Sur le terrain", cote, titre)}
{chr(10).join(blocs)}
    </div>
  </section>
"""


def _voisins(fiche, base):
    fiches = "\n".join(
        f"""        <li>
          <a class="voisin revele trace" href="{base}services/{slug}.html">
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
{briques.intercalaire("N° 06", "Autres prestations", "Souvent menées ensemble",
                      "Ce qui va|avec ce lot")}
      <ul class="voisins">
{fiches}
      </ul>
    </div>
  </section>
"""


def corps(fiche, base):
    """Assemble la page complète d'une prestation."""
    questions = f"""
  <section class="section" aria-labelledby="questions">
    <div class="zone">
{briques.intercalaire("N° 05", "Questions", "Sur cette prestation",
                      "Ce qu'on nous|demande")}
{briques.questions_liste(prestations.questions_de(fiche))}
    </div>
  </section>
"""
    return (
        _tirage(fiche)
        + _prestations(fiche)
        + _methode(fiche)
        + _reperes(fiche)
        + _zone(base)
        + _local(fiche)
        + questions
        + _voisins(fiche, base)
        + briques.appel(
            base,
            "Un projet de " + fiche["nom_menu"].lower() + " ?",
            "Nous nous déplaçons, mesurons et vous remettons un devis "
            "détaillé et gratuit sous 72 heures.",
        )
    )

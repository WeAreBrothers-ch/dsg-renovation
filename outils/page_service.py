"""Le corps d'une page de prestation.

Une page peut réunir plusieurs lots — plâtrerie, cloisons et faux
plafonds se posent ensemble. Les prestations et le contenu local sont
alors groupés par lot, chacun sous son propre intitulé : la page reste
lisible, et chaque métier garde ses mots-clés.
"""

import briques
import prestations
import repli
import service_liens
from ouverture import ouverture
from lausanne_finitions import LOCAL as LOCAL_FINITIONS
from lausanne_gros_oeuvre import LOCAL as LOCAL_GROS_OEUVRE

LOCAL = dict(LOCAL_GROS_OEUVRE, **LOCAL_FINITIONS)


def _tirage(fiche):
    """Le tirage d'ouverture : une page de métier se montre d'abord.

    Il s'affiche d'emblée — c'est l'image principale de la page — puis
    s'élargit au défilement, comme le comparateur de l'accueil.
    """
    image = f"""<img src="{fiche['image']}" alt="{fiche['alt']}"
           width="1600" height="900" fetchpriority="high" decoding="async">"""
    return ouverture(image, "Lausanne &amp; arc lémanique", "tirage") + "\n"


def _prestations(fiche):
    """Ce que couvre la page : un onglet par lot, la liste repliée.

    Trois lots affichés d'un bloc, c'est une vingtaine de lignes de
    puces avant le premier paragraphe utile. Un onglet par lot, et la
    liste des postes derrière une ligne qui s'ouvre : on choisit ce
    qu'on veut lire.
    """
    panneaux = []
    for lot in prestations.lots_de(fiche):
        textes = "".join("<p>%s</p>" % t for t in lot["intro"])
        panneaux.append((lot["nom"], f"""
        <div class="service__texte">
          {textes}
        </div>
        <div class="replis" style="margin-top:var(--sp-6)">
{repli.repli_liste("Le détail des postes", lot["prestations"],
                   "%d postes" % len(lot["prestations"]))}
        </div>"""))
    return f"""
  <section class="section" aria-labelledby="quoi">
    <div class="zone">
{briques.intercalaire("Prestations", "Ce que couvre la page",
                      "Ce que nous|faisons")}
{repli.onglets(panneaux, "Les lots de cette prestation")}
    </div>
  </section>
"""


def _methode(fiche):
    """La méthode, étape par étape, chacune derrière son intitulé."""
    etapes = [(titre, "<p>%s</p>" % texte)
              for titre, texte in prestations.etapes_de(fiche)]
    return f"""
  <section class="section" aria-labelledby="comment">
    <div class="zone">
{briques.intercalaire("Méthode", "Du premier appel à la réception",
                      "Comment nous|procédons")}
{repli.replis(etapes)}
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


def _local(fiche):
    """Ce que le bâti lausannois impose, un onglet par lot."""
    panneaux = []
    for slug in fiche["lots"]:
        bloc = LOCAL[slug]
        points = "\n".join(
            "              <li>%s</li>" % pt for pt in bloc["encadre"]["points"]
        )
        textes = "".join("<p>%s</p>" % t for t in bloc["paragraphes"])
        panneaux.append((bloc["titre"].replace("|", " "), f"""
        <div class="service__deux">
          <div class="service__texte">
            {textes}
          </div>
          <aside class="encadre">
            <p class="etiquette encadre__titre">{bloc['encadre']['titre']}</p>
            <ul class="encadre__liste">
{points}
            </ul>
          </aside>
        </div>"""))
    premier = LOCAL[fiche["lots"][0]]
    seul = len(fiche["lots"]) == 1
    titre = premier["titre"] if seul else "Ce que le bâti|lausannois impose"
    cote = premier["cote"] if seul else "Lot par lot"
    return f"""
  <section class="section" aria-labelledby="local">
    <div class="zone">
{briques.intercalaire("Sur le terrain", cote, titre)}
{repli.onglets(panneaux, "Le bâti lausannois, lot par lot")}
    </div>
  </section>
"""


def corps(fiche, base):
    """Assemble la page complète d'une prestation."""
    questions = f"""
  <section class="section" aria-labelledby="questions">
    <div class="zone">
{briques.intercalaire("Questions", "Sur cette prestation",
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
        + service_liens.zone(base)
        + _local(fiche)
        + questions
        + service_liens.voisins(fiche, base)
        + briques.appel(
            base,
            "Un projet de " + fiche["nom_menu"].lower() + " ?",
            "Nous nous déplaçons, mesurons et vous remettons un devis "
            "détaillé et gratuit 72 heures après la visite.",
        )
    )

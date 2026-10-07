"""Le corps d'une page de prestation.

Une page peut réunir plusieurs lots — plâtrerie, cloisons et faux
plafonds se posent ensemble. Les prestations et le contenu local sont
alors groupés par lot, chacun sous son propre intitulé : la page reste
lisible, et chaque métier garde ses mots-clés.
"""

import briques
import confiance
import prestations
import repli
import service_liens
from lausanne_finitions import LOCAL as LOCAL_FINITIONS
from lausanne_gros_oeuvre import LOCAL as LOCAL_GROS_OEUVRE
from lausanne_solutions import LOCAL as LOCAL_SOLUTIONS

LOCAL = dict(LOCAL_GROS_OEUVRE, **LOCAL_FINITIONS, **LOCAL_SOLUTIONS)


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
{repli.repli_liste("Ce que comprend la prestation", lot["prestations"],
                   "%d postes" % len(lot["prestations"]), ouvert=True)}
        </div>"""))
    return f"""
  <section class="section" aria-labelledby="quoi">
    <div class="zone">
{briques.intercalaire("Prestations", "Ce que couvre la page",
                      prestations.intertitres_de(fiche)["quoi"])}
{repli.onglets(panneaux, "Les travaux de cette page")}
    </div>
  </section>
"""


def _methode(fiche):
    """La méthode, étape par étape, en cases d'un même cadre.

    Les étapes tiennent en une ou deux phrases : elles se lisent d'un
    coup d'œil, comme le déroulé de l'accueil, plutôt qu'en dépliants.
    Cinq étapes prennent leur propre grille (.etapes--cinq) : jamais de
    rangée creuse.
    """
    etapes = [(titre, texte, "") for titre, texte in prestations.etapes_de(fiche)]
    classe = "etapes--cinq" if len(etapes) == 5 else ""
    return f"""
  <section class="section sur-sombre" aria-labelledby="comment">
    <div class="zone">
{briques.intercalaire("Méthode", "Du premier appel à la fin des travaux",
                      prestations.intertitres_de(fiche)["comment"])}
{confiance.etapes("comment", etapes, classe)}
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
    cote = premier["cote"] if seul else "Métier par métier"
    return f"""
  <section class="section" aria-labelledby="local">
    <div class="zone">
{briques.intercalaire("Sur le terrain", cote, titre)}
{repli.onglets(panneaux, "Le bâti lausannois, métier par métier")}
    </div>
  </section>
"""


def corps(fiche, base):
    """Assemble la page complète d'une prestation."""
    questions = f"""
  <section class="section" aria-labelledby="questions">
    <div class="zone">
{briques.intercalaire("Questions", "Ce qu'on nous demande",
                      prestations.intertitres_de(fiche)["questions"])}
{briques.questions_liste(prestations.questions_de(fiche))}
    </div>
  </section>
"""
    return (
        _prestations(fiche)
        + _methode(fiche)
        + service_liens.zone(base, fiche)
        + _local(fiche)
        + questions
        + service_liens.voisins(fiche, base)
        + briques.appel(
            base,
            "Un projet de " + fiche["nom_menu"].lower() + " ?",
            "Nous nous déplaçons, mesurons et vous remettons un devis "
            "détaillé et gratuit 72 heures après la visite.",
            travaux=fiche["slug"],
        )
    )

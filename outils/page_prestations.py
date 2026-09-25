"""Corps de la page pilier des prestations.

Les neuf lots, le besoin auquel chacun répond, l'ordre dans lequel ils
s'enchaînent, et pourquoi les confier à une seule entreprise.
"""

import briques
import briques_bis
import repli
import contenu_divers


def savoir_faire(services, base=""):
    """Page pilier : les neuf lots, leur ordre, et le besoin qu'ils couvrent."""
    return f"""
  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("Les neuf lots", "Une seule entreprise",
                      "Les lots que|nous menons",
                      "Cinq pages pour neuf métiers : ceux qui se posent "
                      "ensemble sur un chantier partagent la leur. Chacune "
                      "dit ce qu'elle couvre, comment nous procédons et ce "
                      "que le bâti lausannois lui impose.")}
{briques.liste_metiers(services, base)}
    </div>
  </section>

  <section class="section" aria-labelledby="tBesoins">
    <div class="zone">
{briques.intercalaire("Par besoin", "Ce qu'on nous dit au téléphone",
                      "Quel lot|pour quel besoin",
                      "Personne n'appelle pour demander « de la plâtrerie ». "
                      "Voici les phrases que nous entendons vraiment, et le "
                      "lot qui y répond.")}
{briques_bis.besoins(contenu_divers.BESOINS, services, base)}
    </div>
  </section>

  <section class="section" aria-labelledby="tOrdre">
    <div class="zone">
{briques.intercalaire("L'ordre", "Pourquoi on ne peint pas en premier",
                      "Dans quel ordre|les lots s'enchaînent",
                      "Un chantier de rénovation ne se compose pas, il se "
                      "séquence. Inverser deux lots, c'est refaire le "
                      "premier.")}
{repli.replis([(titre, "<p>%s</p>" % texte)
                for titre, texte in contenu_divers.ENCHAINEMENT])}
    </div>
  </section>

  <section class="section" aria-labelledby="tPourquoi">
    <div class="zone">
{briques.intercalaire("Le principe", "Pourquoi une seule entreprise",
                      "Neuf lots chez nous,|ou neuf entreprises")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Une rénovation qui passe par neuf entreprises différentes, c'est
          neuf devis à comparer, neuf plannings à faire coïncider et, au
          moindre retard, neuf interlocuteurs qui se renvoient la
          responsabilité.</p>
          <p>Quand le plâtrier, le peintre, le carreleur et le poseur de sol
          appartiennent à la même maison, la question ne se pose pas : le
          fond mal dressé est repris par celui qui l'a fait, et le planning
          se recale en interne.</p>
          <p>C'est aussi ce qui nous permet de vous donner une date de
          livraison, et de la tenir.</p>
        </div>
        <aside class="encadre">
          <p class="etiquette encadre__titre">Ce que vous ne gérez pas</p>
          <ul class="encadre__liste">
            <li>La coordination des corps de métier entre eux.</li>
            <li>Les temps de séchage et leur incidence sur le planning.</li>
            <li>Les reprises entre deux lots, réglées en interne.</li>
            <li>L'évacuation des déchets et le nettoyage final.</li>
          </ul>
        </aside>
      </div>
    </div>
  </section>
""" + briques.appel(
        base,
        "Un lot, ou le chantier entier",
        "Nous intervenons aussi bien sur un seul poste que sur une rénovation "
        "complète. Décrivez votre projet, nous vous disons ce qu'il demande.",
    )

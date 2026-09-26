"""Corps de la page pilier des prestations.

Les prestations, le besoin auquel chacune répond, l'ordre dans lequel
les travaux s'enchaînent, et pourquoi les confier à une seule entreprise.
"""

import briques
import briques_bis
import repli
import contenu_divers


def savoir_faire(services, base=""):
    """Page pilier : les prestations, leur ordre, et le besoin qu'elles couvrent."""
    return f"""
  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("Nos prestations", "Une seule entreprise",
                      "Toutes nos prestations|de rénovation",
                      "Chaque page détaille ce que comprend la prestation, "
                      "comment nous procédons et ce que les immeubles "
                      "lausannois lui imposent.")}
{briques.liste_metiers(services, base)}
    </div>
  </section>

  <section class="section" aria-labelledby="tBesoins">
    <div class="zone">
{briques.intercalaire("Par besoin", "Ce qu'on nous dit au téléphone",
                      "Votre besoin,|la bonne prestation",
                      "Personne n'appelle pour demander « de la plâtrerie ». "
                      "Voici les phrases que nous entendons vraiment, et la "
                      "prestation qui y répond.")}
{briques_bis.besoins(contenu_divers.BESOINS, services, base)}
    </div>
  </section>

  <section class="section sur-sombre" aria-labelledby="tOrdre">
    <div class="zone">
{briques.intercalaire("L'ordre", "Pourquoi on ne peint pas en premier",
                      "Dans quel ordre|se font les travaux",
                      "Un chantier de rénovation ne se compose pas, il se "
                      "séquence. Inverser deux étapes, c'est refaire la "
                      "première.")}
{repli.replis([(titre, "<p>%s</p>" % texte)
                for titre, texte in contenu_divers.ENCHAINEMENT])}
    </div>
  </section>

  <section class="section" aria-labelledby="tPourquoi">
    <div class="zone">
{briques.intercalaire("Le principe", "Pourquoi une seule entreprise",
                      "Une seule entreprise,|ou neuf")}
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
            <li>Les reprises entre deux métiers, réglées en interne.</li>
            <li>L'évacuation des déchets et le nettoyage final.</li>
          </ul>
        </aside>
      </div>
    </div>
  </section>
""" + briques.appel(
        base,
        "Un seul poste, ou le chantier entier",
        "Nous intervenons aussi bien sur un seul poste que sur une rénovation "
        "complète. Décrivez votre projet, nous vous disons ce qu'il demande.",
    )

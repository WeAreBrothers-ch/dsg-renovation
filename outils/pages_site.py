"""Corps des pages entreprise et savoir-faire, et accès aux fragments.

`fragment()` vit ici parce que toutes les pages y puisent : ce sont les
blocs repris tels quels du dossier d'origine.
"""

import io
import os

import briques

DOSSIER = os.path.join(os.path.dirname(__file__), "fragments")


def fragment(nom):
    """Bloc repris tel quel du dossier d'origine."""
    with io.open(os.path.join(DOSSIER, nom + ".html"), encoding="utf-8") as f:
        return f.read()


def entreprise(services, base=""):
    """Qui nous sommes, ce que nous garantissons, comment nous travaillons."""
    engagements = [
        ("Un seul interlocuteur",
         "Un responsable de chantier unique pilote tous les lots, du devis à "
         "la remise des clés. Vous ne coordonnez personne."),
        ("Un planning daté",
         "Le calendrier des corps de métier vous est transmis avant le "
         "démarrage, semaine par semaine, et tenu."),
        ("Des salariés, pas une cascade",
         "Onze professionnels de l'entreprise sur les chantiers. Les mêmes "
         "visages du premier au dernier jour."),
        ("Une réception en règle",
         "Visite contradictoire, liste des réserves, reprise sous dix jours "
         "et nettoyage complet inclus."),
    ]
    cartes = "\n".join(
        f"""        <li class="engagement revele trace">
          <h3 class="h4">{titre}</h3>
          <p class="etape__texte">{texte}</p>
        </li>"""
        for titre, texte in engagements
    )
    return f"""
  <section class="section" aria-labelledby="tHistoire">
    <div class="zone">
{briques.intercalaire("N° 01", "Histoire", "Depuis 2019 à Lausanne",
                      "D'où vient|l'entreprise")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>DSG Rénovation a été fondée en 2019 à Lausanne, sur un
          savoir-faire transmis depuis plus de quarante ans. L'entreprise est
          jeune, le métier ne l'est pas.</p>
          <p>Nous avons choisi de rester une structure à taille humaine, avec
          onze professionnels salariés et un réseau de partenaires de la
          région que nous suivons depuis des années. C'est ce qui nous permet
          de tenir un planning : nous savons qui vient, et quand.</p>
          <p>Nous ne faisons que de la rénovation. Pas de construction neuve,
          pas de promotion. Un logement occupé, un immeuble habité, un
          chantier à mener sans déranger les voisins : c'est notre terrain.</p>
        </div>
{briques.releve_chiffre()}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tEngagements">
    <div class="zone">
{briques.intercalaire("N° 02", "Engagements", "Ce sur quoi nous nous tenons",
                      "Quatre engagements,|tenus par écrit")}
      <ul class="engagements">
{cartes}
      </ul>
    </div>
  </section>

  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("N° 03", "Savoir-faire", "Neuf lots · une seule entreprise",
                      "Ce que nous|savons faire")}
{briques.liste_metiers(services, base)}
    </div>
  </section>
""" + briques.appel(
        base,
        "Parlons de votre projet",
        "Un appel suffit pour savoir si nous sommes la bonne entreprise pour "
        "votre chantier. Nous le disons franchement quand ce n'est pas le cas.",
    )


def savoir_faire(services, base=""):
    """Page pilier : elle porte les neuf lots et renvoie vers chacun."""
    return f"""
  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("N° 01", "Les neuf lots", "Une seule entreprise",
                      "Les lots que|nous menons",
                      "Chaque lot a sa page : ce qu'il couvre, comment nous "
                      "procédons, combien de temps il prend et ce qu'on nous "
                      "demande le plus souvent à son sujet.")}
{briques.liste_metiers(services, base)}
    </div>
  </section>

  <section class="section" aria-labelledby="tPourquoi">
    <div class="zone">
{briques.intercalaire("N° 02", "Le principe", "Pourquoi une seule entreprise",
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
{briques.releve_chiffre()}
      </div>
    </div>
  </section>
""" + briques.appel(
        base,
        "Un lot, ou le chantier entier",
        "Nous intervenons aussi bien sur un seul poste que sur une rénovation "
        "complète. Décrivez votre projet, nous vous disons ce qu'il demande.",
    )

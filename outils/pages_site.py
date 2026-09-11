"""Corps des pages entreprise et savoir-faire, et accès aux fragments.

`fragment()` vit ici parce que toutes les pages y puisent : ce sont les
blocs repris tels quels du dossier d'origine.
"""

import io
import os

import briques
import briques_bis
import contenu_divers
import contenu_entreprise as ce

DOSSIER = os.path.join(os.path.dirname(__file__), "fragments")


def fragment(nom):
    """Bloc repris tel quel du dossier d'origine."""
    with io.open(os.path.join(DOSSIER, nom + ".html"), encoding="utf-8") as f:
        return f.read()


def entreprise(services, base=""):
    """Qui nous sommes, comment se déroule un chantier, nos limites."""
    engagements = "\n".join(
        f"""        <li class="engagement revele trace">
          <h3 class="h4">{titre}</h3>
          <p class="etape__texte">{texte}</p>
        </li>"""
        for titre, texte in ce.ENGAGEMENTS
    )
    return f"""
  <section class="section" aria-labelledby="tHistoire">
    <div class="zone">
{briques.intercalaire("N° 01", "Histoire", "Depuis 2019 à Lausanne",
                      "D'où vient|l'entreprise")}
      <div class="service__deux revele">
        <div class="service__texte">
          {"".join("<p>%s</p>" % p for p in ce.HISTOIRE)}
        </div>
{briques.releve_chiffre()}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tMetier">
    <div class="zone">
{briques.intercalaire("N° 02", "Notre métier", "Rénovation, et rien d'autre",
                      "Le bâti existant,|pas le neuf")}
      <div class="service__texte revele">
        {"".join("<p>%s</p>" % p for p in ce.METIER)}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tDeroule">
    <div class="zone">
{briques.intercalaire("N° 03", "Déroulé", "Du premier appel aux clés",
                      "Comment se déroule|un chantier",
                      "Six temps, dans cet ordre, sur tous nos chantiers — "
                      "qu'il s'agisse d'un seul lot ou d'une rénovation "
                      "complète.")}
{briques_bis.frise(ce.DEROULE)}
    </div>
  </section>

  <section class="section" aria-labelledby="tLimites">
    <div class="zone">
{briques.intercalaire("N° 04", "Nos limites", "Dire non fait partie du métier",
                      "Ce que nous|ne faisons pas",
                      "Une entreprise qui accepte tout finit par mal faire "
                      "quelque chose. Voici où nous nous arrêtons.")}
{briques_bis.limites(ce.LIMITES)}
    </div>
  </section>

  <section class="section" aria-labelledby="tEngagements">
    <div class="zone">
{briques.intercalaire("N° 05", "Engagements", "Ce sur quoi nous nous tenons",
                      "Quatre engagements,|tenus par écrit")}
      <ul class="engagements">
{engagements}
      </ul>
    </div>
  </section>

  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("N° 06", "Savoir-faire", "Neuf lots · une seule entreprise",
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
    """Page pilier : les neuf lots, leur ordre, et le besoin qu'ils couvrent."""
    return f"""
  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("N° 01", "Les neuf lots", "Une seule entreprise",
                      "Les lots que|nous menons",
                      "Chaque lot a sa page : ce qu'il couvre, comment nous "
                      "procédons, combien de temps il prend et ce que le bâti "
                      "lausannois lui impose.")}
{briques.liste_metiers(services, base)}
    </div>
  </section>

  <section class="section" aria-labelledby="tBesoins">
    <div class="zone">
{briques.intercalaire("N° 02", "Par besoin", "Ce qu'on nous dit au téléphone",
                      "Quel lot|pour quel besoin",
                      "Personne n'appelle pour demander « de la plâtrerie ». "
                      "Voici les phrases que nous entendons vraiment, et le "
                      "lot qui y répond.")}
{briques_bis.besoins(contenu_divers.BESOINS, services, base)}
    </div>
  </section>

  <section class="section" aria-labelledby="tOrdre">
    <div class="zone">
{briques.intercalaire("N° 03", "L'ordre", "Pourquoi on ne peint pas en premier",
                      "Dans quel ordre|les lots s'enchaînent",
                      "Un chantier de rénovation ne se compose pas, il se "
                      "séquence. Inverser deux lots, c'est refaire le "
                      "premier.")}
{briques_bis.frise(contenu_divers.ENCHAINEMENT, avec_cote=False)}
    </div>
  </section>

  <section class="section" aria-labelledby="tPourquoi">
    <div class="zone">
{briques.intercalaire("N° 04", "Le principe", "Pourquoi une seule entreprise",
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
        <aside class="encadre trace">
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

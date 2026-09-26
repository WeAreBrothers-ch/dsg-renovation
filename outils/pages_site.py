"""Corps de la page entreprise, et accès aux fragments.

`fragment()` vit ici parce que toutes les pages y puisent : ce sont les
blocs repris tels quels du dossier d'origine.
"""

import io
import os

import briques
import briques_bis
import repli
import confiance
import contenu_divers
import contenu_entreprise as ce

DOSSIER = os.path.join(os.path.dirname(__file__), "fragments")


def fragment(nom):
    """Bloc repris tel quel du dossier d'origine."""
    with io.open(os.path.join(DOSSIER, nom + ".html"), encoding="utf-8") as f:
        return f.read()


def entreprise(services, base=""):
    """Qui nous sommes, comment se déroule un chantier, nos limites."""
    engagements = repli.replis(
        [(titre, "<p>%s</p>" % texte) for titre, texte in ce.ENGAGEMENTS],
        numerote=False,
    )
    return f"""
  <section class="section" aria-labelledby="tHistoire">
    <div class="zone">
{briques.intercalaire("Histoire", "Depuis 2019 à Lausanne",
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
{briques.intercalaire("Notre métier", "Rénovation, et rien d'autre",
                      "Le bâti existant,|pas le neuf")}
      <div class="service__texte revele">
        {"".join("<p>%s</p>" % p for p in ce.METIER)}
      </div>
    </div>
  </section>

  <section class="section sur-sombre" id="deroule" aria-labelledby="tDeroule">
    <div class="zone">
{briques.intercalaire("Déroulé", "Du premier appel aux clés",
                      "Comment se déroule|un chantier",
                      "Six temps, dans cet ordre, sur tous nos chantiers — "
                      "qu'il s'agisse d'un seul lot ou d'une rénovation "
                      "complète.")}
{repli.replis([(titre, "<p>%s</p>" % texte, cote)
                for titre, texte, cote in ce.DEROULE])}
    </div>
  </section>

  <section class="section" aria-labelledby="tLimites">
    <div class="zone">
{briques.intercalaire("Nos limites", "Dire non fait partie du métier",
                      "Ce que nous|ne faisons pas",
                      "Une entreprise qui accepte tout finit par mal faire "
                      "quelque chose. Voici où nous nous arrêtons.")}
{repli.replis([(titre, "<p>%s</p>" % texte)
                for titre, texte in ce.LIMITES], numerote=False)}
    </div>
  </section>

  <section class="section" aria-labelledby="tEngagements">
    <div class="zone">
{briques.intercalaire("Engagements", "Ce sur quoi nous nous tenons",
                      "Quatre engagements,|tenus par écrit")}
{engagements}
    </div>
  </section>

  <section class="partenaires" id="references" aria-labelledby="tPartenaires">
    <div class="zone">
{briques.intercalaire("Références", "Régies, propriétaires et architectes",
                      "Ils nous confient|leurs biens",
                      "Une partie de notre activité vient de clients qui nous "
                      "rappellent. C'est la seule référence qui vaille dans un "
                      "métier où tout se sait vite.")}
      <div class="service__texte revele" style="margin-bottom:var(--sp-7)">
        <p>Les grandes régies de la place lausannoise nous confient des
        remises en état entre deux locations, parfois plusieurs logements du
        même immeuble sur une même année. Ce sont des chantiers courts,
        cadrés par une date de libération, où la fiabilité compte davantage
        que le prix : un logement rendu en retard, c'est un mois de loyer
        perdu pour le propriétaire.</p>
        <p>Les architectes nous confient l'exécution de lots sur descriptif.
        Les propriétaires privés nous appellent le plus souvent après une
        recommandation de voisinage — et repassent pour la pièce suivante
        deux ans plus tard.</p>
      </div>
      {fragment('partenaires')}
    </div>
  </section>

  <section class="section" aria-labelledby="tTemoins">
    <div class="zone">
{briques.intercalaire("Retours", "Ce que disent nos clients",
                      "Trois chantiers,|trois avis")}
{confiance.temoins()}
    </div>
  </section>

  <section class="section" aria-labelledby="tModes">
    <div class="zone">
{briques.intercalaire("Collaborations", "Selon qui commande",
                      "Trois façons|de travailler avec nous",
                      "Une régie, un architecte et un propriétaire n'attendent "
                      "pas la même chose. Nous n'organisons donc pas le "
                      "chantier de la même manière.")}
{briques_bis.cartes(contenu_divers.COLLABORATIONS)}
    </div>
  </section>

  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("Prestations", "Cinq pages, neuf métiers",
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

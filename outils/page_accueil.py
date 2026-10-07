"""Corps de la page d'accueil.

L'accueil ne reprend pas le texte des pages profondes : il en donne
l'accroche et y renvoie. Deux pages qui disent la même chose se
concurrencent dans les résultats de recherche au lieu de s'additionner.
"""

import briques
import carte
import confiance
from donnees_site import COMMUNES
from pages_site import fragment

# La légende, posée dans l'image comme toutes celles du site (briques.vue),
# reprend ce que montrent les deux tirages (voir leurs textes
# alternatifs) : aucune information nouvelle n'est avancée. Les deux
# boutons montrent un état entier d'un geste — au doigt, c'est plus
# sûr qu'une poignée à saisir. Ils attendent le script (comparateur.js
# retire `hidden`) : sans lui, ils ne feraient rien.
LEGENDE_COMPARATEUR = """<figcaption class="legende legende--comparateur">
          <span class="vue__texte">
            <span class="vue__lieu">Appartement Beaulieu</span>
            <span class="vue__quoi">La cuisine ouverte sur le séjour, parquet chêne posé</span>
          </span>
          <span class="bascule" role="group" aria-label="Montrer un état entier" data-bascule hidden>
            <button class="bascule__choix" type="button" data-comparer="100" aria-pressed="false">Avant</button>
            <button class="bascule__choix" type="button" data-comparer="0" aria-pressed="false">Après</button>
          </span>
        </figcaption>"""


def accueil(services, base=""):
    """Page d'accueil : la preuve, les chiffres, les prestations, le déroulé."""
    villes = "".join('<li data-lieu="%s">%s</li>' % (carte.ancre(c), c)
                     for c in COMMUNES)
    return f"""
  <section class="couverture" aria-labelledby="t01">
    <div class="zone grille12 couverture__grille">
      <div class="couverture__texte">
        <p class="intercalaire__nom couverture__nature">Du sol au plafond, tout en maîtrise.</p>
        <h1 id="t01">Entreprise de rénovation à Lausanne</h1>
        <p class="chapo couverture__chapo"><span class="couverture__portee">Rénovation
        totale d'appartements, de maisons et d'immeubles à Lausanne et sur
        l'arc lémanique.</span>
        <span class="couverture__promesse"><span>Un seul interlocuteur,</span>
        <span>tous les corps de métier,</span>
        <span>un chantier livré propre</span>
        <span>et dans les délais.</span></span></p>
        <div class="couverture__actions">
          <a class="btn btn--plein" href="{base}devis.html#formulaire">Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
          <a class="couverture__lien" href="{base}realisations.html">Voir nos réalisations<span class="fleche" aria-hidden="true"></span></a>
        </div>
        <ul class="couverture__garanties">
          <li>Visite et devis <span>gratuits</span></li>
          <li>Devis détaillé <span>72 h après la visite</span></li>
          <li>Sans <span>engagement</span></li>
        </ul>
      </div>
      <figure class="couverture__media">
        <div class="couverture__cadre">
        {fragment('comparateur')}
        </div>
        {LEGENDE_COMPARATEUR}
      </figure>
    </div>

{confiance.bande_references(base)}
  </section>

  <section class="section sur-sombre" aria-labelledby="tEntreprise">
    <div class="zone">
{briques.intercalaire("L'entreprise", "Chiffres à janvier 2026",
                      "Quarante ans de métier,|une équipe lausannoise")}
      <p class="declaration entreprise__intro">Fondée en <span class="nb">2019</span>
      sur un savoir-faire transmis depuis plus de <span class="nb">40</span> ans,
      DSG Rénovation intervient à Lausanne, Genève et sur tout l'arc lémanique.
      Rénover, c'est notre métier — pas une activité parmi d'autres.</p>
{briques.releve_chiffre()}
      <p class="suite"><a href="{base}entreprise.html">Découvrir l'entreprise<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("Prestations", "Tous les corps de métier",
                      "Nos travaux de rénovation,|un seul interlocuteur",
                      "Tous nos travaux sont réalisés par des salariés de "
                      "l'entreprise ou par des partenaires que nous suivons "
                      "depuis des années.")}
{briques.liste_metiers(services, base)}
      <p class="suite"><a href="{base}services.html">Voir toutes nos prestations<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="tChantier">
    <div class="zone">
{briques.intercalaire("Réalisations", "Un chantier récent",
                      "Une rénovation lausannoise,|en détail")}
      {fragment('signature')}
      <p class="suite"><a href="{base}realisations.html">Voir toutes nos réalisations<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="tZone">
    <div class="zone">
{briques.intercalaire("Zone", "Atelier à Lausanne, avenue de Béthusy",
                      "Rénovation à Lausanne|et sur l'arc lémanique",
                      "Nous restons sur l'arc lémanique. Un chantier proche, "
                      "c'est une équipe qui arrive à l'heure et qui repasse "
                      "sans compter quand une reprise est nécessaire.")}
{carte.carte()}
      <div class="service__deux">
        <div class="service__texte">
          <p>À Lausanne, nous travaillons aussi bien dans les immeubles
          anciens de Sous-Gare, de Chauderon et du Vallon que dans les
          logements d'après-guerre de Bellevaux, de Montoie et de Vennes, et
          dans les villas des hauts — Chailly, Épalinges, Le Mont.</p>
          <p>Autour de la ville, nous intervenons chaque semaine à Pully,
          Prilly, Renens, Ecublens et Lutry, ainsi que sur La Côte, à Lavaux
          et jusqu'à Genève.</p>
          <p><a href="{base}realisations.html">Voir les chantiers livrés</a>
          dans la région.</p>
        </div>
        <ul class="lots service__villes">{villes}</ul>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tEtapes">
    <div class="zone">
{briques.intercalaire("Déroulé", "De la demande à la livraison",
                      "Comment se passe|votre demande",
                      "Six temps, les mêmes sur tous nos chantiers. Vous "
                      "savez à chaque étape ce qui vient ensuite, et quand.")}
{confiance.etapes()}
      <p class="suite"><a href="{base}entreprise.html#deroule">Le déroulé complet d'un chantier<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>
""" + briques.appel(
        base,
        "Demandez votre devis gratuit",
        "Décrivez votre projet en une minute. Nous nous déplaçons, mesurons "
        "et vous remettons un devis détaillé et gratuit 72 heures après la "
        "visite.",
    )

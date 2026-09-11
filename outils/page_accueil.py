"""Corps de la page d'accueil.

L'accueil ne reprend pas le texte des pages profondes : il en donne
l'accroche et y renvoie. Deux pages qui disent la même chose se
concurrencent dans les résultats de recherche au lieu de s'additionner.
"""

import briques
from donnees_site import COMMUNES
from pages_site import fragment


def accueil(services, base=""):
    """Page d'accueil : la preuve, les chiffres, les lots, les renvois."""
    villes = "".join("<li>%s</li>" % c for c in COMMUNES)
    return f"""
  <section class="couverture" id="p01" aria-labelledby="t01">
    <div class="zone grille12 couverture__grille">
      <div class="couverture__texte">
        <p class="etiquette">Entreprise de rénovation · Lausanne</p>
        <h1 id="t01">
          <span class="ligne"><span>Du sol</span></span>
          <span class="ligne"><span>au plafond,</span></span>
          <span class="ligne"><span>tout en</span></span>
          <span class="ligne"><span><span class="souligne">maîtrise.</span></span></span>
        </h1>
        <p class="chapo couverture__chapo">Rénovation totale d'appartements, de
        maisons et d'immeubles à Lausanne et sur l'arc lémanique. Un seul
        interlocuteur, tous les corps de métier, un chantier livré propre et
        dans les délais.</p>
        <div class="couverture__actions">
          <a class="btn btn--plein" href="{base}devis.html" data-magnetique>Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
          <a class="btn btn--cadre" href="{base}realisations.html">Voir nos réalisations</a>
        </div>
      </div>

      <div class="couverture__preuve">
      {fragment('comparateur')}
      </div>
    </div>

    <div class="zone couverture__cartouche">
    {fragment('identite')}
    </div>
  </section>

  {fragment('bandeau')}

  <section class="section" aria-labelledby="tEntreprise">
    <div class="zone">
{briques.intercalaire("N° 01", "L'entreprise", "Relevé arrêté en janvier 2026",
                      "Professionnalisme,|fiabilité et passion")}
      <p class="texte entreprise__intro revele">Fondée en <span class="nb">2019</span>
      sur un savoir-faire transmis depuis plus de <span class="nb">40</span> ans,
      DSG Rénovation intervient à Lausanne, Genève et sur tout l'arc lémanique.
      Rénover, c'est notre métier — pas une activité parmi d'autres.</p>
{briques.releve_chiffre()}
      <p class="suite revele"><a href="{base}entreprise.html">Découvrir l'entreprise<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="tLots">
    <div class="zone">
{briques.intercalaire("N° 02", "Savoir-faire", "Neuf lots · une seule entreprise",
                      "Neuf métiers,|un seul chantier",
                      "Tous nos lots sont réalisés par des salariés de "
                      "l'entreprise ou par des partenaires que nous suivons "
                      "depuis des années.")}
{briques.liste_metiers(services, base)}
      <p class="suite revele"><a href="{base}services.html">Voir le détail de chaque lot<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="tChantier">
    <div class="zone">
{briques.intercalaire("N° 03", "Réalisations", "Extrait du registre des chantiers",
                      "Un chantier,|en détail")}
      {fragment('signature')}
      <p class="suite revele"><a href="{base}realisations.html">Voir les six fiches de chantier<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>

  <section class="section" aria-labelledby="tZone">
    <div class="zone">
{briques.intercalaire("N° 04", "Zone", "Atelier à Lausanne, avenue de Béthusy",
                      "Où nous|intervenons",
                      "Nous restons sur l'arc lémanique. Un chantier proche, "
                      "c'est une équipe qui arrive à l'heure et qui repasse "
                      "sans compter quand une reprise est nécessaire.")}
      <div class="service__deux revele">
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

  <section class="partenaires" aria-labelledby="tRef">
    <div class="zone">
{briques.intercalaire("N° 05", "Références", "Régies, propriétaires et architectes",
                      "Ils nous confient|leurs biens")}
      {fragment('partenaires')}
      <p class="suite revele"><a href="{base}references.html">Lire les retours de nos clients<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>
""" + briques.appel(
        base,
        "Ouvrez votre dossier",
        "Décrivez votre projet en une minute. Nous nous déplaçons, mesurons "
        "et vous remettons un devis détaillé et gratuit sous 72 heures.",
    )

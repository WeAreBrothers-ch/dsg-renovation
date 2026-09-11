"""Corps des pages réalisations, références, questions et devis.

Ces quatre pages reprennent les blocs du dossier d'origine, sortis de
la page unique et remis dans leur propre page avec leur en-tête.
"""

import briques
from pages_site import fragment


def realisations(services, base=""):
    """Le registre des chantiers, filtres compris."""
    return f"""
  <section class="section" aria-labelledby="tFiches">
    <div class="zone">
{briques.intercalaire("N° 01", "Registre", "Six chantiers livrés",
                      "Le registre|des chantiers",
                      "Chaque fiche donne le relevé complet du chantier. "
                      "Dépliez-la pour lire le détail des travaux, ou "
                      "agrandissez la vue.")}
      {fragment('filtres')}
      {fragment('chantiers')}
      <p class="chantiers__vide chapo" id="aucunChantier" hidden>Aucune fiche ne correspond à ce filtre pour le moment.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="tSignature">
    <div class="zone">
{briques.intercalaire("N° 02", "Pièce jointe", "Chantier signature",
                      "Six appartements,|en site occupé")}
      {fragment('signature')}
    </div>
  </section>
""" + briques.appel(
        base,
        "Votre chantier, le prochain",
        "Décrivez votre projet : nous vous dirons ce qu'il demande, combien de "
        "temps il prend et ce qu'il coûte.",
    )


def references(services, base=""):
    """Régies, architectes et propriétaires qui nous font travailler."""
    return f"""
  <section class="partenaires" aria-labelledby="tPartenaires">
    <div class="zone">
{briques.intercalaire("N° 01", "Partenaires", "Régies, propriétaires et architectes",
                      "Régies, architectes|et propriétaires")}
      {fragment('partenaires')}
    </div>
  </section>

  <section class="section" aria-labelledby="tTemoins">
    <div class="zone">
{briques.intercalaire("N° 02", "Retours", "Ce que disent nos clients",
                      "Trois chantiers,|trois avis")}
      {fragment('temoins')}
    </div>
  </section>

  <section class="section" aria-labelledby="tRegies">
    <div class="zone">
{briques.intercalaire("N° 03", "Régies", "Remises en état et site occupé",
                      "Travailler avec|une régie")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Les remises en état entre deux locations représentent une part
          importante de notre activité à Lausanne. Elles ont leurs
          contraintes propres : une date de libération ferme, un budget
          arrêté, et un état des lieux qui ne souffre pas l'approximation.</p>
          <p>Nous intervenons appartement par appartement, y compris dans un
          immeuble habité, en libérant les surfaces au fil des relocations.
          Le nettoyage de fin de travaux est compris : le logement est
          reloueable le jour de la réception.</p>
          <p><a href="{base}services/nettoyage-fin-de-chantier.html">Voir le
          lot nettoyage</a> ou <a href="{base}realisations.html">consulter nos
          chantiers d'immeuble</a>.</p>
        </div>
{briques.releve_chiffre()}
      </div>
    </div>
  </section>
""" + briques.appel(
        base,
        "Un parc à entretenir ?",
        "Nous établissons des devis par logement et intervenons au fil des "
        "relocations, avec une date de libération ferme.",
    )


def questions(services, base=""):
    """Les questions qui reviennent avant la signature d'un devis."""
    liens = "\n".join(
        '          <li><a href="%sservices/%s.html">%s</a></li>'
        % (base, s["slug"], s["nom"])
        for s in services
    )
    return f"""
  <section class="section" aria-labelledby="tQuestions">
    <div class="zone">
{briques.intercalaire("N° 01", "Questions", "Avant de signer un devis",
                      "Les six questions|qui reviennent")}
      {fragment('questions')}
    </div>
  </section>

  <section class="section" aria-labelledby="tParLot">
    <div class="zone">
{briques.intercalaire("N° 02", "Par lot", "Questions propres à chaque métier",
                      "Une question|sur un lot précis ?")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Chaque page de prestation porte les questions propres à son
          métier : durée, préparation des supports, compatibilité des
          matériaux, contraintes d'un logement occupé.</p>
          <p>Si votre question n'y figure pas, appelez-nous. Nous répondons
          plus vite au téléphone que par écrit.</p>
        </div>
        <ul class="lots service__villes">
{liens}
        </ul>
      </div>
    </div>
  </section>
""" + briques.appel(
        base,
        "Une question sans réponse ?",
        "Posez-la directement. Un appel de cinq minutes évite souvent une "
        "visite inutile, dans un sens comme dans l'autre.",
    )


def devis(services, base=""):
    """Le bordereau de demande et les coordonnées."""
    return f"""
  <section class="section" aria-labelledby="tDevis">
    <div class="zone">
{briques.intercalaire("N° 01", "Demande", "Réponse sous 72 heures ouvrables",
                      "Le bordereau|de demande",
                      "Décrivez votre projet en une minute. Nous nous "
                      "déplaçons, mesurons et vous remettons un devis détaillé "
                      "et gratuit.")}

      <div class="grille12 demande__grille">
        {fragment('formulaire')}
        {fragment('coordonnees')}
      </div>
    </div>
  </section>
"""

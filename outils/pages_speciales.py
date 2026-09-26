"""Deux pages hors parcours : la page introuvable et le remerciement.

Toutes deux sont en noindex et absentes du plan du site. La page 404
est servie par le serveur à la place de n'importe quelle adresse
inconnue : elle doit donc rattraper le visiteur, avec les prestations
et le téléphone, plutôt que de le laisser repartir vers Google.
"""

import briques
from donnees_site import TELEPHONE, TELEPHONE_BRUT
from gabarit_liens import accueil


def _action_accueil(base):
    return ('<a class="btn btn--plein" href="%s">Retour à l\'accueil'
            '<span class="fleche" aria-hidden="true"></span></a>' % accueil(base))


def introuvable(services, base):
    """404 : l'adresse n'existe pas, voici par où continuer."""
    page = {
        "courante": "404.html",
        "h1": ["Cette page", "n'existe pas"],
        "chapo": "L'adresse a peut-être changé avec le nouveau site. Nos "
                 "prestations, nos réalisations et le formulaire de devis "
                 "sont à un clic.",
    }
    return briques.couverture(page, base, [("Accueil", "/"), ("Page introuvable", "")],
                              _action_accueil(base)) + f"""
  <section class="section" aria-labelledby="tPrestations404">
    <div class="zone">
{briques.intercalaire("Prestations", "Tout ce que nous faisons",
                      "Nos prestations|de rénovation")}
{briques.liste_metiers(services, base)}
      <p class="suite revele"><a href="{base}realisations.html">Voir nos réalisations<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>
"""


def merci(services, base):
    """Après l'envoi du formulaire sans JavaScript : la suite, en clair."""
    page = {
        "courante": "merci.html",
        "h1": ["Merci, votre demande", "est bien partie"],
        "chapo": "Nous vous rappelons pour un premier échange de quelques "
                 "minutes. La visite suit, sous une semaine, et le devis 72 "
                 "heures après la visite.",
    }
    return briques.couverture(page, base, [("Accueil", "/"), ("Demande envoyée", "")],
                              _action_accueil(base)) + f"""
  <section class="section" aria-labelledby="tSuiteMerci">
    <div class="zone">
{briques.intercalaire("En attendant", "Une question urgente ?",
                      "Appelez-nous|directement",
                      "Du lundi au vendredi, nous répondons au "
                      '<a href="tel:%s">%s</a>.' % (TELEPHONE_BRUT, TELEPHONE))}
      <p class="suite revele"><a href="{base}realisations.html">Voir nos réalisations<span class="fleche" aria-hidden="true"></span></a></p>
    </div>
  </section>
"""


# fichier, préfixe des liens, titre, description, corps
PAGES = [
    ("404.html", "/", "Page introuvable — DSG Rénovation",
     "Cette adresse n'existe pas sur le site de DSG Rénovation, entreprise "
     "de rénovation à Lausanne.", introuvable),
    ("merci.html", "", "Demande envoyée — DSG Rénovation",
     "Votre demande de devis est bien partie : nous vous rappelons pour "
     "fixer la visite.", merci),
]

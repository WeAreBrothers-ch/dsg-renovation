"""Liens du chrome qui dépendent de la page consultée, et adresses
publiques des pages."""

import re

from donnees_site import SITE

# Un lien interne vers une page, entre guillemets : relatif (« devis.html »,
# « ../services/peinture.html#zone »), depuis la racine (« /devis.html »)
# ou absolu sur le site (canonique, og:url, balisage structuré).
_LIEN_PAGE = re.compile(
    r"(?<=[\"'])((?:%s/|/|(?:\.\./)+|\./)?(?:[a-z0-9-]+/)*[a-z0-9-]+)\.html(?=[#?\"'])"
    % re.escape(SITE))


def adresse(fichier):
    """Adresse publique d'une page : son fichier sans « .html ».

    « services/peinture.html » se publie à « services/peinture » ; le
    serveur sert le fichier (.htaccess) et renvoie l'ancienne adresse en
    « .html » vers la nouvelle. « index.html » est le dossier lui-même.
    """
    chemin = fichier[:-len(".html")] if fichier.endswith(".html") else fichier
    if chemin == "index" or chemin.endswith("/index"):
        return chemin[:-len("index")]
    return chemin


def adresses_propres(html):
    """Les liens internes d'une page, sans « .html » : une seule adresse
    par page, celle qu'on lit dans la barre du navigateur et chez Google.
    Les commentaires et le texte ne sont pas touchés."""
    return _LIEN_PAGE.sub(lambda m: adresse(m.group(1) + ".html") or "./", html)


def accueil(base):
    """Le lien vers l'accueil : la racine du site, jamais « index.html ».

    L'adresse canonique de l'accueil est « / » : un lien vers
    « index.html » ferait exister deux adresses pour la même page (le
    serveur redirige la seconde, mais chaque redirection coûte un
    aller-retour). « ./ » depuis la racine, « ../ » depuis services/.
    """
    return base or "./"


def vers_devis(base, courante, travaux=None):
    """Le lien d'appel « Devis gratuit » : droit au formulaire.

    Sur la page de devis, l'appel descend au formulaire au lieu de
    recharger la page : un bouton qui renvoie où l'on est déjà est un
    bouton mort. Depuis une page de prestation, `travaux` pré-coche la
    prestation dans le formulaire (assets/js/formulaire.js).
    """
    if courante == "devis.html":
        return "#formulaire"
    requete = "?travaux=%s" % travaux if travaux else ""
    return "%sdevis.html%s#formulaire" % (base, requete)

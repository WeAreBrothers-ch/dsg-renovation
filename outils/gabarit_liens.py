"""Liens du chrome qui dépendent de la page consultée."""


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

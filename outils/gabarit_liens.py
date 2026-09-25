"""Liens du chrome qui dépendent de la page consultée."""


def vers_devis(base, courante):
    """Sur la page de devis, l'appel descend au bordereau au lieu de
    recharger la page : un bouton qui renvoie où l'on est déjà est un
    bouton mort."""
    return "#bordereau" if courante == "devis.html" else base + "devis.html"

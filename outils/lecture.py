"""Lire la suite : au téléphone, un texte long montre son premier paragraphe.

Trois paragraphes de sérif tiennent un écran entier de téléphone, et
une page de prestation en compte une demi-douzaine : on fait défiler du
texte sans voir ce qui suit. Le premier paragraphe dit l'essentiel ; le
reste vient d'une touche, « Lire la suite ».

Le pliage est posé ici, sur la page assemblée, plutôt que dans chaque
gabarit : il vaut pour tout bloc de texte courant (.service__texte) qui
a assez à replier. Le texte reste entier dans la page — Google le lit —
et sans script, ou dès la tablette, il se lit d'un tenant
(17-repli.css, assets/js/onglets.js).
"""

import re

_BLOC = re.compile(r'<div class="[^"]*\bservice__texte\b[^"]*"[^>]*>')
_DIV = re.compile(r"<(/?)div\b")
_PARAGRAPHE = re.compile(r"<p>(.*?)</p>", re.S)
_ENFANT = re.compile(r"<(?!/)(?!a\b|b\b|i\b|em\b|strong\b|span\b|br\b|abbr\b)([a-z0-9]+)\b")

# En deçà, replier ferait gagner deux lignes pour une touche de plus.
SUITE_MINIMALE = 200

BOUTON = ('<button class="plie__bouton" type="button">Lire la suite'
          '<span class="depliant__signe" aria-hidden="true"></span></button>')


def _fin(html, debut):
    """La fin du <div> ouvert à `debut`, <div> imbriqués compris."""
    profondeur, curseur = 0, debut
    while True:
        balise = _DIV.search(html, curseur)
        if balise is None:
            return -1
        profondeur += -1 if balise.group(1) else 1
        curseur = balise.end()
        if profondeur == 0:
            return balise.start()


def _a_replier(interieur):
    """Seulement des paragraphes simples, et assez de texte après le premier."""
    balises = _ENFANT.findall(interieur)
    if len(balises) < 2 or any(b != "p" for b in balises):
        return False
    paragraphes = _PARAGRAPHE.findall(interieur)
    if len(paragraphes) != len(balises):
        return False
    suite = sum(len(re.sub(r"<[^>]+>", "", p)) for p in paragraphes[1:])
    return suite >= SUITE_MINIMALE


def plier(html):
    """Marque les textes à replier et leur ajoute le bouton."""
    morceaux, curseur = [], 0
    for bloc in _BLOC.finditer(html):
        if bloc.start() < curseur:
            continue
        fin = _fin(html, bloc.start())
        if fin == -1 or not _a_replier(html[bloc.end():fin]):
            continue
        ouverture = bloc.group(0)[:-1] + " data-plie>"
        morceaux.append(html[curseur:bloc.start()])
        morceaux.append(ouverture + html[bloc.end():fin].rstrip() + BOUTON + "\n        ")
        curseur = fin
    morceaux.append(html[curseur:])
    return "".join(morceaux)

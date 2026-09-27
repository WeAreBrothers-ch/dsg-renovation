"""Les points d'une suite à faire glisser.

Au téléphone, le déroulé, les cartes et les besoins défilent de côté
(16-composants.css). Sous chaque suite, une rangée de points dit
combien de cases elle compte et laquelle est à l'écran
(assets/js/onglets.js) : on sait qu'il y a une suite, et où l'on en est.

Les points sont posés ici, sur la page assemblée, pour que leur place
soit réservée dès le premier affichage : rien ne bouge quand le script
arrive. Sans script, ou dès 600 px, où les suites reprennent leur
grille, ils n'apparaissent pas.
"""

import re

_SUITE = re.compile(r'<(ol|ul) class="(?:etapes|cartes|besoins)\b[^"]*"[^>]*>')
_LISTE = re.compile(r"<(/?)(ul|ol|li)\b")


def _fin_et_cases(html, debut):
    """La fin de la liste ouverte à `debut` et le nombre de ses cases
    (les <li> de premier niveau : une carte contient sa propre liste)."""
    profondeur, cases = 0, 0
    for balise in _LISTE.finditer(html, debut):
        fermante, nom = balise.group(1), balise.group(2)
        if nom == "li":
            if not fermante and profondeur == 1:
                cases += 1
            continue
        profondeur += -1 if fermante else 1
        if profondeur == 0:
            return html.find(">", balise.end()) + 1, cases
    return -1, 0


def pointer(html):
    """Ajoute sous chaque suite à faire glisser sa rangée de points."""
    morceaux, curseur = [], 0
    for suite in _SUITE.finditer(html):
        if suite.start() < curseur:
            continue
        fin, cases = _fin_et_cases(html, suite.start())
        if fin == -1 or cases < 2:
            continue
        points = '<span class="est-actif"></span>' + "<span></span>" * (cases - 1)
        morceaux.append(html[curseur:fin])
        morceaux.append('\n      <p class="points" aria-hidden="true">%s</p>' % points)
        curseur = fin
    morceaux.append(html[curseur:])
    return "".join(morceaux)

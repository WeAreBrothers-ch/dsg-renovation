"""Relie chaque section à son titre, pour les lecteurs d'écran.

Les sections annoncent leur titre par `aria-labelledby="tXxx"`, mais
l'intercalaire qui porte ce titre ne reçoit pas d'identifiant : la
référence pointait dans le vide, et un lecteur d'écran annonçait des
régions sans nom. Plutôt que d'ajouter un paramètre aux quelque
soixante appels de `intercalaire()`, la correspondance est posée ici,
une fois la page assemblée : le premier titre de niveau 2 sans
identifiant qui suit la section reçoit celui qu'elle attend.
"""

import re

_SECTION = re.compile(r'<section\b[^>]*\baria-labelledby="([^"]+)"[^>]*>')
_TITRE = re.compile(r'<h2(?![^>]*\bid=)([^>]*)>')


def lier_titres(html):
    """Pose sur chaque titre l'identifiant que sa section référence."""
    morceaux = []
    curseur = 0
    for section in _SECTION.finditer(html):
        ident = section.group(1)
        debut = section.end()
        if ('id="%s"' % ident) in html:
            continue
        titre = _TITRE.search(html, debut)
        suivante = html.find("<section", debut)
        if titre is None or (suivante != -1 and titre.start() > suivante):
            continue
        morceaux.append(html[curseur:titre.start()])
        morceaux.append('<h2 id="%s"%s>' % (ident, titre.group(1)))
        curseur = titre.end()
    morceaux.append(html[curseur:])
    return "".join(morceaux)

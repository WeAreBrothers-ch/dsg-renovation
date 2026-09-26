"""Les espaces insécables de la typographie française.

Les textes s'écrivent avec une espace ordinaire avant « : ; ? ! » et
après « « ». À l'affichage, cette espace laisse le navigateur couper la
ligne juste avant le signe, qui se retrouve seul en début de ligne.
Cette passe la remplace par une espace insécable, dans le texte visible
seulement : les balises, leurs attributs, les scripts, le balisage
structuré et les styles ne sont pas touchés.
"""

import re

# Ce qu'il ne faut pas lire comme du texte : commentaires, scripts
# (balisage structuré compris), styles, et toute balise avec ses attributs.
_HORS_TEXTE = re.compile(r"(<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)",
                         re.S | re.I)
_AVANT_SIGNE = re.compile(r"\s+([:;?!»])")
_APRES_GUILLEMET = re.compile(r"«\s+")
INSECABLE = " "


def _texte(fragment):
    fragment = _AVANT_SIGNE.sub(INSECABLE + r"\1", fragment)
    return _APRES_GUILLEMET.sub("«" + INSECABLE, fragment)


def espacer(html):
    """Pose les espaces insécables dans le texte visible d'une page."""
    morceaux = _HORS_TEXTE.split(html)
    # split() avec un groupe : le texte aux rangs pairs, les balises aux impairs.
    return "".join(_texte(m) if i % 2 == 0 else m for i, m in enumerate(morceaux))

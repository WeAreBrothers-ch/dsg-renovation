"""Le rythme des fonds : jamais deux sections de même fond à la suite.

Une page entièrement blanche se lit comme un seul bloc, et le lecteur
ne sait plus où finit une section. Quatre fonds se relaient donc dans
chaque page : blanc, pâle (.sur-pale), sombre (.sur-sombre) et vif
(.sur-vif, le renvoi final). Leurs couleurs sont dans 00-jetons.css.

Les deux derniers sont choisis à la main, dans les gabarits : ce sont
des décisions de mise en page. Les deux premiers se déduisent : une
section sans fond déclaré prend le contraire de celle qui la précède.
Ajouter, retirer ou déplacer une section ne demande donc jamais de
recalculer l'alternance à la main.
"""

import re

_SECTION = re.compile(r'<section class="([^"]*)"')

# Le fond que chaque classe impose, dans l'ordre où on les teste.
_FONDS_IMPOSES = [
    ("sur-vif", "vif"),
    ("sur-sombre", "nuit"),
    ("sur-pale", "pale"),
    ("partenaires", "pale"),   # bande des références : son propre creux
    ("couverture", "blanc"),   # la couverture de l'accueil
]


def _fond_impose(classes):
    for classe, fond in _FONDS_IMPOSES:
        if classe in classes:
            return fond
    return None


def rythmer(html):
    """Pose .sur-pale sur une section sur deux, dans <main> seulement.

    La page commence toujours sur du blanc : la couverture de l'accueil
    et l'en-tête des pages intérieures le sont.
    """
    debut = html.find("<main")
    fin = html.find("</main>")
    if debut == -1 or fin == -1:
        return html
    precedent = ["blanc"]

    def poser(correspondance):
        classes = correspondance.group(1).split()
        impose = _fond_impose(classes)
        if impose:
            precedent[0] = impose
            return correspondance.group(0)
        if "section" not in classes:
            return correspondance.group(0)
        fond = "pale" if precedent[0] == "blanc" else "blanc"
        precedent[0] = fond
        if fond == "pale":
            classes.append("sur-pale")
        return '<section class="%s"' % " ".join(classes)

    corps = _SECTION.sub(poser, html[debut:fin])
    return html[:debut] + corps + html[fin:]

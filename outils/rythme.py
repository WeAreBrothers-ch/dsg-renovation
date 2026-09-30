"""Le rythme des fonds : jamais deux sections de même fond à la suite.

Une page d'un seul fond se lit comme un seul bloc, et le lecteur ne
sait plus où finit une section. Quatre fonds se relaient donc dans
chaque page : le fond de la page (« blanc » ci-dessous : la chaux),
pâle (.sur-pale : le blanc franc), sombre (.sur-sombre, la nuit) et vif
(.sur-vif, la brique du renvoi final). Leurs couleurs sont dans
00-jetons.css.

Les deux derniers sont choisis à la main, dans les gabarits : ce sont
des décisions de mise en page. Les deux premiers se déduisent : une
section sans fond déclaré prend le contraire de celle qui la précède.
Ajouter, retirer ou déplacer une section ne demande donc jamais de
recalculer l'alternance à la main.

Une suite de sections libres qui finirait sur le fond de la section
imposée qui la suit (la bande des références, blanche elle aussi) part
de l'autre fond, quand la section qui la précède le permet : après une
bande sombre, les deux départs se valent.
"""

import re

_SECTION = re.compile(r'<section class="([^"]*)"')

# Le fond que chaque classe impose, dans l'ordre où on les teste.
_FONDS_IMPOSES = [
    ("sur-vif", "vif"),
    ("sur-sombre", "nuit"),
    ("sur-pale", "pale"),
    ("partenaires", "pale"),   # bande des références : le blanc
    ("couverture", "blanc"),   # la couverture de l'accueil
]


def _fond_impose(classes):
    for classe, fond in _FONDS_IMPOSES:
        if classe in classes:
            return fond
    return None


def _autre(fond):
    return "pale" if fond == "blanc" else "blanc"


def _fonds(balises):
    """Le fond de chaque section : imposé par sa classe, laissé au rythme
    (None), ou hors du rythme (les blocs qui ne sont pas des sections)."""
    fonds = []
    for classes in balises:
        impose = _fond_impose(classes)
        fonds.append(impose if impose or "section" in classes else "hors")
    return fonds


def rythmer(html):
    """Pose .sur-pale sur une section sur deux, dans <main> seulement.

    La page commence toujours sur du blanc : la couverture de l'accueil
    et l'en-tête des pages intérieures le sont.
    """
    debut = html.find("<main")
    fin = html.find("</main>")
    if debut == -1 or fin == -1:
        return html
    corps = html[debut:fin]
    trouvees = list(_SECTION.finditer(corps))
    balises = [t.group(1).split() for t in trouvees]
    fonds = _fonds(balises)
    precedent, i = "blanc", 0
    while i < len(fonds):
        if fonds[i] is not None:
            if fonds[i] != "hors":
                precedent = fonds[i]
            i += 1
            continue
        # Une suite de sections libres, jusqu'à la prochaine section imposée.
        suite = []
        while i < len(fonds) and fonds[i] in (None, "hors"):
            if fonds[i] is None:
                suite.append(i)
            i += 1
        suivant = fonds[i] if i < len(fonds) else None
        depart = _autre(precedent)
        dernier = depart if len(suite) % 2 else _autre(depart)
        if dernier == suivant and precedent not in ("blanc", "pale"):
            depart = _autre(depart)
        for rang, j in enumerate(suite):
            fonds[j] = depart if rang % 2 == 0 else _autre(depart)
        precedent = fonds[suite[-1]]
    morceaux, curseur = [], 0
    for trouvee, classes, fond in zip(trouvees, balises, fonds):
        if fond == "pale" and not _fond_impose(classes):
            morceaux.append(corps[curseur:trouvee.start()])
            morceaux.append('<section class="%s"' % " ".join(classes + ["sur-pale"]))
            curseur = trouvee.end()
    morceaux.append(corps[curseur:])
    return html[:debut] + "".join(morceaux) + html[fin:]

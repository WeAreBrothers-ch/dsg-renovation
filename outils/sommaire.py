"""Le sommaire de page, au téléphone et sur tablette.

Une page longue se lit mal au pouce : on ne sait ni ce qu'elle
contient, ni où l'on en est, et l'on fait défiler jusqu'à tomber sur
ce qu'on cherche. Sous l'en-tête de la page, une rangée de cases
reprend donc l'intitulé de chaque section (celui de sa marge) ; elle
reste en haut de l'écran pendant la lecture, la section en cours y est
marquée, et chaque case mène droit à sa section (assets/js/nav.js).

Le sommaire se déduit de la page assemblée : ajouter, retirer ou
renommer une section le met à jour sans rien toucher ici. Sur grand
écran, la marge de chaque section joue déjà ce rôle : il n'y paraît
pas (05-navigation.css).
"""

import re
import unicodedata

_SECTION = re.compile(r"<section\b[^>]*>")
_NOM = re.compile(r'<p class="intercalaire__nom[^"]*">(.*?)</p>', re.S)
_TITRE = re.compile(r"<h2\b([^>]*)>")
_ID = re.compile(r'\bid="([^"]+)"')
_GRILLE_COUVERTURE = re.compile(r'<div class="[^"]*\bcouverture__grille\b[^"]*"[^>]*>')
_OUVERTURE = re.compile(r'<figure class="ouverture\b[^"]*"[^>]*>')

# Les sections qui n'ont pas leur case : la couverture de l'accueil,
# la bande de chiffres sans titre, et l'appel final, que la barre
# d'action du bas d'écran fait déjà.
_HORS_SOMMAIRE = ("couverture", "rappel", "section--serre")

# En deçà, la page se parcourt d'un coup d'œil : pas de sommaire.
MINIMUM = 3


def _classes(balise):
    trouvee = re.search(r'class="([^"]*)"', balise)
    return trouvee.group(1).split() if trouvee else []


def _ancre(libelle, prises):
    """Un identifiant lisible et libre, tiré de l'intitulé."""
    ascii_ = unicodedata.normalize("NFKD", libelle).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-z0-9]+", "-", ascii_.lower()).strip("-") or "section"
    ident, rang = base, 2
    while ident in prises:
        ident, rang = "%s-%d" % (base, rang), rang + 1
    return ident


def _fin_de_bloc(corps, debut, nom="section"):
    """La fin (après la balise fermante) de l'élément `nom` ouvert à
    `debut`, éléments de même nom imbriqués compris."""
    profondeur, curseur = 0, debut
    balise = re.compile(r"<(/?)%s\b" % nom)
    while True:
        trouvee = balise.search(corps, curseur)
        if trouvee is None:
            return len(corps)
        profondeur += -1 if trouvee.group(1) else 1
        curseur = trouvee.end()
        if profondeur == 0:
            return corps.find(">", curseur) + 1


def _entrees(corps, prises):
    """Les cases du sommaire, et le corps où chaque titre visé a un id."""
    sections = list(_SECTION.finditer(corps))
    entrees, morceaux, curseur = [], [], 0
    for rang, section in enumerate(sections):
        if any(c in _classes(section.group(0)) for c in _HORS_SOMMAIRE):
            continue
        limite = sections[rang + 1].start() if rang + 1 < len(sections) else len(corps)
        nom = _NOM.search(corps, section.end(), limite)
        titre = _TITRE.search(corps, section.end(), limite)
        if nom is None or titre is None:
            continue
        libelle = re.sub(r"<[^>]+>", "", nom.group(1)).strip()
        ident = _ID.search(titre.group(1))
        if ident:
            ident = ident.group(1)
        else:
            # Section nommée par aria-label : son titre n'a pas d'id.
            ident = _ancre(libelle, prises)
            prises.add(ident)
            morceaux.append(corps[curseur:titre.start()])
            morceaux.append('<h2 id="%s"%s>' % (ident, titre.group(1)))
            curseur = titre.end()
        entrees.append((libelle, ident))
    morceaux.append(corps[curseur:])
    return entrees, "".join(morceaux)


def _placer(corps, sommaire):
    """Pose le sommaire juste sous l'en-tête de la page, dès le premier
    écran : sous l'en-tête des pages intérieures ; à l'accueil, sous la
    couverture (texte, image avant / après, appel), avant les
    références. Il doit rester un enfant de <main> pour coller en haut
    de l'écran jusqu'au bout de la page : la couverture est donc coupée
    après son image, et sa suite (cartouche, références) passe dans un
    simple bloc, sans rien changer à l'écran large."""
    premiere = _SECTION.search(corps)
    if premiere and "couverture" in _classes(premiere.group(0)):
        fin = _fin_de_bloc(corps, premiere.start())
        image = _OUVERTURE.search(corps, premiere.end(), fin)
        grille = _GRILLE_COUVERTURE.search(corps, premiere.end(), fin)
        if image:
            coupe = _fin_de_bloc(corps, image.start(), "figure")
        elif grille:
            coupe = _fin_de_bloc(corps, grille.start(), "div")
        else:
            return corps[:fin] + sommaire + corps[fin:]
        fermeture = corps.rfind("</section>", coupe, fin)
        return (corps[:coupe] + "\n  </section>" + sommaire
                + '  <div class="couverture__suite">'
                + corps[coupe:fermeture] + "</div>"
                + corps[fermeture + len("</section>"):])
    fin_entete = corps.find("</header>")
    if fin_entete != -1 and (premiere is None or fin_entete < premiere.start()):
        place = fin_entete + len("</header>")
    elif premiere:
        place = premiere.start()
    else:
        return corps
    return corps[:place] + sommaire + corps[place:]


def poser(html):
    """Insère le sommaire dans <main>, s'il a assez de cases."""
    debut = html.find("<main")
    fin = html.find("</main>")
    if debut == -1 or fin == -1:
        return html
    prises = set(_ID.findall(html))
    entrees, corps = _entrees(html[debut:fin], prises)
    if len(entrees) < MINIMUM:
        return html
    cases = "\n".join(
        '    <li><a href="#%s">%s</a></li>' % (ident, libelle)
        for libelle, ident in entrees
    )
    sommaire = (
        '\n<nav class="sommaire" aria-label="Sur cette page" data-sommaire>\n'
        '  <ul class="sommaire__liste">\n%s\n  </ul>\n</nav>\n' % cases
    )
    return html[:debut] + _placer(corps, sommaire) + html[fin:]

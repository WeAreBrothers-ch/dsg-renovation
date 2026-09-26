"""Les ouvriers du site : des silhouettes pleines, posées çà et là.

Un charpentier cloue une planche sur un tréteau, un poseur de sol pose
des carreaux, un électricien visse une ampoule, un peintre passe un mur
au rouleau. Chacun vit seul dans le bas d'une section, sur la limite
avec la suivante, qui lui sert de sol, et travaille à son rythme : il
arrive en marchant, travaille, repart, revient (assets/js/equipe.js).
Quatre sur l'accueil, deux ou trois sur les autres pages, aucun sur
les pages légales.

Le style : une silhouette pleine, grosse tête ronde, membres épais aux
bouts arrondis, sans casque ; l'encre du fond où elle se trouve.

Ce fichier écrit le dessin immobile. Sans script, ou pour un visiteur
qui demande moins de mouvement, chaque ouvrier reste saisi au milieu de
sa tâche. Cette image est celle que calcule le script
(equipe_immobile.json : la rotation de chaque articulation, l'état de
chaque accessoire). Après une retouche des gestes dans equipe.js, la
relever : ouvrir l'accueil avec « prefers-reduced-motion: reduce »
(outils de développement > Rendu), coller RELEVE dans la console, puis
coller le presse-papiers dans equipe_immobile.json.

Repères d'un ouvrier (unités du dessin) : pieds au sol en (0, 0),
hanche à -36, épaules à -60, tête centrée à -75.
"""

import io
import json
import os
import re

# Relevé de l'image immobile, à coller dans la console du navigateur.
RELEVE = """copy(JSON.stringify(Object.fromEntries([...document.querySelectorAll("svg[data-metier]")]
.map(s => [s.dataset.metier, {os: Object.fromEntries([...s.querySelectorAll("[data-os]")]
.map(e => [e.dataset.os, e.getAttribute("transform")])), accessoires: Object.fromEntries(
[...s.querySelectorAll("[data-accessoire]")].map(e => [e.dataset.accessoire, Object.fromEntries(
[...e.attributes].filter(a => /^(transform|opacity|width|x|y|x1|y1|x2|y2)$/.test(a.name)
|| a.name === "class" && a.value.includes("est-allume")).map(a => [a.name, a.value]))]))}])), null, 1))"""

# L'accueil, placé à la main : la section (son titre), le métier, la
# place dans la largeur, et le sens de la marche. Un ouvrier sur deux
# vient de la droite, pour qu'aucun ne suive le précédent.
ACCUEIL = [
    ("tEntreprise", "peinture", 70, "gauche"),
    ("tLots", "sol", 18, "droite"),
    ("tZone", "ampoule", 80, "gauche"),
    ("tEtapes", "marteau", 24, "droite"),
]

# Ailleurs, une section sur deux (trois ouvriers au plus), le métier de
# la page d'abord.
METIERS = ["peinture", "sol", "ampoule", "marteau"]
PREFERES = {
    "services/peinture.html": ["peinture", "ampoule", "marteau"],
    "services/carrelage-sols.html": ["sol", "marteau", "peinture"],
    "services/platrerie-cloisons.html": ["marteau", "peinture", "ampoule"],
    "services/renovation-salle-de-bains.html": ["sol", "ampoule", "peinture"],
    "services/remise-en-etat-appartement.html": ["peinture", "sol", "marteau"],
    "services/nettoyage-fin-de-chantier.html": ["sol", "peinture", "ampoule"],
    "services/renovation-complete.html": ["marteau", "ampoule", "sol"],
}
PLACES = [(22, "droite"), (76, "gauche"), (30, "droite")]
SANS_OUVRIERS = ("mentions-legales.html", "confidentialite.html")

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipe_immobile.json"),
             encoding="utf-8") as _f:
    IMMOBILE = json.load(_f)

# Le marteau prolonge l'avant-bras : manche jusqu'à -22, tête en travers.
MARTEAU = ('<g class="equipe__outil"><line x1="0" y1="-33" x2="0" y2="-22"/>'
           '<rect x="-6.5" y="-23" width="13" height="7" rx="2"/></g>')


# Ce que le script fait varier sur chaque accessoire : seuls ces
# attributs viennent de l'image immobile, le reste est du dessin fixe.
ANIMES = {
    "clou": ("transform",), "impact": ("opacity",), "carreau-main": ("transform", "opacity"),
    "ampoule": ("transform",), "halo": ("opacity",), "peinture": ("width",),
    "perche": ("x1", "y1", "x2", "y2", "opacity"), "rouleau": ("x", "y", "opacity"),
}


def _attributs(metier, nom, **defauts):
    """Les attributs d'un accessoire dans l'image immobile."""
    valeurs = dict(defauts)
    releve = IMMOBILE.get(metier, {}).get("accessoires", {}).get(nom, {})
    animes = ANIMES.get(nom, ("opacity",) if nom.startswith("carreau-") else ())
    valeurs.update({cle: v for cle, v in releve.items() if cle in animes})
    return "".join(' %s="%s"' % (cle, valeur) for cle, valeur in valeurs.items())


def _ouvrier(metier, outil_av=""):
    """Une silhouette : bassin, jambes, torse, tête, bras."""
    os_ = IMMOBILE.get(metier, {}).get("os", {})

    def t(nom):
        return os_.get(nom, "rotate(0)")

    def jambe(cote):
        return (
            f'<g data-os="cuisse-{cote}" transform="{t("cuisse-" + cote)}">'
            f'<line x1="0" y1="-36" x2="0" y2="-18"/>'
            f'<g data-os="tibia-{cote}" transform="{t("tibia-" + cote)}">'
            f'<line x1="0" y1="-18" x2="0" y2="0"/></g></g>'
        )

    def bras(cote, outil):
        return (
            f'<g data-os="bras-{cote}" transform="{t("bras-" + cote)}">'
            f'<line x1="0" y1="-60" x2="0" y2="-46"/>'
            f'<g data-os="avant-bras-{cote}" transform="{t("avant-bras-" + cote)}">'
            f'<line x1="0" y1="-46" x2="0" y2="-33"/>{outil}</g></g>'
        )

    return (
        f'<g data-os="marcheur" transform="{t("marcheur")}">'
        f'<g data-os="bassin" transform="{t("bassin")}">'
        f'<g class="equipe__corps">'
        f'{jambe("arr")}'
        f'<g data-os="torse" transform="{t("torse")}">'
        f'{bras("arr", "")}'
        f'<line x1="0" y1="-36" x2="0" y2="-64"/>'
        f'<circle cx="0" cy="-75" r="11"/>'
        f'{bras("av", outil_av)}'
        f'</g>'
        f'{jambe("av")}'
        f'</g></g></g>'
    )


def _accessoires(metier):
    """Ce qui reste au poste : tréteau, carreaux, ampoule, mur."""
    a = lambda nom, **d: _attributs(metier, nom, **d)
    if metier == "marteau":
        return (
            '<g class="equipe__decor"><rect x="10" y="-31" width="44" height="5" rx="1"/>'
            '<path d="M16 -26 11 0M16 -26 21 0M48 -26 43 0M48 -26 53 0"/></g>'
            f'<g class="equipe__clou" data-accessoire="clou"{a("clou")}>'
            '<path d="M27 -31V-38.5M24 -38.5h6"/></g>'
            f'<g class="equipe__impact" data-accessoire="impact"{a("impact", opacity="0")}>'
            '<path d="M18 -44l-4 -3M36 -44l4 -3M27 -48v-4"/></g>'
        )
    if metier == "sol":
        carreaux = "".join(
            '<rect class="equipe__carreau" data-accessoire="carreau-%d"%s/>'
            % (i, a("carreau-%d" % i, x=x, y="-4.5", width="16", height="4.5"))
            for i, x in enumerate((16, 32, 48))
        )
        return f'<g>{carreaux}</g>'
    if metier == "ampoule":
        rayons = "".join(
            '<line x1="0" y1="-11" x2="0" y2="-16" transform="rotate(%d)"/>' % angle
            for angle in range(0, 360, 45)
        )
        verre = IMMOBILE.get(metier, {}).get("accessoires", {}).get("verre", {}).get("class", "equipe__ampoule")
        return (
            '<g class="equipe__decor"><line x1="20" y1="-106" x2="20" y2="-96"/>'
            '<rect x="16" y="-97" width="8" height="6" rx="1"/></g>'
            f'<g class="equipe__halo" data-accessoire="halo"{a("halo", opacity="0")}>'
            f'<g transform="translate(20 -84)">{rayons}</g></g>'
            f'<g data-accessoire="ampoule"{a("ampoule")}>'
            f'<circle class="{verre}" data-accessoire="verre" cx="20" cy="-84" r="7"/></g>'
        )
    if metier == "peinture":
        return (
            f'<rect class="equipe__peinture" data-accessoire="peinture"{a("peinture", x="16", y="-82", width="0", height="82")}/>'
            '<rect class="equipe__mur" x="16" y="-82" width="68" height="82"/>'
            f'<line class="equipe__perche" data-accessoire="perche"{a("perche")}/>'
            f'<rect class="equipe__rouleau" data-accessoire="rouleau"{a("rouleau", width="6", height="16", rx="3")}/>'
        )
    return ""


def scene(metier, place, sens):
    """Un ouvrier, posé dans le bas d'une section."""
    outil = MARTEAU if metier == "marteau" else ""
    if metier == "sol":
        outil = ('<rect class="equipe__carreau" data-accessoire="carreau-main"%s/>'
                 % _attributs(metier, "carreau-main", x="-8", y="-30", width="16", height="4.5"))
    return (
        f'<div class="ouvrier ouvrier--{sens}" data-ouvrier aria-hidden="true">'
        f'<div class="zone ouvrier__zone"><div class="ouvrier__poste" style="--place:{place}%">'
        f'<svg class="equipe__dessin" data-metier="{metier}" viewBox="-40 -128 120 132" '
        f'focusable="false">{_accessoires(metier)}{_ouvrier(metier, outil)}</svg>'
        f'</div></div></div>'
    )


def _fond(classes):
    for fond in ("sur-sombre", "sur-pale", "sur-vif", "partenaires"):
        if fond in classes:
            return fond
    return "blanc"


def _sections(html):
    """Les titres des sections qui peuvent accueillir un ouvrier : pas
    le renvoi final, ni les sections resserrées, ni une section suivie
    d'une autre du même fond, où la limite qui lui sert de sol ne se
    verrait pas."""
    balises = []
    for balise in re.findall(r"<section\b[^>]*>", html):
        classes = re.search(r'class="([^"]*)"', balise)
        titre = re.search(r'aria-labelledby="([^"]*)"', balise)
        balises.append((set(classes.group(1).split()) if classes else set(),
                        titre.group(1) if titre else None))
    titres = []
    for i, (c, titre) in enumerate(balises):
        suivante = balises[i + 1][0] if i + 1 < len(balises) else {"sur-sombre"}
        if (titre and "section" in c and not c & {"rappel", "sur-vif", "section--serre"}
                and _fond(c) != _fond(suivante)):
            titres.append(titre)
    return titres


def _scenes(html, fichier):
    if fichier == "index.html":
        return ACCUEIL
    titres = _sections(html)
    retenus = titres[1::2][:len(PLACES)] or titres[:1]
    ordre = PREFERES.get(fichier)
    if not ordre:
        # Un ordre propre à chaque page, stable d'une construction à l'autre.
        decalage = sum(map(ord, fichier)) % len(METIERS)
        ordre = METIERS[decalage:] + METIERS[:decalage]
    return [(titre, ordre[i % len(ordre)], PLACES[i][0], PLACES[i][1])
            for i, titre in enumerate(retenus)]


def poser(html, fichier):
    """Pose les ouvriers d'une page dans leurs sections."""
    if fichier in SANS_OUVRIERS:
        return html
    for titre, metier, place, sens in _scenes(html, fichier):
        ouverture = re.search(r'<section\b[^>]*\baria-labelledby="%s"[^>]*>' % re.escape(titre), html)
        if ouverture:
            html = html[:ouverture.end()] + scene(metier, place, sens) + html[ouverture.end():]
    return html

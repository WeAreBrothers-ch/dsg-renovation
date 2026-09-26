"""La frise de l'accueil : quatre ouvriers au travail, dessinés au trait.

Un charpentier cloue une planche sur un tréteau, un poseur de sol pose
des carreaux, un électricien visse une ampoule, un peintre passe un mur
au rouleau. Chacun arrive à son poste en marchant, travaille, puis
repart : le mouvement est calculé par assets/js/equipe.js.

Ce fichier écrit le dessin immobile. Sans script, ou pour un visiteur
qui demande moins de mouvement, la frise reste une illustration :
chacun saisi au milieu de sa tâche. Cette image est celle que calcule
le script (equipe_immobile.json : la rotation de chaque articulation,
l'état de chaque accessoire). Après une retouche des gestes dans
equipe.js, la relever : ouvrir l'accueil avec « prefers-reduced-motion:
reduce » (outils de développement > Rendu), coller RELEVE dans la
console, puis coller le presse-papiers dans equipe_immobile.json.

Repères d'un ouvrier (unités du dessin) : pieds au sol en (0, 0),
hanche à -36, épaules à -60, tête centrée à -72.5.
"""

import io
import json
import os

# Relevé de l'image immobile, à coller dans la console du navigateur.
RELEVE = """copy(JSON.stringify(Object.fromEntries([...document.querySelectorAll("svg[data-metier]")]
.map(s => [s.dataset.metier, {os: Object.fromEntries([...s.querySelectorAll("[data-os]")]
.map(e => [e.dataset.os, e.getAttribute("transform")])), accessoires: Object.fromEntries(
[...s.querySelectorAll("[data-accessoire]")].map(e => [e.dataset.accessoire, Object.fromEntries(
[...e.attributes].filter(a => /^(transform|opacity|width|x|y|x1|y1|x2|y2)$/.test(a.name)
|| a.name === "class" && a.value.includes("est-allume")).map(a => [a.name, a.value]))]))}])), null, 1))"""

# Ordre de gauche à droite, et place de chaque poste dans la largeur.
POSTES = [("marteau", 12), ("sol", 36), ("ampoule", 60), ("peinture", 82)]

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipe_immobile.json"),
             encoding="utf-8") as _f:
    IMMOBILE = json.load(_f)


# Le marteau prolonge l'avant-bras : manche jusqu'à -23.5, tête en travers.
MARTEAU = ('<g class="equipe__outil"><line x1="0" y1="-33" x2="0" y2="-23.5"/>'
           '<rect x="-4.5" y="-23.5" width="9" height="5" rx="1"/></g>')


def _attributs(metier, nom, **defauts):
    """Les attributs d'un accessoire dans l'image immobile."""
    valeurs = dict(defauts)
    valeurs.update(IMMOBILE[metier]["accessoires"].get(nom, {}))
    return "".join(' %s="%s"' % (cle, valeur) for cle, valeur in valeurs.items())


def _ouvrier(metier, outil_av=""):
    """Un ouvrier : bassin, jambes, torse, tête casquée, bras."""
    os = IMMOBILE[metier]["os"]

    def jambe(cote):
        return (
            f'<g data-os="cuisse-{cote}" transform="{os["cuisse-" + cote]}">'
            f'<line x1="0" y1="-36" x2="0" y2="-18"/>'
            f'<g data-os="tibia-{cote}" transform="{os["tibia-" + cote]}">'
            f'<line x1="0" y1="-18" x2="0" y2="0"/>'
            f'<g data-os="pied-{cote}" transform="{os["pied-" + cote]}">'
            f'<line x1="0" y1="0" x2="4" y2="0"/></g></g></g>'
        )

    def bras(cote, outil):
        return (
            f'<g data-os="bras-{cote}" transform="{os["bras-" + cote]}">'
            f'<line x1="0" y1="-60" x2="0" y2="-46"/>'
            f'<g data-os="avant-bras-{cote}" transform="{os["avant-bras-" + cote]}">'
            f'<line x1="0" y1="-46" x2="0" y2="-33"/>{outil}</g></g>'
        )

    return (
        f'<g data-os="marcheur" transform="{os["marcheur"]}">'
        f'<g data-os="bassin" transform="{os["bassin"]}">'
        f'{jambe("arr")}'
        f'<g data-os="torse" transform="{os["torse"]}">'
        f'{bras("arr", "")}'
        f'<line x1="0" y1="-36" x2="0" y2="-64"/>'
        f'<circle cx="0" cy="-72.5" r="8.5"/>'
        f'<path class="equipe__casque" d="M-9.3 -74.5a9.3 9.3 0 0 1 18.6 0zM-11.5 -74.5h23"/>'
        f'{bras("av", outil_av)}'
        f'</g>'
        f'{jambe("av")}'
        f'</g></g>'
    )


def _accessoires(metier):
    """Ce qui reste au poste : tréteau, carreaux, ampoule, mur."""
    a = lambda nom, **d: _attributs(metier, nom, **d)
    if metier == "marteau":
        return (
            '<g class="equipe__decor"><rect x="10" y="-30" width="44" height="4"/>'
            '<path d="M16 -26 11 0M16 -26 21 0M48 -26 43 0M48 -26 53 0"/></g>'
            f'<g class="equipe__clou" data-accessoire="clou"{a("clou")}>'
            '<path d="M27 -30V-37.5M24.5 -37.5h5"/></g>'
            f'<g class="equipe__impact" data-accessoire="impact"{a("impact")}>'
            '<path d="M20 -41l-3 -2M34 -41l3 -2M27 -44v-3"/></g>'
        )
    if metier == "sol":
        carreaux = "".join(
            '<rect class="equipe__carreau" data-accessoire="carreau-%d"%s/>'
            % (i, a("carreau-%d" % i, x=x, y="-3.5", width="14", height="3.5"))
            for i, x in enumerate((17, 33, 49))
        )
        return f'<g>{carreaux}</g>'
    if metier == "ampoule":
        rayons = "".join(
            '<line x1="0" y1="-9" x2="0" y2="-13" transform="rotate(%d)"/>' % angle
            for angle in range(0, 360, 45)
        )
        verre = IMMOBILE[metier]["accessoires"].get("verre", {}).get("class", "equipe__ampoule")
        return (
            '<g class="equipe__decor"><line x1="20" y1="-128" x2="20" y2="-95"/>'
            '<rect x="17" y="-95" width="6" height="5"/></g>'
            f'<g class="equipe__halo" data-accessoire="halo"{a("halo")}>'
            f'<g transform="translate(20 -84)">{rayons}</g></g>'
            f'<g data-accessoire="ampoule"{a("ampoule")}>'
            f'<circle class="{verre}" data-accessoire="verre" cx="20" cy="-84" r="5.5"/></g>'
        )
    if metier == "peinture":
        return (
            f'<rect class="equipe__peinture" data-accessoire="peinture"{a("peinture", x="16", y="-82", height="82")}/>'
            '<rect class="equipe__mur" x="16" y="-82" width="68" height="82"/>'
            f'<line class="equipe__perche" data-accessoire="perche"{a("perche")}/>'
            f'<rect class="equipe__rouleau" data-accessoire="rouleau"{a("rouleau", width="4", height="12", rx="1.5")}/>'
        )
    return ""


def frise():
    """La frise complète, prête à poser sous la couverture de l'accueil."""
    postes = []
    for metier, place in POSTES:
        outil = MARTEAU if metier == "marteau" else ""
        if metier == "sol":
            outil = ('<rect class="equipe__carreau" data-accessoire="carreau-main"%s/>'
                     % _attributs(metier, "carreau-main", x="-7", y="-33", width="14", height="3.5"))
        postes.append(
            f'      <div class="equipe__poste" style="--place:{place}%">'
            f'<svg class="equipe__dessin" data-metier="{metier}" viewBox="-40 -128 120 132" '
            f'focusable="false">{_accessoires(metier)}{_ouvrier(metier, outil)}</svg></div>'
        )
    return (
        '    <div class="zone equipe-cadre">\n'
        '      <div class="equipe" data-equipe aria-hidden="true">\n'
        + "\n".join(postes) + "\n"
        '      </div>\n'
        '      <button class="equipe__pause" type="button" data-equipe-pause hidden '
        'aria-pressed="false">'
        '<span class="visuellement-cache">Mettre en pause l\'animation des ouvriers</span></button>\n'
        '    </div>\n'
    )

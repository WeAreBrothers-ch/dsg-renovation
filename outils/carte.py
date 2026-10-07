"""La carte de la zone : le Léman au trait, un repère par commune.

Un plan d'implantation à l'échelle du lac : la rive en trait d'encre, l'eau
hachurée comme sur un plan, un carré rouge par commune desservie (le même
que les puces de la liste), l'atelier marqué plus fort. L'échelle et le
nord, comme sur tout plan.

Le contour est celui du Léman entier, rive française comprise, tiré des
limites généralisées de l'OFS (swisstopo), publiées par le paquet npm
swiss-maps (2026). Les repères sont placés au centre de chaque localité ;
chacun a été vérifié dans le périmètre de sa commune sur les mêmes
données. Ajouter une commune à donnees_site.COMMUNES demande ses
coordonnées ici : la construction s'arrête sinon.

Le plan est tracé en SVG, à la construction ; les noms sont du HTML posé
dessus, en pourcentage du plan, pour garder leur taille de texte à toutes
les largeurs. Sept communes tiennent en cinq kilomètres autour de
Lausanne : comme sur une carte imprimée, un carton les montre agrandies,
dans le blanc que le lac laisse au pied du plan. Au survol d'une commune,
sur le plan ou dans la liste, son repère se marque des deux côtés
(carte.js).
"""

import math

from donnees_site import COMMUNES

# Le cadre du plan, en degrés : de Genève à Montreux, des hauts de
# Lausanne au bout du lac.
_OUEST, _EST = 6.09, 6.98
_SUD, _NORD = 46.19, 46.56
# Une seule latitude de référence suffit à cette échelle (60 km).
_K = math.cos(math.radians(46.4))
LARGEUR = 1000
_ECHELLE = LARGEUR / ((_EST - _OUEST) * _K)
HAUTEUR = round((_NORD - _SUD) * _ECHELLE)
_KM_PAR_DEGRE = 111.32 * _K

# Rive du Léman (longitude, latitude), OFS / swisstopo, généralisée.
_LEMAN = """
6.8601,46.3954 6.8578,46.3948 6.8607,46.3905 6.8590,46.3872 6.8577,46.3886
6.8573,46.3883 6.8583,46.3872 6.8564,46.3866 6.8491,46.3895 6.8310,46.3870
6.8111,46.3921 6.8062,46.3954 6.7902,46.3945 6.7606,46.4019 6.7568,46.4040
6.7364,46.4060 6.7250,46.4092 6.6791,46.4086 6.6631,46.4059 6.6372,46.4074
6.6055,46.4036 6.5887,46.4036 6.5455,46.3961 6.5205,46.4057 6.5123,46.4060
6.4926,46.3996 6.4860,46.3956 6.4832,46.3929 6.4831,46.3831 6.4781,46.3769
6.4314,46.3614 6.4141,46.3612 6.4051,46.3522 6.3982,46.3503 6.3909,46.3418
6.3812,46.3428 6.3604,46.3496 6.3578,46.3559 6.3511,46.3635 6.3516,46.3683
6.3456,46.3712 6.3314,46.3707 6.3245,46.3727 6.3225,46.3702 6.3028,46.3671
6.3033,46.3657 6.2933,46.3614 6.2773,46.3509 6.2777,46.3464 6.2720,46.3385
6.2570,46.3255 6.2588,46.3215 6.2535,46.3118 6.2503,46.3081 6.2428,46.3055
6.2433,46.2996 6.2370,46.2913 6.2291,46.2870 6.2165,46.2733 6.2104,46.2667
6.1997,46.2652 6.1951,46.2589 6.1924,46.2469 6.1948,46.2434 6.1934,46.2390
6.1912,46.2342 6.1730,46.2131 6.1655,46.2099 6.1631,46.2107 6.1586,46.2074
6.1566,46.2093 6.1580,46.2071 6.1553,46.2058 6.1507,46.2064 6.1489,46.2081
6.1539,46.2123 6.1528,46.2168 6.1544,46.2224 6.1502,46.2293 6.1544,46.2468
6.1523,46.2525 6.1571,46.2568 6.1629,46.2643 6.1671,46.2652 6.1701,46.2716
6.1721,46.2760 6.1679,46.2831 6.1709,46.2899 6.1727,46.2902 6.1719,46.2932
6.1711,46.2960 6.1822,46.3060 6.1873,46.3120 6.1948,46.3171 6.2009,46.3268
6.2035,46.3311 6.2036,46.3361 6.2076,46.3402 6.2080,46.3486 6.2135,46.3545
6.2215,46.3644 6.2275,46.3678 6.2340,46.3729 6.2365,46.3780 6.2455,46.3846
6.2483,46.3883 6.2594,46.3943 6.2748,46.3916 6.2786,46.3966 6.2829,46.3984
6.2825,46.4068 6.2909,46.4155 6.2916,46.4240 6.2977,46.4256 6.2981,46.4273
6.3068,46.4305 6.3101,46.4334 6.3211,46.4451 6.3325,46.4504 6.3393,46.4580
6.3468,46.4625 6.3524,46.4623 6.3743,46.4668 6.3805,46.4659 6.3846,46.4659
6.3922,46.4617 6.4043,46.4605 6.4218,46.4699 6.4366,46.4720 6.4502,46.4755
6.4556,46.4800 6.4630,46.4799 6.4617,46.4830 6.4648,46.4884 6.4703,46.4921
6.4805,46.4927 6.4829,46.4936 6.4834,46.4987 6.4874,46.5030 6.4877,46.5027
6.4897,46.5023 6.4947,46.5055 6.4947,46.5055 6.4959,46.5054 6.4978,46.5066
6.5013,46.5106 6.5060,46.5161 6.5097,46.5173 6.5141,46.5164 6.5201,46.5170
6.5371,46.5092 6.5404,46.5094 6.5407,46.5084 6.5605,46.5091 6.5660,46.5134
6.5736,46.5146 6.5789,46.5188 6.5874,46.5189 6.5929,46.5193 6.6025,46.5137
6.6041,46.5128 6.6086,46.5138 6.6148,46.5119 6.6188,46.5089 6.6194,46.5103
6.6268,46.5073 6.6272,46.5070 6.6273,46.5070 6.6285,46.5062 6.6291,46.5078
6.6312,46.5082 6.6329,46.5084 6.6356,46.5080 6.6369,46.5076 6.6401,46.5067
6.6427,46.5061 6.6428,46.5066 6.6429,46.5066 6.6647,46.5073 6.6690,46.5058
6.6768,46.5055 6.7045,46.4979 6.7222,46.4879 6.7313,46.4880 6.7353,46.4904
6.7438,46.4906 6.7517,46.4878 6.7619,46.4813 6.7787,46.4756 6.7867,46.4754
6.7997,46.4734 6.8099,46.4719 6.8097,46.4704 6.8142,46.4713 6.8334,46.4686
6.8364,46.4618 6.8530,46.4581 6.8609,46.4483 6.8661,46.4498 6.8741,46.4493
6.8784,46.4471 6.8831,46.4424 6.8860,46.4435 6.8909,46.4403 6.9027,46.4416
6.9100,46.4365 6.9097,46.4322 6.9131,46.4300 6.9168,46.4313 6.9203,46.4303
6.9244,46.4255 6.9242,46.4224 6.9280,46.4195 6.9279,46.4155 6.9317,46.4096
6.9260,46.4036 6.9244,46.3987 6.9198,46.3984 6.9195,46.3963 6.9013,46.3977
6.8964,46.3957 6.8896,46.3968 6.8865,46.4010 6.8882,46.3975 6.8743,46.3957
6.8765,46.3931 6.8768,46.3915 6.8815,46.3899 6.8773,46.3904 6.8774,46.3890
6.8765,46.3912 6.8738,46.3960 6.8677,46.3942 6.8610,46.3963
"""

# Latitude, longitude du centre de chaque localité, puis le côté où
# s'écrit son nom sur le plan et dans le carton : e(st), o(uest), n(ord),
# s(ud), ou None. Les communes serrées autour de Lausanne ne sont nommées
# que dans le carton ; Lausanne l'est sur le plan au téléphone seulement,
# où le carton manque. Elle est marquée à l'atelier.
LIEUX = {
    "Lausanne": (46.5240, 6.6460, "n", "e"),
    "Pully": (46.5100, 6.6614, None, "e"),
    "Prilly": (46.5367, 6.6031, None, "n"),
    "Renens": (46.5397, 6.5881, None, "o"),
    "Ecublens": (46.5280, 6.5619, None, "e"),
    "Épalinges": (46.5486, 6.6706, None, "o"),
    "Lutry": (46.5031, 6.6858, None, "o"),
    "Morges": (46.5111, 6.4983, "o", None),
    "Nyon": (46.3832, 6.2397, "o", None),
    "Vevey": (46.4628, 6.8432, "o", None),
    "Montreux": (46.4350, 6.9140, "o", None),
    "Genève": (46.2044, 6.1432, "e", None),
}

_LAC = (46.43, 6.53)

# Le carton : Lausanne et ses environs, agrandis deux fois et demie, posés
# au pied du plan à droite, où le dessin laisse un blanc (le Chablais).
# Trop petit au téléphone pour qu'on y lise sept noms, il paraît dès la
# tablette (13-carte.css) ; la liste sous le plan les nomme toutes.
_CARTON_GEO = (6.545, 6.700, 46.494, 46.558)   # ouest, est, sud, nord
_ZOOM = 2.5


def _plan(lat, lon):
    """Coordonnées sur le plan, en unités du dessin."""
    return (lon - _OUEST) * _K * _ECHELLE, (_NORD - lat) * _ECHELLE


def _carton():
    """Le cadre de repérage sur le plan (x, y, l, h) et le carton (idem)."""
    ouest, est, sud, nord = _CARTON_GEO
    x, y = _plan(nord, ouest)
    x2, y2 = _plan(sud, est)
    l, h = (x2 - x) * _ZOOM, (y2 - y) * _ZOOM
    return (x, y, x2 - x, y2 - y), (LARGEUR - l, HAUTEUR - h, l, h)


def _dans_carton(lat, lon):
    (x, y, _, _), (cx, cy, _, _) = _carton()
    px, py = _plan(lat, lon)
    return cx + (px - x) * _ZOOM, cy + (py - y) * _ZOOM


def _pour_cent(x, y):
    return "left:%.2f%%;top:%.2f%%" % (100 * x / LARGEUR, 100 * y / HAUTEUR)


def ancre(nom):
    """Le nom d'une commune sans accent ni majuscule : la clé qui relie
    sa ligne de la liste à son repère sur le plan."""
    table = str.maketrans("éèêëàâîïôöûüç", "eeeeaaiioouuc")
    return nom.lower().translate(table).replace(" ", "-")


def _rive():
    points = [tuple(map(float, p.split(","))) for p in _LEMAN.split()]
    trace = ["%.1f %.1f" % _plan(lat, lon) for lon, lat in points]
    return "M" + " L".join(trace) + "Z"


def _repere(nom, x, y, cote, carton=False, serre=False):
    """Un repère. `carton` : posé dans le carton ; `serre` : posé sur le
    plan mais nommé dans le carton — au téléphone, sans carton, le plan
    ne garde que les villes qu'il peut nommer."""
    classes = "carte__lieu" + (" carte__lieu--%s" % cote if cote else "")
    if nom == "Lausanne":
        classes += " carte__lieu--atelier"
    if carton:
        classes += " carte__lieu--carton"
    if serre:
        classes += " carte__lieu--serre"
    texte = f'<span class="carte__nom">{nom}</span>' if cote else ""
    return (f'          <li class="{classes}" data-lieu="{ancre(nom)}" '
            f'style="{_pour_cent(x, y)}">{texte}</li>')


def carte():
    """La figure : le plan, son carton, les repères, l'échelle, le nord,
    la source."""
    manquantes = [c for c in COMMUNES if c not in LIEUX]
    if manquantes:
        raise SystemExit("carte.py : coordonnées manquantes pour %s"
                         % ", ".join(manquantes))
    (lx, ly, ll, lh), (cx, cy, cl, ch) = _carton()
    plan, carton = [], []
    for nom in COMMUNES:
        lat, lon, cote_plan, cote_carton = LIEUX[nom]
        plan.append(_repere(nom, *_plan(lat, lon), cote_plan,
                            serre=bool(cote_carton)))
        if cote_carton:
            carton.append(_repere(nom, *_dans_carton(lat, lon), cote_carton, True))
    rive = _rive()
    dix_km = 100 * 10 / _KM_PAR_DEGRE * _K * _ECHELLE / LARGEUR
    # Le carton reprend la rive, agrandie : on la déplace et on l'agrandit
    # d'un seul geste, découpée à son cadre.
    tx, ty = cx - lx * _ZOOM, cy - ly * _ZOOM
    return f"""      <figure class="carte" role="img" aria-label="Plan du Léman : l'atelier à Lausanne et les communes où nous intervenons, de Genève à Montreux">
        <div class="carte__plan" style="aspect-ratio:{LARGEUR}/{HAUTEUR}">
          <svg class="carte__fond" viewBox="0 0 {LARGEUR} {HAUTEUR}" aria-hidden="true" focusable="false">
            <defs>
              <pattern id="carteEau" width="8" height="8" patternUnits="userSpaceOnUse"><path class="carte__onde" d="M0 4H8"/></pattern>
              <pattern id="carteEauCarton" width="{8 / _ZOOM:g}" height="{8 / _ZOOM:g}" patternUnits="userSpaceOnUse"><path class="carte__onde" d="M0 {4 / _ZOOM:g}H{8 / _ZOOM:g}"/></pattern>
              <path id="carteRive" d="{rive}"/>
              <clipPath id="carteDecoupe"><rect x="{cx:.1f}" y="{cy:.1f}" width="{cl:.1f}" height="{ch:.1f}"/></clipPath>
            </defs>
            <use class="carte__lac" href="#carteRive"/>
            <use class="carte__eau" href="#carteRive" fill="url(#carteEau)"/>
            <g class="carte__zoom">
            <rect class="carte__loupe" x="{lx:.1f}" y="{ly:.1f}" width="{ll:.1f}" height="{lh:.1f}"/>
            <path class="carte__renvoi" d="M{lx:.1f} {ly + lh:.1f}L{cx:.1f} {cy:.1f}M{lx + ll:.1f} {ly + lh:.1f}L{cx + cl:.1f} {cy:.1f}"/>
            <g clip-path="url(#carteDecoupe)">
              <rect class="carte__carton-fond" x="{cx:.1f}" y="{cy:.1f}" width="{cl:.1f}" height="{ch:.1f}"/>
              <g transform="translate({tx:.1f} {ty:.1f}) scale({_ZOOM:g})">
                <use class="carte__lac" href="#carteRive"/>
                <use class="carte__eau" href="#carteRive" fill="url(#carteEauCarton)"/>
              </g>
            </g>
            <rect class="carte__carton" x="{cx:.1f}" y="{cy:.1f}" width="{cl:.1f}" height="{ch:.1f}"/>
            </g>
          </svg>
          <span class="carte__nom-lac" style="{_pour_cent(*_plan(*_LAC))}" aria-hidden="true">Léman</span>
          <span class="carte__titre-carton" style="{_pour_cent(cx, cy + ch)}" aria-hidden="true">Lausanne et environs</span>
          <ul class="carte__lieux" aria-hidden="true">
{chr(10).join(plan)}
{chr(10).join(carton)}
          </ul>
          <span class="carte__releve" aria-hidden="true">
            <span class="carte__nord">N</span>
            <span class="carte__echelle" style="width:{dix_km:.2f}%">10 km</span>
          </span>
        </div>
        <figcaption class="carte__legende">
          <span class="carte__cle carte__cle--atelier">Atelier, avenue de Béthusy</span>
          <span class="carte__cle">Communes où nous intervenons</span>
          <span class="carte__source">Contours : OFS, swisstopo</span>
        </figcaption>
      </figure>"""

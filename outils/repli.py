"""Onglets et dépliants : montrer moins, sans rien retirer.

Une page de chantier ne s'étale pas, elle se feuillette. Ces deux
composants gardent tout le contenu dans la page — donc lisible par un
moteur — mais n'en montrent que les intitulés.

Sans JavaScript, les onglets affichent tous leurs panneaux et les
dépliants restent ouvrables : rien n'est jamais inaccessible.
"""

_compteur = {"n": 0}


def _identifiant(prefixe):
    _compteur["n"] += 1
    return "%s%d" % (prefixe, _compteur["n"])


def onglets(panneaux, etiquette):
    """Un jeu d'onglets : une languette par panneau, un seul visible.

    `panneaux` : liste de (intitulé, contenu HTML).
    """
    if len(panneaux) < 2:
        return panneaux[0][1] if panneaux else ""

    base = _identifiant("jeu")
    languettes, corps = [], []
    for rang, (nom, contenu) in enumerate(panneaux):
        onglet_id = "%s-o%d" % (base, rang)
        panneau_id = "%s-p%d" % (base, rang)
        languettes.append(
            '<button class="jeu__onglet" type="button" role="tab" data-onglet'
            ' id="%s" aria-controls="%s" aria-selected="%s">%s</button>'
            % (onglet_id, panneau_id, "true" if rang == 0 else "false", nom)
        )
        corps.append(
            '<div class="jeu__panneau" role="tabpanel" data-panneau id="%s"'
            ' aria-labelledby="%s">\n%s\n</div>' % (panneau_id, onglet_id, contenu)
        )
    return (
        '      <div class="jeu" data-onglets>\n'
        '        <div class="jeu__barre" role="tablist" aria-label="%s"'
        ' data-onglets-barre hidden>\n          %s\n        </div>\n'
        '        %s\n      </div>'
        % (etiquette, "\n          ".join(languettes), "\n        ".join(corps))
    )


def replis(entrees, numerote=True):
    """Une suite de lignes dépliables.

    `entrees` : (intitulé, corps HTML) ou (intitulé, corps, cote).
    Fermée, chaque ligne se lit comme une ligne de sommaire.
    """
    lignes = []
    for rang, entree in enumerate(entrees, 1):
        titre, corps = entree[0], entree[1]
        cote = entree[2] if len(entree) > 2 else ""
        numero = ('<span class="repli__n" aria-hidden="true">%02d</span>' % rang
                  if numerote else '<span class="repli__n"></span>')
        marque = '<span class="repli__cote">%s</span>' % cote if cote else "<span></span>"
        lignes.append(f"""        <details class="repli revele trace">
          <summary class="repli__tete">
            {numero}
            <span class="repli__titre">{titre}</span>
            {marque}
            <span class="repli__signe" aria-hidden="true"></span>
          </summary>
          <div class="repli__corps">{corps}</div>
        </details>""")
    return '      <div class="replis">\n' + "\n".join(lignes) + "\n      </div>"


def repli_liste(titre, items, cote=""):
    """Une seule ligne dépliable qui cache une liste de postes."""
    lignes = "\n".join("            <li>%s</li>" % i for i in items)
    corps = '<ul class="service__liste">\n%s\n          </ul>' % lignes
    marque = '<span class="repli__cote">%s</span>' % cote if cote else "<span></span>"
    return f"""        <details class="repli repli--liste revele trace">
          <summary class="repli__tete">
            <span class="repli__n"></span>
            <span class="repli__titre">{titre}</span>
            {marque}
            <span class="repli__signe" aria-hidden="true"></span>
          </summary>
          <div class="repli__corps">{corps}</div>
        </details>"""

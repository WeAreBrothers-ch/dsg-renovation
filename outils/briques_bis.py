"""Cartes à filet et tableau des besoins.

Ils suivent la règle du dossier : pas de fond, pas de rayon, un filet
tiré à la règle et une étiquette dactylographiée. Le carton et l'encre,
rien d'autre.

Ce qui se lit en liste longue a migré vers `repli` : une page de
chantier se feuillette, elle ne se déroule pas.
"""


def cartes(items):
    """Cartes à filet : un titre, une cote, un texte, des étiquettes.

    `items` : (titre, cote, texte, étiquettes) — les étiquettes sont
    facultatives et peuvent être une liste vide.
    """
    blocs = []
    for titre, cote, texte, jetons in items:
        lots = ""
        if jetons:
            lots = ('<ul class="lots carte__lots">'
                    + "".join("<li>%s</li>" % j for j in jetons) + "</ul>")
        blocs.append(f"""        <li class="carte revele">
          <p class="etiquette carte__cote">{cote}</p>
          <h3 class="h3 carte__titre">{titre}</h3>
          <p class="carte__texte">{texte}</p>
          {lots}
        </li>""")
    return '      <ul class="cartes">\n' + "\n".join(blocs) + "\n      </ul>"


def _insecable(texte):
    """Soude les guillemets français à leur texte : un « » ne doit jamais
    tomber seul en début ou en fin de ligne."""
    return texte.replace("« ", "«&nbsp;").replace(" »", "&nbsp;»")


def besoins(lignes, services, base):
    """Ce que dit le client, et le lot qui y répond.

    Une entrée par besoin réellement formulé au téléphone : c'est la
    formulation du visiteur, pas le vocabulaire du métier. Le nom du lot
    est repris de sa fiche, jamais déduit de son adresse : un slug n'a
    ni accent ni majuscule.
    """
    noms = {s["slug"]: s["nom"] for s in services}
    rangs = "\n".join(
        f"""        <li class="besoin revele">
          <p class="besoin__dit">{_insecable(dit)}</p>
          <p class="besoin__note">{note}</p>
          <a class="besoin__lot" href="{base}services/{slug}.html">{noms[slug]}<span class="fleche" aria-hidden="true"></span></a>
        </li>"""
        for dit, slug, note in lignes
    )
    return '      <ul class="besoins">\n' + rangs + "\n      </ul>"

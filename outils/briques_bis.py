"""Cartes à filet, tableau des besoins, postes, et la glissière qui
fait défiler les suites de cases au téléphone.

Ils suivent la règle du dossier : pas de fond, pas de rayon, un filet
tiré à la règle et une étiquette dactylographiée. Le carton et l'encre,
rien d'autre.

Ce qui s'ouvre ligne à ligne vit dans `repli` ; ce qui doit se lire
d'un coup d'œil se montre ouvert, ici (`postes`).
"""


def glissiere(balise, classe, cases, attributs=""):
    """Une suite de cases à faire glisser au téléphone : la liste, marquée
    .glissiere (16-composants.css, onglets.js), et sa rangée de repères.

    Un carré par case, le premier marqué. Écrite dans la page plutôt
    qu'ajoutée par le script, la rangée a sa place dès le premier
    affichage : rien ne bouge à l'arrivée d'onglets.js, qui ne fait que
    déplacer la marque. La feuille la montre au téléphone seulement, et
    seulement avec le script. `cases` : le HTML de chaque case.
    """
    reperes = '<span data-actif></span>' + "<span></span>" * (len(cases) - 1)
    return (f'      <{balise} class="{classe} glissiere"{attributs}>\n'
            + "\n".join(cases) + f"\n      </{balise}>\n"
            + f'      <div class="glissiere__reperes" aria-hidden="true">{reperes}</div>')


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
        blocs.append(f"""        <li class="carte">
          <p class="etiquette carte__cote">{cote}</p>
          <h3 class="h3 carte__titre">{titre}</h3>
          <p class="carte__texte">{texte}</p>
          {lots}
        </li>""")
    return glissiere("ul", "cartes", blocs)


def postes(items, numerote=False):
    """Une liste ouverte : chaque poste, son intitulé et sa phrase, d'un
    filet à l'autre, deux par ligne dès la tablette.

    Pour ce qui doit se lire d'un coup d'œil — ce que contient un devis,
    ce que nous ne faisons pas — et non s'ouvrir ligne à ligne : une page
    qui enchaîne les dépliants se parcourt comme une foire aux
    questions. `items` : (intitulé, phrase).
    """
    balise = "ol" if numerote else "ul"
    lignes = []
    for rang, (titre, texte) in enumerate(items, 1):
        numero = ('<span class="poste__n" aria-hidden="true">%02d</span>' % rang
                  if numerote else "")
        lignes.append(f"""        <li class="poste">
          {numero}<h3 class="h4 poste__titre">{titre}</h3>
          <p class="texte poste__texte">{texte}</p>
        </li>""")
    return ('      <%s class="postes">\n' % balise + "\n".join(lignes)
            + "\n      </%s>" % balise)


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
    rangs = [
        f"""        <li class="besoin">
          <p class="besoin__dit">{_insecable(dit)}</p>
          <p class="besoin__note">{note}</p>
          <a class="besoin__lot" href="{base}services/{slug}.html">{noms[slug]}<span class="fleche" aria-hidden="true"></span></a>
        </li>"""
        for dit, slug, note in lignes
    ]
    return glissiere("ul", "besoins", rangs)

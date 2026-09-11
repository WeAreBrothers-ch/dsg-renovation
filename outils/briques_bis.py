"""Composants nés du contenu neuf : frise, cartes, tableau de besoins.

Ils suivent la règle du dossier : pas de fond, pas de rayon, un filet
tiré à la règle et une étiquette dactylographiée. Le carton et l'encre,
rien d'autre.
"""


def frise(etapes, avec_cote=True):
    """Une suite d'étapes numérotées, chacune sur son filet.

    `etapes` accepte deux formes : (titre, texte) ou (titre, texte, cote).
    La cote se pose à droite, comme la durée sur un bordereau.
    """
    lignes = []
    for rang, etape in enumerate(etapes, 1):
        titre, texte = etape[0], etape[1]
        cote = etape[2] if len(etape) > 2 and avec_cote else ""
        marque = ('<span class="temps__cote donnee">%s</span>' % cote) if cote else ""
        lignes.append(f"""        <li class="temps revele trace">
          <span class="temps__n">{rang:02d}</span>
          <div class="temps__corps">
            <h3 class="h4">{titre}</h3>
            <p class="temps__texte">{texte}</p>
          </div>
          {marque}
        </li>""")
    return '      <ol class="frise">\n' + "\n".join(lignes) + "\n      </ol>"


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
        blocs.append(f"""        <li class="carte revele trace">
          <p class="etiquette carte__cote">{cote}</p>
          <h3 class="h3 carte__titre">{titre}</h3>
          <p class="carte__texte">{texte}</p>
          {lots}
        </li>""")
    return '      <ul class="cartes">\n' + "\n".join(blocs) + "\n      </ul>"


def besoins(lignes, services, base):
    """Ce que dit le client, et le lot qui y répond.

    Une entrée par besoin réellement formulé au téléphone : c'est la
    formulation du visiteur, pas le vocabulaire du métier. Le nom du lot
    est repris de sa fiche, jamais déduit de son adresse : un slug n'a
    ni accent ni majuscule.
    """
    noms = {s["slug"]: s["nom"] for s in services}
    rangs = "\n".join(
        f"""        <li class="besoin revele trace">
          <p class="besoin__dit">{dit}</p>
          <div class="besoin__reponse">
            <a class="besoin__lot" href="{base}services/{slug}.html">{noms[slug]}<span class="fleche" aria-hidden="true"></span></a>
            <p class="besoin__note">{note}</p>
          </div>
        </li>"""
        for dit, slug, note in lignes
    )
    return '      <ul class="besoins">\n' + rangs + "\n      </ul>"


def limites(items):
    """Ce que nous ne faisons pas : un titre barré d'un trait, un motif."""
    blocs = "\n".join(
        f"""        <li class="limite revele trace">
          <h3 class="h4 limite__titre">{titre}</h3>
          <p class="etape__texte">{texte}</p>
        </li>"""
        for titre, texte in items
    )
    return '      <ul class="limites">\n' + blocs + "\n      </ul>"


def liste_sobre(paragraphes, numerotee=True):
    """Une liste de conseils : un chiffre, un paragraphe, un filet."""
    balise = "ol" if numerotee else "ul"
    items = "\n".join(
        f"""        <li class="conseil revele trace"><p>{p}</p></li>"""
        for p in paragraphes
    )
    return '      <%s class="conseils">\n' % balise + items + "\n      </%s>" % balise

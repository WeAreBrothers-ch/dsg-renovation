"""Fragments de page réutilisés d'un bout à l'autre du site.

Ce sont les mêmes composants que le dossier d'origine : intercalaire,
liste des métiers, relevé chiffré, appel à l'action. Les reprendre tels
quels garantit qu'une page de service ressemble au reste du site.
"""

from donnees_site import RELEVE, TELEPHONE, TELEPHONE_BRUT


def couverture(page, base, fil, action=None):
    """En-tête de page : fil d'Ariane, étiquette, titre, chapô, actions.

    `action` remplace le bouton de devis là où il pointerait vers la page
    consultée : un bouton qui renvoie où l'on se trouve déjà est un
    bouton mort.
    """
    miettes = "\n          ".join(
        ('<a href="%s%s">%s</a>\n          <span aria-hidden="true">/</span>'
         % (base, url, nom)) if url else "<span>%s</span>" % nom
        for nom, url in fil
    )
    lignes = "\n          ".join(
        '<span class="ligne"><span>%s</span></span>' % l for l in page["h1"]
    )
    principale = action or (
        '<a class="btn btn--plein" href="%sdevis.html" data-magnetique>'
        'Demander un devis gratuit<span class="fleche" aria-hidden="true">'
        "</span></a>" % base
    )
    return f"""
  <header class="piece piece--titre">
    <div class="zone">
      <div class="piece__entete trace--bas trace revele">
        <nav class="piece__chemin donnee" aria-label="Fil d'Ariane">
          {miettes}
        </nav>

        <p class="etiquette">{page['etiquette']}</p>
        <h1 class="piece__titre" data-lignes>
          {lignes}
        </h1>
        <p class="chapo piece__chapo">{page['chapo']}</p>

        <div class="couverture__actions">
          {principale}
          <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
        </div>
      </div>
    </div>
  </header>
"""


def intercalaire(numero, nom, cote, titre, chapo=""):
    """L'en-tête de section du dossier : repère, cote, titre.

    Les lignes du titre se séparent par une barre verticale, et non par
    un saut de ligne : l'antislash se perdrait d'un niveau
    d'échappement à l'autre en traversant les f-strings.
    """
    lignes = titre.replace("|", "<br>")
    texte = ('<p class="chapo intercalaire__chapo">%s</p>' % chapo) if chapo else ""
    return f"""      <div class="intercalaire revele">
        <span class="repere trace trace--bas"><b>{numero}</b>{nom}</span>
        <span class="intercalaire__cote">{cote}</span>
        <h2 class="h2" data-lignes>{lignes}</h2>
        {texte}
      </div>"""


def liste_metiers(services, base, courant=None):
    """La liste des neuf lots, chacun menant à sa page."""
    lignes = []
    for s in services:
        if s["slug"] == courant:
            continue
        lignes.append(f"""        <li>
          <a class="metiers__ligne" href="{base}services/{s['slug']}.html">
            <span class="metiers__n">{s['numero']}</span>
            <span class="metiers__titre">{s['nom']}</span>
            <span class="metiers__desc">{s['resume']}</span>
            <span class="metiers__chev" aria-hidden="true"></span>
            <span class="metiers__vue" aria-hidden="true"><img src="{s['image']}" alt="" width="316" height="395" loading="lazy" decoding="async"></span>
          </a>
        </li>""")
    return ('      <ul class="metiers revele" data-suivi-vignette>\n'
            + "\n".join(lignes) + "\n      </ul>")


def releve_chiffre():
    """Les quatre chiffres de l'entreprise, en chemises de dossier."""
    cellules = "\n".join(
        f"""        <li class="preuve revele">
          <span class="preuve__onglet etiquette">{nom}</span>
          <p class="preuve__chiffre">
            <span class="preuve__val" data-compteur="{val}">{val}</span>{'<span class="preuve__plus">' + plus + '</span>' if plus else ''}
          </p>
          <p class="preuve__texte">{texte}</p>
        </li>"""
        for nom, val, plus, texte in RELEVE
    )
    return '      <ul class="preuves">\n' + cellules + "\n      </ul>"


def appel(base, titre, texte):
    """Le renvoi de fin de page vers la demande de devis."""
    return f"""
  <section class="section rappel sur-sombre" aria-labelledby="rappelTitre">
    <div class="zone rappel__grille">
      <div>
        <p class="etiquette">Prochaine étape</p>
        <h2 class="h2 rappel__titre" id="rappelTitre">{titre}</h2>
        <p class="chapo" style="margin-top:var(--sp-5)">{texte}</p>
      </div>
      <div class="rappel__actions">
        <a class="btn btn--plein" href="{base}devis.html" data-magnetique>Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
        <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a>
      </div>
    </div>
  </section>
"""


def questions_liste(paires):
    """Liste de questions dépliables, telle quelle dans le dossier."""
    items = "\n".join(
        f"""        <li>
          <details class="question">
            <summary class="question__tete">{q}<span class="depliant__signe" aria-hidden="true"></span></summary>
            <div class="question__corps"><p>{r}</p></div>
          </details>
        </li>"""
        for q, r in paires
    )
    return '      <ul class="questions__liste revele">\n' + items + "\n      </ul>"

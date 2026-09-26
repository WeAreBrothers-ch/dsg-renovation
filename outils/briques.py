"""Fragments de page réutilisés d'un bout à l'autre du site.

Ce sont les mêmes composants que le dossier d'origine : intercalaire,
liste des métiers, relevé chiffré, appel à l'action. Les reprendre tels
quels garantit qu'une page de service ressemble au reste du site.
"""

from donnees_site import RELEVE, TELEPHONE, TELEPHONE_BRUT
from gabarit_liens import accueil, vers_devis


def couverture(page, base, fil, action=None):
    """En-tête de page : fil d'Ariane, titre, chapô, actions.

    `action` remplace le bouton de devis là où il pointerait vers la page
    consultée : un bouton qui renvoie où l'on se trouve déjà est un
    bouton mort. Dans `fil`, « / » désigne l'accueil, une adresse vide
    la page consultée (qui n'est pas un lien).
    """
    miettes = "\n          ".join(
        ('<a href="%s">%s</a>\n          <span aria-hidden="true">/</span>'
         % (accueil(base) if url == "/" else base + url, nom)) if url
        else "<span>%s</span>" % nom
        for nom, url in fil
    )
    # Le titre de page s'affiche d'emblée, sans révélation : c'est
    # souvent le plus grand élément du premier écran, et le retarder
    # retarderait d'autant le premier affichage utile (LCP).
    titre = " ".join(page["h1"])
    principale = action if action is not None else (
        '<a class="btn btn--plein" href="%s">'
        'Demander un devis gratuit<span class="fleche" aria-hidden="true">'
        "</span></a>" % vers_devis(base, page["courante"], page.get("travaux"))
    )
    return f"""
  <header class="piece">
    <div class="zone">
      <div class="piece__entete">
        <div class="piece__marge">
          <nav class="piece__chemin" aria-label="Fil d'Ariane">
          {miettes}
          </nav>
        </div>
        <div class="piece__tete">
          <h1 class="piece__titre">{titre}</h1>
          <p class="chapo piece__chapo">{page['chapo']}</p>
          <div class="couverture__actions">
          {principale}
          <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}<span class="fleche" aria-hidden="true"></span></a>
          </div>
        </div>
      </div>
    </div>
  </header>
"""


def intercalaire(nom, cote, titre, chapo=""):
    """L'en-tête de section : l'intitulé et sa cote dans la marge, le
    titre dans la colonne de droite.

    Les lignes du titre se séparent par une barre verticale, et non par
    un saut de ligne : l'antislash se perdrait d'un niveau
    d'échappement à l'autre en traversant les f-strings.
    """
    lignes = titre.replace("|", " <br>")
    texte = ('<p class="chapo intercalaire__chapo">%s</p>' % chapo) if chapo else ""
    return f"""      <div class="intercalaire">
        <div class="intercalaire__marge revele">
          <p class="intercalaire__nom">{nom}</p>
          <p class="intercalaire__cote">{cote}</p>
        </div>
        <div class="intercalaire__corps revele">
          <h2 class="h2" data-lignes>{lignes}</h2>
          {texte}
        </div>
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
    return ('      <ul class="metiers revele">\n'
            + "\n".join(lignes) + "\n      </ul>")


def releve_chiffre():
    """Les quatre chiffres de l'entreprise, en chemises de dossier."""
    cellules = "\n".join(
        f"""        <li class="preuve revele">
          <span class="preuve__onglet etiquette">{nom}</span>
          <p class="preuve__chiffre">
            <span class="preuve__val">{val}</span>{'<span class="preuve__plus">' + plus + '</span>' if plus else ''}
          </p>
          <p class="preuve__texte">{texte}</p>
        </li>"""
        for nom, val, plus, texte in RELEVE
    )
    return '      <ul class="preuves">\n' + cellules + "\n      </ul>"


def appel(base, titre, texte, travaux=None):
    """Le renvoi de fin de page vers la demande de devis.

    `travaux` : la prestation à pré-cocher dans le formulaire.
    """
    return f"""
  <section class="section rappel sur-vif" aria-labelledby="rappelTitre">
    <div class="zone rappel__grille">
      <p class="intercalaire__nom rappel__marge">Prochaine étape</p>
      <div class="rappel__corps">
        <h2 class="rappel__titre" id="rappelTitre">{titre}</h2>
        <p class="chapo">{texte}</p>
        <div class="rappel__actions">
          <a class="btn btn--plein" href="{vers_devis(base, '', travaux)}">Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
          <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}<span class="fleche" aria-hidden="true"></span></a>
        </div>
      </div>
    </div>
  </section>
"""


def questions_liste(paires):
    """Liste de questions dépliables.

    Elles empruntent le dépliant de bordereau, comme le reste du site :
    deux accordéons de dessins différents sur une même page se lisent
    comme deux composants sans rapport.
    """
    import repli
    return repli.replis([(q, "<p>%s</p>" % r) for q, r in paires],
                        numerote=False)

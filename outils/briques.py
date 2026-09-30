"""Fragments de page réutilisés d'un bout à l'autre du site.

Ce sont les mêmes composants que le dossier d'origine : intercalaire,
liste des métiers, relevé chiffré, appel à l'action. Les reprendre tels
quels garantit qu'une page de service ressemble au reste du site.
"""

from donnees_site import RELEVE, TELEPHONE, TELEPHONE_BRUT
from gabarit_liens import accueil, vers_devis


def vue(media, base, classe="", priorite=True):
    """Une photo et sa légende posée dedans, en bas : le lieu, ce qu'on
    voit, et le chemin vers la fiche du chantier quand il y en a une.

    `media` : src, alt, lieu, quoi, et facultativement ancre (fiche de la
    page des réalisations), largeur, hauteur. La légende vit dans
    l'image, sur un voile d'encre : aucune bande de texte ne flotte entre
    la photo et la section suivante.
    """
    chargement = ('fetchpriority="high"' if priorite
                  else 'loading="lazy"')
    lien = ""
    if media.get("ancre"):
        lien = (f'<a class="vue__lien" href="{base}realisations.html#{media["ancre"]}">'
                'Voir le chantier<span class="fleche" aria-hidden="true"></span></a>')
    src = media["src"]
    if not src.startswith("http"):
        src = base + src
    return f"""<figure class="vue {classe}">
          <img src="{src}" alt="{media['alt']}"
               width="{media.get('largeur', 1600)}" height="{media.get('hauteur', 1000)}" {chargement} decoding="async">
          <figcaption class="vue__legende">
            <span class="vue__texte"><span class="vue__lieu">{media['lieu']}</span><span class="vue__quoi">{media['quoi']}</span></span>
            {lien}
          </figcaption>
        </figure>"""


def couverture(page, base, fil, action=None):
    """En-tête de page : fil d'Ariane, titre, chapô, actions — et, quand
    la page a sa photo (`page["media"]`), la photo à droite, comme la
    couverture de l'accueil.

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
    media = page.get("media")
    classe = "piece piece--vue" if media else "piece"
    # Quatre repères au pied du texte : ce qu'on veut savoir avant
    # d'appeler (durées, conditions, horaires), lu d'un coup d'œil.
    faits = ""
    if page.get("faits"):
        faits = ('<dl class="piece__faits">' + "".join(
            "<div><dt>%s</dt><dd>%s</dd></div>" % f for f in page["faits"])
            + "</dl>")
    photo = vue(media, base, "piece__vue") if media else ""
    return f"""
  <header class="{classe}">
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
          {faits}
          <div class="couverture__actions">
          {principale}
          <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}<span class="fleche" aria-hidden="true"></span></a>
          </div>
        </div>
        {photo}
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
            <span class="metiers__vue" aria-hidden="true"><img src="{s['image']}" alt="" width="316" height="237" loading="lazy" decoding="async"></span>
            <span class="metiers__titre">{s['nom']}</span>
            <span class="metiers__desc">{s['resume']}</span>
            <span class="metiers__chev" aria-hidden="true"></span>
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

    Un cadre à repères, comme les blocs du plan : à gauche, la question
    et les deux façons d'y répondre ; à droite, comment nous joindre —
    téléphone, courriel, horaires, atelier. La page se referme sur une
    décision facile, avec tout ce qu'il faut pour la prendre.
    `travaux` : la prestation à pré-cocher dans le formulaire.
    """
    import donnees_site as d
    return f"""
  <section class="section rappel" aria-labelledby="rappelTitre">
    <div class="zone">
      <div class="rappel__cadre revele">
        <div class="rappel__corps">
          <p class="intercalaire__nom">Prochaine étape</p>
          <h2 class="rappel__titre" id="rappelTitre">{titre}</h2>
          <p class="chapo">{texte}</p>
          <div class="rappel__actions">
            <a class="btn btn--plein" href="{vers_devis(base, '', travaux)}">Demander un devis gratuit<span class="fleche" aria-hidden="true"></span></a>
            <a class="btn btn--cadre" href="tel:{TELEPHONE_BRUT}">{TELEPHONE}<span class="fleche" aria-hidden="true"></span></a>
          </div>
        </div>
        <dl class="rappel__joindre">
          <div><dt>Téléphone</dt><dd><a href="tel:{TELEPHONE_BRUT}">{TELEPHONE}</a></dd></div>
          <div><dt>Courriel</dt><dd><a href="mailto:{d.COURRIEL}">{d.COURRIEL}</a></dd></div>
          <div><dt>Horaires</dt><dd>{d.HORAIRES}</dd></div>
          <div><dt>Atelier</dt><dd>{d.RUE}, {d.CODE_POSTAL} {d.VILLE}</dd></div>
        </dl>
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

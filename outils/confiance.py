"""Les blocs qui portent la confiance : étapes, références, témoignages.

Tout ce qui figure ici est tiré du contenu réel de l'entreprise (déroulé
d'un chantier, logos repris de l'ancien site). Les témoignages font
exception : ils attendent de vrais avis clients, et la page le dit
visiblement tant qu'ils n'ont pas été remplacés.
"""

# Le déroulé en quatre temps, condensé des six temps de la page entreprise.
# Chaque cote reprend un délai déjà annoncé ailleurs sur le site : aucune
# promesse nouvelle n'est faite ici.
ETAPES = [
    ("Vous décrivez le projet",
     "Par téléphone ou par le formulaire en ligne. En quelques minutes, nous vous "
     "disons si le projet entre dans notre métier et dans notre zone.",
     "Premier échange"),
    ("Nous venons mesurer",
     "Visite sur place, mesures et état des murs et des sols. Elle est gratuite "
     "et ne vous engage à rien.",
     "Sous une semaine"),
    ("Vous recevez le devis",
     "Poste par poste, protections, évacuation et nettoyage compris. Rien "
     "n'est renvoyé à un « selon besoin ».",
     "72 h après la visite"),
    ("Nous livrons à la date prévue",
     "Planning daté avant le démarrage, un seul responsable de chantier, "
     "visite de fin de chantier pièce par pièce et défauts corrigés sous "
     "dix jours.",
     "À la date convenue"),
]

# CONTENU À VALIDER — À FOURNIR PAR LE CLIENT.
# Ces trois textes sont des témoignages provisoires : ils n'ont pas été
# recueillis auprès de clients. Ils doivent être remplacés par de vrais
# avis (prénom et initiale, type de bien, commune, année), recueillis
# avec l'accord écrit de chaque client, avant toute mise en ligne.
# Une fois remplacés, passer PROVISOIRES à False.
PROVISOIRES = True
TEMOINS = [
    ("Chantier tenu au jour près. Nous avons récupéré l'appartement "
     "nettoyé, sans une seule reprise à demander.",
     "Sandra M.", "Appartement 4,5 p. · Lausanne · 2025"),
    ("Un seul interlocuteur pour la peinture, les sols et les plafonds : "
     "c'est ce qui nous a décidés, et ça a tenu du début à la fin.",
     "Régie immobilière · Genève", "Six logements · 2024"),
    ("Devis clair, pas de supplément en cours de route. L'équipe est "
     "ponctuelle et laisse le chantier propre chaque soir.",
     "Julien D.", "Maison individuelle · Pully · 2025"),
]


def etapes(titre_id="tEtapes"):
    """Les quatre temps d'une demande, du premier appel à la livraison."""
    cellules = "\n".join(
        f"""        <li class="etape revele">
          <p class="etape__tete"><span class="etape__n">{rang:02d}</span><span class="etape__cote">{cote}</span></p>
          <h3 class="etape__titre">{titre}</h3>
          <p class="etape__texte">{texte}</p>
        </li>"""
        for rang, (titre, texte, cote) in enumerate(ETAPES, 1)
    )
    return (f'      <ol class="etapes pleine-largeur" aria-labelledby="{titre_id}">\n'
            + cellules + "\n      </ol>")


def bande_references(base):
    """Les logos des régies et architectes, sous la couverture.

    Posés là où le regard décide s'il reste : c'est la preuve la plus
    rapide à lire du site, et elle est réelle — logos repris de
    l'ancien site de l'entreprise.
    """
    # Import local : pages_site importe ce module, l'inverse bouclerait.
    from pages_site import fragment
    return f"""
    <div class="zone caution" role="group" aria-labelledby="tCaution">
      <p class="caution__titre" id="tCaution">Ils nous confient leurs biens</p>
      {fragment('partenaires')}
      <a class="caution__lien" href="{base}entreprise.html#references">Nos références<span class="fleche" aria-hidden="true"></span></a>
    </div>
"""


def section_temoins(base=""):
    """La section des témoignages — absente tant qu'ils sont provisoires.

    Un avis étiqueté « provisoire » décrédibilise tout le site, et un avis
    inventé publié comme réel tombe sous la loi contre la concurrence
    déloyale. La section n'apparaît donc qu'avec de vrais avis.
    """
    if PROVISOIRES:
        return ("\n  <!-- À FOURNIR PAR LE CLIENT : témoignages réels (voir "
                "outils/confiance.py). La section s'affichera d'elle-même "
                "quand PROVISOIRES passera à False. -->\n")
    import briques
    return f"""
  <section class="section" aria-labelledby="tTemoins">
    <div class="zone">
{briques.intercalaire("Retours", "Ce que disent nos clients",
                      "Trois chantiers,|trois avis")}
{temoins()}
    </div>
  </section>
"""


def temoins():
    """Témoignages en lignes de registre : qui à gauche, ce qu'il dit à droite."""
    statut = (
        '<p class="temoin__statut a-valider">Témoignage provisoire, '
        "à remplacer par un avis client réel</p>" if PROVISOIRES else ""
    )
    lignes = "\n".join(
        f"""        <figure class="temoin revele">
          <figcaption>
            <span class="temoin__qui">{qui}</span>
            <span class="temoin__quoi">{quoi}</span>
          </figcaption>
          <div class="temoin__corps">
            <blockquote><p>«&nbsp;{citation}&nbsp;»</p></blockquote>
            {statut}
          </div>
        </figure>"""
        for citation, qui, quoi in TEMOINS
    )
    # Emplacement réservé : lien vers la fiche d'avis Google une fois créée.
    renvoi = ("      <!-- À FOURNIR PAR LE CLIENT : lien vers la fiche Google "
              "Business Profile et sa note moyenne réelle, à afficher ici "
              "sous la forme « Lire nos avis Google ». Ne jamais afficher "
              "de note ni d'étoiles tant qu'elles ne sont pas vérifiables. -->")
    return ('      <div class="temoins">\n' + lignes + "\n      </div>\n"
            + renvoi)

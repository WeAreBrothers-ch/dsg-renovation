"""Corps des pages réalisations, références, questions et devis.

Chaque page mêle les blocs du dossier d'origine — les six fiches de
chantier, les logos, les témoignages — et du contenu écrit pour elle.
"""

import briques
import briques_bis
import repli
import contenu_devis as cd
import contenu_divers as div
import contenu_questions as cq
from pages_site import fragment


def realisations(services, base=""):
    """Le registre des chantiers, les familles de biens, les imprévus.

    Six fiches. La photo de la villa de Chailly (dégagement et cuisine)
    et celle du chantier à la une (immeuble Béthusy) montrent la même
    pièce sous deux angles : l'ancien site n'en fournit pas d'autre. Une
    vraie photo de Chailly la remplacera (BRIEF-PHOTOS.md). Le texte du
    loft de Sévelin décrit ce que montre sa photo (parquet, faux plafond
    éclairé).
    """
    return f"""
  <section class="section" aria-labelledby="tFiches">
    <div class="zone">
{briques.intercalaire("Réalisations", "Six chantiers livrés",
                      "Nos derniers chantiers|de rénovation",
                      "Pour chaque chantier : la surface, la durée et les "
                      "travaux réalisés. Cliquez sur une photo pour "
                      "l'agrandir.")}
      {fragment('filtres')}
      {fragment('chantiers')}
      <p class="chantiers__vide chapo pleine-largeur" id="aucunChantier" hidden>Aucun chantier ne correspond à ce filtre pour le moment.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="tSignature">
    <div class="zone">
{briques.intercalaire("À la une", "Un immeuble habité",
                      "Six appartements rénovés,|locataires en place")}
      {fragment('signature')}
    </div>
  </section>

  <section class="section sur-sombre" aria-labelledby="tBiens">
    <div class="zone">
{briques.intercalaire("Familles", "Ce que nous reprenons dans la région",
                      "Trois types de biens,|trois chantiers différents",
                      "Un appartement de Sous-Gare, une villa de Chailly et "
                      "un immeuble locatif ne se rénovent pas de la "
                      "même façon, ni pour les mêmes raisons.")}
{briques_bis.cartes(div.BIENS)}
    </div>
  </section>

  <section class="section" aria-labelledby="tSurprises">
    <div class="zone">
{briques.intercalaire("Imprévus", "Ce qu'on découvre en ouvrant",
                      "Ce qu'il y a|derrière les murs",
                      "Dans un logement ancien, la dépose réserve toujours "
                      "quelque chose. Les quatre cas ci-dessous reviennent "
                      "sur un chantier lausannois sur deux.")}
{repli.replis([(titre, "<p>%s</p>" % texte)
                for titre, texte in div.SURPRISES])}
    </div>
  </section>
""" + briques.appel(
        base,
        "Votre chantier, le prochain",
        "Décrivez votre projet : nous vous dirons ce qu'il demande, combien de "
        "temps il prend et ce qu'il coûte.",
    )


def devis(services, base=""):
    """Le bordereau d'abord, puis tout ce qu'on se demande avant de signer.

    Le formulaire ouvre la page : quelqu'un qui arrive ici veut demander
    un devis, pas lire. Le reste répond à ceux qui hésitent encore : ce
    que contient le devis se lit ouvert, comme les lignes d'un devis ;
    les questions tiennent en un bloc à onglets.
    """
    contient = briques_bis.postes(cd.CONTIENT, numerote=True)
    preparer = "\n".join(
        "            <li><strong>%s</strong> — %s</li>" % (t, x)
        for t, x in cd.PREPARER
    )
    # Les questions en un seul bloc, un onglet par moment du projet :
    # quatre sections de dépliants à la suite se lisaient comme une
    # seule liste sans fin.
    questions = repli.onglets(
        [(groupe["nom"], briques.questions_liste(groupe["questions"]))
         for groupe in cq.GROUPES],
        "Les questions, par moment du projet",
    )
    return f"""
  <section class="section" aria-labelledby="tDemande">
    <div class="zone">
{briques.intercalaire("Votre demande", "Visite gratuite, sans engagement",
                      "Décrivez|votre projet",
                      "Une minute suffit. Nous nous déplaçons, mesurons et "
                      "vous remettons un devis détaillé et gratuit.")}

      <div class="grille12 demande__grille pleine-largeur">
        {fragment('formulaire')}
        {fragment('coordonnees')}
      </div>
    </div>
  </section>

  <section class="section sur-sombre" aria-labelledby="tContient">
    <div class="zone">
{briques.intercalaire("Le devis", "Ce qui doit y figurer",
                      "Ce que contient|notre devis",
                      "Un devis de rénovation se lit poste par poste. Voici "
                      "ce que vous trouverez dans le nôtre, et ce qu'il faut "
                      "chercher dans n'importe quel autre.")}
{contient}
    </div>
  </section>

  <section class="section" aria-labelledby="tComparer">
    <div class="zone">
{briques.intercalaire("Comparer", "Deux devis, deux chantiers",
                      "Comment comparer|deux devis",
                      "Un écart de trente pour cent entre deux devis ne "
                      "signifie presque jamais que l'un est trop cher. Il "
                      "signifie qu'ils ne décrivent pas le même travail.")}
{repli.replis([(p.split(".")[0] + ".", "<p>%s</p>" % p)
                for p in cd.COMPARER])}
    </div>
  </section>

  <section class="section" aria-labelledby="tPreparer">
    <div class="zone">
{briques.intercalaire("La visite", "Ce qui fait gagner du temps",
                      "Ce qu'il faut|préparer")}
      <div class="service__deux">
        <div class="service__texte">
          <p>La visite dure entre trente minutes et une heure et demie selon
          l'ampleur du projet. Cinq éléments préparés à l'avance suffisent à
          la rendre nettement plus utile — et le devis nettement plus juste.</p>
          <p>Rien n'est obligatoire : venir sans rien ne nous empêchera pas
          de relever et de chiffrer.</p>
        </div>
        <aside class="encadre">
          <p class="etiquette encadre__titre">À rassembler avant notre passage</p>
          <ul class="encadre__liste">
{preparer}
          </ul>
        </aside>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tQuestions">
    <div class="zone">
{briques.intercalaire("Questions", "Du premier appel à la livraison",
                      "Les questions|qu'on nous pose")}
{questions}
    </div>
  </section>
"""

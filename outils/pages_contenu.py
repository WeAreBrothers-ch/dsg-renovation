"""Corps des pages réalisations, références, questions et devis.

Chaque page mêle les blocs du dossier d'origine — les six fiches de
chantier, les logos, les témoignages — et du contenu écrit pour elle.
"""

import briques
import briques_bis
import contenu_devis as cd
import contenu_divers as div
import contenu_questions as cq
from pages_site import fragment


def realisations(services, base=""):
    """Le registre des chantiers, les familles de biens, les imprévus."""
    return f"""
  <section class="section" aria-labelledby="tFiches">
    <div class="zone">
{briques.intercalaire("N° 01", "Registre", "Six chantiers livrés",
                      "Le registre|des chantiers",
                      "Chaque fiche donne le relevé complet du chantier. "
                      "Dépliez-la pour lire le détail des travaux, ou "
                      "agrandissez la vue.")}
      {fragment('filtres')}
      {fragment('chantiers')}
      <p class="chantiers__vide chapo" id="aucunChantier" hidden>Aucune fiche ne correspond à ce filtre pour le moment.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="tSignature">
    <div class="zone">
{briques.intercalaire("N° 02", "Pièce jointe", "Chantier signature",
                      "Six appartements,|en site occupé")}
      {fragment('signature')}
    </div>
  </section>

  <section class="section" aria-labelledby="tBiens">
    <div class="zone">
{briques.intercalaire("N° 03", "Familles", "Ce que nous reprenons dans la région",
                      "Trois types de biens,|trois chantiers différents",
                      "Un appartement de Sous-Gare, une villa de Chailly et "
                      "un immeuble de rendement ne se rénovent pas de la "
                      "même façon, ni pour les mêmes raisons.")}
{briques_bis.cartes(div.BIENS)}
    </div>
  </section>

  <section class="section" aria-labelledby="tSurprises">
    <div class="zone">
{briques.intercalaire("N° 04", "Imprévus", "Ce qu'on découvre en ouvrant",
                      "Ce qu'il y a|derrière les murs",
                      "Dans un logement ancien, la dépose réserve toujours "
                      "quelque chose. Les quatre cas ci-dessous reviennent "
                      "sur un chantier lausannois sur deux.")}
{briques_bis.frise(div.SURPRISES, avec_cote=False)}
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
    un devis, pas lire. Le reste répond à ceux qui hésitent encore.
    """
    contient = "\n".join(
        f"""        <li class="temps revele trace">
          <span class="temps__n">{i:02d}</span>
          <div class="temps__corps">
            <h3 class="h4">{titre}</h3>
            <p class="temps__texte">{texte}</p>
          </div>
        </li>"""
        for i, (titre, texte) in enumerate(cd.CONTIENT, 1)
    )
    preparer = "\n".join(
        "            <li><strong>%s</strong> — %s</li>" % (t, x)
        for t, x in cd.PREPARER
    )
    groupes = "".join(
        f"""
  <section class="section" aria-label="{groupe['nom']}">
    <div class="zone">
{briques.intercalaire(groupe["numero"], groupe["nom"], groupe["cote"],
                      groupe["titre"])}
{briques.questions_liste(groupe["questions"])}
    </div>
  </section>
"""
        for groupe in cq.GROUPES
    )
    return f"""
  <section class="section" aria-labelledby="tBordereau">
    <div class="zone">
{briques.intercalaire("N° 01", "Demande", "Réponse sous 72 heures ouvrables",
                      "Le bordereau|de demande",
                      "Décrivez votre projet en une minute. Nous nous "
                      "déplaçons, mesurons et vous remettons un devis détaillé "
                      "et gratuit.")}

      <div class="grille12 demande__grille">
        {fragment('formulaire')}
        {fragment('coordonnees')}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tContient">
    <div class="zone">
{briques.intercalaire("N° 02", "Le devis", "Ce qui doit y figurer",
                      "Ce que contient|notre devis",
                      "Un devis de rénovation se lit poste par poste. Voici "
                      "ce que vous trouverez dans le nôtre, et ce qu'il faut "
                      "chercher dans n'importe quel autre.")}
      <ol class="frise">
{contient}
      </ol>
    </div>
  </section>

  <section class="section" aria-labelledby="tComparer">
    <div class="zone">
{briques.intercalaire("N° 03", "Comparer", "Deux devis, deux chantiers",
                      "Comment comparer|deux devis",
                      "Un écart de trente pour cent entre deux devis ne "
                      "signifie presque jamais que l'un est trop cher. Il "
                      "signifie qu'ils ne décrivent pas le même travail.")}
{briques_bis.liste_sobre(cd.COMPARER)}
    </div>
  </section>

  <section class="section" aria-labelledby="tPreparer">
    <div class="zone">
{briques.intercalaire("N° 04", "La visite", "Ce qui fait gagner du temps",
                      "Ce qu'il faut|préparer")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>La visite dure entre trente minutes et une heure et demie selon
          l'ampleur du projet. Cinq éléments préparés à l'avance suffisent à
          la rendre nettement plus utile — et le devis nettement plus juste.</p>
          <p>Rien n'est obligatoire : venir sans rien ne nous empêchera pas
          de relever et de chiffrer.</p>
        </div>
        <aside class="encadre trace">
          <p class="etiquette encadre__titre">À rassembler avant notre passage</p>
          <ul class="encadre__liste">
{preparer}
          </ul>
        </aside>
      </div>
    </div>
  </section>
{groupes}"""

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


def references(services, base=""):
    """Partenaires, témoignages, modes de collaboration, réciprocité."""
    reciproque = "\n".join(
        "            <li>%s</li>" % p for p in div.RECIPROQUE
    )
    return f"""
  <section class="partenaires" aria-labelledby="tPartenaires">
    <div class="zone">
{briques.intercalaire("N° 01", "Partenaires", "Régies, propriétaires et architectes",
                      "Régies, architectes|et propriétaires",
                      "Une partie de notre activité vient de clients qui nous "
                      "rappellent. C'est la seule référence qui vaille dans "
                      "un métier où tout se sait vite.")}
      <div class="service__texte revele" style="margin-bottom:var(--sp-7)">
        <p>Les grandes régies de la place lausannoise nous confient des
        remises en état entre deux locations, parfois plusieurs logements du
        même immeuble sur une même année. Ce sont des chantiers courts,
        cadrés par une date de libération, où la fiabilité compte davantage
        que le prix : un logement rendu en retard, c'est un mois de loyer
        perdu pour le propriétaire.</p>
        <p>Les architectes nous confient l'exécution de lots sur descriptif.
        Les propriétaires privés, eux, nous appellent le plus souvent après
        une recommandation de voisinage — et repassent pour la pièce
        suivante deux ans plus tard.</p>
      </div>
      {fragment('partenaires')}
    </div>
  </section>

  <section class="section" aria-labelledby="tTemoins">
    <div class="zone">
{briques.intercalaire("N° 02", "Retours", "Ce que disent nos clients",
                      "Trois chantiers,|trois avis")}
      {fragment('temoins')}
    </div>
  </section>

  <section class="section" aria-labelledby="tModes">
    <div class="zone">
{briques.intercalaire("N° 03", "Collaborations", "Selon qui commande",
                      "Trois façons|de travailler avec nous",
                      "Une régie, un architecte et un propriétaire n'attendent "
                      "pas la même chose. Nous n'organisons donc pas le "
                      "chantier de la même manière.")}
{briques_bis.cartes(div.COLLABORATIONS)}
    </div>
  </section>

  <section class="section" aria-labelledby="tReciproque">
    <div class="zone">
{briques.intercalaire("N° 04", "En retour", "Ce qui fait tenir un planning",
                      "Ce que nous vous|demandons")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Un chantier tenu n'est jamais le fait de l'entreprise seule. Ces
          quatre points paraissent évidents ; ce sont pourtant eux qui font
          déraper les plannings, bien plus souvent que les imprévus
          techniques.</p>
          <p>Nous préférons les écrire au début plutôt que de les reprocher à
          la fin.</p>
        </div>
        <aside class="encadre trace">
          <p class="etiquette encadre__titre">Quatre choses qui font gagner des jours</p>
          <ul class="encadre__liste">
{reciproque}
          </ul>
        </aside>
      </div>
    </div>
  </section>
""" + briques.appel(
        base,
        "Un parc à entretenir ?",
        "Nous établissons des devis par logement et intervenons au fil des "
        "relocations, avec une date de libération ferme.",
    )


def questions(services, base=""):
    """Vingt questions, groupées par moment du projet."""
    sections = []
    for groupe in cq.GROUPES:
        sections.append(f"""
  <section class="section" aria-label="{groupe['nom']}">
    <div class="zone">
{briques.intercalaire(groupe["numero"], groupe["nom"], groupe["cote"],
                      groupe["titre"])}
{briques.questions_liste(groupe["questions"])}
    </div>
  </section>
""")
    liens = "\n".join(
        '          <li><a href="%sservices/%s.html">%s</a></li>'
        % (base, s["slug"], s["nom"])
        for s in services
    )
    sections.append(f"""
  <section class="section" aria-labelledby="tParLot">
    <div class="zone">
{briques.intercalaire("N° 05", "Par lot", "Questions propres à chaque métier",
                      "Une question|sur un lot précis ?")}
      <div class="service__deux revele">
        <div class="service__texte">
          <p>Chaque page de prestation porte les questions propres à son
          métier : durée, préparation des supports, compatibilité des
          matériaux, contraintes d'un logement occupé, et ce que le bâti
          lausannois impose à ce lot en particulier.</p>
          <p>Si votre question n'y figure pas, appelez-nous. Nous répondons
          plus vite au téléphone que par écrit.</p>
        </div>
        <ul class="lots service__villes">
{liens}
        </ul>
      </div>
    </div>
  </section>
""")
    return "".join(sections) + briques.appel(
        base,
        "Une question sans réponse ?",
        "Posez-la directement. Un appel de cinq minutes évite souvent une "
        "visite inutile, dans un sens comme dans l'autre.",
    )


def devis(services, base=""):
    """Ce que contient un devis, comment le comparer, puis le bordereau."""
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
    return f"""
  <section class="section" aria-labelledby="tContient">
    <div class="zone">
{briques.intercalaire("N° 01", "Le devis", "Ce qui doit y figurer",
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
{briques.intercalaire("N° 02", "Comparer", "Deux devis, deux chantiers",
                      "Comment comparer|deux devis",
                      "Un écart de trente pour cent entre deux devis ne "
                      "signifie presque jamais que l'un est trop cher. Il "
                      "signifie qu'ils ne décrivent pas le même travail.")}
{briques_bis.liste_sobre(cd.COMPARER)}
    </div>
  </section>

  <section class="section" aria-labelledby="tPreparer">
    <div class="zone">
{briques.intercalaire("N° 03", "La visite", "Ce qui fait gagner du temps",
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

  <section class="section" aria-labelledby="tBordereau">
    <div class="zone">
{briques.intercalaire("N° 04", "Demande", "Réponse sous 72 heures ouvrables",
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
"""

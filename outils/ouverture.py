"""L'image d'ouverture : cadrée dans la colonne, puis élargie au défilement.

Il sert aux pages de prestation, autour du tirage du métier (l'accueil
montre son comparateur à côté du titre, sans ouverture). Les deux
rideaux couleur du fond masquent les bords de l'image ;
assets/js/ouverture.js les écarte à mesure qu'on descend. Sans script,
ou si le visiteur demande moins de mouvement, l'image reste simplement
cadrée.
"""


def ouverture(contenu, legende, variante=""):
    """Enveloppe `contenu` (image ou comparateur) dans le cadre d'ouverture.

    `legende` est du HTML déjà échappé, affiché sous l'image (voir
    « Légende » dans assets/css/10-comparateur.css).
    """
    classe = "ouverture ouverture--%s" % variante if variante else "ouverture"
    return f"""  <figure class="{classe}" data-ouverture>
    <div class="ouverture__cadre">
      {contenu}
      <span class="ouverture__rideau ouverture__rideau--g" aria-hidden="true"></span>
      <span class="ouverture__rideau ouverture__rideau--d" aria-hidden="true"></span>
    </div>
    <figcaption class="zone legende">{legende}</figcaption>
  </figure>"""

"""L'image d'ouverture : cadrée dans la colonne, puis élargie au défilement.

Le même bloc sert à l'accueil (autour du comparateur avant / après) et
aux pages de prestation (autour du tirage du métier). Les deux rideaux
couleur plâtre masquent les bords de l'image ; assets/js/ouverture.js
les écarte à mesure qu'on descend. Sans script, ou si le visiteur
demande moins de mouvement, l'image reste simplement cadrée.
"""


def ouverture(contenu, legende, variante=""):
    """Enveloppe `contenu` (image ou comparateur) dans le cadre d'ouverture.

    `legende` est du HTML déjà échappé, affiché sous l'image.
    """
    classe = "ouverture ouverture--%s" % variante if variante else "ouverture"
    return f"""  <figure class="{classe}" data-ouverture>
    <div class="ouverture__cadre">
      {contenu}
      <span class="ouverture__rideau ouverture__rideau--g" aria-hidden="true"></span>
      <span class="ouverture__rideau ouverture__rideau--d" aria-hidden="true"></span>
    </div>
    <figcaption class="zone ouverture__legende">{legende}</figcaption>
  </figure>"""

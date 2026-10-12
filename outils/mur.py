"""Le mur à l'entrée : un mur dessiné en élévation, à casser pour entrer.

Le visiteur qui arrive sur le site trouve un mur. Trois coups le
cassent (mur.js, 20-mur.css) : le premier fait tomber une brique, le
deuxième celles qui l'entourent, le troisième l'abat, et le site apparaît
derrière.

Le mur se dresse devant qui arrive de l'extérieur : d'un moteur de
recherche, d'un lien, d'un favori. Qui vient d'une page du site est
déjà entré, même dans un nouvel onglet ; une fois cassé, il ne revient
plus dans l'onglet, même au rechargement. Rien n'est gardé d'une visite
à l'autre (la politique de confidentialité le promet) : la seule trace
est en stockage de session, effacée avec l'onglet. L'adresse « ?mur »
le remonte à volonté, pour le montrer au client.

Rien ne dépend de lui. Le contenu est dans la page, derrière : sans
JavaScript, ou si mur.js ne s'exécute pas, il ne se monte jamais ou
tombe de lui-même au chargement complet. Il ne peut pas bloquer
l'entrée.
"""

from donnees_site import LOGO_AVIF, LOGO_HAUTEUR, LOGO_LARGEUR, LOGO_WEBP, MARQUE

# La même clé que mur.js.
CLE = "dsg-mur"

# Posé dans <head>, avant le premier rendu : décide si le mur se monte
# (classe « mur-ferme » : la page ne défile plus, le mur se montre dès
# qu'il est lu). Il se monte si l'onglet n'a pas encore cassé le mur et
# que la page précédente n'est pas du site, ou si l'adresse demande
# « ?mur ». Sinon, l'onglet est noté entré. Si mur.js ne s'est pas
# annoncé (« mur-pret ») au chargement complet, le mur se retire de
# lui-même, et annonce « mur:ouvert » comme mur.js (motion.js attend ce
# signal pour tracer).
SCRIPT_TETE = (
    '<script>(function(h){var k="%s",v=false,d=false,r=document.referrer;'
    'try{v=sessionStorage.getItem(k)==="1"}catch(e){}'
    'try{d=!!r&&new URL(r).origin===location.origin}catch(e){}'
    'if(/[?&]mur(=|&|$)/.test(location.search)||(!v&&!d)){'
    'h.classList.add("mur-ferme");'
    'addEventListener("load",function(){if(!h.classList.contains("mur-pret")){'
    'h.classList.remove("mur-ferme");var m=document.getElementById("mur");'
    'if(m){m.hidden=true}document.dispatchEvent(new Event("mur:ouvert"))}})}'
    'else{try{sessionStorage.setItem(k,"1")}catch(e){}}})(document.documentElement)</script>'
    % CLE
)

# Sur le mur, un cartouche de plan, dessiné comme le reste du site : un
# cadre d'un pixel, les repères d'angle du bloc qui ouvre, le logo de
# l'en-tête, le titre, puis une rangée de deux cases — trois carrés qui
# comptent les coups, le bouton. Le strict nécessaire : ce qui reste à
# frapper ne s'écrit que pour les lecteurs d'écran (murAnnonce, mis à
# jour par mur.js).

# Juste après le mur : il se montre avant que le reste de la page soit
# lu, aucune image du site ne passe avant lui.
_DEVOILER = (
    '<script>if(document.documentElement.classList.contains("mur-ferme"))'
    '{document.getElementById("mur").hidden=false}</script>'
)


def mur(base):
    """Le mur et son cartouche, en tête de <body>.

    Masqué (hidden) tant que le script de tête n'a pas décidé de le
    monter : sans JavaScript, il n'existe pas pour le visiteur.
    """
    return f"""<div class="mur" id="mur" role="dialog" aria-modal="true" aria-labelledby="murTitre" aria-describedby="murAnnonce" tabindex="-1" hidden>
  <canvas class="mur__briques" aria-hidden="true"></canvas>
  <div class="mur__cartouche">
    <div class="mur__tete">
      <picture><source type="image/avif" srcset="{base}{LOGO_AVIF}"><img class="mur__logo" src="{base}{LOGO_WEBP}" alt="{MARQUE}" width="{LOGO_LARGEUR}" height="{LOGO_HAUTEUR}"></picture>
      <p class="mur__titre" id="murTitre">Cassez le mur pour entrer.</p>
    </div>
    <p class="visuellement-cache" id="murAnnonce" aria-live="polite">Trois coups.</p>
    <div class="mur__bas">
      <ol class="mur__coups" aria-hidden="true"><li></li><li></li><li></li></ol>
      <button class="btn btn--plein mur__frapper" type="button" id="murFrapper">Frapper<span class="fleche" aria-hidden="true"></span></button>
    </div>
  </div>
</div>
{_DEVOILER}
"""

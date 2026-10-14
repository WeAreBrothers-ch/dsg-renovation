/* ============================================================
   DSG RÉNOVATION — TRAME DU RELEVÉ
   La nuit porte la trame du plan : un point tous les --trame-pas,
   comme le quadrillage du géomètre, que la feuille peint elle-même
   (--trame-fond, 00-jetons.css). Ici, dans la bande de noir nacré de
   chaque page et dans le pied, une onde carrée — un plan n'a pas
   d'angle arrondi — s'y propage au rouge écrit de la nuit depuis le
   point qu'on touche : la toile ne porte que l'onde, posée point pour
   point sur ceux de la feuille. Les cases de la bande n'ont pas de
   fond : l'onde passe sous elles comme la trame.

   Transposé du « Sonar Grid » de 21st.dev (composant React) : même
   idée, écrite pour ce site, sans dépendance.

   Le mouvement ne répond qu'à un geste, comme ailleurs sur le site.
   Seule exception, celle du comparateur : à sa première apparition,
   la bande montre une fois ce qu'elle sait faire — une onde déjà
   partie, une seconde qui la suit —, moins de cinq secondes en tout,
   puis la trame se tient immobile. Mouvement réduit : la trame et
   une onde figée, rien ne bouge. Sans JavaScript, pas d'onde : la
   trame de la feuille seule. Pur décor, la toile est cachée aux
   lecteurs d'écran et ne reçoit aucun clic.
   ============================================================ */
(function () {
  "use strict";

  var bandes = document.querySelectorAll("main .section.sur-sombre, .pied.sur-sombre");
  if (!bandes.length || !("getContext" in document.createElement("canvas"))) { return; }

  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  /* La feuille arrondit le milieu de la surface au pixel, si elle le
     peut (--trame-calage, 00-jetons.css) : la toile fait de même. */
  var calageArrondi = !!(window.CSS && CSS.supports && CSS.supports("width", "round(down, 1.5px, 1px)"));

  /* Une onde vit 3 s. Elle porte jusqu'à RAYON_MAX px au bureau, moins
     au téléphone (voir portee()). Sa crête allume les points sur un
     demi-pas en avant, et laisse derrière elle un sillage de SILLAGE
     pas qui s'éteint. */
  var DUREE_ONDE = 3000;
  var RAYON_MAX = 560;
  var AVANT = 0.6;
  var SILLAGE = 3;
  /* À l'arrivée : la première onde a déjà parcouru le huitième de sa
     vie, la seconde part après DELAI_SECONDE. Moins de cinq secondes
     de mouvement en tout. */
  var AVANCE_ARRIVEE = 0.12;
  var DELAI_SECONDE = 1200;
  /* Taille des points, en pixels CSS : au repos (--trame-taille), sur
     la crête. */
  var POINT = 2;
  var POINT_CRETE = 3.5;
  /* Des clics en rafale : au-delà de ONDES_MAX, la plus ancienne cède. */
  var ONDES_MAX = 6;

  /**
   * Courbe de sortie (--e-sortie, approchée) : l'onde part vite et se
   * pose. Jamais d'entrée lente.
   * @param {number} t
   * @returns {number}
   */
  function sortie(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  /**
   * Installe la trame sous le contenu d'une bande.
   * @param {HTMLElement} bande
   */
  function installer(bande) {
    var toile = document.createElement("canvas");
    toile.className = "trame";
    toile.setAttribute("aria-hidden", "true");
    bande.insertBefore(toile, bande.firstChild);

    var ctx = toile.getContext("2d");
    if (!ctx) { return; }

    var largeur = 0;
    var hauteur = 0;
    /* Premier nœud de la toile : là où la feuille pose ses points. */
    var origineX = 0;
    var origineY = 0;
    var densite = 1;
    var pas = 24;
    var couleurOnde = "";
    var ondes = [];
    var image = 0;
    var taille = "";

    function lireJetons() {
      var style = window.getComputedStyle(toile);
      pas = parseFloat(style.getPropertyValue("--trame-pas")) || 24;
      couleurOnde = style.getPropertyValue("--trame-onde").trim();
    }

    /* Reste positif d'une division : un nœud à gauche de la toile
       donne un premier nœud dans la toile, pas avant elle. */
    function modulo(a, b) {
      return ((a % b) + b) % b;
    }

    /* Ce dont dépendent les nœuds : la bande, au centième de pixel, et
       la densité de l'écran (un zoom la change). */
    function mesure() {
      var cadre = bande.getBoundingClientRect();
      return [cadre.width, cadre.height, window.devicePixelRatio || 1]
        .map(function (v) { return v.toFixed(2); }).join(" ");
    }

    /* Le milieu d'un côté de la bande, là où la feuille pose un point :
       arrondi au pixel inférieur comme --trame-calage (un point de
       --trame-taille dont le bord gauche tombe sur un pixel entier). */
    function milieu(cote) {
      var bord = cote / 2 - POINT / 2;
      return (calageArrondi ? Math.floor(bord) : bord) + POINT / 2;
    }

    /* La toile se mesure à la bande, à la densité réelle de l'écran
       (trois pixels par point au téléphone) : une toile plus grossière,
       agrandie, flouterait l'onde et la décalerait d'un pixel sur les
       points de la feuille. Ceux-ci sont centrés dans la bande
       (--trame-calage) : un point au milieu, les autres de pas en pas.
       La toile peut ne pas couvrir toute la bande (le pied la tient sous
       son filet rouge) : ses nœuds se comptent depuis le milieu de la
       bande, pas depuis le sien. Quand la bande change de hauteur, les
       points de la feuille se recentrent : les ondes en cours se
       reposent sur les nouveaux nœuds. */
    function dimensionner() {
      /* La toile reprend d'abord la mesure que lui donne la feuille
         (toute la bande), puis se fixe à un nombre entier de pixels
         d'écran : une bande de 474,4 px en fait 1423,2, la toile n'en
         a que 1423, et le navigateur l'étirerait d'un rien — l'onde
         baverait d'un pixel au bas de la bande. Fixée par défaut, elle
         s'arrête un tiers de pixel plus tôt au plus, invisible, ne
         déborde jamais de la bande et ne s'étire jamais. */
      toile.style.width = "";
      toile.style.height = "";
      densite = Math.min(window.devicePixelRatio || 1, 3);
      var boite = toile.getBoundingClientRect();
      var cadre = bande.getBoundingClientRect();
      toile.width = Math.max(1, Math.floor(boite.width * densite + 0.01));
      toile.height = Math.max(1, Math.floor(boite.height * densite + 0.01));
      largeur = toile.width / densite;
      hauteur = toile.height / densite;
      toile.style.width = largeur + "px";
      toile.style.height = hauteur + "px";
      taille = mesure();
      lireJetons();
      origineX = modulo(milieu(cadre.width) - (boite.left - cadre.left), pas);
      origineY = modulo(milieu(cadre.height) - (boite.top - cadre.top), pas);
      ondes.forEach(function (onde) {
        var centre = noeud(onde.x, onde.y);
        onde.x = centre.x;
        onde.y = centre.y;
      });
      dessiner(performance.now());
    }

    /**
     * Ramène un point de la bande au nœud de trame le plus proche :
     * l'onde part d'un piquet, et ses côtés suivent les rangées.
     * @param {number} x
     * @param {number} y
     * @returns {{x: number, y: number}}
     */
    function noeud(x, y) {
      return {
        x: origineX + Math.round((x - origineX) / pas) * pas,
        y: origineY + Math.round((y - origineY) / pas) * pas
      };
    }

    /* La portée suit la largeur de la bande : 296 px au téléphone, la
       moitié de la bande environ au bureau. */
    function portee() {
      return Math.min(largeur * 0.4 + 140, RAYON_MAX);
    }

    /**
     * Pose une onde ; `age` (0 à 1) la fait partir déjà avancée.
     * @param {number} x
     * @param {number} y
     * @param {number} age
     */
    function lancer(x, y, age) {
      var centre = noeud(x, y);
      ondes.push({
        x: centre.x,
        y: centre.y,
        depart: performance.now() - age * DUREE_ONDE,
        portee: portee()
      });
      if (ondes.length > ONDES_MAX) { ondes.shift(); }
      if (!image) { image = window.requestAnimationFrame(boucle); }
    }

    /**
     * Pose sur la toile les points qu'une onde allume.
     * @param {{x: number, y: number, portee: number}} onde
     * @param {number} t  avancée de l'onde, de 0 à 1
     */
    function dessinerOnde(onde, t) {
      var rayon = sortie(t) * onde.portee;
      var force = Math.pow(1 - t, 0.9);
      var avant = pas * AVANT;
      var sillage = pas * SILLAGE;
      var x0 = origineX;
      var y0 = origineY;
      var exterieur = rayon + avant;
      /* On ne parcourt que les nœuds du carré qu'atteint l'onde. */
      var colMin = Math.max(0, Math.ceil((onde.x - exterieur - x0) / pas));
      var colMax = Math.floor((Math.min(largeur, onde.x + exterieur) - x0) / pas);
      var rangMin = Math.max(0, Math.ceil((onde.y - exterieur - y0) / pas));
      var rangMax = Math.floor((Math.min(hauteur, onde.y + exterieur) - y0) / pas);
      ctx.fillStyle = couleurOnde;
      for (var r = rangMin; r <= rangMax; r++) {
        var y = y0 + r * pas;
        for (var c = colMin; c <= colMax; c++) {
          var x = x0 + c * pas;
          /* Distance de plan : le plus grand des deux écarts, d'où
             une onde carrée. `ecart` est positif derrière la crête. */
          var ecart = rayon - Math.max(Math.abs(x - onde.x), Math.abs(y - onde.y));
          if (ecart < -avant || ecart > sillage) { continue; }
          var k = ecart < 0 ? 1 + ecart / avant : Math.pow(1 - ecart / sillage, 2);
          var cote = POINT + (POINT_CRETE - POINT) * k;
          ctx.globalAlpha = k * force;
          poser(x, y, cote);
        }
      }
      ctx.globalAlpha = 1;
    }

    /**
     * Pose un point carré centré sur un nœud, en pixels d'écran entiers.
     * Le navigateur peint un point de la feuille sur les pixels dont le
     * centre tombe dans le point : on arrondit de même, et au repos
     * (--trame-taille) le point de l'onde couvre exactement celui de la
     * feuille, sans liseré.
     * @param {number} x  nœud, en pixels CSS de la toile
     * @param {number} y
     * @param {number} cote  côté du point, en pixels CSS
     */
    function poser(x, y, cote) {
      var c = Math.max(1, Math.round(cote * densite));
      var gauche = Math.ceil(x * densite - c / 2 - 0.5);
      var haut = Math.ceil(y * densite - c / 2 - 0.5);
      ctx.fillRect(gauche, haut, c, c);
    }

    function dessiner(maintenant) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, toile.width, toile.height);
      ondes = ondes.filter(function (onde) {
        var t = onde.fige !== undefined ? onde.fige : (maintenant - onde.depart) / DUREE_ONDE;
        if (t >= 1) { return false; }
        dessinerOnde(onde, Math.max(0, t));
        return true;
      });
    }

    function boucle(maintenant) {
      dessiner(maintenant);
      var enCours = ondes.some(function (onde) { return onde.fige === undefined; });
      image = enCours ? window.requestAnimationFrame(boucle) : 0;
    }

    /* Le premier repère de l'onde d'arrivée : dans le haut de la bande,
       aux deux tiers de sa largeur, là où le texte laisse de l'air. */
    function arrivee() {
      lancer(largeur * 0.72, Math.min(hauteur * 0.3, 260), AVANCE_ARRIVEE);
      window.setTimeout(function () {
        lancer(largeur * 0.88, Math.min(hauteur * 0.55, 420), 0);
      }, DELAI_SECONDE);
    }

    dimensionner();

    /* La bande change de taille (écran tourné, « Lire la suite »
       déplié, polices arrivées) : la toile se remet à sa nouvelle
       mesure. La mesure exacte de la bande compte, pas seulement celle
       de la toile : un quart de pixel de hauteur peut déplacer d'un
       pixel le milieu où la feuille pose ses points. */
    if ("ResizeObserver" in window) {
      new ResizeObserver(function () {
        if (mesure() !== taille) { dimensionner(); }
      }).observe(bande);
    }

    if (mouvementReduit) {
      /* Le relevé figé : une onde arrêtée à mi-course, sans mouvement. */
      var centre = noeud(largeur * 0.72, Math.min(hauteur * 0.3, 260));
      ondes.push({
        x: centre.x, y: centre.y, fige: 0.35,
        portee: portee()
      });
      dessiner(performance.now());
      return;
    }

    /* Un toucher sans défilement, un clic : l'onde part de là. Les
       liens et les boutons gardent leur geste à eux. */
    bande.addEventListener("click", function (evenement) {
      var cible = evenement.target;
      if (cible instanceof Element && cible.closest("a, button, input, select, textarea, label")) { return; }
      var boite = toile.getBoundingClientRect();
      lancer(evenement.clientX - boite.left, evenement.clientY - boite.top, 0);
    });

    /* L'arrivée se joue quand le haut de la bande atteint les deux
       cinquièmes de l'écran : la première onde est alors en vue, même
       au téléphone, quelle que soit la hauteur de la bande. */
    if (!("IntersectionObserver" in window)) { return; }
    var observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) { return; }
        observateur.disconnect();
        arrivee();
      });
    }, { rootMargin: "0px 0px -60% 0px" });
    observateur.observe(bande);
  }

  Array.prototype.forEach.call(bandes, function (bande) {
    if (bande instanceof HTMLElement) { installer(bande); }
  });
}());

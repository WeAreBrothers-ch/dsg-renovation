/* ============================================================
   DSG RÉNOVATION — TRAME DU RELEVÉ
   La bande de noir nacré de chaque page porte la trame du plan : un
   point tous les --trame-pas, comme le quadrillage du géomètre.
   Une onde carrée — un plan n'a pas d'angle arrondi — s'y propage au
   rouge écrit de la nuit depuis le point qu'on touche.

   Transposé du « Sonar Grid » de 21st.dev (composant React) : même
   idée, écrite pour ce site, sans dépendance.

   Le mouvement ne répond qu'à un geste, comme ailleurs sur le site.
   Seule exception, celle du comparateur : à sa première apparition,
   la bande montre une fois ce qu'elle sait faire — une onde déjà
   partie, une seconde qui la suit —, moins de cinq secondes en tout,
   puis la trame se tient immobile. Mouvement réduit : la trame et
   une onde figée, rien ne bouge. Sans JavaScript, ni l'une ni
   l'autre : le fond nacré seul, comme avant. Pur décor, la toile est
   cachée aux lecteurs d'écran et ne reçoit aucun clic.
   ============================================================ */
(function () {
  "use strict";

  var bandes = document.querySelectorAll("main .section.sur-sombre");
  if (!bandes.length || !("getContext" in document.createElement("canvas"))) { return; }

  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

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
  /* Taille des points, en pixels CSS : au repos, sur la crête. */
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

    /* Le fond de la trame, dessiné une fois par taille : chaque image
       le recopie, puis pose les ondes dessus. */
    var fond = document.createElement("canvas");
    var ctxFond = fond.getContext("2d");

    var largeur = 0;
    var hauteur = 0;
    var densite = 1;
    var pas = 24;
    var couleurPoint = "";
    var couleurOnde = "";
    var ondes = [];
    var image = 0;
    var taille = "";

    function lireJetons() {
      var style = window.getComputedStyle(toile);
      pas = parseFloat(style.getPropertyValue("--trame-pas")) || 24;
      couleurPoint = style.getPropertyValue("--trame-point").trim();
      couleurOnde = style.getPropertyValue("--trame-onde").trim();
    }

    /* Décalage de la trame : centrée dans la bande, pour que ses bords
       tombent également à gauche et à droite. */
    function origine(cote) {
      return (cote - Math.floor(cote / pas) * pas) / 2;
    }

    function dimensionner() {
      var boite = toile.getBoundingClientRect();
      largeur = Math.round(boite.width);
      hauteur = Math.round(boite.height);
      taille = largeur + "x" + hauteur;
      densite = Math.min(window.devicePixelRatio || 1, 2);
      [toile, fond].forEach(function (c) {
        c.width = Math.max(1, Math.round(largeur * densite));
        c.height = Math.max(1, Math.round(hauteur * densite));
      });
      lireJetons();
      ctxFond.setTransform(densite, 0, 0, densite, 0, 0);
      ctxFond.clearRect(0, 0, largeur, hauteur);
      ctxFond.fillStyle = couleurPoint;
      var x0 = origine(largeur);
      var y0 = origine(hauteur);
      for (var y = y0; y <= hauteur; y += pas) {
        for (var x = x0; x <= largeur; x += pas) {
          ctxFond.fillRect(x - POINT / 2, y - POINT / 2, POINT, POINT);
        }
      }
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
      var x0 = origine(largeur);
      var y0 = origine(hauteur);
      return {
        x: x0 + Math.round((x - x0) / pas) * pas,
        y: y0 + Math.round((y - y0) / pas) * pas
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
      var x0 = origine(largeur);
      var y0 = origine(hauteur);
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
          ctx.fillRect(x - cote / 2, y - cote / 2, cote, cote);
        }
      }
      ctx.globalAlpha = 1;
    }

    function dessiner(maintenant) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, toile.width, toile.height);
      ctx.drawImage(fond, 0, 0);
      ctx.setTransform(densite, 0, 0, densite, 0, 0);
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
       déplié) : la trame se redessine à sa nouvelle mesure. */
    if ("ResizeObserver" in window) {
      new ResizeObserver(function () {
        var boite = toile.getBoundingClientRect();
        if (Math.round(boite.width) + "x" + Math.round(boite.height) !== taille) { dimensionner(); }
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

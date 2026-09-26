/* ============================================================
   DSG RÉNOVATION — COMPARATEUR AVANT / APRÈS
   Glissière accessible : souris, tactile et clavier (flèches,
   Origine, Fin). Sans JavaScript, la vue reste coupée à 50 %.

   À sa première apparition, la poignée fait d'elle-même un aller-
   retour lent : on comprend qu'elle se déplace avant même d'y
   toucher. Le geste s'interrompt au premier contact, et n'a pas
   lieu si le visiteur demande moins de mouvement.
   ============================================================ */
(function () {
  "use strict";

  var blocs = document.querySelectorAll("[data-comparateur]");
  if (!blocs.length) { return; }

  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Démonstration : trois étapes, depuis le centre. */
  var DEMO_ETAPES = [50, 34, 64, 50];
  var DEMO_DUREE_ETAPE = 700;
  var DEMO_DELAI = 450;

  /**
   * Courbe symétrique : départ et arrivée en douceur.
   * @param {number} t
   * @returns {number}
   */
  function adoucir(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  /**
   * Installe une glissière sur un bloc de comparaison.
   * @param {HTMLElement} bloc
   */
  function installer(bloc) {
    var poignee = bloc.querySelector(".comparateur__poignee");
    if (!(poignee instanceof HTMLElement)) { return; }

    var position = 50;
    var enCours = false;
    var demoEnCours = false;
    var demoFaite = false;

    /**
     * Applique une position en pourcentage, bornée à [0, 100].
     * @param {number} valeur
     */
    function placer(valeur) {
      position = Math.max(0, Math.min(100, valeur));
      bloc.style.setProperty("--pos", position.toFixed(2) + "%");
      poignee.setAttribute("aria-valuenow", String(Math.round(position)));
      /* L'état avant travaux occupe la gauche de la poignée, l'état
         livré la droite : on annonce la part de chacun. */
      var gauche = Math.round(position);
      poignee.setAttribute("aria-valuetext",
        "Avant travaux à gauche : " + gauche + " %, après travaux à droite : " + (100 - gauche) + " %");
    }

    /**
     * Convertit une abscisse écran en pourcentage de la largeur du bloc.
     * @param {number} x
     * @returns {number}
     */
    function depuisX(x) {
      var cadre = bloc.getBoundingClientRect();
      if (cadre.width === 0) { return position; }
      return ((x - cadre.left) / cadre.width) * 100;
    }

    function arreterDemo() {
      demoEnCours = false;
      demoFaite = true;
    }

    function lancerDemo() {
      if (demoFaite || mouvementReduit) { return; }
      demoEnCours = true;
      var depart = null;
      var total = DEMO_DUREE_ETAPE * (DEMO_ETAPES.length - 1);

      function pas(horodatage) {
        if (!demoEnCours) { return; }
        if (depart === null) { depart = horodatage; }
        var ecoule = Math.min(horodatage - depart, total);
        var rang = Math.min(Math.floor(ecoule / DEMO_DUREE_ETAPE), DEMO_ETAPES.length - 2);
        var t = adoucir((ecoule - rang * DEMO_DUREE_ETAPE) / DEMO_DUREE_ETAPE);
        placer(DEMO_ETAPES[rang] + (DEMO_ETAPES[rang + 1] - DEMO_ETAPES[rang]) * t);
        if (ecoule < total) {
          window.requestAnimationFrame(pas);
        } else {
          arreterDemo();
        }
      }
      window.requestAnimationFrame(pas);
    }

    bloc.addEventListener("pointerdown", function (evenement) {
      arreterDemo();
      enCours = true;
      try {
        bloc.setPointerCapture(evenement.pointerId);
      } catch (erreur) {
        /* Capture refusée (pointeur déjà relâché) : le glissement
           continue tant que le pointeur reste sur le bloc. */
      }
      placer(depuisX(evenement.clientX));
    });

    bloc.addEventListener("pointermove", function (evenement) {
      if (!enCours) { return; }
      evenement.preventDefault();
      placer(depuisX(evenement.clientX));
    });

    /**
     * @param {PointerEvent} evenement
     */
    function relacher(evenement) {
      if (!enCours) { return; }
      enCours = false;
      if (bloc.hasPointerCapture(evenement.pointerId)) {
        bloc.releasePointerCapture(evenement.pointerId);
      }
    }
    bloc.addEventListener("pointerup", relacher);
    bloc.addEventListener("pointercancel", relacher);

    poignee.addEventListener("focus", arreterDemo);
    poignee.addEventListener("keydown", function (evenement) {
      var pas = evenement.shiftKey ? 10 : 2;
      var touches = { ArrowLeft: -pas, ArrowDown: -pas, ArrowRight: pas, ArrowUp: pas };

      if (Object.prototype.hasOwnProperty.call(touches, evenement.key)) {
        evenement.preventDefault();
        placer(position + touches[evenement.key]);
      } else if (evenement.key === "Home") {
        evenement.preventDefault();
        placer(0);
      } else if (evenement.key === "End") {
        evenement.preventDefault();
        placer(100);
      }
    });

    placer(50);

    if (mouvementReduit || !("IntersectionObserver" in window)) { return; }
    var observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) { return; }
        observateur.disconnect();
        window.setTimeout(lancerDemo, DEMO_DELAI);
      });
    }, { threshold: 0.5 });
    observateur.observe(bloc);
  }

  Array.prototype.forEach.call(blocs, function (bloc) {
    if (bloc instanceof HTMLElement) { installer(bloc); }
  });
}());

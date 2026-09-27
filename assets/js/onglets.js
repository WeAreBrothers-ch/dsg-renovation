/* ============================================================
   DSG RÉNOVATION — ONGLETS
   Un jeu d'onglets ne montre qu'un panneau à la fois. Sans
   JavaScript, tous les panneaux restent visibles et la barre
   d'onglets ne s'affiche pas : le contenu est intégralement
   lisible, et intégralement indexé.
   ============================================================ */
(function () {
  "use strict";

  /* Au téléphone, les dépliants marqués data-replie-telephone partent
     fermés : la page se lit en intitulés, on ouvre ce qu'on veut lire.
     Ils sont tous sous le premier écran : les refermer ne fait rien
     bouger sous les yeux. Sans script, ou sur un écran plus large, ils
     restent ouverts. */
  if (!window.matchMedia("(min-width: 768px)").matches) {
    Array.prototype.forEach.call(document.querySelectorAll("details[data-replie-telephone]"), function (depliant) {
      depliant.open = false;
    });
  }

  /* Lire la suite (outils/lecture.py) : le texte se déplie en entier,
     le bouton s'efface, et le focus passe au premier paragraphe
     révélé, d'où le clavier et les lecteurs d'écran reprennent. */
  Array.prototype.forEach.call(document.querySelectorAll("[data-plie]"), function (bloc) {
    var bouton = bloc.querySelector(".plie__bouton");
    if (!bouton) { return; }
    bouton.addEventListener("click", function () {
      bloc.classList.add("est-deplie");
      var suite = bloc.children[1];
      if (suite instanceof HTMLElement) {
        suite.setAttribute("tabindex", "-1");
        suite.focus({ preventScroll: true });
      }
    });
  });

  /* Suites à faire glisser (16-composants.css) : au téléphone, le
     déroulé et les cartes défilent de côté. Tant qu'une suite déborde,
     elle prend le focus, pour se laisser parcourir au clavier ; elle le
     rend dès qu'elle retrouve sa grille. Les besoins, eux, sont des
     liens : le focus les fait déjà venir. */
  var suites = document.querySelectorAll(".etapes, .cartes");
  function focaliserSuites() {
    Array.prototype.forEach.call(suites, function (suite) {
      /* Les repères d'angle de la grille débordent d'un demi-repère :
         seule une suite qui défile vraiment compte. */
      var defile = window.getComputedStyle(suite).overflowX !== "visible";
      if (defile && suite.scrollWidth > suite.clientWidth + 1) {
        suite.setAttribute("tabindex", "0");
      } else {
        suite.removeAttribute("tabindex");
      }
    });
  }
  if (suites.length) {
    focaliserSuites();
    window.addEventListener("resize", focaliserSuites);
  }

  var jeux = document.querySelectorAll("[data-onglets]");
  if (!jeux.length) { return; }

  /**
   * Active un panneau et désactive les autres.
   * @param {Array<HTMLElement>} boutons
   * @param {Array<HTMLElement>} panneaux
   * @param {number} rang
   */
  function activer(boutons, panneaux, rang) {
    boutons.forEach(function (bouton, i) {
      var actif = i === rang;
      bouton.setAttribute("aria-selected", actif ? "true" : "false");
      bouton.setAttribute("tabindex", actif ? "0" : "-1");
    });
    panneaux.forEach(function (panneau, i) {
      panneau.hidden = i !== rang;
    });
  }

  Array.prototype.forEach.call(jeux, function (jeu) {
    var barre = jeu.querySelector("[data-onglets-barre]");
    var boutons = Array.prototype.slice.call(jeu.querySelectorAll("[data-onglet]"));
    var panneaux = Array.prototype.slice.call(jeu.querySelectorAll("[data-panneau]"));
    if (!barre || boutons.length < 2 || boutons.length !== panneaux.length) { return; }

    /* La barre n'existe que si le script tourne : sans lui, elle
       n'aurait aucun effet et n'afficherait que du bruit. */
    barre.hidden = false;

    boutons.forEach(function (bouton, rang) {
      bouton.addEventListener("click", function () {
        activer(boutons, panneaux, rang);
      });

      /* Flèches gauche et droite : le déplacement attendu dans une
         barre d'onglets, imposé par la norme d'accessibilité. */
      bouton.addEventListener("keydown", function (evenement) {
        var pas = 0;
        if (evenement.key === "ArrowRight") { pas = 1; }
        if (evenement.key === "ArrowLeft") { pas = -1; }
        if (pas === 0) { return; }
        evenement.preventDefault();
        var cible = (rang + pas + boutons.length) % boutons.length;
        activer(boutons, panneaux, cible);
        boutons[cible].focus();
      });
    });

    activer(boutons, panneaux, 0);
  });
}());

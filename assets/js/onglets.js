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

  /* Lire la suite (outils/lecture.py) : le texte se déplie en entier
     et le bouton devient « Réduire » ; à l'ouverture, le focus passe
     au premier paragraphe révélé. Replié, le texte ramène l'écran à
     son début s'il était passé au-dessus. */
  Array.prototype.forEach.call(document.querySelectorAll("[data-plie]"), function (bloc) {
    var bouton = bloc.querySelector(".plie__bouton");
    var libelle = bloc.querySelector(".plie__texte");
    if (!bouton || !libelle) { return; }
    bouton.addEventListener("click", function () {
      var ouvrir = !bloc.classList.contains("est-deplie");
      bloc.classList.toggle("est-deplie", ouvrir);
      bouton.setAttribute("aria-expanded", String(ouvrir));
      libelle.textContent = ouvrir ? "Réduire" : "Lire la suite";
      if (ouvrir) {
        var suite = bloc.children[1];
        if (suite instanceof HTMLElement) {
          suite.setAttribute("tabindex", "-1");
          suite.focus({ preventScroll: true });
        }
      } else if (bloc.getBoundingClientRect().top < 0) {
        bloc.scrollIntoView({ block: "start" });
      }
    });
  });

  /* Suites à faire glisser (16-composants.css) : au téléphone, le
     déroulé, les cartes et les besoins défilent de côté. Tant qu'une
     suite défile, elle prend le focus pour se laisser parcourir au
     clavier — sauf les besoins, qui sont des liens : le focus les fait
     déjà venir —, et sa rangée de repères (écrite dans la page,
     outils/briques_bis.reperes) marque la case à l'écran : un carré
     par case, celui-là s'allonge. Ce n'est qu'une indication
     (aria-hidden). Dès que la suite retrouve sa grille, elle rend le
     focus et la feuille masque la rangée ; quand elle défile de
     nouveau (écran tourné), la marque se recale sur la case à
     l'écran. */
  var suites = Array.prototype.map.call(document.querySelectorAll(".etapes, .cartes, .besoins"), function (suite) {
    var reperes = suite.nextElementSibling;
    return {
      suite: suite,
      reperes: reperes && reperes.classList.contains("suite__reperes") ? reperes : null,
      focalisable: !suite.classList.contains("besoins"),
      actif: 0,
      attente: 0
    };
  });

  /* Seule une suite qui défile vraiment compte : une grille dont un
     contour déborde d'un pixel ne se parcourt pas. */
  function defile(suite) {
    return window.getComputedStyle(suite).overflowX !== "visible" &&
      suite.scrollWidth > suite.clientWidth + 1;
  }

  /** @param {{suite: Element, reperes: Element, actif: number, attente: number}} s */
  function marquer(s) {
    s.attente = 0;
    var cases = s.suite.children;
    if (!s.reperes || cases.length < 2 || !defile(s.suite)) { return; }
    var pas = cases[1].offsetLeft - cases[0].offsetLeft;
    if (pas <= 0) { return; }
    /* Au bout de la course, la dernière case est entière à l'écran sans
       avoir pu s'aligner sur la marge : c'est elle qu'on regarde. */
    var fin = s.suite.scrollLeft >= s.suite.scrollWidth - s.suite.clientWidth - 2;
    var rang = fin ? cases.length - 1 : Math.round(s.suite.scrollLeft / pas);
    if (rang === s.actif) { return; }
    s.reperes.children[s.actif].removeAttribute("data-actif");
    s.reperes.children[rang].setAttribute("data-actif", "");
    s.actif = rang;
  }

  function ajusterSuites() {
    suites.forEach(function (s) {
      if (s.focalisable) {
        if (defile(s.suite)) {
          s.suite.setAttribute("tabindex", "0");
        } else {
          s.suite.removeAttribute("tabindex");
        }
      }
      marquer(s);
    });
  }

  suites.forEach(function (s) {
    s.suite.addEventListener("scroll", function () {
      if (!s.attente) {
        s.attente = window.requestAnimationFrame(function () { marquer(s); });
      }
    }, { passive: true });
  });
  if (suites.length) {
    ajusterSuites();
    window.addEventListener("resize", ajusterSuites);
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

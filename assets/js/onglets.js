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

  /* Glissières (16-composants.css, outils/briques_bis.glissiere) : au
     téléphone, déroulés, cartes et besoins défilent de côté. Tant
     qu'une suite défile, elle prend le focus pour se laisser parcourir
     au clavier — sauf si ses cases sont des liens : le focus les fait
     déjà venir —, et sa rangée de repères marque la case à l'écran (un
     carré par case, celui-là s'allonge ; une simple indication,
     aria-hidden). Les mesures ne changent qu'avec la taille de la
     suite : elles sont prises à ce moment-là (ResizeObserver), et le
     défilement ne lit plus que sa position. */
  var glissieres = Array.prototype.map.call(document.querySelectorAll(".glissiere"), function (suite) {
    return {
      suite: suite,
      reperes: suite.nextElementSibling,
      focalisable: !suite.querySelector("a[href]"),
      actif: 0,
      defile: false,
      pas: 0,
      course: 0
    };
  });

  /**
   * Marque la case à l'écran.
   * @param {{suite: Element, reperes: Element, actif: number, defile: boolean, pas: number, course: number}} g
   */
  function marquer(g) {
    if (!g.defile || g.pas <= 0) { return; }
    /* Au bout de la course, la dernière case est entière à l'écran sans
       avoir pu s'aligner sur la marge : c'est elle qu'on regarde. */
    var rang = g.suite.scrollLeft >= g.course - 2
      ? g.suite.children.length - 1
      : Math.round(g.suite.scrollLeft / g.pas);
    if (rang === g.actif) { return; }
    g.reperes.children[g.actif].removeAttribute("data-actif");
    g.reperes.children[rang].setAttribute("data-actif", "");
    g.actif = rang;
  }

  /**
   * Mesure une suite : défile-t-elle (une grille dont un contour
   * déborde d'un pixel ne se parcourt pas), et de combien par case.
   * @param {{suite: Element, focalisable: boolean, defile: boolean, pas: number, course: number}} g
   */
  function mesurer(g) {
    var suite = g.suite;
    var cases = suite.children;
    g.defile = window.getComputedStyle(suite).overflowX !== "visible" &&
      suite.scrollWidth > suite.clientWidth + 1;
    g.pas = cases.length > 1 ? cases[1].offsetLeft - cases[0].offsetLeft : 0;
    g.course = suite.scrollWidth - suite.clientWidth;
    if (g.focalisable) {
      if (g.defile) {
        suite.setAttribute("tabindex", "0");
      } else {
        suite.removeAttribute("tabindex");
      }
    }
    marquer(g);
  }

  glissieres.forEach(function (g) {
    g.suite.addEventListener("scroll", function () { marquer(g); }, { passive: true });
  });
  if ("ResizeObserver" in window) {
    var observateur = new ResizeObserver(function (entrees) {
      entrees.forEach(function (entree) {
        glissieres.forEach(function (g) {
          if (g.suite === entree.target) { mesurer(g); }
        });
      });
    });
    glissieres.forEach(function (g) { observateur.observe(g.suite); });
  } else {
    glissieres.forEach(mesurer);
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

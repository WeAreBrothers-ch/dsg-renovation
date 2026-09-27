/* ============================================================
   DSG RÉNOVATION — NAVIGATION
   Liste des prestations sous « Prestations », menu plein écran,
   barre d'action mobile, en-tête qui s'efface à la lecture.
   ============================================================ */
(function () {
  "use strict";

  /** @type {HTMLElement|null} */
  var menu = document.getElementById("menu");
  /** @type {HTMLButtonElement|null} */
  var burger = document.getElementById("burger");
  /** @type {HTMLButtonElement|null} */
  var fermer = document.getElementById("menuFermer");
  /** @type {HTMLElement|null} */
  var barreMobile = document.getElementById("barreMobile");
  /** @type {HTMLElement|null} */
  var groupe = document.getElementById("navPrestations");
  /** @type {HTMLElement|null} */
  var entete = document.getElementById("entete");
  var grandEcran = window.matchMedia("(min-width: 1024px)");

  var enAttente = false;
  var saisieEnCours = false;
  var dernierY = window.scrollY;
  var enteteCache = false;

  /* ---------- Liste des prestations ----------
     Le lien « Prestations » mène à la page pilier ; la case voisine
     ouvre la liste. Une souris l'ouvre au survol, avec un court délai
     à la sortie pour ne pas la refermer au moindre écart. Échap la
     referme et rend le focus au bouton. */
  if (groupe) {
    var deplier = groupe.querySelector(".nav__deplier");
    var survol = window.matchMedia("(hover: hover) and (pointer: fine)");
    var minuterie = 0;

    /** @param {boolean} ouvert */
    var basculerListe = function (ouvert) {
      window.clearTimeout(minuterie);
      groupe.setAttribute("data-ouvert", ouvert ? "true" : "false");
      if (deplier) { deplier.setAttribute("aria-expanded", ouvert ? "true" : "false"); }
    };
    var listeOuverte = function () { return groupe.getAttribute("data-ouvert") === "true"; };

    if (deplier) {
      deplier.addEventListener("click", function () { basculerListe(!listeOuverte()); });
    }
    groupe.addEventListener("mouseenter", function () {
      if (survol.matches) { basculerListe(true); }
    });
    groupe.addEventListener("mouseleave", function () {
      if (!survol.matches) { return; }
      window.clearTimeout(minuterie);
      minuterie = window.setTimeout(function () { basculerListe(false); }, 180);
    });
    /* Le focus quitte le groupe : la liste se referme. */
    groupe.addEventListener("focusout", function (evenement) {
      var suivant = evenement.relatedTarget;
      if (!(suivant instanceof Node) || !groupe.contains(suivant)) { basculerListe(false); }
    });
    document.addEventListener("keydown", function (evenement) {
      if (evenement.key === "Escape" && listeOuverte()) {
        basculerListe(false);
        if (deplier instanceof HTMLElement) { deplier.focus(); }
      }
    });
    document.addEventListener("click", function (evenement) {
      if (listeOuverte() && evenement.target instanceof Node && !groupe.contains(evenement.target)) {
        basculerListe(false);
      }
    });
  }

  /* ---------- Menu plein écran ----------
     Ouvert, il est le seul contenu atteignable : le reste de la page
     passe en « inert », le focus ne peut plus s'en échapper. */
  var arrierePlan = ["entete", "contenu"].map(function (id) { return document.getElementById(id); })
    .concat(Array.prototype.slice.call(document.querySelectorAll("footer, .barre-mobile, .saut")))
    .filter(function (element) { return element instanceof HTMLElement; });

  /**
   * Ouvre ou ferme le menu et verrouille le défilement de la page.
   * @param {boolean} ouvert
   */
  function basculerMenu(ouvert) {
    if (!menu || !burger) { return; }
    menu.setAttribute("data-ouvert", ouvert ? "true" : "false");
    burger.setAttribute("aria-expanded", ouvert ? "true" : "false");
    burger.setAttribute("aria-label", ouvert ? "Fermer le menu" : "Ouvrir le menu");
    document.body.style.overflow = ouvert ? "hidden" : "";
    arrierePlan.forEach(function (element) {
      if (ouvert) { element.setAttribute("inert", ""); } else { element.removeAttribute("inert"); }
    });

    if (ouvert) {
      var premier = menu.querySelector("a, button");
      if (premier instanceof HTMLElement) { premier.focus(); }
    } else {
      burger.focus();
    }
  }

  function menuEstOuvert() {
    return !!menu && menu.getAttribute("data-ouvert") === "true";
  }

  if (burger) {
    burger.addEventListener("click", function () { basculerMenu(!menuEstOuvert()); });
  }
  if (fermer) {
    fermer.addEventListener("click", function () { basculerMenu(false); });
  }
  if (menu) {
    menu.addEventListener("click", function (evenement) {
      var cible = evenement.target;
      if (cible instanceof Element && cible.closest("a")) { basculerMenu(false); }
    });
  }
  document.addEventListener("keydown", function (evenement) {
    if (evenement.key === "Escape" && menuEstOuvert()) { basculerMenu(false); }
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1023 && menuEstOuvert()) { basculerMenu(false); }
  });

  /* ---------- Barre mobile ----------
     Elle n'apparaît qu'une fois la couverture passée : en haut de page,
     les boutons de la couverture font déjà ce travail. Elle s'efface
     pendant qu'on remplit un champ : elle masquerait ce qu'on écrit. */
  function mettreAJourBarre() {
    if (!barreMobile) { return; }
    var visible = window.scrollY > 480 && !saisieEnCours;
    barreMobile.setAttribute("data-visible", visible ? "true" : "false");
  }

  /* ---------- En-tête ----------
     Au téléphone et sur tablette, il s'efface quand on descend et
     revient dès qu'on remonte : quelques pixels de marge évitent qu'il
     clignote au moindre frémissement du doigt. Il reste là en haut de
     page, menu ouvert, et dès que le clavier y amène le focus. */
  function mettreAJourEntete() {
    if (!entete) { return; }
    var y = window.scrollY;
    var ecart = y - dernierY;
    var fixe = grandEcran.matches || y < 160 || menuEstOuvert() || entete.contains(document.activeElement);
    if (fixe) {
      enteteCache = false;
      dernierY = y;
    } else if (Math.abs(ecart) > 8) {
      enteteCache = ecart > 0;
      dernierY = y;
    }
    entete.setAttribute("data-cache", enteteCache ? "true" : "false");
  }

  function auDefilement() {
    mettreAJourBarre();
    mettreAJourEntete();
    enAttente = false;
  }

  window.addEventListener("scroll", function () {
    if (enAttente) { return; }
    enAttente = true;
    window.requestAnimationFrame(auDefilement);
  }, { passive: true });

  document.addEventListener("focusin", function (evenement) {
    var cible = evenement.target;
    saisieEnCours = cible instanceof Element && cible.matches("input, select, textarea");
    mettreAJourBarre();
    mettreAJourEntete();
  });
  document.addEventListener("focusout", function () {
    saisieEnCours = false;
    window.setTimeout(mettreAJourBarre, 60);
  });

  auDefilement();
}());

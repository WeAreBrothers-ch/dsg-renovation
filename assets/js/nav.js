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
     Elle n'apparaît qu'une fois sorti de l'écran l'appel de la
     couverture : tant qu'il est visible, il fait ce travail, et deux
     « Devis gratuit » l'un sous l'autre se disputeraient le pouce. Elle
     s'efface pendant qu'on remplit un champ : elle masquerait ce qu'on
     écrit. */
  var appelCouverture = document.querySelector(".couverture__actions .btn--plein");
  function mettreAJourBarre() {
    if (!barreMobile) { return; }
    var passee = appelCouverture
      ? appelCouverture.getBoundingClientRect().bottom < 0
      : window.scrollY > 480;
    var visible = passee && !saisieEnCours;
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
    var avant = enteteCache;
    var fixe = grandEcran.matches || y < 160 || menuEstOuvert() || entete.contains(document.activeElement);
    if (fixe) {
      enteteCache = false;
      dernierY = y;
    } else if (Date.now() < guideJusqua) {
      /* Un saut du sommaire : l'en-tête reste effacé, même en
         remontant, pour que le titre visé arrive sous la rangée. */
      enteteCache = true;
      dernierY = y;
    } else if (Math.abs(ecart) > 8) {
      enteteCache = ecart > 0;
      dernierY = y;
    }
    entete.setAttribute("data-cache", enteteCache ? "true" : "false");
    if (sommaire && avant !== enteteCache) {
      accompagner();
      placerSommaire();
    }
  }

  /* ---------- Sommaire de page ----------
     Au téléphone et sur tablette, la rangée des sections
     (outils/sommaire.py) colle sous l'en-tête. Quand l'en-tête
     s'efface, elle monte à sa place : un décalage, jamais un
     changement de mise en page, et seulement une fois arrivée en
     haut, pour qu'elle suive la page jusque-là. La section en cours
     y est marquée, et sa case ramenée en vue dans la rangée. */
  var sommaire = document.querySelector("[data-sommaire]");
  var rangee = sommaire ? sommaire.querySelector("ul") : null;
  var liens = sommaire ? Array.prototype.slice.call(sommaire.querySelectorAll('a[href^="#"]')) : [];
  var sections = liens.map(function (lien) {
    var titre = document.getElementById(lien.getAttribute("href").slice(1));
    return titre ? (titre.closest("section") || titre) : null;
  });
  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)");
  var courante = -1;
  var guideJusqua = 0;
  var minuterieAccompagner = 0;

  function sommaireCollant() {
    return !!sommaire && sommaire.offsetParent !== null && window.getComputedStyle(sommaire).position === "sticky";
  }

  /* La rangée glisse avec l'en-tête, à la même allure. */
  function accompagner() {
    sommaire.classList.add("est-anime");
    window.clearTimeout(minuterieAccompagner);
    minuterieAccompagner = window.setTimeout(function () { sommaire.classList.remove("est-anime"); }, 400);
  }

  function placerSommaire() {
    var decalage = 0;
    if (enteteCache && sommaireCollant() && entete) {
      /* Sa place dans la page : le bas du bloc qui la précède. Elle
         monte avec la page jusqu'en haut de l'écran, et s'y arrête. */
      var precedent = sommaire.previousElementSibling;
      var haut = precedent ? precedent.getBoundingClientRect().bottom : 0;
      var collee = parseFloat(window.getComputedStyle(sommaire).top) || 0;
      decalage = Math.max(haut, 0) - Math.max(haut, collee);
    }
    sommaire.style.transform = decalage ? "translateY(" + decalage + "px)" : "";
  }

  function montrerCase(lien) {
    if (!rangee) { return; }
    var gauche = lien.offsetLeft - (rangee.clientWidth - lien.offsetWidth) / 2;
    rangee.scrollTo({ left: Math.max(0, gauche), behavior: mouvementReduit.matches ? "auto" : "smooth" });
  }

  function marquerSection() {
    var ligne = window.innerHeight * 0.35;
    var active = -1;
    sections.forEach(function (section, rang) {
      if (section && section.getBoundingClientRect().top <= ligne) { active = rang; }
    });
    if (active === courante) { return; }
    if (courante >= 0) { liens[courante].removeAttribute("aria-current"); }
    if (active >= 0) {
      liens[active].setAttribute("aria-current", "true");
      montrerCase(liens[active]);
    }
    courante = active;
  }

  /* Les fondus de bord, d'un côté ou de l'autre, tant qu'il reste des
     cases à faire venir de ce côté. */
  function borderRangee() {
    if (!rangee) { return; }
    var reste = rangee.scrollWidth - rangee.clientWidth - rangee.scrollLeft;
    rangee.classList.toggle("a-gauche", rangee.scrollLeft > 1);
    rangee.classList.toggle("a-droite", reste > 1);
  }

  if (sommaire) {
    liens.forEach(function (lien, rang) {
      lien.addEventListener("click", function (evenement) {
        var section = sections[rang];
        if (!section || !sommaireCollant()) { return; }
        evenement.preventDefault();
        var titre = document.getElementById(lien.getAttribute("href").slice(1));
        var repere = section.querySelector(".intercalaire") || titre || section;
        var cible = repere.getBoundingClientRect().top + window.scrollY - sommaire.offsetHeight - 16;
        guideJusqua = Date.now() + 1200;
        window.scrollTo({ top: Math.max(0, cible), behavior: mouvementReduit.matches ? "auto" : "smooth" });
        if (window.history.replaceState) { window.history.replaceState(null, "", lien.getAttribute("href")); }
        /* Le focus suit : le clavier et les lecteurs d'écran
           repartent de la section choisie. */
        if (titre) {
          titre.setAttribute("tabindex", "-1");
          titre.focus({ preventScroll: true });
        }
      });
    });
    if (rangee) {
      rangee.addEventListener("scroll", borderRangee, { passive: true });
      window.addEventListener("resize", borderRangee);
      borderRangee();
    }
  }

  function auDefilement() {
    mettreAJourBarre();
    mettreAJourEntete();
    if (sommaire) {
      placerSommaire();
      marquerSection();
    }
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

  /* ---------- Volets du pied de page ----------
     Au téléphone, les listes du pied (le site, les prestations, les
     zones) se replient sous leur intitulé, qui devient un bouton. La
     feuille les replie dès le premier affichage (.js) : rien ne bouge
     quand ce script arrive. Sur un écran plus large, les colonnes sont
     ouvertes et les intitulés redeviennent de simples titres. */
  var volets = Array.prototype.slice.call(document.querySelectorAll("[data-volet]"));
  var colonnes = window.matchMedia("(min-width: 768px)");

  function poserVolets() {
    volets.forEach(function (volet) {
      var titre = volet.querySelector("h3");
      var liste = volet.querySelector("ul");
      if (!titre || !liste) { return; }
      var bouton = titre.querySelector("button");
      if (!colonnes.matches && !bouton) {
        bouton = document.createElement("button");
        bouton.type = "button";
        bouton.className = "pied__bascule";
        bouton.setAttribute("aria-expanded", "false");
        bouton.setAttribute("aria-controls", liste.id);
        bouton.textContent = titre.textContent;
        var signe = document.createElement("span");
        signe.className = "pied__signe";
        signe.setAttribute("aria-hidden", "true");
        bouton.appendChild(signe);
        titre.textContent = "";
        titre.appendChild(bouton);
        bouton.addEventListener("click", function () {
          var ouvert = volet.classList.toggle("est-ouvert");
          bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
        });
      } else if (colonnes.matches && bouton) {
        titre.textContent = bouton.textContent;
        volet.classList.remove("est-ouvert");
      }
    });
  }

  if (volets.length) {
    poserVolets();
    if (colonnes.addEventListener) { colonnes.addEventListener("change", poserVolets); }
  }

  auDefilement();
}());

/* ============================================================
   DSG RÉNOVATION — MOUVEMENT
   Révélations au défilement, photos qui se dévoilent, chiffres qui
   défilent, profondeur des grandes photos, année courante.
   Tout contenu reste lisible si ce fichier ne s'exécute pas.
   ============================================================ */
(function () {
  "use strict";

  /* Ce fichier s'exécute : les blocs masqués en attente de révélation
     le seront bien. Sans cette classe, la page les réaffiche d'office
     au chargement (voir SCRIPT_JS dans outils/gabarit.py). */
  document.documentElement.classList.add("motion");

  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Année du copyright ---------- */
  var annee = document.getElementById("annee");
  if (annee) { annee.textContent = String(new Date().getFullYear()); }

  /* ---------- Découpe des titres en lignes masquées ----------
     Chaque <br> devient une ligne indépendante, révélée en cascade. */
  var titres = document.querySelectorAll("[data-lignes]");

  Array.prototype.forEach.call(titres, function (titre) {
    var lignes = titre.innerHTML.split(/<br\s*\/?>/i);
    if (lignes.length < 1) { return; }
    /* Les lignes sont jointes par une espace : en blocs, elles vont à
       la ligne à l'écran, mais le texte du titre (celui que lisent
       Google et les lecteurs d'écran) garde ses mots séparés. */
    titre.innerHTML = lignes.map(function (ligne) {
      return '<span class="ligne"><span>' + ligne + "</span></span>";
    }).join(" ");
  });

  /* ---------- Révélations ---------- */
  var aReveler = document.querySelectorAll(".revele");

  function toutAfficher() {
    Array.prototype.forEach.call(aReveler, function (element) {
      element.classList.add("est-vu");
    });
  }

  if (!("IntersectionObserver" in window)) {
    toutAfficher();
  } else {
    var observateur = new IntersectionObserver(function (entrees) {
      var rang = 0;
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) { return; }
        var element = entree.target;
        if (element instanceof HTMLElement) {
          element.style.transitionDelay = (mouvementReduit ? 0 : Math.min(rang, 5) * 70) + "ms";
        }
        element.classList.add("est-vu");
        rang += 1;
        observateur.unobserve(element);
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -5% 0px" });

    Array.prototype.forEach.call(aReveler, function (element) { observateur.observe(element); });
  }

  /* ---------- Chiffres qui défilent ----------
     Les chiffres de l'entreprise montent de zéro à leur valeur quand
     ils arrivent à l'écran. La valeur est écrite dans la page : Google,
     les lecteurs d'écran et un visiteur sans script la lisent telle
     quelle. Chiffres tabulaires : la largeur ne bouge pas. */
  var chiffres = document.querySelectorAll(".preuve__val");
  if (chiffres.length && !mouvementReduit && "IntersectionObserver" in window) {
    var observateurChiffres = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) { return; }
        observateurChiffres.unobserve(entree.target);
        var element = entree.target;
        var cible = parseInt(element.textContent, 10);
        if (!(cible > 0)) { return; }
        var debut = null;
        var duree = 1400;
        function pas(horodatage) {
          if (debut === null) { debut = horodatage; }
          var t = Math.min((horodatage - debut) / duree, 1);
          element.textContent = String(Math.round(cible * (1 - Math.pow(1 - t, 3))));
          if (t < 1) { window.requestAnimationFrame(pas); }
        }
        element.textContent = "0";
        window.requestAnimationFrame(pas);
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(chiffres, function (element) { observateurChiffres.observe(element); });
  }

  /* ---------- Profondeur des grandes photos ----------
     Les photos d'en-tête et du chantier à la une glissent d'un rien
     dans leur cadre pendant le défilement : la page gagne de la
     profondeur sans que rien ne bouge dans la mise en page (transform
     seul). Coupé en mouvement réduit. */
  var profondes = document.querySelectorAll(".piece__image img, .signature__cadre img");
  if (profondes.length && !mouvementReduit) {
    var attente = false;
    var peindreProfondeur = function () {
      attente = false;
      var hauteur = window.innerHeight;
      Array.prototype.forEach.call(profondes, function (image) {
        var cadre = image.parentElement.getBoundingClientRect();
        if (cadre.bottom < 0 || cadre.top > hauteur) { return; }
        /* -1 quand le cadre entre par le bas, +1 quand il sort par le haut. */
        var avance = ((hauteur - cadre.top) / (hauteur + cadre.height)) * 2 - 1;
        image.style.transform = "translate3d(0," + (avance * -4).toFixed(2) + "%,0) scale(1.1)";
      });
    };
    var demanderProfondeur = function () {
      if (attente) { return; }
      attente = true;
      window.requestAnimationFrame(peindreProfondeur);
    };
    window.addEventListener("scroll", demanderProfondeur, { passive: true });
    window.addEventListener("resize", demanderProfondeur, { passive: true });
    peindreProfondeur();
  }

  /* ---------- Vignettes des savoir-faire (tactile) ----------
     Faute de survol sur téléphone, chaque vignette se décoffre quand sa
     ligne est bien montée dans l'écran — en plein geste de défilement.
     La marge basse retarde le déclenchement pour que la révélation ne
     soit jamais déjà faite quand la ligne arrive à hauteur de lecture. */
  var lignesMetiers = document.querySelectorAll(".metiers__ligne");
  var REGLAGE_VUE = { threshold: 0.5, rootMargin: "0px 0px -12% 0px" };

  if (lignesMetiers.length && "IntersectionObserver" in window) {
    var observateurMetiers = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) { return; }
        entree.target.setAttribute("data-vue-visible", "true");
        observateurMetiers.unobserve(entree.target);
      });
    }, REGLAGE_VUE);

    Array.prototype.forEach.call(lignesMetiers, function (ligne) {
      observateurMetiers.observe(ligne);
    });
  } else {
    Array.prototype.forEach.call(lignesMetiers, function (ligne) {
      ligne.setAttribute("data-vue-visible", "true");
    });
  }
}());

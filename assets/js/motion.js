/* ============================================================
   DSG RÉNOVATION — MOUVEMENT
   Année courante du pied de page, l'enseigne qui s'allume, et le plan
   qui se trace.

   Quand un bloc arrive à l'écran, ses traits se tracent : le toit de
   l'intitulé, les filets des bordereaux ; la carte se relève depuis
   l'atelier et ses piquets se plantent (09-trace.css, 13-carte.css). Seuls les traits bougent : le
   texte et les photos sont là dès le premier affichage. Les révélations
   retirées le 05/10/2026 laissaient au téléphone des zones vides et des
   photos à moitié découvertes pendant qu'on faisait défiler ; rien de
   tel ici, rien n'attend d'être dévoilé.

   Une seule fois par bloc. Si le visiteur demande moins de mouvement,
   ou sans IntersectionObserver, tout est tracé d'emblée.
   ============================================================ */
(function () {
  "use strict";

  /* Ce fichier s'exécute : la page garde sa classe « js » (voir
     SCRIPT_JS dans outils/gabarit.py), dont dépendent les volets du
     pied de page, les onglets, les filtres et les traits à tracer. */
  document.documentElement.classList.add("motion");

  /* ---------- Année du copyright ---------- */
  var annee = document.getElementById("annee");
  if (annee) { annee.textContent = String(new Date().getFullYear()); }

  /* ---------- L'enseigne s'allume ----------
     D'après « Text Hover Effect » (21st.dev), réécrit sans dépendance :
     là où passe la souris, ou le doigt posé sur l'enseigne du pied, une
     lueur au rouge du toit s'allume dans les lettres (08-bas.css). Le
     script ne donne que la position ; la feuille allume et éteint. */
  var enseigne = document.querySelector(".pied__logotype");
  if (enseigne instanceof HTMLElement && "PointerEvent" in window) {
    var lueur = { x: 0, y: 0, image: 0 };
    var poser = function (evenement) {
      var boite = enseigne.getBoundingClientRect();
      lueur.x = evenement.clientX - boite.left;
      lueur.y = evenement.clientY - boite.top;
    };
    var peindre = function () {
      lueur.image = 0;
      enseigne.style.setProperty("--lx", lueur.x.toFixed(1) + "px");
      enseigne.style.setProperty("--ly", lueur.y.toFixed(1) + "px");
    };
    enseigne.addEventListener("pointerenter", function (evenement) {
      poser(evenement);
      peindre();
      enseigne.classList.add("est-allume");
    });
    enseigne.addEventListener("pointermove", function (evenement) {
      poser(evenement);
      if (!lueur.image) { lueur.image = window.requestAnimationFrame(peindre); }
    });
    enseigne.addEventListener("pointerleave", function () { enseigne.classList.remove("est-allume"); });
  }

  /* ---------- Le plan se trace ---------- */
  var BLOCS = ".intercalaire__marge, .metiers, .lots.service__villes, .piece__faits, " +
              ".rappel__joindre, .service__liste, .releve--regle, .replis, .leman";
  /* Au-delà, les filets partent ensemble : un long bordereau ne doit pas
     mettre plus d'une seconde à se tracer. */
  var RANG_MAX = 10;

  var blocs = document.querySelectorAll(BLOCS);
  Array.prototype.forEach.call(blocs, function (bloc) {
    Array.prototype.forEach.call(bloc.children, function (enfant, rang) {
      if (enfant instanceof HTMLElement) {
        enfant.style.setProperty("--rang", String(Math.min(rang, RANG_MAX)));
      }
    });
  });

  function tracer(bloc) { bloc.classList.add("est-trace"); }

  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduit || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(blocs, tracer);
    return;
  }
  /* Un bloc se trace quand il a passé le bas de l'écran d'un huitième :
     on le voit se faire, pas seulement fini. */
  var observateur = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (entree) {
      if (!entree.isIntersecting) { return; }
      observateur.unobserve(entree.target);
      tracer(entree.target);
    });
  }, { rootMargin: "0px 0px -12% 0px" });
  Array.prototype.forEach.call(blocs, function (bloc) { observateur.observe(bloc); });
}());

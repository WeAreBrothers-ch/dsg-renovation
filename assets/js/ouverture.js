/* ============================================================
   DSG RÉNOVATION — OUVERTURE
   L'image d'ouverture arrive cadrée dans la colonne de la page,
   puis s'élargit jusqu'aux bords de l'écran à mesure qu'on
   descend : deux rideaux couleur du fond s'écartent.

   Tout passe par `transform` : aucune mise en page n'est
   recalculée pendant le défilement, et rien ne peut se décaler.
   Sans ce script, ou si le visiteur demande moins de mouvement,
   l'image reste simplement cadrée — c'est un état complet.
   ============================================================ */
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { return; }

  var blocs = document.querySelectorAll("[data-ouverture]");
  if (!blocs.length) { return; }

  var entete = document.getElementById("entete");

  /* L'ouverture commence quand le haut de l'image passe sous les neuf
     dixièmes de l'écran, et s'achève quand il atteint l'en-tête. */
  var DEBUT_ECRAN = 0.9;

  /**
   * Adoucit la progression : l'image s'ouvre vite, puis se pose.
   * @param {number} t progression entre 0 et 1
   * @returns {number}
   */
  function adoucir(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  /**
   * Prépare une ouverture et renvoie ses deux fonctions de mise à jour.
   * @param {HTMLElement} bloc
   * @returns {{mesurer: function(): void, peindre: function(): void}|null}
   */
  function installer(bloc) {
    var cadre = bloc.querySelector(".ouverture__cadre");
    var gauche = bloc.querySelector(".ouverture__rideau--g");
    var droite = bloc.querySelector(".ouverture__rideau--d");
    if (!(cadre instanceof HTMLElement) || !(gauche instanceof HTMLElement) ||
        !(droite instanceof HTMLElement)) { return null; }

    /* Les étiquettes du comparateur suivent le bord de la fenêtre. */
    var etatGauche = bloc.querySelector(".comparateur__etat--apres");
    var etatDroite = bloc.querySelector(".comparateur__etat--avant");

    var debut = 0;
    var fin = 1;
    var marge = 0;

    function mesurer() {
      var haut = cadre.getBoundingClientRect().top + window.scrollY;
      var arret = entete ? entete.offsetHeight : 0;
      fin = Math.max(1, haut - arret);
      debut = Math.min(fin - 1, Math.max(0, haut - window.innerHeight * DEBUT_ECRAN));
      marge = gauche.offsetWidth;
    }

    function peindre() {
      var brut = (window.scrollY - debut) / (fin - debut);
      var ouvert = adoucir(Math.max(0, Math.min(1, brut)));
      gauche.style.transform = "translate3d(" + (-ouvert * 100).toFixed(3) + "%,0,0)";
      droite.style.transform = "translate3d(" + (ouvert * 100).toFixed(3) + "%,0,0)";
      if (etatGauche instanceof HTMLElement) {
        etatGauche.style.transform = "translate3d(" + (-ouvert * marge).toFixed(1) + "px,0,0)";
      }
      if (etatDroite instanceof HTMLElement) {
        etatDroite.style.transform = "translate3d(" + (ouvert * marge).toFixed(1) + "px,0,0)";
      }
    }

    return { mesurer: mesurer, peindre: peindre };
  }

  var ouvertures = [];
  Array.prototype.forEach.call(blocs, function (bloc) {
    if (!(bloc instanceof HTMLElement)) { return; }
    var ouverture = installer(bloc);
    if (ouverture) { ouvertures.push(ouverture); }
  });
  if (!ouvertures.length) { return; }

  var enAttente = false;

  function toutPeindre() {
    ouvertures.forEach(function (o) { o.peindre(); });
    enAttente = false;
  }

  function demander() {
    if (enAttente) { return; }
    enAttente = true;
    window.requestAnimationFrame(toutPeindre);
  }

  function toutMesurer() {
    ouvertures.forEach(function (o) { o.mesurer(); });
    demander();
  }

  window.addEventListener("scroll", demander, { passive: true });
  window.addEventListener("resize", toutMesurer, { passive: true });
  /* Les polices et les images peuvent déplacer le haut de l'image après
     le premier rendu : on remesure une fois la page chargée. */
  window.addEventListener("load", toutMesurer);
  toutMesurer();
}());

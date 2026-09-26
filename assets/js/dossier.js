/* ============================================================
   DSG RÉNOVATION — TRI DES RÉALISATIONS
   Les filtres n'apparaissent que si ce script s'exécute :
   sans JavaScript, toutes les fiches restent visibles.
   ============================================================ */
(function () {
  "use strict";

  var barreFiltres = document.getElementById("filtresChantiers");
  var grille = document.getElementById("grilleChantiers");
  var compteur = document.getElementById("compteChantiers");
  if (!barreFiltres || !grille) { return; }

  var boutons = barreFiltres.querySelectorAll("[data-filtre]");
  var fiches = grille.querySelectorAll("[data-type]");
  var messageVide = document.getElementById("aucunChantier");
  if (!boutons.length || !fiches.length) { return; }

  barreFiltres.hidden = false;

  /**
   * Accorde le compteur de fiches visibles.
   * @param {number} nombre
   */
  function majCompteur(nombre) {
    if (!compteur) { return; }
    compteur.textContent = nombre + (nombre > 1 ? " chantiers affichés" : " chantier affiché");
  }

  /**
   * N'affiche que les fiches du type demandé.
   * @param {string} type - « tous » ou une valeur de data-type
   */
  function filtrer(type) {
    var visibles = 0;

    Array.prototype.forEach.call(fiches, function (fiche) {
      var correspond = type === "tous" || fiche.getAttribute("data-type") === type;
      if (fiche instanceof HTMLElement) { fiche.hidden = !correspond; }
      if (correspond) { visibles += 1; }
    });

    Array.prototype.forEach.call(boutons, function (bouton) {
      var actif = bouton.getAttribute("data-filtre") === type;
      bouton.setAttribute("aria-pressed", actif ? "true" : "false");
    });

    if (messageVide) { messageVide.hidden = visibles > 0; }
    majCompteur(visibles);
  }

  Array.prototype.forEach.call(boutons, function (bouton) {
    bouton.addEventListener("click", function () {
      filtrer(bouton.getAttribute("data-filtre") || "tous");
    });
  });

  majCompteur(fiches.length);
}());

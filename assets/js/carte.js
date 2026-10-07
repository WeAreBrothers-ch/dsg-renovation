/* ============================================================
   DSG RÉNOVATION — CARTE DE LA ZONE
   Une commune survolée, sur le plan ou dans la liste, se marque des
   deux côtés : son repère grossit et prend le rouge du toit, son nom
   paraît sur le plan, sa ligne de la liste passe au rouge écrit.
   Survol seulement : au doigt, le plan et la liste se lisent tels
   quels, et sans ce script aussi.
   ============================================================ */
(function () {
  "use strict";

  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) { return; }
  var lieux = document.querySelectorAll("[data-lieu]");
  if (!lieux.length) { return; }

  /**
   * Marque ou démarque toutes les apparitions d'une commune.
   * @param {string} cle
   * @param {boolean} oui
   */
  function marquer(cle, oui) {
    Array.prototype.forEach.call(lieux, function (lieu) {
      if (lieu.getAttribute("data-lieu") === cle) { lieu.classList.toggle("est-montre", oui); }
    });
  }

  Array.prototype.forEach.call(lieux, function (lieu) {
    var cle = lieu.getAttribute("data-lieu") || "";
    lieu.addEventListener("mouseenter", function () { marquer(cle, true); });
    lieu.addEventListener("mouseleave", function () { marquer(cle, false); });
  });
}());

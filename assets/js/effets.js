/* ============================================================
   DSG RÉNOVATION — BOUTONS MAGNÉTIQUES
   Les boutons d'appel s'inclinent très légèrement vers la souris.
   L'attraction se sent, elle ne se voit pas : un bouton qui fuit
   sous le curseur devient difficile à viser. Le déplacement est
   donc faible et plafonné, pour que la cible reste là où l'œil
   l'a posée. Neutralisé au doigt et en mouvement réduit.
   ============================================================ */
(function () {
  "use strict";

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { return; }
  if (!window.matchMedia("(pointer: fine)").matches) { return; }

  var ATTRACTION = 0.08;
  var ECART_MAX = 4;

  /**
   * @param {number} valeur
   * @param {number} limite
   * @returns {number}
   */
  function borner(valeur, limite) {
    return Math.max(-limite, Math.min(limite, valeur));
  }

  var aimants = document.querySelectorAll("[data-magnetique]");

  Array.prototype.forEach.call(aimants, function (aimant) {
    if (!(aimant instanceof HTMLElement)) { return; }

    aimant.addEventListener("pointermove", function (evenement) {
      if (evenement.pointerType !== "mouse") { return; }
      var cadre = aimant.getBoundingClientRect();
      var dx = borner((evenement.clientX - (cadre.left + cadre.width / 2)) * ATTRACTION, ECART_MAX);
      var dy = borner((evenement.clientY - (cadre.top + cadre.height / 2)) * ATTRACTION, ECART_MAX);
      aimant.style.transform = "translate3d(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px,0)";
    }, { passive: true });

    aimant.addEventListener("pointerleave", function () { aimant.style.transform = ""; });
    aimant.addEventListener("blur", function () { aimant.style.transform = ""; });
  });
}());

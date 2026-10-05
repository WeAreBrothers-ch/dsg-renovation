/* ============================================================
   DSG RÉNOVATION — MOUVEMENT
   Année courante du pied de page.

   Le site n'anime plus rien au défilement : ni révélations, ni photos
   qui se dévoilent, ni chiffres qui défilent, ni profondeur des
   grandes photos. Au téléphone, ces effets laissaient des zones vides
   et des photos à moitié découvertes pendant qu'on faisait défiler,
   et retardaient la lecture. Tout s'affiche d'emblée.
   ============================================================ */
(function () {
  "use strict";

  /* Ce fichier s'exécute : la page garde sa classe « js » (voir
     SCRIPT_JS dans outils/gabarit.py), dont dépendent les volets du
     pied de page, les onglets et les filtres. */
  document.documentElement.classList.add("motion");

  /* ---------- Année du copyright ---------- */
  var annee = document.getElementById("annee");
  if (annee) { annee.textContent = String(new Date().getFullYear()); }
}());

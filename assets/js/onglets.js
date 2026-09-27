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

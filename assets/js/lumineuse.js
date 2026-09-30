/* ============================================================
   DSG RÉNOVATION — TABLE LUMINEUSE
   Les vues d'archive s'ouvrent en plein écran, comme des tirages
   posés sur une table lumineuse. Navigation clavier, tactile et
   souris. Sans JavaScript, chaque vue reste un lien vers la photo.
   ============================================================ */
(function () {
  "use strict";

  var galeries = document.querySelectorAll("[data-galerie]");
  if (!galeries.length || typeof HTMLDialogElement === "undefined") { return; }

  var boite = document.createElement("dialog");
  boite.className = "lumineuse";
  boite.setAttribute("aria-label", "Vue agrandie");
  boite.innerHTML =
    '<button class="lumineuse__fermer" type="button" aria-label="Fermer la vue">&times;</button>' +
    '<figure class="lumineuse__cadre">' +
      '<img class="lumineuse__img" alt="">' +
      '<figcaption class="lumineuse__legende"><span class="lumineuse__texte">' +
      '<span class="lumineuse__lieu"></span><span class="lumineuse__quoi"></span></span>' +
      '<span class="lumineuse__compte"></span></figcaption>' +
    "</figure>" +
    '<button class="lumineuse__nav lumineuse__nav--prec" type="button" aria-label="Vue précédente"></button>' +
    '<button class="lumineuse__nav lumineuse__nav--suiv" type="button" aria-label="Vue suivante"></button>';
  document.body.appendChild(boite);

  var image = boite.querySelector(".lumineuse__img");
  var lieu = boite.querySelector(".lumineuse__lieu");
  var quoi = boite.querySelector(".lumineuse__quoi");
  var compte = boite.querySelector(".lumineuse__compte");

  /** @type {Element[]} */
  var groupe = [];
  var rang = 0;
  var declencheur = null;

  /**
   * Charge la vue d'un rang donné, en bouclant aux extrémités.
   * @param {number} cible
   */
  function afficher(cible) {
    if (!groupe.length) { return; }
    rang = (cible + groupe.length) % groupe.length;

    var lien = groupe[rang];
    var vignette = lien.querySelector("img");

    boite.setAttribute("data-charge", "false");
    image.src = lien.getAttribute("href") || "";
    image.alt = (vignette && vignette.getAttribute("alt")) || "";
    /* La légende parle en deux voix, comme celles du site : le lieu,
       puis ce qu'on voit — le dernier segment de « data-legende ». */
    var morceaux = (lien.getAttribute("data-legende") || "").split(" · ");
    var vu = morceaux.length > 1 ? morceaux.pop() : "";
    lieu.textContent = morceaux.join(" · ");
    quoi.textContent = vu;
    compte.textContent = (rang + 1) + " / " + groupe.length;
  }

  image.addEventListener("load", function () {
    boite.setAttribute("data-charge", "true");
  });

  /**
   * Ouvre la table lumineuse sur une vue.
   * @param {Element[]} vues
   * @param {number} depart
   * @param {Element} origine - élément à re-focaliser à la fermeture
   */
  function ouvrir(vues, depart, origine) {
    groupe = vues;
    declencheur = origine;
    afficher(depart);
    boite.showModal();
    document.body.style.overflow = "hidden";
  }

  boite.addEventListener("close", function () {
    document.body.style.overflow = "";
    if (declencheur instanceof HTMLElement) { declencheur.focus(); }
  });

  boite.querySelector(".lumineuse__fermer").addEventListener("click", function () { boite.close(); });
  boite.querySelector(".lumineuse__nav--prec").addEventListener("click", function () { afficher(rang - 1); });
  boite.querySelector(".lumineuse__nav--suiv").addEventListener("click", function () { afficher(rang + 1); });

  /* Un clic hors du tirage ferme la vue. */
  boite.addEventListener("click", function (evenement) {
    if (evenement.target === boite) { boite.close(); }
  });

  boite.addEventListener("keydown", function (evenement) {
    if (evenement.key === "ArrowLeft") { evenement.preventDefault(); afficher(rang - 1); }
    if (evenement.key === "ArrowRight") { evenement.preventDefault(); afficher(rang + 1); }
  });

  /* Balayage tactile */
  var departX = null;
  boite.addEventListener("pointerdown", function (evenement) {
    departX = evenement.pointerType === "touch" ? evenement.clientX : null;
  });
  boite.addEventListener("pointerup", function (evenement) {
    if (departX === null) { return; }
    var ecart = evenement.clientX - departX;
    if (Math.abs(ecart) > 48) { afficher(ecart > 0 ? rang - 1 : rang + 1); }
    departX = null;
  });

  /* Branchement des galeries */
  Array.prototype.forEach.call(galeries, function (galerie) {
    var vues = Array.prototype.slice.call(galerie.querySelectorAll("a[data-vue]"));
    if (!vues.length) { return; }

    vues.forEach(function (vue, index) {
      vue.addEventListener("click", function (evenement) {
        if (evenement.metaKey || evenement.ctrlKey || evenement.shiftKey) { return; }
        evenement.preventDefault();
        ouvrir(vues, index, vue);
      });
    });
  });
}());

/* ============================================================
   DSG RÉNOVATION — BORDEREAU DE DEMANDE
   Validation côté client, puis envoi.

   Deux voies d'envoi :
   - si le formulaire porte une adresse dans data-envoi (Formspree,
     Web3Forms, formulaire Infomaniak…), la demande y part
     directement et le visiteur reste sur la page ;
   - sinon, repli : le logiciel de messagerie du visiteur s'ouvre
     avec la demande préremplie.
   Sans JavaScript, l'attribut action du formulaire prend le relais.
   ============================================================ */
(function () {
  "use strict";

  var formulaire = document.getElementById("bordereau");
  if (!(formulaire instanceof HTMLFormElement)) { return; }

  var retour = document.getElementById("bordereauRetour");
  var bouton = formulaire.querySelector('button[type="submit"]');
  var POINT_ENVOI = (formulaire.getAttribute("data-envoi") || "").trim();
  var DESTINATAIRE = "contact@dsg-renov.ch";
  var TELEPHONE = "+41 21 847 02 02";
  var MOTIF_EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;
  /* Champs qui ne se valident pas un par un : les pastilles sont
     facultatives, le piège à robots doit rester vide. */
  var HORS_VALIDATION = ["travaux", "site_web"];

  /** Libellés affichés dans le courriel, dans l'ordre du bordereau. */
  var CHAMPS = [
    { nom: "travaux", libelle: "Travaux concernés" },
    { nom: "type", libelle: "Type de bien" },
    { nom: "lieu", libelle: "Commune du bien" },
    { nom: "surface", libelle: "Surface approximative" },
    { nom: "delai", libelle: "Démarrage souhaité" },
    { nom: "message", libelle: "Description du projet" },
    { nom: "nom", libelle: "Nom" },
    { nom: "telephone", libelle: "Téléphone" },
    { nom: "email", libelle: "Courriel" }
  ];

  /**
   * Affiche ou efface le message d'erreur d'un champ.
   * @param {Element} controle
   * @param {string} message - chaîne vide pour effacer
   */
  function signaler(controle, message) {
    var bloc = controle.closest(".champ");
    if (!bloc) { return; }
    var zone = bloc.querySelector(".champ__erreur");
    bloc.classList.toggle("champ--erreur", message !== "");
    controle.setAttribute("aria-invalid", message !== "" ? "true" : "false");
    if (zone) { zone.textContent = message; }
  }

  /**
   * Vérifie un champ et renvoie son message d'erreur (vide si valide).
   * @param {HTMLInputElement|HTMLSelectElement|HTMLTextAreaElement} controle
   * @returns {string}
   */
  function verifier(controle) {
    var valeur = controle.value.trim();

    if (controle instanceof HTMLInputElement && controle.type === "checkbox") {
      return !controle.required || controle.checked ? "" : "Merci de cocher cette case pour continuer.";
    }
    if (controle.required && valeur === "") {
      return "Ce champ est obligatoire.";
    }
    if (controle.type === "email" && valeur !== "" && !MOTIF_EMAIL.test(valeur)) {
      return "Adresse de courriel invalide.";
    }
    if (controle.name === "telephone" && valeur !== "" && valeur.replace(/[^0-9]/g, "").length < 9) {
      return "Numéro trop court pour être rappelé.";
    }
    return "";
  }

  /** @returns {Array<HTMLInputElement|HTMLSelectElement|HTMLTextAreaElement>} */
  function controles() {
    return Array.prototype.filter.call(
      formulaire.querySelectorAll("input, select, textarea"),
      function (element) { return HORS_VALIDATION.indexOf(element.name) === -1; }
    );
  }

  /* Efface l'erreur dès que le visiteur corrige. */
  controles().forEach(function (controle) {
    controle.addEventListener("input", function () {
      if (controle.closest(".champ--erreur")) { signaler(controle, verifier(controle)); }
    });
    controle.addEventListener("blur", function () {
      if (controle.value.trim() !== "") { signaler(controle, verifier(controle)); }
    });
  });

  /**
   * Réponses du bordereau, dans l'ordre, prêtes à être lues.
   * @returns {Array<string>}
   */
  function resume() {
    var donnees = new FormData(formulaire);
    return CHAMPS.map(function (champ) {
      var valeur = donnees.getAll(champ.nom).map(function (v) { return String(v).trim(); })
        .filter(function (v) { return v !== ""; }).join(", ");
      return champ.libelle + " : " + (valeur === "" ? "—" : valeur);
    });
  }

  /** @returns {string} */
  function objet() {
    var nom = formulaire.elements.namedItem("nom");
    return "Demande de devis — " + (nom instanceof HTMLInputElement ? nom.value.trim() : "");
  }

  /**
   * Affiche le message de retour et y porte le focus.
   * @param {string} texte
   * @param {boolean} [enErreur]
   */
  function annoncer(texte, enErreur) {
    if (!retour) { return; }
    retour.textContent = texte;
    retour.classList.toggle("message-formulaire--erreur", Boolean(enErreur));
    retour.focus();
  }

  /** @param {boolean} actif */
  function patienter(actif) {
    if (!(bouton instanceof HTMLButtonElement)) { return; }
    bouton.disabled = actif;
    bouton.setAttribute("aria-busy", actif ? "true" : "false");
  }

  function ouvrirMessagerie() {
    var lignes = ["Demande de devis déposée depuis le site dsg-renov.ch", ""].concat(resume());
    window.location.href = "mailto:" + DESTINATAIRE +
      "?subject=" + encodeURIComponent(objet()) +
      "&body=" + encodeURIComponent(lignes.join("\n"));
    annoncer("Votre logiciel de messagerie s'ouvre avec la demande préremplie. " +
      "S'il ne s'ouvre pas, écrivez directement à " + DESTINATAIRE + " ou appelez le " + TELEPHONE + ".");
  }

  function envoyer() {
    var donnees = new FormData(formulaire);
    donnees.set("travaux", donnees.getAll("travaux").join(", "));
    donnees.set("_subject", objet());
    patienter(true);

    window.fetch(POINT_ENVOI, { method: "POST", body: donnees, headers: { Accept: "application/json" } })
      .then(function (reponse) {
        if (!reponse.ok) { throw new Error("Réponse " + reponse.status); }
        formulaire.reset();
        annoncer("Merci, votre demande est bien arrivée. Nous vous rappelons pour fixer la visite.");
      })
      .catch(function () {
        annoncer("La demande n'a pas pu partir — votre connexion ou notre service a peut-être " +
          "flanché. Réessayez dans un instant, ou appelez-nous au " + TELEPHONE + ".", true);
      })
      .then(function () { patienter(false); });
  }

  formulaire.addEventListener("submit", function (evenement) {
    evenement.preventDefault();

    var premierFautif = null;
    controles().forEach(function (controle) {
      var message = verifier(controle);
      signaler(controle, message);
      if (message !== "" && premierFautif === null) { premierFautif = controle; }
    });

    if (premierFautif) {
      if (retour) { retour.textContent = ""; }
      premierFautif.focus();
      return;
    }

    /* Un robot a rempli le piège : on fait mine d'avoir reçu. */
    var piege = formulaire.elements.namedItem("site_web");
    if (piege instanceof HTMLInputElement && piege.value !== "") {
      annoncer("Merci, votre demande est bien arrivée.");
      return;
    }

    if (POINT_ENVOI !== "" && "fetch" in window) { envoyer(); } else { ouvrirMessagerie(); }
  });
}());

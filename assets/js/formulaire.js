/* ============================================================
   DSG RÉNOVATION — DEMANDE DE DEVIS
   Validation côté client, puis envoi.

   La demande part vers envoi.php (attribut data-envoi), sur
   l'hébergement du site : le script la transmet par e-mail, photos
   jointes. Réussie, elle mène à merci.html. Si data-envoi est vide,
   repli : le logiciel de messagerie du visiteur s'ouvre avec la
   demande préremplie. Sans JavaScript, l'attribut action du
   formulaire prend le relais.
   ============================================================ */
(function () {
  "use strict";

  var formulaire = document.getElementById("formulaire");
  if (!(formulaire instanceof HTMLFormElement)) { return; }

  var retour = document.getElementById("formulaireRetour");
  var bouton = formulaire.querySelector('button[type="submit"]');
  var POINT_ENVOI = (formulaire.getAttribute("data-envoi") || "").trim();
  var PAGE_MERCI = "merci.html";
  var DESTINATAIRE = "contact@dsg-renov.ch";
  var TELEPHONE = "+41 21 847 02 02";
  var MOTIF_EMAIL = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i;

  /* Photos : mêmes limites qu'envoi.php, vérifiées avant l'envoi pour
     ne pas faire attendre le visiteur sur un envoi voué à l'échec. */
  var PHOTOS_MAX = 6;
  var PHOTO_POIDS_MAX = 8 * 1024 * 1024;
  var PHOTOS_POIDS_TOTAL = 20 * 1024 * 1024;

  /* Champs qui ne se valident pas un par un : les pastilles sont
     facultatives, le piège à robots doit rester vide. */
  var HORS_VALIDATION = ["travaux[]", "site_web"];

  /* Un message d'erreur dit quel champ manque, et pourquoi on le
     demande : « Ce champ est obligatoire » ne dit ni l'un ni l'autre. */
  var MESSAGES_MANQUANTS = {
    message: "Décrivez votre projet en quelques mots\u00a0: pièces, travaux envisagés.",
    nom: "Indiquez votre nom, pour que nous sachions qui rappeler.",
    telephone: "Indiquez un numéro de téléphone pour que nous puissions vous rappeler."
  };

  /** Libellés affichés dans le courriel de repli, dans l'ordre du formulaire. */
  var CHAMPS = [
    { nom: "travaux[]", libelle: "Travaux concernés" },
    { nom: "message", libelle: "Description du projet" },
    { nom: "type", libelle: "Type de bien" },
    { nom: "lieu", libelle: "Commune du bien" },
    { nom: "surface", libelle: "Surface approximative" },
    { nom: "delai", libelle: "Démarrage souhaité" },
    { nom: "nom", libelle: "Nom" },
    { nom: "telephone", libelle: "Téléphone" },
    { nom: "rappel", libelle: "Rappel souhaité" },
    { nom: "email", libelle: "Courriel" }
  ];

  /* ---------- Prestation pré-cochée ----------
     Les boutons « Devis gratuit » d'une page de prestation mènent ici
     avec ?travaux=<prestation> : la case correspondante est cochée. */
  (function precocher() {
    var demandee = new URLSearchParams(window.location.search).get("travaux");
    if (!demandee) { return; }
    Array.prototype.forEach.call(formulaire.querySelectorAll("[data-prestation]"), function (caseACocher) {
      if (caseACocher instanceof HTMLInputElement && caseACocher.getAttribute("data-prestation") === demandee) {
        caseACocher.checked = true;
      }
    });
  }());

  /* ---------- Retour d'un envoi sans JavaScript ----------
     envoi.php renvoie ici avec ?erreur=1 quand la demande n'est pas
     partie : on le dit, avec une autre voie pour nous joindre. */
  if (new URLSearchParams(window.location.search).has("erreur")) {
    window.addEventListener("load", function () {
      annoncer("La demande n'a pas pu partir. Vérifiez les champs et réessayez, " +
        "ou appelez-nous au " + TELEPHONE + ".", true);
    });
  }

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
   * Vérifie les photos choisies.
   * @param {HTMLInputElement} controle
   * @returns {string}
   */
  function verifierPhotos(controle) {
    var fichiers = Array.prototype.slice.call(controle.files || []);
    if (!fichiers.length) { return ""; }
    if (fichiers.length > PHOTOS_MAX) {
      return "Six photos au plus\u00a0: choisissez les plus parlantes.";
    }
    var total = 0;
    for (var i = 0; i < fichiers.length; i += 1) {
      var fichier = fichiers[i];
      total += fichier.size;
      if (fichier.type && fichier.type.indexOf("image/") !== 0) {
        return "«\u00a0" + fichier.name + "\u00a0» n'est pas une photo.";
      }
      if (fichier.size > PHOTO_POIDS_MAX) {
        return "«\u00a0" + fichier.name + "\u00a0» dépasse 8 Mo\u00a0: envoyez une version plus légère.";
      }
    }
    if (total > PHOTOS_POIDS_TOTAL) {
      return "Les photos dépassent 20 Mo au total\u00a0: retirez-en une ou deux.";
    }
    return "";
  }

  /**
   * Vérifie un champ et renvoie son message d'erreur (vide si valide).
   * @param {HTMLInputElement|HTMLSelectElement|HTMLTextAreaElement} controle
   * @returns {string}
   */
  function verifier(controle) {
    if (controle instanceof HTMLInputElement && controle.type === "file") {
      return verifierPhotos(controle);
    }
    var valeur = controle.value.trim();
    if (controle.required && valeur === "") {
      return MESSAGES_MANQUANTS[controle.name] || "Ce champ est nécessaire pour vous répondre.";
    }
    if (controle.type === "email" && valeur !== "" && !MOTIF_EMAIL.test(valeur)) {
      return "Cette adresse e-mail ne semble pas complète (exemple\u00a0: nom@domaine.ch).";
    }
    if (controle.name === "telephone" && valeur !== "" && valeur.replace(/[^0-9]/g, "").length < 9) {
      return "Ce numéro paraît trop court pour être rappelé.";
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
    var evenement = controle instanceof HTMLInputElement && controle.type === "file" ? "change" : "input";
    controle.addEventListener(evenement, function () {
      if (controle.closest(".champ--erreur") || evenement === "change") { signaler(controle, verifier(controle)); }
    });
    controle.addEventListener("blur", function () {
      if (controle.value.trim() !== "") { signaler(controle, verifier(controle)); }
    });
  });

  /**
   * Réponses du formulaire, dans l'ordre, prêtes à être lues.
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
    lignes.push("", "Photos : à joindre à ce message si vous en avez.");
    window.location.href = "mailto:" + DESTINATAIRE +
      "?subject=" + encodeURIComponent(objet()) +
      "&body=" + encodeURIComponent(lignes.join("\n"));
    /* Ce n'est pas une réussite : rien n'est parti tant que le visiteur
       n'a pas envoyé le courriel. Le message le dit, sans cadre vert. */
    annoncer("Votre logiciel de messagerie devrait s'ouvrir avec la demande préremplie\u00a0: " +
      "pensez à l'envoyer. S'il ne s'ouvre pas, écrivez à " + DESTINATAIRE +
      " ou appelez le " + TELEPHONE + ".", true);
  }

  /**
   * Lit les erreurs renvoyées par envoi.php et les pose sur les champs.
   * @param {Object<string,string>} erreurs
   * @returns {boolean} vrai si au moins un champ a été signalé
   */
  function erreursDuServeur(erreurs) {
    var premier = null;
    Object.keys(erreurs || {}).forEach(function (nom) {
      var controle = formulaire.elements.namedItem(nom === "photos" ? "photos[]" : nom);
      if (controle instanceof Element) {
        signaler(controle, erreurs[nom]);
        if (!premier && controle instanceof HTMLElement) { premier = controle; }
      }
    });
    if (premier) { premier.focus(); }
    return premier !== null;
  }

  function envoyer() {
    var donnees = new FormData(formulaire);
    /* Les cases s'appellent travaux[] pour que PHP les reçoive toutes
       sans JavaScript ; envoyées d'ici, elles partent jointes en une
       ligne, que le script accepte aussi. */
    var choisis = donnees.getAll("travaux[]");
    donnees.delete("travaux[]");
    donnees.set("travaux", choisis.join(", "));
    patienter(true);

    window.fetch(POINT_ENVOI, { method: "POST", body: donnees, headers: { Accept: "application/json" } })
      .then(function (reponse) {
        return reponse.json().catch(function () { return {}; }).then(function (corps) {
          return { ok: reponse.ok, statut: reponse.status, corps: corps };
        });
      })
      .then(function (resultat) {
        if (resultat.ok) {
          window.location.href = PAGE_MERCI;
          return;
        }
        if (resultat.statut === 422 && erreursDuServeur(resultat.corps.erreurs)) {
          annoncer("Un champ demande votre attention avant l'envoi.", true);
          return;
        }
        var raison = resultat.statut === 413
          ? "Les photos sont trop lourdes pour partir\u00a0: retirez-en une ou deux, ou envoyez-les ensuite par e-mail à " + DESTINATAIRE + "."
          : resultat.statut === 429
            ? "Plusieurs demandes viennent de partir de cet appareil. Patientez quelques minutes, ou appelez-nous au " + TELEPHONE + "."
            : "La demande n'a pas pu partir. Réessayez dans un instant, ou appelez-nous au " + TELEPHONE + ".";
        annoncer(raison, true);
      })
      .catch(function () {
        annoncer("La demande n'a pas pu partir\u00a0: la connexion semble interrompue. " +
          "Réessayez dans un instant, ou appelez-nous au " + TELEPHONE + ".", true);
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
      window.location.href = PAGE_MERCI;
      return;
    }

    if (POINT_ENVOI !== "" && "fetch" in window) { envoyer(); } else { ouvrirMessagerie(); }
  });
}());

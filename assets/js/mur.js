/* ============================================================
   DSG RÉNOVATION — LE MUR À L'ENTRÉE
   Le visiteur qui arrive trouve un mur de briques passé à la chaux,
   une plaque vissée dessus : « Pour entrer sur le site, cassez le
   mur. » Trois coups, pas un de plus : le premier le fissure, le
   deuxième en fait tomber des briques, le troisième l'abat — une onde
   part du point frappé, les briques tombent, et le site est derrière.

   Les fissures se tracent comme les traits du plan (09-trace.css) :
   d'un seul trait, depuis le point frappé. Un coup porté sur la plaque
   fissure le mur juste à côté d'elle, là où l'on voit les briques ;
   la plaque, elle, tremble, et penche au deuxième coup.

   Le mur se dresse devant qui arrive de l'extérieur du site, une fois
   par onglet (outils/mur.py décide, avant le premier rendu). Au clavier, le bouton « Frapper le mur » donne
   les coups ; la consigne annonce ce qui reste. Mouvement réduit :
   les fissures et les trous paraissent d'un coup, et le mur s'efface
   au troisième au lieu de tomber. Sans canevas, les trois coups
   restent, le mur s'efface au dernier.
   ============================================================ */
(function () {
  "use strict";

  var racine = document.documentElement;
  var CLE = "dsg-mur";

  /** L'onglet est entré : le mur ne s'y dressera plus (outils/mur.py). */
  function noter() {
    try { window.sessionStorage.setItem(CLE, "1"); } catch (erreur) { /* stockage refusé */ }
  }

  /** @type {HTMLElement|null} */
  var mur = document.getElementById("mur");
  if (!mur || !racine.classList.contains("mur-ferme")) {
    if (mur) { mur.remove(); }
    return;
  }

  /** @type {HTMLCanvasElement} */
  var toile = /** @type {HTMLCanvasElement} */ (mur.querySelector(".mur__briques"));
  /** @type {HTMLElement} */
  var plaque = /** @type {HTMLElement} */ (mur.querySelector(".mur__plaque"));
  var consigne = document.getElementById("murConsigne");
  /* Le texte de la consigne ; la plaque garde la hauteur de la plus
     longue (20-mur.css). */
  var consigneTexte = consigne ? consigne.querySelector("span") || consigne : null;
  var bouton = document.getElementById("murFrapper");
  var marques = mur.querySelectorAll(".mur__coups li");
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var COUPS = 3;
  /* Ce que dit la consigne avant chaque coup, puis quand le mur tombe.
     Les espaces insécables que outils/typographie.py pose dans les pages. */
  var CONSIGNES = [
    "Trois coups suffisent : frappez où vous voulez.",
    "Ça se fissure. Encore deux coups.",
    "Ça tient encore. Un dernier coup !",
    "Le mur tombe. Bienvenue chez DSG Rénovation."
  ];
  /* Une brique fait 94 % de son pas en longueur, son rang 36 % ; le joint
     6 % (le motif --mur-motif de 00-jetons.css, à la même échelle). */
  var RANG = 0.36;
  var JOINT = 0.06;
  /* Pesanteur des briques et des éclats, en px/s². */
  var PESANTEUR = 3200;
  /* L'onde qui abat le mur : px parcourus par milliseconde. */
  var ONDE = 2.2;
  /* Une fissure se trace en 260 ms, quelle que soit sa longueur. */
  var TRACE = 260;
  /* Au-delà, le mur se retire même s'il reste une brique en vue. */
  var CHUTE_MAX = 2600;
  var GRAINE = 20261012;
  var PIXELS_MAX = 6e6;
  /* Le calque, repeint à chaque image, est moins dense : deux millions
     de points au plus. Ce qui bouge n'a pas besoin du grain du mur. */
  var PIXELS_CALQUE = 2e6;

  var style = window.getComputedStyle(mur);
  var teintes = style.getPropertyValue("--mur-teintes").trim().split(/\s+/);
  var mortier = style.getPropertyValue("--mur-mortier").trim() || "#CDC6BC";
  var encre = style.getPropertyValue("--mur-fissure").trim() || "#1B1B1B";
  var rgbOmbre = style.getPropertyValue("--c-encre-rgb").trim() || "27,27,27";
  var rgbLumiere = style.getPropertyValue("--c-blanc-rgb").trim() || "255,255,255";
  if (!teintes[0]) { teintes = ["#F4F1EC"]; }

  /** @param {number} a */
  function ombre(a) { return "rgba(" + rgbOmbre + "," + a + ")"; }
  /** @param {number} a */
  function lumiere(a) { return "rgba(" + rgbLumiere + "," + a + ")"; }

  /**
   * Hasard reproductible (mulberry32) : un coup rejoué après un
   * redimensionnement redessine les mêmes fissures.
   * @param {number} graine
   * @returns {function(): number}
   */
  function hasard(graine) {
    var a = graine >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* ---------- La page derrière ----------
     Tant que le mur tient, rien d'autre ne reçoit le focus. */
  var inertes = [];
  Array.prototype.forEach.call(document.body.children, function (element) {
    if (element === mur || element.tagName === "SCRIPT" || element.hasAttribute("inert")) { return; }
    element.setAttribute("inert", "");
    inertes.push(element);
  });

  /* Deux toiles : le mur peint, qui ne change qu'à un coup (les
     fissures s'y tracent par petits bouts), et par-dessus, sous la
     plaque, le calque de ce qui bouge — éclats, poussière, briques qui
     tombent —, seul repeint à chaque image. */
  var mctx = toile.getContext ? toile.getContext("2d") : null;
  var calque = document.createElement("canvas");
  calque.className = "mur__briques";
  calque.setAttribute("aria-hidden", "true");
  toile.parentNode.insertBefore(calque, toile.nextSibling);
  var ctx = mctx ? calque.getContext("2d") : null;

  var larg = 0, haut = 0, dpr = 1, dprCalque = 1;
  var L = 96, H = 34.56, J = 5.76;
  /** @type {Array<{x:number,y:number,teinte:string,graine:number,tombee:boolean}>} */
  var briques = [];
  var coups = 0;
  var abattu = false;
  var ouvert = false;
  /** Les coups portés, en fractions du mur, pour les rejouer. */
  var impacts = [];
  /** Fissures en train de se tracer. */
  var salves = [];
  /** Briques qui tombent. */
  var corps = [];
  /** Éclats et poussière. */
  var eclats = [];
  var poussieres = [];
  /** La plaque penche au deuxième coup (degrés), puis tombe. */
  var inclinaison = 0;
  var chutePlaque = null;
  var debutChute = 0;
  var boucle = 0;
  var dernier = 0;
  /* Le calque porte encore l'image précédente. */
  var calqueSali = false;

  /** Le pas d'une brique, réglé par la feuille (--mur-pas). */
  function lirePas() {
    var pas = parseFloat(window.getComputedStyle(mur).backgroundSize);
    if (!(pas > 0)) { pas = Math.min(128, Math.max(72, window.innerWidth * 0.085)); }
    return pas;
  }

  /* ---------- Le mur peint ---------- */

  /**
   * Une brique et son mortier (à droite et dessous), sur le mur peint.
   * Un badigeon inégal, un grain, une arête éclairée, parfois un coin
   * écorné.
   * @param {CanvasRenderingContext2D} c
   * @param {{x:number,y:number,teinte:string,graine:number}} b
   */
  function peindreBrique(c, b) {
    var w = L - J, h = H - J, rnd = hasard(b.graine);
    c.fillStyle = mortier;
    c.fillRect(b.x, b.y, L, H);
    /* L'ombre de la brique sur le joint qui la porte. */
    c.fillStyle = ombre(0.1);
    c.fillRect(b.x, b.y + h, L, Math.max(1, J * 0.4));
    c.fillStyle = b.teinte;
    c.fillRect(b.x, b.y, w, h);
    /* Le badigeon : plus mince d'un côté, la brique y transparaît. */
    var gx = b.x + rnd() * w, gy = b.y + rnd() * h;
    var halo = c.createRadialGradient(gx, gy, 0, gx, gy, w * 0.7);
    halo.addColorStop(0, ombre(0.02 + rnd() * 0.035));
    halo.addColorStop(1, ombre(0));
    c.fillStyle = halo;
    c.fillRect(b.x, b.y, w, h);
    for (var k = 0; k < 9; k++) {
      c.fillStyle = ombre(0.05 + rnd() * 0.07);
      c.fillRect(b.x + rnd() * (w - 2), b.y + rnd() * (h - 2), 1 + rnd() * 1.2, 1 + rnd() * 1.2);
    }
    c.fillStyle = lumiere(0.75);
    c.fillRect(b.x, b.y, w, 1);
    c.fillStyle = ombre(0.07);
    c.fillRect(b.x, b.y + h - 1.5, w, 1.5);
    if (rnd() < 0.16) {
      var e = 2 + rnd() * 4, droite = rnd() < 0.5, bas = rnd() < 0.5;
      var cx = droite ? b.x + w : b.x, cy = bas ? b.y + h : b.y;
      c.fillStyle = mortier;
      c.beginPath();
      c.moveTo(cx, cy);
      c.lineTo(cx + (droite ? -e : e), cy);
      c.lineTo(cx, cy + (bas ? -e * 0.8 : e * 0.8));
      c.closePath();
      c.fill();
    }
  }

  /** Le mur entier, à la taille de l'écran, puis les coups déjà portés. */
  function monter() {
    larg = mur.clientWidth;
    haut = mur.clientHeight;
    if (!ctx || !mctx || !larg || !haut) { return; }
    /* Deux fois la densité de l'écran au plus, et six millions de
       points : un écran de 27 pouces ne réclame pas une toile de quinze
       millions. */
    dpr = Math.min(window.devicePixelRatio || 1, 2, Math.sqrt(PIXELS_MAX / (larg * haut)));
    dprCalque = Math.min(dpr, Math.max(0.75, Math.sqrt(PIXELS_CALQUE / (larg * haut))));
    L = lirePas();
    H = L * RANG;
    J = L * JOINT;
    toile.width = Math.round(larg * dpr);
    toile.height = Math.round(haut * dpr);
    calque.width = Math.round(larg * dprCalque);
    calque.height = Math.round(haut * dprCalque);
    mctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    mctx.clearRect(0, 0, larg, haut);

    briques = [];
    var rnd = hasard(GRAINE);
    for (var r = 0; r * H < haut; r++) {
      /* Les rangs impairs décalés d'une demi-brique, comme le motif. */
      for (var x = r % 2 ? -L / 2 : 0; x < larg; x += L) {
        briques.push({
          x: x, y: r * H,
          teinte: teintes[Math.floor(rnd() * teintes.length)],
          graine: Math.floor(rnd() * 4294967296),
          tombee: false
        });
      }
    }
    briques.forEach(function (b) { peindreBrique(mctx, b); });

    salves = [];
    corps = [];
    impacts.forEach(function (impact) { porter(impact, true); });
    mur.classList.add("est-peint");
    peindre(window.performance.now());
  }

  /* ---------- Fissures ---------- */

  /**
   * Une branche de fissure : une ligne brisée qui dévie un peu à chaque
   * pas, et lâche parfois une branche plus fine.
   * @param {Array} traits
   * @param {number} x
   * @param {number} y
   * @param {number} angle
   * @param {number} longueur
   * @param {number} epaisseur
   * @param {number} decalage  distance au point frappé où elle part
   * @param {function(): number} rnd
   * @param {number} profondeur
   */
  function branche(traits, x, y, angle, longueur, epaisseur, decalage, rnd, profondeur) {
    var points = [x, y], parcouru = 0;
    while (parcouru < longueur) {
      angle += (rnd() - 0.5) * 0.8;
      var pas = L * 0.16 * (0.6 + rnd() * 0.8);
      x += Math.cos(angle) * pas;
      y += Math.sin(angle) * pas;
      parcouru += pas;
      points.push(x, y);
      if (profondeur < 1 && rnd() < 0.2) {
        branche(traits, x, y, angle + (rnd() < 0.5 ? -1 : 1) * (0.5 + rnd() * 0.5),
          (longueur - parcouru) * 0.6 + L * 0.2, 1, decalage + parcouru, rnd, profondeur + 1);
      }
    }
    traits.push({ points: points, epaisseur: epaisseur, decalage: decalage, fin: decalage + parcouru });
  }

  /**
   * Les fissures d'un coup : des branches en étoile, plus longues et plus
   * nombreuses au deuxième.
   * @param {number} x0
   * @param {number} y0
   * @param {number} force  0 au premier coup, 1 au deuxième
   * @param {function(): number} rnd
   */
  function fissures(x0, y0, force, rnd) {
    var traits = [];
    var n = 5 + Math.floor(rnd() * 3) + force * 2;
    var portee = L * (1.4 + force * 1.1);
    var depart = rnd() * Math.PI * 2;
    for (var i = 0; i < n; i++) {
      var angle = depart + (i / n) * Math.PI * 2 + (rnd() - 0.5) * 0.7;
      branche(traits, x0, y0, angle, portee * (0.55 + rnd() * 0.65), 1.5, 0, rnd, 0);
    }
    return traits;
  }

  /**
   * Le bout de fissure compris entre les distances `de` et `a` du point
   * frappé : en creux, une arête de chaux dessous, l'encre dessus. Elle
   * ne court que sur les briques encore en place (source-atop) : jamais
   * dans un trou.
   * @param {CanvasRenderingContext2D} c
   * @param {{points:Array<number>,epaisseur:number,decalage:number}} trait
   * @param {number} de
   * @param {number} a
   */
  function tracer(c, trait, de, a) {
    /* Un demi-pixel de recouvrement : aucun jour entre deux bouts. */
    var debut = Math.max(0, de - trait.decalage - 0.5), fin = a - trait.decalage;
    if (fin <= debut) { return; }
    var p = trait.points, parcouru = 0, ouvert = false;
    c.beginPath();
    for (var i = 2; i < p.length && parcouru < fin; i += 2) {
      var dx = p[i] - p[i - 2], dy = p[i + 1] - p[i - 1], d = Math.sqrt(dx * dx + dy * dy);
      if (parcouru + d > debut) {
        if (!ouvert) {
          var k0 = Math.max(0, debut - parcouru) / d;
          c.moveTo(p[i - 2] + dx * k0, p[i - 1] + dy * k0);
          ouvert = true;
        }
        var k1 = Math.min(1, (fin - parcouru) / d);
        c.lineTo(p[i - 2] + dx * k1, p[i - 1] + dy * k1);
      }
      parcouru += d;
    }
    if (!ouvert) { return; }
    c.save();
    c.globalCompositeOperation = "source-atop";
    c.lineJoin = "miter";
    c.lineCap = "butt";
    c.lineWidth = trait.epaisseur;
    c.translate(0.8, 0.9);
    c.strokeStyle = lumiere(0.85);
    c.stroke();
    c.translate(-0.8, -0.9);
    c.strokeStyle = encre;
    c.stroke();
    c.restore();
  }

  /**
   * Le creux du coup : une écaille de badigeon arrachée, plus large au
   * deuxième coup.
   * @param {CanvasRenderingContext2D} c
   * @param {number} x
   * @param {number} y
   * @param {number} force
   * @param {function(): number} rnd
   */
  function cratere(c, x, y, force, rnd) {
    var r = H * (0.34 + force * 0.14);
    c.save();
    c.globalCompositeOperation = "source-atop";
    [[1, 0.13], [0.55, 0.22]].forEach(function (couche) {
      c.fillStyle = ombre(couche[1]);
      c.beginPath();
      for (var k = 0; k < 9; k++) {
        var a = (k / 9) * Math.PI * 2, rr = r * couche[0] * (0.6 + rnd() * 0.6);
        c[k ? "lineTo" : "moveTo"](x + Math.cos(a) * rr * 1.25, y + Math.sin(a) * rr);
      }
      c.closePath();
      c.fill();
    });
    c.restore();
  }

  /* ---------- Les coups ---------- */

  /**
   * La brique sous un point, ou null.
   * @param {number} x
   * @param {number} y
   */
  function briqueSous(x, y) {
    for (var i = 0; i < briques.length; i++) {
      var b = briques[i];
      if (!b.tombee && x >= b.x && x < b.x + L && y >= b.y && y < b.y + H) { return b; }
    }
    return null;
  }

  /**
   * Une brique repeinte seule, avec les coups qu'elle a reçus : la même
   * graine, les mêmes creux, les mêmes fissures. Rien n'est relu sur le
   * mur peint (une relecture de la toile coûte, au téléphone, plus que
   * de tout repeindre).
   * @param {{x:number,y:number,teinte:string,graine:number}} b
   * @param {number} sx  coin de la part visible, en points de la toile
   * @param {number} sy
   * @param {number} sw
   * @param {number} sh
   * @returns {HTMLCanvasElement}
   */
  function repeindre(b, sx, sy, sw, sh) {
    var piece = document.createElement("canvas");
    piece.width = sw;
    piece.height = sh;
    var c = piece.getContext("2d");
    c.setTransform(dpr, 0, 0, dpr, -sx, -sy);
    peindreBrique(c, b);
    impacts.forEach(function (impact) {
      var rnd = hasard(impact.graine), x = impact.x * larg, y = impact.y * haut;
      cratere(c, x, y, impact.coup - 1, rnd);
      fissures(x, y, impact.coup - 1, rnd).forEach(function (t) { tracer(c, t, 0, Infinity); });
    });
    return piece;
  }

  /**
   * Une brique se détache et tombe. Au deuxième coup, elle est repeinte
   * à part et laisse un trou ; quand le mur s'abat (`entier`), le mur
   * peint, masqué, sert lui-même de source.
   * Seule la part de la brique qui était à l'écran tombe : celles du
   * bord gauche en dépassaient d'une moitié.
   * @param {{x:number,y:number,tombee:boolean}} b
   * @param {boolean} entier
   * @param {number} vx
   * @param {number} vy
   * @param {number} va
   * @param {number} retard  ms avant qu'elle ne parte
   * @param {number} maintenant
   */
  function detacher(b, entier, vx, vy, va, retard, maintenant) {
    b.tombee = true;
    var x0 = Math.max(0, b.x), y0 = Math.max(0, b.y);
    var x1 = Math.min(larg, b.x + L), y1 = Math.min(haut, b.y + H);
    if (x1 <= x0 || y1 <= y0) { return; }
    var sx = Math.round(x0 * dpr), sy = Math.round(y0 * dpr);
    var sw = Math.max(1, Math.round(x1 * dpr) - sx), sh = Math.max(1, Math.round(y1 * dpr) - sy);
    var source = toile;
    if (!entier) {
      source = repeindre(b, sx, sy, sw, sh);
      sx = sy = 0;
      mctx.clearRect(b.x, b.y, L, H);
    }
    corps.push({
      source: source, sx: sx, sy: sy, sw: sw, sh: sh,
      dx: x0 - b.x - L / 2, dy: y0 - b.y - H / 2, dw: x1 - x0, dh: y1 - y0,
      x: b.x + L / 2, y: b.y + H / 2, a: 0,
      vx: vx, vy: vy, va: va,
      depart: maintenant + retard
    });
  }

  /**
   * Des éclats et un nuage de poussière, au point frappé.
   * @param {number} x
   * @param {number} y
   * @param {number} force
   * @param {string} teinte
   */
  function projeter(x, y, force, teinte) {
    var n = 10 + force * 8;
    for (var i = 0; i < n; i++) {
      var a = -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 1.7;
      var v = 140 + Math.random() * (260 + force * 160);
      eclats.push({
        x: x, y: y, a: Math.random() * 6,
        vx: Math.cos(a) * v, vy: Math.sin(a) * v, va: (Math.random() - 0.5) * 18,
        taille: 2 + Math.random() * (3 + force * 2),
        teinte: Math.random() < 0.3 ? mortier : teinte,
        vie: 0.9 + Math.random() * 0.5
      });
    }
    for (var k = 0; k < 3 + force; k++) {
      poussieres.push({
        x: x + (Math.random() - 0.5) * H, y: y + (Math.random() - 0.5) * H * 0.6,
        r: H * (0.4 + Math.random() * 0.4), vie: 0, duree: 0.6 + Math.random() * 0.35
      });
    }
  }

  /**
   * Un coup sur le mur : rejoué d'un coup (redimensionnement, mouvement
   * réduit) ou animé.
   * @param {{x:number,y:number,coup:number,graine:number}} impact
   * @param {boolean} aussitot
   */
  function porter(impact, aussitot) {
    if (impact.coup >= COUPS) { return; }
    var x = impact.x * larg, y = impact.y * haut;
    var force = impact.coup - 1;
    var rnd = hasard(impact.graine);
    var touchee = briqueSous(x, y);
    var maintenant = window.performance.now();

    if (!aussitot) { achever(); }
    cratere(mctx, x, y, force, rnd);
    var traits = fissures(x, y, force, rnd);

    /* Au deuxième coup, les briques autour du point frappé tombent. */
    if (impact.coup === 2) {
      briques.forEach(function (b) {
        if (b.tombee) { return; }
        var dx = b.x + L / 2 - x, dy = b.y + H / 2 - y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (b !== touchee && d > L * 0.8 * (0.8 + rnd() * 0.4)) { return; }
        if (aussitot) {
          b.tombee = true;
          mctx.clearRect(b.x, b.y, L, H);
          return;
        }
        detacher(b, false, dx / (d || 1) * (60 + Math.random() * 140),
          -60 - Math.random() * 160, (Math.random() - 0.5) * 7, Math.random() * 40, maintenant);
      });
    }

    var fin = traits.reduce(function (m, t) { return Math.max(m, t.fin); }, 0);
    if (aussitot) {
      traits.forEach(function (t) { tracer(mctx, t, 0, Infinity); });
    } else {
      salves.push({ traits: traits, debut: maintenant, vitesse: fin / TRACE, fin: fin, trace: 0 });
      projeter(x, y, force, touchee ? touchee.teinte : teintes[0]);
    }
  }

  /** Les fissures en cours, tracées jusqu'au bout sur le mur peint. */
  function achever() {
    salves.forEach(function (salve) {
      salve.traits.forEach(function (t) { tracer(mctx, t, salve.trace, Infinity); });
    });
    salves = [];
  }

  /**
   * Le troisième coup : une onde part du point frappé, chaque brique
   * tombe quand elle l'atteint, la plaque avec elles.
   * @param {number} x0
   * @param {number} y0
   */
  function abattre(x0, y0) {
    abattu = true;
    var maintenant = window.performance.now();
    if (!ctx || reduit) {
      mur.classList.add("est-efface");
      window.setTimeout(ouvrir, 320);
      return;
    }
    if (plaque.getAnimations) {
      plaque.getAnimations().forEach(function (animation) { animation.cancel(); });
    }
    achever();
    toile.style.visibility = "hidden";
    briques.forEach(function (b) {
      if (b.tombee) { return; }
      var dx = b.x + L / 2 - x0, dy = b.y + H / 2 - y0;
      var d = Math.sqrt(dx * dx + dy * dy) || 1;
      /* Près du coup, les briques sautent ; plus loin, elles s'affaissent. */
      var pres = Math.max(0, 1 - d / (L * 3));
      detacher(b, true, dx / d * (30 + Math.random() * 120 + pres * 260),
        -Math.random() * 90 - pres * 260, (Math.random() - 0.5) * (3 + pres * 8),
        d / ONDE * (0.85 + Math.random() * 0.3), maintenant);
    });
    var boite = plaque.getBoundingClientRect();
    var pdx = boite.left + boite.width / 2 - x0, pdy = boite.top + boite.height / 2 - y0;
    chutePlaque = {
      y: 0, vy: -120, a: inclinaison * Math.PI / 180,
      va: (pdx < 0 ? -1 : 1) * (0.5 + Math.random() * 0.5),
      depart: maintenant + Math.sqrt(pdx * pdx + pdy * pdy) / ONDE * 0.6 + 80
    };
    debutChute = maintenant;
    projeter(x0, y0, 2, (briqueSous(x0, y0) || { teinte: teintes[0] }).teinte);
    relancer();
  }

  /* ---------- La plaque ---------- */

  /** La plaque tremble ; au deuxième coup, une vis lâche et elle penche. */
  function secouer() {
    var avant = inclinaison;
    if (coups === 2) {
      inclinaison = 2;
      plaque.classList.add("est-devissee");
    }
    plaque.style.transform = "rotate(" + inclinaison + "deg)";
    if (reduit || !plaque.animate) { return; }
    plaque.animate([
      { transform: "rotate(" + avant + "deg)" },
      { transform: "translate(-3px, 1px) rotate(" + (avant + 1.4) + "deg)" },
      { transform: "translate(2px, 0) rotate(" + (inclinaison - 0.9) + "deg)" },
      { transform: "rotate(" + inclinaison + "deg)" }
    ], { duration: 360, easing: "cubic-bezier(.23,1,.32,1)" });
  }

  /**
   * Un coup porté sur la plaque fissure le mur à côté d'elle : on y
   * voit les briques.
   * @param {number} x
   * @param {number} y
   * @returns {Array<number>}
   */
  function horsPlaque(x, y) {
    var boite = plaque.getBoundingClientRect();
    var marge = L * 0.6;
    if (x < boite.left - marge || x > boite.right + marge ||
        y < boite.top - marge || y > boite.bottom + marge) { return [x, y]; }
    var cx = boite.left + boite.width / 2, cy = boite.top + boite.height / 2;
    var places = [];
    /* Des points tout autour de la plaque, gardés dans l'écran. */
    for (var k = 0; k < 24; k++) {
      var a = (k / 24) * Math.PI * 2;
      var px = cx + Math.cos(a) * (boite.width / 2 + marge + L * 0.3);
      var py = cy + Math.sin(a) * (boite.height / 2 + marge + L * 0.3);
      if (px > H && px < larg - H && py > H && py < haut - H) { places.push([px, py]); }
    }
    if (!places.length) { return [x, y]; }
    /* Le plus proche du point frappé, à un rien près. */
    places.sort(function (p, q) {
      return Math.hypot(p[0] - x, p[1] - y) - Math.hypot(q[0] - x, q[1] - y);
    });
    return places[Math.floor(Math.random() * Math.min(3, places.length))];
  }

  /**
   * Un coup, au point (x, y) du mur.
   * @param {number} x
   * @param {number} y
   */
  function frapper(x, y) {
    if (coups >= COUPS || ouvert) { return; }
    coups += 1;
    if (marques[coups - 1]) { marques[coups - 1].classList.add("est-frappe"); }
    if (consigneTexte) { consigneTexte.textContent = CONSIGNES[coups]; }
    try {
      if (coups < COUPS) { secouer(); }
      if (coups === COUPS) {
        abattre(x, y);
        return;
      }
      if (!ctx) { return; }
      var point = horsPlaque(x, y);
      var impact = {
        x: point[0] / larg, y: point[1] / haut, coup: coups,
        graine: Math.floor(Math.random() * 4294967296)
      };
      impacts.push(impact);
      porter(impact, reduit);
      relancer();
    } catch (erreur) {
      /* Rien ne doit retenir le visiteur derrière le mur. */
      ouvrir();
    }
  }

  /* ---------- L'animation ---------- */

  function relancer() {
    if (boucle || reduit) {
      if (reduit) { peindre(window.performance.now()); }
      return;
    }
    dernier = window.performance.now();
    boucle = window.requestAnimationFrame(image);
  }

  /** @param {number} t */
  function image(t) {
    var dt = Math.min(0.034, Math.max(0, (t - dernier) / 1000));
    dernier = t;
    var actif = peindre(t, dt);
    if (abattu && (!actif || t - debutChute > CHUTE_MAX)) {
      boucle = 0;
      ouvrir();
      return;
    }
    boucle = actif ? window.requestAnimationFrame(image) : 0;
  }

  /**
   * Une image : les fissures s'allongent sur le mur peint ; le calque,
   * effacé, reçoit les briques qui tombent, les éclats et la poussière ;
   * la plaque tombe. Renvoie vrai tant que quelque chose bouge.
   * @param {number} t
   * @param {number} [dt]
   * @returns {boolean}
   */
  function peindre(t, dt) {
    if (!ctx) { return false; }
    dt = dt || 0;
    var actif = false;
    if (calqueSali) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, calque.width, calque.height);
      calqueSali = false;
    }
    ctx.setTransform(dprCalque, 0, 0, dprCalque, 0, 0);

    /* Les fissures s'allongent sur le mur peint, du bout tracé à
       l'image précédente jusqu'où elles en sont. */
    salves = salves.filter(function (salve) {
      var s = Math.min(salve.fin, (t - salve.debut) * salve.vitesse);
      actif = true;
      if (s <= salve.trace) { return true; }
      salve.traits.forEach(function (trait) { tracer(mctx, trait, salve.trace, s); });
      salve.trace = s;
      return s < salve.fin;
    });

    corps = corps.filter(function (c) {
      if (t >= c.depart) {
        c.vy += PESANTEUR * dt;
        c.x += c.vx * dt;
        c.y += c.vy * dt;
        c.a += c.va * dt;
      }
      if (c.y - L > haut) { return false; }
      dessinerBrique(c);
      actif = true;
      return true;
    });

    eclats = eclats.filter(function (e) {
      e.vie -= dt;
      e.vy += PESANTEUR * 0.8 * dt;
      e.x += e.vx * dt;
      e.y += e.vy * dt;
      e.a += e.va * dt;
      if (e.vie <= 0 || e.y > haut + 20) { return false; }
      ctx.save();
      ctx.globalAlpha = Math.min(1, e.vie / 0.3);
      ctx.translate(e.x, e.y);
      ctx.rotate(e.a);
      ctx.fillStyle = e.teinte;
      ctx.fillRect(-e.taille / 2, -e.taille * 0.35, e.taille, e.taille * 0.7);
      ctx.fillStyle = ombre(0.18);
      ctx.fillRect(-e.taille / 2, e.taille * 0.2, e.taille, e.taille * 0.15);
      ctx.restore();
      actif = true;
      return true;
    });

    poussieres = poussieres.filter(function (p) {
      p.vie += dt;
      var k = p.vie / p.duree;
      if (k >= 1) { return false; }
      var r = p.r * (1 + k * 1.6);
      var nuage = ctx.createRadialGradient(p.x, p.y - k * H * 0.5, 0, p.x, p.y - k * H * 0.5, r);
      nuage.addColorStop(0, "rgba(" + rgbLumiere + "," + (0.55 * (1 - k)) + ")");
      nuage.addColorStop(1, "rgba(" + rgbLumiere + ",0)");
      ctx.fillStyle = nuage;
      ctx.fillRect(p.x - r, p.y - k * H * 0.5 - r, r * 2, r * 2);
      actif = true;
      return true;
    });

    if (chutePlaque) {
      var p = chutePlaque;
      if (t >= p.depart) {
        p.vy += PESANTEUR * dt;
        p.y += p.vy * dt;
        p.a += p.va * dt;
      }
      plaque.style.transform = "translateY(" + p.y.toFixed(1) + "px) rotate(" + p.a.toFixed(3) + "rad)";
      if (p.y < haut * 1.2) { actif = true; }
    }
    calqueSali = corps.length > 0 || eclats.length > 0 || poussieres.length > 0;
    return actif;
  }

  /**
   * Une brique en chute, prise à sa source.
   * @param {{source:HTMLCanvasElement,sx:number,sy:number,sw:number,sh:number,dx:number,dy:number,dw:number,dh:number,x:number,y:number,a:number}} c
   */
  function dessinerBrique(c) {
    ctx.save();
    ctx.translate(c.x, c.y);
    ctx.rotate(c.a);
    ctx.drawImage(c.source, c.sx, c.sy, c.sw, c.sh, c.dx, c.dy, c.dw, c.dh);
    ctx.restore();
  }

  /* ---------- Entrer ---------- */

  function ouvrir() {
    if (ouvert) { return; }
    ouvert = true;
    noter();
    if (boucle) { window.cancelAnimationFrame(boucle); }
    window.removeEventListener("resize", surRedimension);
    inertes.forEach(function (element) { element.removeAttribute("inert"); });
    racine.classList.remove("mur-ferme");
    mur.remove();
    /* Le plan se trace maintenant (motion.js). */
    document.dispatchEvent(new Event("mur:ouvert"));
  }

  /* ---------- Les gestes ---------- */

  mur.addEventListener("pointerdown", function (evenement) {
    if (evenement.button !== 0) { return; }
    var boite = mur.getBoundingClientRect();
    frapper(evenement.clientX - boite.left, evenement.clientY - boite.top);
  });
  /* Le clavier (Entrée, Espace) : un clic sans pointeur. Les clics d'une
     souris ou d'un doigt ont déjà frappé à l'appui. */
  if (bouton) {
    bouton.addEventListener("click", function (evenement) {
      if (evenement.detail !== 0) { return; }
      var boite = bouton.getBoundingClientRect();
      frapper(boite.left + boite.width * Math.random(), boite.top + boite.height / 2);
    });
  }
  mur.addEventListener("contextmenu", function (evenement) { evenement.preventDefault(); });

  var attente = 0;
  function surRedimension() {
    window.clearTimeout(attente);
    attente = window.setTimeout(function () { if (!abattu) { monter(); } }, 120);
  }
  window.addEventListener("resize", surRedimension);

  monter();
  mur.focus({ preventScroll: true });
  /* Le mur est monté : le script de tête ne le retirera pas de lui-même
     (outils/mur.py). */
  racine.classList.add("mur-pret");
}());

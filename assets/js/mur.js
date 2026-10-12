/* ============================================================
   DSG RÉNOVATION — LE MUR À L'ENTRÉE
   Le visiteur qui arrive trouve un mur de briques passé à la chaux,
   un cartouche de plan posé dessus : « Cassez le mur pour entrer. »
   Trois coups, pas un de plus : le premier fait tomber la
   brique frappée, le deuxième celles qui l'entourent — le site paraît
   dans le trou —, le troisième abat le mur : une onde part du point
   frappé, les briques tombent, et le site est derrière. Pas de
   fissure : des briques qui tombent, des éclats, de la poussière.

   Un coup porté sur le cartouche fait tomber les briques juste à côté
   de lui, là où l'on voit le mur. Le cartouche ne bouge pas : il tombe
   avec le mur, au troisième coup.

   Le mur se dresse devant qui arrive de l'extérieur du site, une fois
   par onglet (outils/mur.py décide, avant le premier rendu). Au
   clavier, le bouton « Frapper » donne les coups ; les lecteurs
   d'écran entendent ce qui reste. Mouvement réduit : les trous paraissent d'un
   coup, et le mur s'efface au troisième au lieu de tomber. Sans
   canevas, les trois coups restent, le mur s'efface au dernier.
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
  var cartouche = /** @type {HTMLElement} */ (mur.querySelector(".mur__cartouche"));
  var annonce = document.getElementById("murAnnonce");
  var bouton = document.getElementById("murFrapper");
  var marques = mur.querySelectorAll(".mur__coups li");
  var reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var COUPS = 3;
  /* Ce qu'entend un lecteur d'écran avant chaque coup, puis quand le
     mur tombe. À l'écran, les trois carrés le disent. */
  var ANNONCES = ["Trois coups.", "Encore deux coups.", "Un dernier coup.", "Le mur tombe."];
  /* Une brique fait 94 % de son pas en longueur, son rang 36 % ; le joint
     6 % (le motif --mur-motif de 00-jetons.css, à la même échelle). */
  var RANG = 0.36;
  var JOINT = 0.06;
  /* Pesanteur des briques et des éclats, en px/s². */
  var PESANTEUR = 3200;
  /* L'onde qui abat le mur : px parcourus par milliseconde. */
  var ONDE = 2.2;
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
  var rgbOmbre = style.getPropertyValue("--c-encre-rgb").trim() || "27,27,27";
  var rgbLumiere = style.getPropertyValue("--c-blanc-rgb").trim() || "255,255,255";
  if (!teintes[0]) { teintes = ["#F4F1EC"]; }

  /** @param {number} a */
  function ombre(a) { return "rgba(" + rgbOmbre + "," + a + ")"; }
  /** @param {number} a */
  function lumiere(a) { return "rgba(" + rgbLumiere + "," + a + ")"; }

  /**
   * Hasard reproductible (mulberry32) : un coup rejoué après un
   * redimensionnement fait tomber les mêmes briques.
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

  /* Deux toiles : le mur peint, qui ne change qu'à un coup (une brique
     en part, un trou reste), et par-dessus, sous le cartouche, le calque
     de ce qui bouge — éclats, poussière, briques qui tombent —, seul
     repeint à chaque image. */
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
  /** Briques qui tombent. */
  var corps = [];
  /** Éclats et poussière. */
  var eclats = [];
  var poussieres = [];
  var chuteCartouche = null;
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
    /* Un grain léger : à côté du cartouche, net, un grain plus fort
       faisait sale. */
    for (var k = 0; k < 4; k++) {
      c.fillStyle = ombre(0.03 + rnd() * 0.05);
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

    corps = [];
    impacts.forEach(function (impact) { porter(impact, true); });
    mur.classList.add("est-peint");
    peindre(window.performance.now());
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
   * Une brique repeinte seule, de la même graine. Rien n'est relu sur le
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
   * Quelques éclats et un peu de poussière, au point frappé : de quoi
   * sentir le coup, pas un feu d'artifice.
   * @param {number} x
   * @param {number} y
   * @param {number} force
   * @param {string} teinte
   */
  function projeter(x, y, force, teinte) {
    var n = 6 + force * 4;
    for (var i = 0; i < n; i++) {
      var a = -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 1.5;
      var v = 100 + Math.random() * (180 + force * 100);
      eclats.push({
        x: x, y: y, a: Math.random() * 6,
        vx: Math.cos(a) * v, vy: Math.sin(a) * v, va: (Math.random() - 0.5) * 10,
        taille: 1.5 + Math.random() * (2.5 + force),
        teinte: Math.random() < 0.3 ? mortier : teinte,
        vie: 0.9 + Math.random() * 0.5
      });
    }
    for (var k = 0; k < 2 + force; k++) {
      poussieres.push({
        x: x + (Math.random() - 0.5) * H, y: y + (Math.random() - 0.5) * H * 0.6,
        r: H * (0.4 + Math.random() * 0.4), vie: 0, duree: 0.6 + Math.random() * 0.35
      });
    }
  }

  /**
   * Un coup sur le mur : des briques s'en détachent — au premier, la
   * brique frappée (ou, sur un trou, la plus proche) ; au deuxième, toutes
   * celles qui l'entourent, sur près d'une brique. Rejoué d'un coup
   * (redimensionnement, mouvement réduit) ou animé.
   * @param {{x:number,y:number,coup:number,graine:number}} impact
   * @param {boolean} aussitot
   */
  function porter(impact, aussitot) {
    if (impact.coup >= COUPS) { return; }
    var x = impact.x * larg, y = impact.y * haut;
    var force = impact.coup - 1;
    var rnd = hasard(impact.graine);
    var maintenant = window.performance.now();
    var rayon = force ? L * 0.8 * (0.8 + rnd() * 0.4) : 0;

    var proches = [];
    briques.forEach(function (b) {
      if (b.tombee) { return; }
      var dx = b.x + L / 2 - x, dy = b.y + H / 2 - y;
      proches.push({ b: b, dx: dx, dy: dy, d: Math.sqrt(dx * dx + dy * dy) });
    });
    proches.sort(function (p, q) { return p.d - q.d; });
    /* La plus proche tombe toujours ; au deuxième coup, trois au moins. */
    var tombent = proches.filter(function (p, rang) { return rang < 1 + force * 2 || p.d <= rayon; });
    var teinte = tombent.length ? tombent[0].b.teinte : teintes[0];

    tombent.forEach(function (p) {
      if (aussitot) {
        p.b.tombee = true;
        mctx.clearRect(p.b.x, p.b.y, L, H);
        return;
      }
      detacher(p.b, false, p.dx / (p.d || 1) * (40 + Math.random() * 90),
        -40 - Math.random() * 100, (Math.random() - 0.5) * 3, Math.random() * 40, maintenant);
    });
    if (!aussitot) { projeter(x, y, force, teinte); }
  }

  /**
   * Le troisième coup : une onde part du point frappé, chaque brique
   * tombe quand elle l'atteint, le cartouche avec elles. Une chute
   * sobre : les briques tombent plus qu'elles ne volent, et tournent à
   * peine.
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
    var frappee = briqueSous(x0, y0);
    toile.style.visibility = "hidden";
    briques.forEach(function (b) {
      if (b.tombee) { return; }
      var dx = b.x + L / 2 - x0, dy = b.y + H / 2 - y0;
      var d = Math.sqrt(dx * dx + dy * dy) || 1;
      /* Près du coup, les briques partent un peu ; plus loin, elles
         s'affaissent. */
      var pres = Math.max(0, 1 - d / (L * 3));
      detacher(b, true, dx / d * (10 + Math.random() * 40 + pres * 120),
        -Math.random() * 30 - pres * 110, (Math.random() - 0.5) * (0.8 + pres * 2.2),
        d / ONDE * (0.9 + Math.random() * 0.2), maintenant);
    });
    var boite = cartouche.getBoundingClientRect();
    var pdx = boite.left + boite.width / 2 - x0, pdy = boite.top + boite.height / 2 - y0;
    chuteCartouche = {
      y: 0, vy: -60, a: 0,
      va: (pdx < 0 ? -1 : 1) * (0.15 + Math.random() * 0.2),
      depart: maintenant + Math.sqrt(pdx * pdx + pdy * pdy) / ONDE * 0.6 + 80
    };
    debutChute = maintenant;
    projeter(x0, y0, 2, frappee ? frappee.teinte : teintes[0]);
    relancer();
  }

  /* ---------- Le cartouche ---------- */

  /**
   * Un coup porté sur le cartouche fait tomber les briques à côté de
   * lui : on y voit le mur.
   * @param {number} x
   * @param {number} y
   * @returns {Array<number>}
   */
  function horsCartouche(x, y) {
    var boite = cartouche.getBoundingClientRect();
    var marge = L * 0.6;
    if (x < boite.left - marge || x > boite.right + marge ||
        y < boite.top - marge || y > boite.bottom + marge) { return [x, y]; }
    var cx = boite.left + boite.width / 2, cy = boite.top + boite.height / 2;
    var places = [];
    /* Des points tout autour du cartouche, gardés dans la partie visible
       de l'écran : le bas du mur passe sous les barres du navigateur. */
    var bas = Math.min(haut, window.innerHeight || haut);
    for (var k = 0; k < 24; k++) {
      var a = (k / 24) * Math.PI * 2;
      var px = cx + Math.cos(a) * (boite.width / 2 + marge + L * 0.3);
      var py = cy + Math.sin(a) * (boite.height / 2 + marge + L * 0.3);
      if (px > H && px < larg - H && py > H && py < bas - H) { places.push([px, py]); }
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
    if (annonce) { annonce.textContent = ANNONCES[coups]; }
    try {
      if (coups === COUPS) {
        abattre(x, y);
        return;
      }
      if (!ctx) { return; }
      var point = horsCartouche(x, y);
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
   * Une image : le calque, effacé, reçoit les briques qui tombent, les
   * éclats et la poussière ; le cartouche tombe. Renvoie vrai tant que
   * quelque chose bouge.
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

    if (chuteCartouche) {
      var p = chuteCartouche;
      if (t >= p.depart) {
        p.vy += PESANTEUR * dt;
        p.y += p.vy * dt;
        p.a += p.va * dt;
      }
      cartouche.style.transform = "translateY(" + p.y.toFixed(1) + "px) rotate(" + p.a.toFixed(3) + "rad)";
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

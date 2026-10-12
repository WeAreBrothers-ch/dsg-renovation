/* ============================================================
   DSG RÉNOVATION — LE MUR À L'ENTRÉE
   Le visiteur qui arrive trouve un mur, dessiné comme le reste du
   site : une élévation de plan, des briques au trait sur la chaux,
   quelques-unes teintées ou hachurées comme l'eau du plan du Léman. Un
   cartouche y est posé : « Cassez le mur pour entrer. »

   Le mur se monte rang par rang, du pied vers le haut, comme le plan se
   trace ailleurs sur le site (motion.js) : moins d'une seconde, et le
   cartouche est là d'emblée. Trois coups, pas un de plus : le premier
   fait tomber la brique frappée, le deuxième celles qui l'entourent —
   le site paraît dans le trou —, le troisième abat le mur : une onde
   part du point frappé, les briques tombent, et le site est derrière.

   Un coup porté sur le cartouche fait tomber les briques juste à côté
   de lui, là où l'on voit le mur. Le cartouche ne bouge pas : il tombe
   avec le mur, au troisième coup.

   Le mur se dresse devant qui arrive de l'extérieur du site, une fois
   par onglet (outils/mur.py décide, avant le premier rendu). Au
   clavier, le bouton « Frapper » donne les coups ; les lecteurs
   d'écran entendent ce qui reste. Mouvement réduit : le mur est là
   d'emblée, les trous paraissent d'un coup, et il s'efface au troisième
   au lieu de tomber. Sans canevas, la feuille reste blanche, les trois
   coups restent, le mur s'efface au dernier.
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
  /* Un rang fait 36 % du pas d'une brique : une brique de terre cuite
     (22 × 6,5 cm, joint compris, à l'échelle près). */
  var RANG = 0.36;
  /* Une brique sur dix est hachurée, à 45°, un trait tous les 5 px. */
  var PART_HACHUREE = 0.1;
  var PAS_HACHURE = 5;
  /* Le mur se monte en 640 ms : 420 du pied au faîte de l'écran, et
     chaque rang se pose de gauche à droite en 220. */
  var MONTEE = 420;
  var BALAYAGE = 220;
  /* Pesanteur des briques et des éclats, en px/s². */
  var PESANTEUR = 3200;
  /* L'onde qui abat le mur : px parcourus par milliseconde. */
  var ONDE = 2.2;
  /* Au-delà, le mur se retire même s'il reste une brique en vue. */
  var CHUTE_MAX = 2600;
  var GRAINE = 20261012;
  var PIXELS_MAX = 6e6;
  /* Le calque, repeint à chaque image, est moins dense : deux millions
     de points au plus. Ce qui bouge n'a pas besoin du trait du mur. */
  var PIXELS_CALQUE = 2e6;

  var style = window.getComputedStyle(mur);
  var papier = style.getPropertyValue("--mur-papier").trim() || "#F4F1EC";
  var trait = style.getPropertyValue("--mur-trait").trim() || "#C3BDB4";
  var hachure = style.getPropertyValue("--mur-hachure").trim() || "rgba(27,27,27,.14)";
  var teintes = style.getPropertyValue("--mur-teintes").trim().split(/\s+/);
  if (!teintes[0]) { teintes = [papier]; }

  /* Les barres du navigateur prennent la couleur du mur tant qu'il
     tient (20-mur.css), puis retrouvent celle du site. */
  var teinteBarres = document.querySelector('meta[name="theme-color"]');
  var teinteSite = teinteBarres ? teinteBarres.getAttribute("content") : null;
  if (teinteBarres) { teinteBarres.setAttribute("content", papier); }

  /**
   * Hasard reproductible (mulberry32) : le même mur à chaque visite, et
   * un coup rejoué après un redimensionnement fait tomber les mêmes
   * briques.
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

  /* Deux toiles : le mur dessiné, qui ne change qu'à un coup (une brique
     en part, un trou reste), et par-dessus, sous le cartouche, le calque
     de ce qui bouge — éclats, briques qui tombent —, seul repeint à
     chaque image. */
  var mctx = toile.getContext ? toile.getContext("2d") : null;
  var calque = document.createElement("canvas");
  calque.className = "mur__briques";
  calque.setAttribute("aria-hidden", "true");
  toile.parentNode.insertBefore(calque, toile.nextSibling);
  var ctx = mctx ? calque.getContext("2d") : null;

  var larg = 0, haut = 0, dpr = 1, dprCalque = 1;
  var L = 80, H = 28.8;
  /**
   * Une brique : sa case (x0, y0) → (x1, y1), en pixels entiers pour un
   * trait net à toute densité, ses deux bords compris — deux briques
   * voisines partagent le trait qui les sépare.
   * @type {Array<{x0:number,y0:number,x1:number,y1:number,teinte:string,hachee:boolean,pose:number,posee:boolean,tombee:boolean}>}
   */
  var briques = [];
  /** Le mur en train de se monter : l'heure du premier rang, ou 0. */
  var montage = 0;
  var coups = 0;
  var abattu = false;
  var ouvert = false;
  /** Les coups portés, en fractions du mur, pour les rejouer. */
  var impacts = [];
  /** Briques qui tombent. */
  var corps = [];
  /** Éclats. */
  var eclats = [];
  var chuteCartouche = null;
  var debutChute = 0;
  var boucle = 0;
  var dernier = 0;
  /* Le calque porte encore l'image précédente. */
  var calqueSali = false;

  /**
   * Une boîte de l'écran dans le repère du mur, qui déborde de l'écran
   * en haut et en bas (20-mur.css) : la toile et les coups s'y comptent.
   * @param {Element} element
   */
  function dansLeMur(element) {
    var m = mur.getBoundingClientRect(), b = element.getBoundingClientRect();
    return { left: b.left - m.left, top: b.top - m.top, right: b.right - m.left,
      bottom: b.bottom - m.top, width: b.width, height: b.height };
  }

  /** La partie du mur visible à l'écran : de `haut` à `bas`. */
  function vue() {
    var m = mur.getBoundingClientRect();
    return { haut: -m.top, bas: -m.top + (window.innerHeight || haut) };
  }

  /** Le pas d'une brique, réglé par la feuille (--mur-pas). */
  function lirePas() {
    var pas = parseFloat(window.getComputedStyle(mur).backgroundSize);
    if (!(pas > 0)) { pas = Math.min(104, Math.max(60, window.innerWidth * 0.065)); }
    return pas;
  }

  /** Le milieu d'une brique. */
  function milieu(b) { return [(b.x0 + b.x1) / 2, (b.y0 + b.y1) / 2]; }

  /* ---------- Le mur dessiné ---------- */

  /**
   * Le contour d'une brique : un trait d'un pixel sur ses quatre bords.
   * Le trait est opaque : là où deux briques le partagent, il ne double
   * pas.
   * @param {CanvasRenderingContext2D} c
   * @param {{x0:number,y0:number,x1:number,y1:number}} b
   */
  function cerner(c, b) {
    var w = b.x1 - b.x0 + 1, h = b.y1 - b.y0 + 1;
    c.fillStyle = trait;
    c.fillRect(b.x0, b.y0, w, 1);
    c.fillRect(b.x0, b.y1, w, 1);
    c.fillRect(b.x0, b.y0, 1, h);
    c.fillRect(b.x1, b.y0, 1, h);
  }

  /**
   * Une brique : sa teinte, ses hachures s'il en a, son contour.
   * @param {CanvasRenderingContext2D} c
   * @param {{x0:number,y0:number,x1:number,y1:number,teinte:string,hachee:boolean}} b
   */
  function peindreBrique(c, b) {
    var w = b.x1 - b.x0, h = b.y1 - b.y0;
    c.fillStyle = b.teinte;
    c.fillRect(b.x0, b.y0, w + 1, h + 1);
    if (b.hachee) {
      c.save();
      c.beginPath();
      c.rect(b.x0 + 1, b.y0 + 1, w - 1, h - 1);
      c.clip();
      c.strokeStyle = hachure;
      c.lineWidth = 1;
      c.beginPath();
      for (var k = -h; k < w; k += PAS_HACHURE) {
        c.moveTo(b.x0 + k, b.y1);
        c.lineTo(b.x0 + k + h, b.y0);
      }
      c.stroke();
      c.restore();
    }
    cerner(c, b);
  }

  /**
   * Le trou d'une brique partie : sa case s'efface, trait compris, et
   * les briques qui le bordent retracent le leur. Entre deux trous, il
   * ne reste aucun trait en l'air.
   * @param {{x0:number,y0:number,x1:number,y1:number}} b
   */
  function trouer(b) {
    mctx.clearRect(b.x0, b.y0, b.x1 - b.x0 + 1, b.y1 - b.y0 + 1);
    briques.forEach(function (v) {
      if (v.tombee || !v.posee) { return; }
      if (v.x1 < b.x0 || v.x0 > b.x1 || v.y1 < b.y0 || v.y0 > b.y1) { return; }
      cerner(mctx, v);
    });
  }

  /**
   * Le mur est monté : la feuille, restée blanche sous lui pendant le
   * montage — on ne voit pas le site avant d'avoir frappé —, s'efface, et
   * les trous laisseront voir le site.
   */
  function monte() {
    montage = 0;
    mur.classList.add("est-peint");
  }

  /** Les briques pas encore posées le sont toutes, d'un coup. */
  function finirMontage() {
    if (!montage) { return; }
    briques.forEach(function (b) {
      if (!b.posee) { b.posee = true; peindreBrique(mctx, b); }
    });
    monte();
  }

  /**
   * Le mur entier, à la taille de l'écran, puis les coups déjà portés.
   * La première fois, il se monte rang par rang (sauf en mouvement
   * réduit) ; après un redimensionnement, il est là d'un coup.
   * @param {boolean} [monterRangParRang]
   */
  function monter(monterRangParRang) {
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
    toile.width = Math.round(larg * dpr);
    toile.height = Math.round(haut * dpr);
    calque.width = Math.round(larg * dprCalque);
    calque.height = Math.round(haut * dprCalque);
    mctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    mctx.clearRect(0, 0, larg, haut);

    /* Le mur se monte du pied de l'écran vers son haut : les rangs sous
       l'écran d'abord, ceux qui le dépassent en dernier. */
    var visible = vue();
    briques = [];
    var rnd = hasard(GRAINE);
    for (var r = 0; r * H < haut; r++) {
      var y0 = Math.round(r * H), y1 = Math.round((r + 1) * H);
      /* Les rangs impairs décalés d'une demi-brique. */
      for (var x = r % 2 ? -L / 2 : 0; x < larg; x += L) {
        var x0 = Math.round(x), x1 = Math.round(x + L);
        var montee = Math.min(1, Math.max(0, (visible.bas - (y0 + y1) / 2) / (visible.bas - visible.haut)));
        briques.push({
          x0: x0, y0: y0, x1: x1, y1: y1,
          teinte: teintes[Math.floor(rnd() * teintes.length)],
          hachee: rnd() < PART_HACHUREE,
          pose: montee * MONTEE + Math.max(0, (x0 + x1) / 2 / larg) * BALAYAGE,
          posee: false,
          tombee: false
        });
      }
    }

    corps = [];
    if (monterRangParRang && !reduit) {
      montage = window.performance.now();
      relancer();
    } else {
      montage = 1;
      finirMontage();
      impacts.forEach(function (impact) { porter(impact, true); });
      peindre(window.performance.now());
    }
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
      if (!b.tombee && x >= b.x0 && x < b.x1 && y >= b.y0 && y < b.y1) { return b; }
    }
    return null;
  }

  /**
   * Une brique redessinée seule, pour tomber. Rien n'est relu sur le mur
   * (une relecture de la toile coûte, au téléphone, plus que de tout
   * redessiner).
   * @param {{x0:number,y0:number,x1:number,y1:number,teinte:string,hachee:boolean}} b
   * @param {number} sx  coin de la part visible, en points de la toile
   * @param {number} sy
   * @param {number} sw
   * @param {number} sh
   * @returns {HTMLCanvasElement}
   */
  function redessiner(b, sx, sy, sw, sh) {
    var piece = document.createElement("canvas");
    piece.width = sw;
    piece.height = sh;
    var c = piece.getContext("2d");
    c.setTransform(dpr, 0, 0, dpr, -sx, -sy);
    peindreBrique(c, b);
    return piece;
  }

  /**
   * Une brique se détache et tombe. Aux deux premiers coups, elle est
   * redessinée à part et laisse un trou ; quand le mur s'abat
   * (`entier`), le mur dessiné, masqué, sert lui-même de source. Seule
   * la part de la brique qui était sur la toile tombe : celles du bord
   * gauche en dépassaient d'une moitié.
   * @param {{x0:number,y0:number,x1:number,y1:number,tombee:boolean}} b
   * @param {boolean} entier
   * @param {number} vx
   * @param {number} vy
   * @param {number} va
   * @param {number} retard  ms avant qu'elle ne parte
   * @param {number} maintenant
   */
  function detacher(b, entier, vx, vy, va, retard, maintenant) {
    b.tombee = true;
    var x0 = Math.max(0, b.x0), y0 = Math.max(0, b.y0);
    var x1 = Math.min(larg, b.x1 + 1), y1 = Math.min(haut, b.y1 + 1);
    if (x1 <= x0 || y1 <= y0) { return; }
    var sx = Math.round(x0 * dpr), sy = Math.round(y0 * dpr);
    var sw = Math.max(1, Math.round(x1 * dpr) - sx), sh = Math.max(1, Math.round(y1 * dpr) - sy);
    var source = toile;
    if (!entier) {
      source = redessiner(b, sx, sy, sw, sh);
      sx = sy = 0;
      trouer(b);
    }
    var m = milieu(b);
    corps.push({
      source: source, sx: sx, sy: sy, sw: sw, sh: sh,
      dx: x0 - m[0], dy: y0 - m[1], dw: x1 - x0, dh: y1 - y0,
      x: m[0], y: m[1], a: 0,
      vx: vx, vy: vy, va: va,
      depart: maintenant + retard
    });
  }

  /**
   * Quelques éclats au point frappé, des bouts de brique dessinés comme
   * elle : de quoi sentir le coup, pas un feu d'artifice.
   * @param {number} x
   * @param {number} y
   * @param {number} force
   * @param {string} teinte
   */
  function projeter(x, y, force, teinte) {
    var n = 4 + force * 3;
    for (var i = 0; i < n; i++) {
      var a = -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 1.4;
      var v = 90 + Math.random() * (160 + force * 90);
      eclats.push({
        x: x, y: y, a: Math.random() * 6,
        vx: Math.cos(a) * v, vy: Math.sin(a) * v, va: (Math.random() - 0.5) * 8,
        taille: 3 + Math.random() * (3 + force * 2),
        teinte: teinte,
        vie: 0.9 + Math.random() * 0.5
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
      var m = milieu(b), dx = m[0] - x, dy = m[1] - y;
      proches.push({ b: b, dx: dx, dy: dy, d: Math.sqrt(dx * dx + dy * dy) });
    });
    proches.sort(function (p, q) { return p.d - q.d; });
    /* La plus proche tombe toujours ; au deuxième coup, trois au moins. */
    var tombent = proches.filter(function (p, rang) { return rang < 1 + force * 2 || p.d <= rayon; });
    var teinte = tombent.length ? tombent[0].b.teinte : papier;

    tombent.forEach(function (p) {
      if (aussitot) {
        p.b.tombee = true;
        trouer(p.b);
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
      var m = milieu(b), dx = m[0] - x0, dy = m[1] - y0;
      var d = Math.sqrt(dx * dx + dy * dy) || 1;
      /* Près du coup, les briques partent un peu ; plus loin, elles
         s'affaissent. */
      var pres = Math.max(0, 1 - d / (L * 3));
      detacher(b, true, dx / d * (10 + Math.random() * 40 + pres * 120),
        -Math.random() * 30 - pres * 110, (Math.random() - 0.5) * (0.8 + pres * 2.2),
        d / ONDE * (0.9 + Math.random() * 0.2), maintenant);
    });
    var boite = dansLeMur(cartouche);
    var pdx = boite.left + boite.width / 2 - x0, pdy = boite.top + boite.height / 2 - y0;
    chuteCartouche = {
      y: 0, vy: -60, a: 0,
      va: (pdx < 0 ? -1 : 1) * (0.15 + Math.random() * 0.2),
      depart: maintenant + Math.sqrt(pdx * pdx + pdy * pdy) / ONDE * 0.6 + 80
    };
    debutChute = maintenant;
    projeter(x0, y0, 2, frappee ? frappee.teinte : papier);
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
    var boite = dansLeMur(cartouche);
    var marge = L * 0.6;
    if (x < boite.left - marge || x > boite.right + marge ||
        y < boite.top - marge || y > boite.bottom + marge) { return [x, y]; }
    var cx = boite.left + boite.width / 2, cy = boite.top + boite.height / 2;
    var places = [];
    /* Des points tout autour du cartouche, gardés dans la partie visible
       du mur : il déborde de l'écran, et passe sous les barres du
       navigateur. */
    var visible = vue();
    for (var k = 0; k < 24; k++) {
      var a = (k / 24) * Math.PI * 2;
      var px = cx + Math.cos(a) * (boite.width / 2 + marge + L * 0.3);
      var py = cy + Math.sin(a) * (boite.height / 2 + marge + L * 0.3);
      if (px > H && px < larg - H && py > visible.haut + H && py < visible.bas - H) { places.push([px, py]); }
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
      finirMontage();
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
   * Une image : le mur se monte, rang par rang ; le calque, effacé,
   * reçoit les briques qui tombent et les éclats ; le cartouche tombe.
   * Renvoie vrai tant que quelque chose bouge.
   * @param {number} t
   * @param {number} [dt]
   * @returns {boolean}
   */
  function peindre(t, dt) {
    if (!ctx) { return false; }
    dt = dt || 0;
    var actif = false;

    if (montage) {
      var ecoule = t - montage, reste = false;
      briques.forEach(function (b) {
        if (b.posee) { return; }
        if (b.pose <= ecoule) { b.posee = true; peindreBrique(mctx, b); } else { reste = true; }
      });
      if (reste) { actif = true; } else { monte(); }
    }

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
      ctx.strokeStyle = trait;
      ctx.lineWidth = 1;
      ctx.strokeRect(-e.taille / 2, -e.taille * 0.35, e.taille, e.taille * 0.7);
      ctx.restore();
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
    calqueSali = corps.length > 0 || eclats.length > 0;
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
    if (teinteBarres && teinteSite) { teinteBarres.setAttribute("content", teinteSite); }
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
      var boite = dansLeMur(bouton);
      frapper(boite.left + boite.width * Math.random(), boite.top + boite.height / 2);
    });
  }
  mur.addEventListener("contextmenu", function (evenement) { evenement.preventDefault(); });

  var attente = 0;
  function surRedimension() {
    window.clearTimeout(attente);
    attente = window.setTimeout(function () { if (!abattu) { monter(false); } }, 120);
  }
  window.addEventListener("resize", surRedimension);

  monter(true);
  mur.focus({ preventScroll: true });
  /* Le mur est monté : le script de tête ne le retirera pas de lui-même
     (outils/mur.py). */
  racine.classList.add("mur-pret");
}());

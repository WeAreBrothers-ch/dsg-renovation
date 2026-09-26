/* ============================================================
   DSG RÉNOVATION — L'ÉQUIPE AU TRAVAIL
   La frise de l'accueil : quatre ouvriers dessinés au trait arrivent à
   leur poste en marchant, travaillent, puis repartent. Un charpentier
   cloue, un poseur pose trois carreaux, un électricien visse une
   ampoule qui s'allume, un peintre passe un mur au rouleau.

   Décor seulement (aria-hidden) : un bouton met l'animation en pause.
   Elle ne tourne pas hors de l'écran, ni onglet caché, ni si le
   visiteur demande moins de mouvement ; sans ce fichier, la frise
   reste une illustration immobile (outils/equipe.py).

   Repères d'un ouvrier : pieds en (0, 0), hanche à -36, épaules 24
   plus haut sur le torse. Angles en degrés, sens du SVG : un membre
   qui pend pivote vers l'arrière quand l'angle croît.
   ============================================================ */
(function () {
  "use strict";

  var frise = document.querySelector("[data-equipe]");
  if (!frise || !window.requestAnimationFrame) { return; }
  var bouton = document.querySelector("[data-equipe-pause]");
  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)");

  var RAD = Math.PI / 180;
  var PAS = 18;                       /* longueur d'une enjambée */
  var CADENCE = 760;                  /* un double pas, en ms */
  var VITESSE = 2 * PAS / CADENCE;    /* unités par ms : le pied d'appui ne glisse pas */
  var FONDU = 0.3;                    /* part de la marche passée à apparaître */
  var TRANSITION = 300;               /* de la marche au geste, et retour */
  var REPOS = 1400;                   /* poste vide avant le retour */

  function borne(t) { return t < 0 ? 0 : (t > 1 ? 1 : t); }
  function lisse(t) { t = borne(t); return t * t * (3 - 2 * t); }
  function mix(a, b, t) { return a + (b - a) * t; }
  function n(v) { return Math.round(v * 100) / 100; }

  /* Deux segments articulés : angle absolu du premier, relatif du
     second, pour que le bout atteigne la cible. `sens` : 1 plie vers
     l'avant (genou), -1 vers l'arrière (coude). */
  function articuler(ox, oy, cx, cy, l1, l2, sens) {
    var dx = cx - ox, dy = cy - oy;
    var d = Math.sqrt(dx * dx + dy * dy);
    d = Math.max(Math.abs(l1 - l2) + 0.01, Math.min(d, l1 + l2 - 0.01));
    var ligne = Math.atan2(-dx, dy);
    var a1 = Math.acos((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d));
    var a2 = Math.acos((l1 * l1 + l2 * l2 - d * d) / (2 * l1 * l2));
    return [(ligne - sens * a1) / RAD, sens * (Math.PI - a2) / RAD];
  }

  function epaule(p) {
    var t = p.torse * RAD;
    return [p.x + 24 * Math.sin(t), -36 + p.y - 24 * Math.cos(t)];
  }

  /* Oriente un bras pour que la main atteigne un point du poste. */
  function viser(p, cote, cible) {
    var e = epaule(p);
    var a = articuler(e[0], e[1], cible[0], cible[1], 14, 13, -1);
    p.bras[cote] = [a[0] - p.torse, a[1]];
  }

  /* Position de la main d'après les angles du bras. */
  function main(p, cote) {
    var e = epaule(p);
    var a1 = (p.torse + p.bras[cote][0]) * RAD, a2 = a1 + p.bras[cote][1] * RAD;
    var cx = e[0] - 14 * Math.sin(a1), cy = e[1] + 14 * Math.cos(a1);
    return [cx - 13 * Math.sin(a2), cy + 13 * Math.cos(a2)];
  }

  function poseDebout() {
    return { x: 0, y: 0, torse: 3, opacite: 1,
             pieds: [[4, 0], [-4, 0]], chevilles: [0, 0],
             bras: [[8, -12], [-8, -12]],
             outil: {} };
  }

  /* La marche : pied d'appui fixe au sol, pied libre en arc, bassin
     qui monte au passage de la jambe, bras en balancier. */
  function marcher(p, phase) {
    function pied(q) {
      q -= Math.floor(q);
      if (q < 0.5) { return [PAS / 2 - q * 2 * PAS, 0]; }
      var u = (q - 0.5) * 2;
      return [-PAS / 2 + u * PAS, -5 * Math.sin(Math.PI * u)];
    }
    p.pieds = [pied(phase), pied(phase + 0.5)];
    p.y = 0.6 * (1 - Math.cos(4 * Math.PI * (phase - 0.25)));
    p.torse = 4;
    var balancier = 22 * Math.cos(2 * Math.PI * phase);
    p.bras = [[balancier, -16], [-balancier, -16]];
  }

  /* Angles des deux jambes : donnés par la pose (genou au sol), ou
     calculés pour que les pieds touchent leur place. */
  function jambes(p) {
    var r = [];
    for (var i = 0; i < 2; i++) {
      r[i] = p.jambes && p.jambes[i] ? p.jambes[i]
        : articuler(0, -36, p.pieds[i][0], p.pieds[i][1] - p.y, 18, 18, 1);
    }
    return r;
  }

  function melanger(a, b, t) {
    var p = poseDebout(), cle, ja = jambes(a), jb = jambes(b);
    p.jambes = [[mix(ja[0][0], jb[0][0], t), mix(ja[0][1], jb[0][1], t)],
                [mix(ja[1][0], jb[1][0], t), mix(ja[1][1], jb[1][1], t)]];
    p.x = mix(a.x, b.x, t); p.y = mix(a.y, b.y, t);
    p.torse = mix(a.torse, b.torse, t); p.opacite = mix(a.opacite, b.opacite, t);
    for (var i = 0; i < 2; i++) {
      p.chevilles[i] = mix(a.chevilles[i], b.chevilles[i], t);
      p.pieds[i] = [mix(a.pieds[i][0], b.pieds[i][0], t), mix(a.pieds[i][1], b.pieds[i][1], t)];
      p.bras[i] = [mix(a.bras[i][0], b.bras[i][0], t), mix(a.bras[i][1], b.bras[i][1], t)];
    }
    var cles = Object.keys(a.outil).concat(Object.keys(b.outil));
    for (var j = 0; j < cles.length; j++) {
      cle = cles[j];
      var va = a.outil[cle], vb = b.outil[cle];
      if (typeof va === "number" && typeof vb === "number") {
        p.outil[cle] = mix(va, vb, t);
      } else if (Array.isArray(va) && Array.isArray(vb)) {
        p.outil[cle] = [mix(va[0], vb[0], t), mix(va[1], vb[1], t)];
      } else {
        p.outil[cle] = vb === undefined || (t < 0.5 && va !== undefined) ? va : vb;
      }
    }
    return p;
  }

  /* ---------- Les quatre gestes ----------
     Chaque geste reçoit le temps écoulé à son poste et la pose à
     remplir ; il y range aussi l'état des accessoires (p.outil). */

  function distance(a, b) { return Math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1])); }

  /* Un point qui tourne autour de l'épaule, de a vers b, par le haut. */
  function arc(centre, a, b, k) {
    var aa = Math.atan2(a[1] - centre[1], a[0] - centre[0]);
    var ab = Math.atan2(b[1] - centre[1], b[0] - centre[0]);
    while (ab < aa) { ab += 2 * Math.PI; }
    var angle = mix(aa, ab, k), rayon = mix(distance(centre, a), distance(centre, b), k);
    return [centre[0] + rayon * Math.cos(angle), centre[1] + rayon * Math.sin(angle)];
  }

  var METIERS = {

    /* Le charpentier : le marteau décrit un arc au-dessus de la tête,
       retombe sur le clou, qui s'enfonce un peu à chaque coup. Le
       marteau prolonge l'avant-bras : la tête est à 25 du coude. */
    marteau: {
      duree: 5400, fin: 0,
      travail: function (t, p) {
        p.torse = 10; p.y = 0.5;
        p.pieds = [[9, 0], [-8, 0]];
        viser(p, 1, [16, -31]);
        var periode = 700, u = (t % periode) / periode;
        var coups = Math.floor(t / periode) + (u >= 0.72 ? 1 : 0);
        var enfonce = Math.min(6, coups * 1.1);
        var e = epaule(p), leve = [-16, -86], clou = [27, -40 + enfonce], k, cible;
        if (u < 0.56) { k = 1 - lisse(u / 0.56); }
        else if (u < 0.72) { k = (u - 0.56) / 0.16; k *= k; }
        else { k = 1; }
        cible = arc(e, leve, clou, k);
        var a = articuler(e[0], e[1], cible[0], cible[1], 14, 25, -1);
        p.bras[0] = [a[0] - p.torse, a[1]];
        p.outil.clou = enfonce;
        p.outil.impact = u >= 0.72 && u < 0.9 ? 1 - (u - 0.72) / 0.18 : 0;
      },
      decor: function (o, etat, fondu) {
        o.acc.clou.setAttribute("transform", "translate(0 " + n(etat.clou) + ")");
        o.acc.clou.setAttribute("opacity", n(fondu));
        o.acc.impact.setAttribute("opacity", n(etat.impact || 0));
      },
      depart: { clou: 0, impact: 0 },
      arrivee: function (e) { return { clou: e.clou, impact: 0 }; }
    },

    /* Le poseur : à genoux, assis sur ses talons, il pose trois
       carreaux et avance d'une longueur entre chacun. */
    sol: {
      duree: 5700, fin: 32,
      travail: function (t, p) {
        var periode = 1900, i = Math.min(2, Math.floor(t / periode));
        var u = (t - i * periode) / periode;
        p.x = i === 0 ? 0 : 16 * (i - 1) + 16 * lisse(u / 0.2);
        p.y = 18.4; p.torse = 58;
        p.jambes = [[8, 82], [14, 76]];
        p.chevilles = [90, 90];
        var poitrine = [p.x + 14, -24], sol = [p.x + 24, -4], k;
        if (u < 0.2) { k = 0; }
        else if (u < 0.5) { k = lisse((u - 0.2) / 0.3); }
        else if (u < 0.62) { k = 1; }
        else { k = 1 - lisse((u - 0.62) / 0.3); }
        viser(p, 0, [mix(poitrine[0], sol[0], k), mix(poitrine[1], sol[1], k) + (u > 0.5 && u < 0.62 ? 0.8 : 0)]);
        viser(p, 1, [p.x + 16, -6]);
        p.outil.poses = i + (u >= 0.5 ? 1 : 0);
        p.outil.enMain = u < 0.5 || u > 0.9 && i < 2 ? 1 : 0;
      },
      decor: function (o, etat, fondu, pose) {
        for (var i = 0; i < 3; i++) {
          o.acc["carreau-" + i].setAttribute("opacity", i < (etat.poses || 0) ? n(fondu) : 0);
        }
        /* Le carreau reste à plat dans la main, quel que soit le bras. */
        var penche = pose.torse + pose.bras[0][0] + pose.bras[0][1];
        o.acc["carreau-main"].setAttribute("transform", "rotate(" + n(-penche) + " 0 -33)");
        o.acc["carreau-main"].setAttribute("opacity", etat.enMain ? 1 : 0);
      },
      depart: { poses: 0, enMain: 0 },
      arrivee: function (e) { return { poses: e.poses, enMain: 0 }; }
    },

    /* L'électricien : il visse l'ampoule, qui grésille puis s'allume. */
    ampoule: {
      duree: 5600, fin: 0,
      travail: function (t, p) {
        p.torse = 4; p.y = 0.3;
        p.pieds = [[6, 0], [-6, 0]];
        var allumage = 3100, vis = t < allumage ? Math.sin(t / 130) : 0;
        viser(p, 0, [19 + 1.2 * vis, -77.8]);
        p.bras[1] = [12, -20];
        p.outil.tourne = 8 * vis;
        var d = t - allumage;
        p.outil.lumiere = d < 0 ? 0 : (d < 90 ? 1 : (d < 180 ? 0.15 : (d < 300 ? 1 : (d < 380 ? 0.4 : 1))));
      },
      decor: function (o, etat, fondu) {
        o.acc.ampoule.setAttribute("transform", "rotate(" + n(etat.tourne || 0) + " 20 -90)");
        o.acc.halo.setAttribute("opacity", n((etat.lumiere || 0) * fondu));
        o.acc.verre.classList.toggle("est-allume", (etat.lumiere || 0) * fondu > 0.5);
      },
      depart: { tourne: 0, lumiere: 0 },
      arrivee: function (e) { return { tourne: 0, lumiere: e.lumiere }; }
    },

    /* Le peintre : il longe le mur, le rouleau monte et descend, la
       couleur suit le rouleau. */
    peinture: {
      duree: 6800, fin: 64,
      travail: function (t, p) {
        p.x = mix(0, 64, t / 6800);
        marcher(p, p.x / (2 * PAS));
        p.y = Math.min(p.y, 0.8); p.torse = 5;
        var rx = p.x + 20, ry = -60 + 14 * Math.sin(t / 1000 * 2 * Math.PI);
        viser(p, 0, [p.x + 14, ry + 12]);
        p.bras[1] = [10 + 6 * Math.sin(t / 700), -18];
        p.outil.rouleau = [rx, ry];
        p.outil.peinture = Math.max(0, Math.min(68, rx - 16));
      },
      porte: function (p) {
        /* En marchant, il tient le rouleau levé devant lui. */
        p.bras[0] = [-40, -60];
        var m = main(p, 0);
        p.outil.rouleau = [m[0] + 6, m[1] - 10];
      },
      decor: function (o, etat, fondu, pose) {
        var m = main(pose, 0), r = pose.outil.rouleau || [m[0] + 6, m[1] - 10];
        o.acc.perche.setAttribute("x1", n(m[0])); o.acc.perche.setAttribute("y1", n(m[1]));
        o.acc.perche.setAttribute("x2", n(r[0])); o.acc.perche.setAttribute("y2", n(r[1] + 6));
        o.acc.perche.setAttribute("opacity", n(pose.opacite));
        o.acc.rouleau.setAttribute("x", n(r[0] - 2)); o.acc.rouleau.setAttribute("y", n(r[1] - 6));
        o.acc.rouleau.setAttribute("opacity", n(pose.opacite));
        o.acc.peinture.setAttribute("width", n(etat.peinture || 0));
        o.acc.peinture.setAttribute("opacity", n(fondu));
      },
      depart: { peinture: 0 },
      arrivee: function (e) { return { peinture: e.peinture }; }
    }
  };

  /* Largeur occupée par chaque poste à droite de sa place (unités) :
     de quoi faire marcher chacun sans traverser son voisin. */
  var EMPRISE = { marteau: 56, sol: 66, ampoule: 28, peinture: 86 };
  var AVANCEMENT = { marteau: 0.318, sol: 0.5, ampoule: 0.7, peinture: 0.45 };

  function Ouvrier(svg) {
    this.svg = svg;
    this.metier = svg.getAttribute("data-metier");
    this.m = METIERS[this.metier];
    this.os = {};
    this.acc = {};
    var self = this;
    Array.prototype.forEach.call(svg.querySelectorAll("[data-os]"), function (el) {
      self.os[el.getAttribute("data-os")] = el;
    });
    Array.prototype.forEach.call(svg.querySelectorAll("[data-accessoire]"), function (el) {
      self.acc[el.getAttribute("data-accessoire")] = el;
    });
    this.entree = this.sortie = 100;
    this.temps = 0;
  }

  Ouvrier.prototype.regler = function (arrivee, depart) {
    this.entree = arrivee;
    this.sortie = depart;
    this.dEntree = arrivee / VITESSE;
    this.dSortie = depart / VITESSE;
    this.cycle = this.dEntree + this.m.duree + this.dSortie + REPOS;
    this.fini = this.m.arrivee(this.geste(this.m.duree).outil);
    /* Au premier affichage, chacun est déjà au milieu de sa tâche :
       c'est aussi la pose du dessin immobile. */
    if (!this.pret) { this.temps = this.dEntree + this.m.duree * AVANCEMENT[this.metier]; }
    this.temps %= this.cycle;
    this.pret = true;
  };

  Ouvrier.prototype.marche = function (t, x0, apparition) {
    var p = poseDebout();
    marcher(p, t / CADENCE);
    p.x = x0 + VITESSE * t;
    if (this.m.porte) { this.m.porte(p); }
    p.opacite = apparition;
    return p;
  };

  Ouvrier.prototype.geste = function (t) {
    var p = poseDebout();
    this.m.travail(t, p);
    return p;
  };

  Ouvrier.prototype.pose = function (t) {
    var m = this.m, e = this.dEntree, w = m.duree, s = this.dSortie, p, a, b;
    if (t < e) {
      p = this.marche(t, -this.entree, lisse(t / (e * FONDU)));
      return { pose: p, etat: m.depart, fondu: 1 };
    }
    t -= e;
    if (t < w) {
      p = this.geste(t);
      if (t < TRANSITION) {
        a = this.marche(e, -this.entree, 1);
        p = melanger(a, p, lisse(t / TRANSITION));
      } else if (t > w - TRANSITION) {
        b = this.marche(0, m.fin, 1);
        p = melanger(p, b, lisse((t - w + TRANSITION) / TRANSITION));
      }
      return { pose: p, etat: p.outil, fondu: 1 };
    }
    t -= w;
    var fini = this.fini;
    if (t < s) {
      p = this.marche(t, m.fin, 1 - lisse((t - s * (1 - FONDU)) / (s * FONDU)));
      return { pose: p, etat: fini, fondu: 1 };
    }
    /* Poste vide : l'ouvrage s'efface, le poste se remet à zéro. */
    t -= s;
    p = this.marche(0, m.fin + this.sortie, 0);
    return t < REPOS / 2 ? { pose: p, etat: fini, fondu: 1 - lisse(t / (REPOS / 2)) }
                         : { pose: p, etat: m.depart, fondu: lisse((t - REPOS / 2) / (REPOS / 2)) };
  };

  Ouvrier.prototype.dessiner = function (instant) {
    var os = this.os, p = instant.pose;
    function rot(el, angle, y) { el.setAttribute("transform", "rotate(" + n(angle) + " 0 " + y + ")"); }
    os.marcheur.setAttribute("transform", "translate(" + n(p.x) + " 0)");
    os.marcheur.setAttribute("opacity", n(p.opacite));
    os.bassin.setAttribute("transform", "translate(0 " + n(p.y) + ")");
    var j = jambes(p), av = j[0], arr = j[1];
    rot(os["cuisse-av"], av[0], -36); rot(os["tibia-av"], av[1], -18);
    rot(os["cuisse-arr"], arr[0], -36); rot(os["tibia-arr"], arr[1], -18);
    rot(os["pied-av"], p.chevilles[0], 0); rot(os["pied-arr"], p.chevilles[1], 0);
    rot(os.torse, p.torse, -36);
    rot(os["bras-av"], p.bras[0][0], -60); rot(os["avant-bras-av"], p.bras[0][1], -46);
    rot(os["bras-arr"], p.bras[1][0], -60); rot(os["avant-bras-arr"], p.bras[1][1], -46);
    this.m.decor(this, instant.etat, instant.fondu, p);
  };

  Ouvrier.prototype.avancer = function (dt) {
    this.temps = (this.temps + dt) % this.cycle;
    this.dessiner(this.pose(this.temps));
  };

  var ouvriers = Array.prototype.map.call(frise.querySelectorAll("[data-metier]"), function (svg) {
    return new Ouvrier(svg);
  });

  /* Les distances de marche suivent la largeur de la frise. */
  function mesurer() {
    var largeur = frise.clientWidth;
    var echelle = parseFloat(getComputedStyle(frise).getPropertyValue("--e")) || 1;
    var places = ouvriers.map(function (o) {
      return parseFloat(o.svg.parentNode.style.getPropertyValue("--place")) / 100 * largeur;
    });
    ouvriers.forEach(function (o, i) {
      var gauche = i === 0 ? places[0] / echelle + 30
        : (places[i] - places[i - 1]) / echelle - EMPRISE[ouvriers[i - 1].metier] - 14;
      var droite = i === ouvriers.length - 1
        ? (largeur - places[i]) / echelle - o.m.fin + 30
        : (places[i + 1] - places[i]) / echelle - o.m.fin - 26;
      o.regler(Math.max(24, Math.min(150, gauche)), Math.max(24, Math.min(150, droite)));
    });
  }

  /* ---------- Horloge : pause, hors écran, onglet caché ---------- */
  var enPause = false, visible = true, requete = 0, precedent = 0;

  function actif() { return !enPause && visible && !document.hidden && !mouvementReduit.matches; }

  function image(maintenant) {
    requete = 0;
    var dt = precedent ? Math.min(64, maintenant - precedent) : 16;
    precedent = maintenant;
    ouvriers.forEach(function (o) { o.avancer(dt); });
    if (actif()) { requete = window.requestAnimationFrame(image); }
  }

  function relancer() {
    if (actif() && !requete) { precedent = 0; requete = window.requestAnimationFrame(image); }
  }

  function arreter() {
    if (requete) { window.cancelAnimationFrame(requete); requete = 0; }
  }

  function basculer() { if (actif()) { relancer(); } else { arreter(); } }

  mesurer();

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entrees) {
      visible = entrees[entrees.length - 1].isIntersecting;
      basculer();
    }).observe(frise);
  }
  document.addEventListener("visibilitychange", basculer);

  var attente = 0;
  window.addEventListener("resize", function () {
    window.clearTimeout(attente);
    attente = window.setTimeout(mesurer, 150);
  });

  if (bouton) {
    bouton.addEventListener("click", function () {
      enPause = !enPause;
      bouton.setAttribute("aria-pressed", enPause ? "true" : "false");
      basculer();
    });
  }

  function preference() {
    if (bouton) { bouton.hidden = mouvementReduit.matches; }
    if (mouvementReduit.matches) {
      arreter();
      /* Une seule image : chacun au milieu de sa tâche. */
      ouvriers.forEach(function (o) {
        o.temps = o.dEntree + o.m.duree * AVANCEMENT[o.metier];
        o.dessiner(o.pose(o.temps));
      });
    } else {
      basculer();
    }
  }
  if (mouvementReduit.addEventListener) { mouvementReduit.addEventListener("change", preference); }
  preference();
})();

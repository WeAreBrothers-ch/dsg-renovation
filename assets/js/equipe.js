/* ============================================================
   DSG RÉNOVATION — LES OUVRIERS DE L'ACCUEIL
   Quatre silhouettes, chacune dans le bas d'une section : un
   charpentier cloue, un poseur pose trois carreaux, un électricien
   visse une ampoule qui s'allume, un peintre passe un mur au rouleau.

   Le défilement les fait vivre : à mesure que la section monte dans
   l'écran, l'ouvrier arrive en marchant, travaille, puis repart. Ses
   pieds avancent exactement de la distance parcourue ; qui s'arrête de
   défiler l'arrête, qui remonte le fait revenir sur ses pas. Un léger
   amorti adoucit le mouvement.

   Décor seulement (aria-hidden). Rien ne bouge si le visiteur demande
   moins de mouvement ; sans ce fichier, chacun reste saisi au milieu de
   sa tâche (outils/equipe.py).

   Repères d'un ouvrier : pieds en (0, 0), hanche à -36, épaules 24
   plus haut sur le torse. Angles en degrés, sens du SVG : un membre
   qui pend pivote vers l'arrière quand l'angle croît.
   ============================================================ */
(function () {
  "use strict";

  var scenes = document.querySelectorAll("[data-ouvrier]");
  if (!scenes.length || !window.requestAnimationFrame) { return; }
  var mouvementReduit = window.matchMedia("(prefers-reduced-motion: reduce)");

  var RAD = Math.PI / 180;
  var PAS = 18;                       /* longueur d'une enjambée */
  var AMORTI = 110;                   /* ms : délai de l'amorti */

  /* Le parcours d'un ouvrier, en part du défilement de sa section :
     il entre, travaille, sort. */
  var ENTREE = 0.04, TRAVAIL = 0.34, SORTIE = 0.7, FIN = 0.96, FONDU = 0.03;

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
             pieds: [[4, 0], [-4, 0]],
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
    var balancier = 24 * Math.cos(2 * Math.PI * phase);
    p.bras = [[balancier, -18], [-balancier, -18]];
  }

  /* Angles des deux jambes : donnés par la pose (genoux au sol), ou
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

  function distance(a, b) { return Math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1])); }

  /* Un point qui tourne autour de l'épaule, de a vers b, par le haut. */
  function arc(centre, a, b, k) {
    var aa = Math.atan2(a[1] - centre[1], a[0] - centre[0]);
    var ab = Math.atan2(b[1] - centre[1], b[0] - centre[0]);
    while (ab < aa) { ab += 2 * Math.PI; }
    var angle = mix(aa, ab, k), rayon = mix(distance(centre, a), distance(centre, b), k);
    return [centre[0] + rayon * Math.cos(angle), centre[1] + rayon * Math.sin(angle)];
  }

  /* ---------- Les quatre gestes ----------
     Chaque geste reçoit son avancement (en ms de geste) et la pose à
     remplir ; il y range aussi l'état des accessoires (p.outil). */
  var METIERS = {

    /* Le charpentier : le marteau décrit un arc au-dessus de la tête,
       retombe sur le clou, qui s'enfonce un peu à chaque coup. Le
       marteau prolonge l'avant-bras : sa tête est à 26,5 du coude. */
    marteau: {
      duree: 4200, fin: 0, demiTour: true,
      travail: function (t, p) {
        p.torse = 10; p.y = 0.5;
        p.pieds = [[9, 0], [-8, 0]];
        viser(p, 1, [16, -32]);
        var periode = 700, u = (t % periode) / periode;
        var coups = Math.floor(t / periode) + (u >= 0.72 ? 1 : 0);
        var enfonce = Math.min(6, coups * 1.2);
        var e = epaule(p), leve = [-26, -80], clou = [27, -42 + enfonce], k, cible;
        if (u < 0.56) { k = 1 - lisse(u / 0.56); }
        else if (u < 0.72) { k = (u - 0.56) / 0.16; k *= k; }
        else { k = 1; }
        cible = arc(e, leve, clou, k);
        var a = articuler(e[0], e[1], cible[0], cible[1], 14, 26.5, -1);
        p.bras[0] = [a[0] - p.torse, a[1]];
        p.outil.clou = enfonce;
        p.outil.impact = u >= 0.72 && u < 0.9 ? 1 - (u - 0.72) / 0.18 : 0;
      },
      decor: function (o, etat) {
        o.acc.clou.setAttribute("transform", "translate(0 " + n(etat.clou || 0) + ")");
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
        var poitrine = [p.x + 14, -26], sol = [p.x + 24, -7.5], k;
        if (u < 0.2) { k = 0; }
        else if (u < 0.5) { k = lisse((u - 0.2) / 0.3); }
        else if (u < 0.62) { k = 1; }
        else { k = 1 - lisse((u - 0.62) / 0.3); }
        viser(p, 0, [mix(poitrine[0], sol[0], k), mix(poitrine[1], sol[1], k)]);
        viser(p, 1, [p.x + 16, -8]);
        p.outil.poses = i + (u >= 0.5 ? 1 : 0);
        p.outil.enMain = u < 0.5 || u > 0.9 && i < 2 ? 1 : 0;
      },
      decor: function (o, etat, pose) {
        for (var i = 0; i < 3; i++) {
          o.acc["carreau-" + i].setAttribute("opacity", i < (etat.poses || 0) ? 1 : 0);
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
      duree: 5000, fin: 0,
      travail: function (t, p) {
        p.torse = 4; p.y = 0.3;
        p.pieds = [[6, 0], [-6, 0]];
        var allumage = 2800, vis = t < allumage ? Math.sin(t / 130) : 0;
        viser(p, 0, [19 + 1.2 * vis, -74]);
        p.bras[1] = [12, -20];
        p.outil.tourne = 8 * vis;
        var d = t - allumage;
        p.outil.lumiere = d < 0 ? 0 : (d < 90 ? 1 : (d < 180 ? 0.15 : (d < 300 ? 1 : (d < 380 ? 0.4 : 1))));
      },
      decor: function (o, etat) {
        o.acc.ampoule.setAttribute("transform", "rotate(" + n(etat.tourne || 0) + " 20 -91)");
        o.acc.halo.setAttribute("opacity", n(etat.lumiere || 0));
        o.acc.verre.classList.toggle("est-allume", (etat.lumiere || 0) > 0.5);
      },
      depart: { tourne: 0, lumiere: 0 },
      arrivee: function (e) { return { tourne: 0, lumiere: e.lumiere }; }
    },

    /* Le peintre : il longe le mur, le rouleau monte et descend, la
       couleur suit le rouleau. */
    peinture: {
      duree: 6000, fin: 64,
      travail: function (t, p) {
        p.x = mix(0, 64, t / 6000);
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
        p.outil.rouleau = [m[0] + 6, m[1] - 12];
      },
      decor: function (o, etat, pose) {
        var m = main(pose, 0), r = pose.outil.rouleau || [m[0] + 6, m[1] - 12];
        o.acc.perche.setAttribute("x1", n(m[0])); o.acc.perche.setAttribute("y1", n(m[1]));
        o.acc.perche.setAttribute("x2", n(r[0])); o.acc.perche.setAttribute("y2", n(r[1] + 8));
        o.acc.perche.setAttribute("opacity", n(pose.opacite));
        o.acc.rouleau.setAttribute("x", n(r[0] - 3)); o.acc.rouleau.setAttribute("y", n(r[1] - 8));
        o.acc.rouleau.setAttribute("opacity", n(pose.opacite));
        o.acc.peinture.setAttribute("width", n(etat.peinture || 0));
      },
      depart: { peinture: 0 },
      arrivee: function (e) { return { peinture: e.peinture }; }
    }
  };

  /* Avancement du geste montré par le dessin immobile (outils/equipe.py). */
  var AVANCEMENT = { marteau: 0.458, sol: 0.5, ampoule: 0.7, peinture: 0.45 };

  function Ouvrier(scene) {
    this.scene = scene;
    this.svg = scene.querySelector("svg[data-metier]");
    this.poste = this.svg.parentNode;
    this.metier = this.svg.getAttribute("data-metier");
    this.m = METIERS[this.metier];
    this.os = {};
    this.acc = {};
    var self = this;
    Array.prototype.forEach.call(this.svg.querySelectorAll("[data-os]"), function (el) {
      self.os[el.getAttribute("data-os")] = el;
    });
    Array.prototype.forEach.call(this.svg.querySelectorAll("[data-accessoire]"), function (el) {
      self.acc[el.getAttribute("data-accessoire")] = el;
    });
    this.fini = this.m.arrivee(this.geste(this.m.duree).outil);
    this.cible = this.montre = -1;
    this.entree = this.sortie = 120;
  }

  /* Distances de marche : de hors champ jusqu'au poste, puis au-delà.
     Le sens de la marche (vers la droite ou la gauche) est donné par
     le dessin retourné (CSS) : le calcul, lui, va toujours vers la
     droite. */
  Ouvrier.prototype.mesurer = function () {
    var largeur = this.scene.clientWidth;
    var echelle = parseFloat(getComputedStyle(this.scene).getPropertyValue("--e")) || 1;
    var place = parseFloat(this.poste.style.getPropertyValue("--place")) / 100;
    var gauche = this.scene.classList.contains("ouvrier--gauche");
    var avant = (gauche ? 1 - place : place) * largeur / echelle;
    var apres = (gauche ? place : 1 - place) * largeur / echelle;
    this.entree = Math.max(60, Math.min(260, avant + 30));
    this.sortie = Math.max(60, Math.min(260, apres - this.m.fin + 30));
  };

  Ouvrier.prototype.geste = function (t) {
    var p = poseDebout();
    this.m.travail(t, p);
    return p;
  };

  /* La marche à la position x (depuis le poste) : l'enjambée suit la
     distance parcourue, le pied d'appui ne glisse pas. */
  Ouvrier.prototype.marche = function (x, depart) {
    var p = poseDebout();
    marcher(p, (x - depart) / (2 * PAS));
    p.x = x;
    if (this.m.porte) { this.m.porte(p); }
    return p;
  };

  /* L'instant qui correspond à un avancement du défilement (0 à 1). */
  Ouvrier.prototype.instant = function (q) {
    var m = this.m, p, k, a, b;
    if (q < TRAVAIL) {
      k = borne((q - ENTREE) / (TRAVAIL - ENTREE));
      p = this.marche(-this.entree * (1 - k), -this.entree);
      p.opacite = lisse(k / 0.25);
      return { pose: p, etat: m.depart };
    }
    if (q < SORTIE) {
      k = (q - TRAVAIL) / (SORTIE - TRAVAIL);
      p = this.geste(k * m.duree);
      if (q < TRAVAIL + FONDU) {
        a = this.marche(0, -this.entree);
        p = melanger(a, p, lisse((q - TRAVAIL) / FONDU));
      } else if (q > SORTIE - FONDU) {
        b = this.marche(m.fin, m.fin);
        p = melanger(p, b, lisse((q - SORTIE + FONDU) / FONDU));
      }
      return { pose: p, etat: p.outil };
    }
    k = borne((q - SORTIE) / (FIN - SORTIE));
    if (m.demiTour) {
      /* Demi-tour : il repart par où il est venu. */
      var retour = this.entree + m.fin;
      p = this.marche(m.fin + retour * k, m.fin);
      p.x = m.fin - retour * k;
      p.demiTour = true;
    } else {
      p = this.marche(m.fin + this.sortie * k, m.fin);
    }
    p.opacite = 1 - lisse((k - 0.75) / 0.25);
    return { pose: p, etat: this.fini };
  };

  Ouvrier.prototype.dessiner = function (instant) {
    var os = this.os, p = instant.pose;
    function rot(el, angle, y) { el.setAttribute("transform", "rotate(" + n(angle) + " 0 " + y + ")"); }
    os.marcheur.setAttribute("transform", "translate(" + n(p.x) + " 0)" + (p.demiTour ? " scale(-1 1)" : ""));
    os.marcheur.setAttribute("opacity", n(p.opacite));
    os.bassin.setAttribute("transform", "translate(0 " + n(p.y) + ")");
    var j = jambes(p);
    rot(os["cuisse-av"], j[0][0], -36); rot(os["tibia-av"], j[0][1], -18);
    rot(os["cuisse-arr"], j[1][0], -36); rot(os["tibia-arr"], j[1][1], -18);
    rot(os.torse, p.torse, -36);
    rot(os["bras-av"], p.bras[0][0], -60); rot(os["avant-bras-av"], p.bras[0][1], -46);
    rot(os["bras-arr"], p.bras[1][0], -60); rot(os["avant-bras-arr"], p.bras[1][1], -46);
    this.m.decor(this, instant.etat, p);
  };

  /* Avancement visé : 0 quand le sol de l'ouvrier entre par le bas de
     l'écran, 1 quand il sort par le haut. */
  Ouvrier.prototype.viser = function (hauteur) {
    var sol = this.scene.getBoundingClientRect().bottom;
    this.cible = borne((hauteur - sol) / hauteur);
  };

  /* Rapproche l'avancement montré de l'avancement visé ; vrai tant
     qu'il reste du chemin. */
  Ouvrier.prototype.avancer = function (dt) {
    if (this.montre < 0) { this.montre = this.cible; }
    var ecart = this.cible - this.montre;
    this.montre = Math.abs(ecart) < 0.0005 ? this.cible : this.montre + ecart * (1 - Math.exp(-dt / AMORTI));
    this.dessiner(this.instant(this.montre));
    return this.montre !== this.cible;
  };

  var ouvriers = Array.prototype.map.call(scenes, function (scene) { return new Ouvrier(scene); });
  var visibles = ouvriers.slice();
  var requete = 0, precedent = 0;

  function image(maintenant) {
    requete = 0;
    var dt = precedent ? Math.min(64, maintenant - precedent) : 16;
    precedent = maintenant;
    var hauteur = window.innerHeight, encore = false;
    visibles.forEach(function (o) {
      o.viser(hauteur);
      if (o.avancer(dt)) { encore = true; }
    });
    if (encore) { requete = window.requestAnimationFrame(image); } else { precedent = 0; }
  }

  function demander() {
    if (!requete && !mouvementReduit.matches) { requete = window.requestAnimationFrame(image); }
  }

  function mesurer() {
    ouvriers.forEach(function (o) { o.mesurer(); });
    demander();
  }

  function demarrer() {
    mesurer();
    if (mouvementReduit.matches) {
      /* Une seule image, chacun au milieu de sa tâche : c'est aussi le
         dessin immobile écrit par outils/equipe.py. */
      ouvriers.forEach(function (o) {
        o.dessiner(o.instant(TRAVAIL + AVANCEMENT[o.metier] * (SORTIE - TRAVAIL)));
      });
      return;
    }
    /* Seuls les ouvriers proches de l'écran sont recalculés. */
    if ("IntersectionObserver" in window) {
      var observateur = new IntersectionObserver(function (entrees) {
        entrees.forEach(function (e) {
          var o = ouvriers.filter(function (x) { return x.scene === e.target; })[0];
          var i = visibles.indexOf(o);
          if (e.isIntersecting && i < 0) { visibles.push(o); }
          if (!e.isIntersecting && i >= 0) { visibles.splice(i, 1); }
        });
        demander();
      }, { rootMargin: "25% 0px" });
      ouvriers.forEach(function (o) { observateur.observe(o.scene); });
    }
    window.addEventListener("scroll", demander, { passive: true });
    var attente = 0;
    window.addEventListener("resize", function () {
      window.clearTimeout(attente);
      attente = window.setTimeout(mesurer, 150);
    });
  }

  demarrer();
})();

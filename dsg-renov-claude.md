# DSG Renovation – Refonte Site Web
## Master Prompt Claude Code

---

## 📌 Contexte & Objectifs

**Client:** DSG Renovation – Entreprise de rénovation locale (40 ans d'expérience, 11 employés, ~600 projets réalisés)  
**Objectif:** Refonte complète du site (actuellement Wix) pour générer plus de clients qualifiés + vitrine professionnelle de haute qualité  
**Localisation:** Lausanne (CH) – avenue de Béthusy 60, 1012 Lausanne | région arc lémanique (Lausanne, Genève)

### Objectifs clés
- ✅ Augmenter les demandes de devis/contact de 40-60% en 3 mois
- ✅ Améliorer la crédibilité et professionnalisme perçu
- ✅ Optimiser pour mobile (actuellement cassé)
- ✅ Générer du trafic SEO local organiquement
- ✅ Afficher galerie de projets avant/après convaincante

---

## 🎨 Direction Artistique

**IMPORTANT:** Consulter le dossier `dsg-renov-direction-artistique/` pour:
- Palette couleurs (identité visuelle cible)
- Typographie et hiérarchie
- Inspirations style (référence: branding local Suisse/arc lémanique)
- Photographie produit/projets (tone & style)
- Spacing et micro-interactions

**À respecter strictement** dans tous les éléments créés (composants React, layouts, images).

---

## 🏗️ Architecture & Stack

### Front-end
- **Framework:** Next.js 14+ (App Router)
- **Styling:** Tailwind CSS (+ custom config pour direction artistique)
- **CMS:** Sanity.io (schéma structure + images optimisées)
- **Hosting:** Infomaniak (Node.js + reverse proxy)

### Back-end / APIs
- **Contact form:** Supabase (stocker leads + emails)
- **Analytics:** Plausible (privacy-first, hébergé EU/CH)
- **SEO:** Open Graph, structured data (JSON-LD), sitemap XML
- **Images:** Sanity CDN + Infomaniak caching

### Infrastructure
- **Domaine:** dsg-renov.ch (déjà existant, géré chez Infomaniak)
- **Hosting:** Infomaniak (Node.js application hosting)
  - Build: `npm run build`
  - Start: `npm run start` (Next.js server mode)
  - Port: 3000 (reverse proxy via Infomaniak)
  - Environment: Production with monitoring
- **Email:** Setup forwarding admin@dsg-renov.ch (Infomaniak mail)
- **Monitoring:** Sentry pour error tracking (optionnel P2)
- **CDN:** Infomaniak caching headers (images Sanity)

---

## 📄 Sitemap & Pages

### Structure (8-10 pages)
```
/                          → Accueil (hero + value prop + CTA)
/services                  → Services détaillés (9 services listés)
/projets                   → Galerie avant/après (filtrable)
/projets/[id]             → Fiche projet détaillée
/about                     → À propos (40 ans, équipe, valeurs)
/contact                   → Formulaire + info contact + carte
/devis                     → Devis gratuit en ligne (landing page)
/blog                      → Articles conseil (optionnel P2)
```

---

## 🎯 Sections Clés & Requirements

### 1️⃣ **Accueil** (`/`)

#### Hero Section
- Tagline premium: "**Vos rénovations, notre passion** – 40 ans d'expertise locale"
- Sous-titre: "De l'appartement au projet complet, nous faisons la différence"
- Fond: Image hero qualité (avant/après OR intérieur rénovation)
- CTA primaire: **"Demander un devis gratuit"** → /devis
- CTA secondaire: "Voir nos projets" → /projets

#### Bandeau "Chiffres clés"
```
600+ projets réalisés
40 ans d'expérience
11 professionnels
35+ partenaires de confiance
```
*Format: 4 colonnes, responsive 2 col mobile*

#### Section "Pourquoi DSG?"
- 3-4 cartes value prop (lisible, pas de jargon)
  - "Rénovation clé en main" 
  - "Délais respectés"
  - "Équipe locale & qualifiée"
  - "Garantie de satisfaction"
- Fond blanc, design épuré

#### Section Services (Preview)
- Showcase 4-5 services principaux
- Mini-card par service (icône/image + titre + short desc)
- Lien "Voir tous les services" → /services

#### Section Projets (Preview)
- Grid 3 derniers/meilleurs projets avant/après
- Layout: avant | après (slider ou galerie)
- Texte court par projet
- CTA "Voir la galerie complète"

#### Logos Clients
- 8 logos affichés (déjà bons)
- Texte: "Nos partenaires et clients nous font confiance"
- Responsive: 4 col > 2 col > 1 col

#### Section Avis/Testimonials
- **IMPORTANT:** Récupérer 5-7 avis clients (via appel/email)
- Format: Citation + nom + titre projet
- Star rating 5/5
- Carousel ou grid selon design

#### CTA Footer (avant footer)
- "Prêt à rénover?" 
- Deux boutons: "Appeler: +41 21 847 02 02" | "Devis en ligne"

### 2️⃣ **Services** (`/services`)

- Breadcrumb: Accueil > Services
- Intro: "Nous offrons une large gamme de services pour tous vos besoins en rénovation"

**Layout:** 9 cartes services (3x3 sur desktop, stack mobile)
Chaque service:
- Image/icône
- Titre (H3)
- Description (80-120 mots, lisible)
- Lien "En savoir plus" (optionnel, vers section détail)

**Services à couvrir:**
1. Rénovation totale (appartement/maison)
2. Travaux de peinture & décoration
3. Plâtrerie & cloisons
4. Faux plafonds
5. Revêtements muraux (papier peint, tapisserie)
6. Pose carrelage
7. Pose sol (parquet, linoléum)
8. Nettoyage fin de travaux
9. Études & consultations (NEW – pour valeur ajoutée)

### 3️⃣ **Projets / Galerie** (`/projets`)

- Title: "Notre portfolio – 600+ rénovations réussies"
- **Filtres:** (radio buttons ou tabs)
  - Type: Tous | Appartement | Maison | Salle de bain | Cuisine | Autre
  - Durée: Tous | < 2 sem | 2-4 sem | 1-3 mois | + 3 mois (optionnel)

**Affichage:**
- Grid 3 colonnes (desktop) > 2 col (tablet) > 1 col (mobile)
- Chaque projet: 
  - Thumbnail avant/après (or slider)
  - Titre projet
  - Type + durée
  - 1-2 ligne description
  - Lien "Voir le projet" → /projets/[slug]

**Minimum requis:** 15 projets photographiés (bonus points: 25+)

### 4️⃣ **Fiche Projet** (`/projets/[slug]`)

- Breadcrumb
- Titre du projet
- Meta: Type | Durée | Zone (Lausanne/Genève/etc)
- Galerie full-width (5-8 photos)
- Description détaillée (250-400 mots)
- Détails "Au programme": liste puce (services appliqués)
- Quote/avis client si dispo
- Photos: tailles 1200×800 min (optimisées Sanity)

### 5️⃣ **À Propos** (`/about`)

- Section "DSG Renovation en chiffres"
- Section "Notre philosophie" (texte + image équipe)
- Section "L'équipe" (3-4 portraits prof + noms/rôles)
- Section "Notre engagement" (valeurs: respect, qualité, délais)
- Timeline: 2019 (création) → aujourd'hui (points clés)

### 6️⃣ **Contact** (`/contact`)

- Formulaire optimisé:
  - Nom
  - Email
  - Téléphone
  - Type de projet (dropdown)
  - Budget estimé (optionnel)
  - Description projet (textarea)
  - Checkbox légal/consentement
  - Bouton "Envoyer ma demande"

- Infos bloc:
  - **Adresse:** Avenue de Béthusy 60, 1012 Lausanne
  - **Tél:** +41 21 847 02 02
  - **Email:** admin@dsg-renov.ch
  - **Horaires:** Lun-Ven 8h-17h (à clarifier)

- Carte Google Maps (embeddée)
- Google Business Profile link (une fois créé)

### 7️⃣ **Devis Gratuit Landing Page** (`/devis`)

- Headline: "Devis gratuit en 48h"
- Sous-titre: "Décrivez votre projet, nous vous proposons une solution"
- Formulaire enrichi:
  - Sections progressives (multi-step optionnel)
  - Photos upload (3-5 max)
  - Calendrier dispo pour rendez-vous
- Garantie: "Aucun engagement • Réponse rapide • Confidentiel"
- Après submit: confirmation email + suivi par phone

---

## 🔍 SEO & Performance

### On-Page SEO
- **H1:** Unique par page (jamais dupliqué)
- **Meta titles:** 50-60 char, inclure "Ecublens" ou "Lausanne" où pertinent
- **Meta descriptions:** 155-160 char, CTA inclus
- **Image alt text:** Descriptif + contexte service/projet
- **Headings hierarchy:** H1 > H2 > H3 (pas de sauts)
- **Internal linking:** 3-5 liens contextuels par page

### Technical SEO
- **Sitemap XML:** Auto-généré par Next.js
- **Robots.txt:** Bien configuré
- **Structured data (JSON-LD):**
  - LocalBusiness (adresse, phone, hours)
  - Organization (logo, contact)
  - ImageObject (photos projets)
  - BreadcrumbList (navigation)
- **Mobile-first indexing:** 100% responsive, Lighthouse > 90
- **Page speed:** Core Web Vitals OK (LCP < 2.5s, CLS < 0.1)

### Local SEO
- **Google Business Profile:** Setup avec photos, avis, horaires
- **Geo keywords:** "rénovation Ecublens", "rénovateur Lausanne", "rénov Genève", etc.
- **NAP consistency:** Adresse identique partout (Google Maps, site, Facebook)
- **Avis clients:** Encourager 5+ avis positifs sur GMB

### Content Strategy
- **Blog (optionnel P2):** 1-2 articles/mois (conseils rénov, tendances, etc.)
- **FAQ:** Section FAQ sur /contact ou /services

---

## 📱 Responsive & Accessibility

- **Breakpoints:** 320px | 768px | 1024px | 1440px
- **Mobile-first:** Conception desktop-down
- **WCAG 2.1 AA:** Contraste texte min AAA, alt text, labels form, nav clavier
- **Performance mobile:** Images lazy-loaded, minification, bundle splitting

---

## 🎬 Animations & UX

- **Hover states:** Subtiles, direction artistique
- **Transitions:** Smooth (200-300ms)
- **Scroll animations:** Fade-in, parallax léger (respecter direction artistique)
- **Loading states:** Skeleton screens ou spinners
- **Error messages:** Clairs et aidants

---

## 📊 Analytics & Conversions

- **Goals Vercel Analytics:**
  - "Devis demanded" (form submit)
  - "Phone call" (click tel: link)
  - "Email click"
  - "Project view" (click sur galerie)

- **Heatmaps:** Optionnel (HotJar) pour voir où les users cliquent

---

## 🔐 Sécurité & Conformité

- **HTTPS:** Obligatoire (Vercel auto)
- **RGPD/LPD:** 
  - Politique de confidentialité claire
  - Consentement cookie (Sanity CMS)
  - Pas de tracking invasif
- **Formulaires:** Validation client-side + server-side
- **Email:** Vérification double-opt-in pour newsletter (futur)

---

## 📋 Livrables & Étapes

### Phase 1: Discovery & Setup (1 semaine)
- [ ] Récupérer photos projets (min 15)
- [ ] Interviews clients pour avis/testimonials
- [ ] Setup Sanity CMS (schéma projets, services, settings)
- [ ] Setup repo Next.js (production build ready)
- [ ] Préparer environment variables pour Infomaniak/Supabase
- [ ] Configure reverse proxy Infomaniak + domain routing

### Phase 2: Design & Dev (2-3 semaines)
- [ ] Componentes React (Hero, Service Card, Project Gallery, etc.)
- [ ] Intégration direction artistique (couleurs, typo, spacing)
- [ ] Pages principales (Accueil, Services, Projets)
- [ ] Formulaire contact + intégration Supabase
- [ ] SEO base + structured data

### Phase 3: Contenu & Optimisations (1-2 semaines)
- [ ] Rédaction contenu pages (textes clairs, lisibles)
- [ ] Upload photos Sanity (optimisation + alt text)
- [ ] Créer fiches projets détaillées
- [ ] Testing mobile, performance, accessibilité

### Phase 4: Launch & Post-Launch (1 semaine)
- [ ] Deploy sur Infomaniak (build + start process)
- [ ] Test prod (domain, SSL, performance)
- [ ] Google Business Profile création
- [ ] Submit sitemap Google Search Console
- [ ] Setup analytics (Plausible)
- [ ] Campagne "Récupérer avis" clients existants
- [ ] Monitoring Sentry (si activé)

---

## 🎯 KPIs de Succès (90 jours)

| Métrique | Baseline | Target |
|----------|----------|--------|
| Demandes de devis/mois | ~5-10 | 15-20 (+50-100%) |
| Trafic organiq. (sessions) | ~50 | 150-200 (+150%) |
| Taux conversion (visit → contact) | 2% | 5-7% |
| Mobile traffic % | ~30% | 50%+ |
| Google Business avis | 0 | 5+ (4.5★+) |
| Bounce rate accueil | ~60% | <45% |

---

## 📞 Contact & Notes

**Client:** DSG Renovation  
**Adresse:** Avenue de Béthusy 60, 1012 Lausanne  
**Tél:** +41 21 847 02 02  
**Contact principal:** [À clarifier avec client]

**Agence:** WeAreBrothers (WAB)  
**Tech Lead:** [Lazizze]

---

## 🚀 Commandes Claude Code

### Installation de base
```bash
npm install next react react-dom
npm install -D tailwindcss postcss autoprefixer
npm install @sanity/client next-sanity
npm install @supabase/supabase-js
```

### Structure de départ
```
dsg-renov/
├── app/
│   ├── (home)/
│   │   └── page.tsx
│   ├── services/
│   │   └── page.tsx
│   ├── projets/
│   │   ├── page.tsx
│   │   └── [slug]/
│   │       └── page.tsx
│   ├── about/
│   ├── contact/
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── HeroSection.tsx
│   ├── ServiceCard.tsx
│   ├── ProjectCard.tsx
│   └── ContactForm.tsx
├── lib/
│   ├── sanity.ts
│   ├── supabase.ts
│   └── seo.ts
├── public/
│   └── images/
├── sanity/
│   ├── schema.ts
│   └── lib/
└── tailwind.config.ts
```

---

**Version:** 1.0  
**Dernière maj:** juillet 2026  
**Status:** 🟢 Ready to dev

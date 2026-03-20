# Avancement - CybOS
Dernière mise à jour : 2026-03-20

Légende :
- 🎨 = Designer (moi)
- 💻 = Dev (Claude)
- 🔍 = Head of Design (Claude vérifie la qualité)
- [x] = fait / [ ] = à faire

## Phase 0 - Setup

### 0.1 - Préparer le fichier Figma

Tout doit être prêt AVANT de lancer la prod. L'objectif : que Claude puisse lire le Figma et travailler sans poser de questions évitables.

Design System :

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Palette de couleurs complète avec noms explicites (ex: blue-800, red-300, pas juste "primary") |
| 🎨 | [x] | Échelle typographique complète : chaque style de texte nommé (h1-bold, text-md, text-sm...) avec font, weight, size, line-height |
| 🎨 | [x] | Spacings définis (8, 16, 24, 32, 48, 64, 128...) |
| 🎨 | [x] | Radius définis (sm, md, lg, full) |
| 🎨 | [x] | Composants avec variants et states (default, hover, active, disabled si applicable) |
| 🎨 | [x] | Couleurs spécifiques par page/section si applicable (ex: chaque projet a sa couleur de fond + couleur texte) |

Maquettes :

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Toutes les pages finalisées |
| 🎨 | [x] | Noms de frames clairs et explicites (ex: "Home - Desktop", "Projet Bouygues", pas "Frame 47") |
| 🎨 | [x] | Contenu textuel final (pas de lorem ipsum dans les maquettes, sauf si c'est voulu) |

Animations et interactions :

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Pour chaque animation souhaitée, annoter dans Figma ou dans un doc à part : quel élément, quel trigger (scroll, hover, clic, chargement de page), état de départ -> état de fin (ex: opacity 0 -> 1, scale 0.8 -> 1), durée approximative (ex: 0.3s, 0.6s), référence visuelle si possible (lien vidéo, site d'inspiration) |
| 🎨 | [x] | Si z-index complexe (éléments qui se superposent) : annoter l'ordre des couches dans un schéma |

Responsive :

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Breakpoint(s) décidé(s) |

### 0.2 - Vérification du fichier Figma

Avant d'exporter quoi que ce soit, envoyer les liens Figma à Claude. Claude joue le rôle de Head of Design et passe en revue le fichier. On itère jusqu'à ce qu'il n'y ait plus de zone d'ombre.

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Envoyer les liens Figma à Claude pour vérification |
| 🔍 | [x] | DS complet ? (couleurs, typo, spacings, radius, composants, variants, states) |
| 🔍 | [x] | Maquettes complètes ? (toutes les pages, desktop + mobile) |
| 🔍 | [x] | Nommage Figma sans erreur ? (frames, layers, composants lisibles par le MCP) |
| 🔍 | [x] | Animations spécifiées ? (trigger, état, durée pour chaque) |
| 🔍 | [x] | Responsive spécifié ? (breakpoints, comportements par section) |
| 🔍 | [x] | Tokens lisibles par le MCP ? (variables Figma, styles) |
| 🔍 | [x] | Éléments ambigus ou manquants identifiés ? |
| 🔍 | [x] | Questions envoyées au designer |
| 🎨 | [x] | Répondre aux questions / corriger le Figma |
| 🔍 | [x] | Vérification finale : plus aucune zone d'ombre |
| 🎨 | [x] | Confirmer : Figma prêt |

### 0.3 - Exporter et organiser les assets

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Exporter TOUTES les images depuis Figma (mockups, backgrounds, icônes, photos, patterns) |
| 🎨 | [x] | Exporter les vidéos si applicable (aucune vidéo dans le projet) |
| 💻 | [x] | Nommage strict : tirets, pas d'accents, pas d'espaces, pas d'apostrophes — renommé par Claude |
| 🎨 | [x] | Organiser dans des sous-dossiers logiques (assets/icons/, assets/backgrounds/, assets/apps/, assets/loaders/) |
| 🎨 | [x] | Vérifier que chaque image référencée dans les maquettes a son fichier exporté correspondant |

### 0.4 - Setup Git

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Créer le repo Git (ou vérifier qu'il existe) |
| 🎨 | [x] | Vérifier que la clé SSH est configurée (pour éviter le blocage en pleine prod) |
| 🎨 | [x] | Mettre tous les assets dans le dossier projet |
| 💻 | [x] | Commit initial avec tous les assets |
| 💻 | [x] | Vérifier que le push fonctionne |

Gate : toutes les cases cochées (0.1 + 0.2 + 0.3 + 0.4) avant de passer à la phase 1.

## Phase 1 - Brief + Audit Figma

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [x] | Envoyer les liens Figma (DS + maquettes desktop + mobile) |
| 💻 | [x] | Fetch Figma + produire le tableau d'audit comparatif |
| 🔍 | [x] | Vérification : tokens lisibles ? Éléments manquants ? Ambiguïtés ? |
| 🔍 | [x] | Questions numérotées envoyées au designer (14 questions) |
| 🎨 | [x] | Répondre à toutes les questions en un bloc |
| 💻 | [x] | Mettre à jour CLAUDE.md avec les décisions |
| 🔍 | [x] | Vérification finale : plus aucune zone d'ombre ? |
| 🎨 | [x] | Confirmer : OK, plus de questions |

Gate : les deux confirment, on passe à la phase 2.

## Phase 2 - Tokens + Styleguide

| Rôle | Status | Tâche |
|------|--------|-------|
| 💻 | [x] | Créer les tokens Python (couleurs, typo, spacings, radius, effets, animations) |
| 💻 | [x] | Construire la page styleguide (palettes, typo, spacings, blocs, barres, icônes) |
| 💻 | [x] | Push |
| 🔍 | [ ] | Auto-vérification : comparer le styleguide codé vs le DS Figma, signaler les écarts |
| 🎨 | [ ] | Review visuelle du styleguide |
| 🎨 | [ ] | Envoyer les retours en batch |
| 💻 | [ ] | Appliquer les corrections, push |
| 🔍 | [ ] | Vérification : corrections appliquées, plus d'écart ? |
| 🎨 | [ ] | Valider le styleguide |

Gate : styleguide validé par le designer avant intégration des pages.

## Phase 3 - Intégration des pages

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [ ] | Définir l'ordre d'intégration |
| 💻 | [ ] | Intégrer [Page 1] |
| 💻 | [ ] | Intégrer [Page 2] |
| 💻 | [ ] | Intégrer [Page 3] |
| 💻 | [ ] | Intégrer [etc.] |
| 💻 | [ ] | Vérifier tous les chemins d'assets avant push |
| 💻 | [ ] | Push |
| 🔍 | [ ] | Auto-vérification : comparer chaque page codée vs maquette Figma, signaler les écarts |
| 🎨 | [ ] | Review visuelle de chaque page |
| 🎨 | [ ] | Envoyer les retours en batch |
| 💻 | [ ] | Appliquer les corrections, push |
| 🔍 | [ ] | Vérification : corrections appliquées ? |
| 🎨 | [ ] | Valider les pages |

## Phase 4 - Animations et interactions

| Rôle | Status | Tâche |
|------|--------|-------|
| 🔍 | [ ] | Relire les specs d'animation de la phase 0, vérifier qu'elles sont complètes |
| 🎨 | [ ] | Compléter les specs si Claude a signalé des manques |
| 💻 | [ ] | Implémenter les animations |
| 💻 | [ ] | Tester en local (npm run dev) |
| 💻 | [ ] | Push |
| 🎨 | [ ] | Review (tester en local ensemble pour les effets subtils) |
| 🎨 | [ ] | Retours en batch |
| 💻 | [ ] | Itérer, push |
| 🎨 | [ ] | Valider les animations |

## Phase 5 - Responsive

| Rôle | Status | Tâche |
|------|--------|-------|
| 💻 | [ ] | Implémenter le responsive |
| 💻 | [ ] | Vérifier overflow-x sur mobile |
| 💻 | [ ] | Désactiver les effets mouse sur tactile |
| 💻 | [ ] | Push |
| 🎨 | [ ] | Tester sur téléphone |
| 🎨 | [ ] | Retours en batch |
| 💻 | [ ] | Corrections, push |
| 🎨 | [ ] | Valider le responsive |

## Phase 6 - Production

| Rôle | Status | Tâche |
|------|--------|-------|
| 🎨 | [ ] | Fournir : texte meta description |
| 🎨 | [ ] | Fournir : image OG (1200x630) |
| 🎨 | [ ] | Fournir : favicon source |
| 💻 | [ ] | Configurer meta/OG/favicon |
| 💻 | [ ] | Configurer analytics |
| 💻 | [ ] | Configurer sitemap + robots.txt |
| 💻 | [ ] | Créer page 404 |
| 💻 | [ ] | Push |
| 🔍 | [ ] | Vérification : tout est en place pour la mise en prod ? (DNS, domaine, redirections) |
| 🎨 | [ ] | Configurer DNS (screenshot des records actuels) |
| 💻 | [ ] | Donner les instructions DNS exactes |
| 🎨 | [ ] | Configurer Vercel (domaine, auto-deploy) |
| 💻 | [ ] | Push final |
| 🎨 | [ ] | Test final sur le domaine live |

## Phase 7 - Debrief

| Rôle | Status | Tâche |
|------|--------|-------|
| 💻 | [ ] | Générer le rapport de debrief complet (déroulé, ce qui a marché, ce qui peut s'améliorer, process recommandé) |
| 🎨 | [ ] | Relire et compléter le rapport |
| 💻 | [ ] | Sauvegarder en mémoire |
| 🎨 | [ ] | Archiver le rapport |

## Décisions en attente
- [Questions ou choix à trancher]

## Notes de session
- [Ce qu'il faut attaquer à la prochaine session]
- [Ce que le designer doit préparer avant]

# CybOS

## Contexte
CybOS est l'interface de la Raspberry Pi de Cyba. C'est un hub qui se lance à l'allumage de la Rasp et permet de naviguer entre toutes les applications installées. ~30 pages. Inclut un hub de choix, des options de personnalisation, des connexions et des mises à jour (via terminal distant).

## Stack technique
- Langage : Python + Pygame
- Résolution native : 800x480 (Waveshare 3.5" DSI)
- Doit supporter des résolutions plus grandes (TV via HDMI) — pas de breakpoints fixes, scaling proportionnel
- Contrainte : 100% offline
- Plateforme : Raspberry Pi 4
- Navigation : D-pad physique (flèches + boutons ABXY, pas de souris/touch)
- Inputs : MCP23017 via I2C (GPIO)

## Commandes
- Dev : `python3 main.py`
- Styleguide : `python3 main.py --styleguide`
- Build : N/A (exécution directe Python)

## Structure du projet
```
CybOS/
├── main.py                      # Point d'entrée
├── CLAUDE.md                    # Contexte projet
├── TODO-CLAUDE.md               # Suivi des tâches
├── assets/
│   ├── apps/                    # Illustrations d'apps (SVG)
│   ├── backgrounds/             # Éléments décoratifs (SVG)
│   ├── fonts/                   # Fonts (DM Serif Text)
│   ├── icons/                   # Icônes (SVG)
│   └── loaders/                 # Frames d'animation loader (SVG)
└── src/
    ├── core/
    │   ├── tokens.py            # Design tokens (couleurs, typo, spacings...)
    │   └── renderer.py          # Fonctions de rendu (texte, formes, blocs)
    ├── components/              # Composants réutilisables (à venir)
    └── screens/
        └── styleguide.py        # Page de démo du DS
```

## Design Tokens

### Couleurs primitives

**Blue :**
| Token | Hex |
|-------|-----|
| blue-50 | #E6F2F1 |
| blue-100 | #BAE3E4 |
| blue-200 | #7DD3D5 |
| blue-300 | #3EBECB |
| blue-400 | #009ABD |
| blue-500 | #006D92 |
| blue-600 | #084D6D |
| blue-700 | #09354C |
| blue-800 | #082837 |

**Red :**
| Token | Hex |
|-------|-----|
| red-50 | #FFE4DC |
| red-100 | #FFC1B7 |
| red-200 | #ED968F |
| red-300 | #CF6F6D |
| red-400 | #AC464B |
| red-500 | #822935 |
| red-600 | #5D1322 |
| red-700 | #3A0613 |
| red-800 | #190105 |

### Couleurs sémantiques

| Token | Valeur | Usage |
|-------|--------|-------|
| title-primary | blue-500 (#006D92) | Titres principaux |
| title-secondary | red-400 (#AC464B) | Titres secondaires |
| text-primary | blue-500 (#006D92) | Texte courant |
| text-secondary | red-400 (#AC464B) | Texte accent |
| text-primary-disable | blue-300 (#3EBECB) | Texte désactivé bleu |
| text-secondary-disable | red-200 (#ED968F) | Texte désactivé rouge |
| action-primary | blue-500 (#006D92) | Actions principales |
| action-secondary | red-400 (#AC464B) | Actions secondaires |
| action-primary-disable | blue-200 (#7DD3D5) | Actions désactivées |
| icons-primary | blue-500 (#006D92) | Icônes principales |
| icons-secondary | red-400 (#AC464B) | Icônes secondaires |
| icons-secondary-dark | red-600 (#5D1322) | Éléments décoratifs sombres |
| icons-secondary-light | red-100 (#FFC1B7) | Éléments décoratifs clairs |
| bloc-bg-light | #E6F2F11A | Fond des blocs (10% opacité) |
| bloc-stroke | blue-50 (#E6F2F1) | Bordure des blocs |
| bar-light | blue-300 (#3EBECB) | Barres de progression (clair) |
| bar-medium | blue-500 (#006D92) | Barres de progression (foncé) |
| bar-background | blue-50 (#E6F2F1) | Fond des barres |

### Typographie

| Token | Font | Weight | Size | Line-height |
|-------|------|--------|------|-------------|
| title-xl | DM Serif Text | Regular (400) | 112px | 100% |
| title-md | DM Serif Text | Regular (400) | 48px | 100% |
| text-medium | Helvetica Neue | Bold (700) | 32px | 100% |
| text-medium-italic | Helvetica Neue | Bold Italic (700) | 32px | 100% |
| text-small | Helvetica Neue | Bold (700) | 20px | 100% |

### Spacings

| Token | Valeur |
|-------|--------|
| sp-8 | 8px |
| sp-12 | 12px |
| sp-16 | 16px |
| sp-20 | 20px |
| sp-32 | 32px |
| sp-48 | 48px |

### Border radius

| Token | Valeur |
|-------|--------|
| radius-default | 12px |
| radius-full | 9999px |

### Effets (Window)

**Window - Default :**
- Background blur: 23.7px
- Drop shadow: #084D6D80, offset (1,1), blur 3
- Drop shadow: #E6F2F1E5, offset (-1,-1), blur 3

**Window - Select :**
- Background blur: 23.7px
- Drop shadow: #084D6D4D, offset (4,4), blur 12
- Drop shadow: #E6F2F1B2, offset (-4,-4), blur 12
- Drop shadow: #084D6D80, offset (1,1), blur 3
- Drop shadow: #E6F2F1E5, offset (-1,-1), blur 3

### Spécifiques

| Token | Valeur |
|-------|--------|
| gap | 32px |
| margin | 32px |
| bloc-responsive-weight-max | 900 |

### Gradients (à extraire visuellement)
- Gradient Typography: blue-300 → blue-400
- Gradient Action: blue-300 → blue-500
- Gradient Background: blue-50 → blue-100
- Gradient Light: blue-50 → blue-50
- Gradient Reflect: (effet reflet, à détailler)

## Décisions prises
- **Stack** : Python + Pygame — léger, pas de serveur web, accès direct framebuffer + GPIO
- **Résolution** : 800x480 natif, scaling proportionnel pour TV/écrans plus grands
- **Navigation** : D-pad uniquement (pas de souris/touch en V1)
- **Onboarding** : pas en V1. Potentiellement un flow Bluetooth au premier lancement si aucun appareil détecté
- **Loader** : animation réelle, boucle de 3s
- **Loading app** : minimum 2s de transition avant lancement
- **Welcome bar** : vraie progression si > 3s, sinon fake de 3s
- **Move app** : déclenché par clic long (2s) sur une app
- **Pop-ups** : navigation gauche/droite entre les options. Shutdown accessible depuis Settings
- **Langue** : tout en français pour la prod (Paramètres, Accueil, Système, Clair/Foncé, etc.)
- **Pop-up template** : "Erreur + [Description]" est un générique réutilisable, pas du contenu final

## Gotchas
[Pièges techniques rencontrés et leurs solutions]

## Erreurs et corrections

### Figma (🎨 Designer)
- **Franglish dans les maquettes** : "Settings", "Home", "Light/Dark", "Power off" utilisés à la place du français. Corrigé → Paramètres, Accueil, Clair/Foncé, Éteindre
- **"Hover" au lieu de "clic long"** : l'annotation sur le move app indiquait "hover" alors qu'il n'y a pas de souris — c'est un clic long 2s. Corrigé dans Figma
- **Nommage des assets Figma** : export avec le format Figma brut (virgules, espaces, `Name=`, `Color=`). Corrigé par Claude au renommage

### Dev (💻 Claude)
[À remplir au fil du projet]

### Process
[À remplir au fil du projet]

## Conventions
[Règles de nommage, patterns récurrents]

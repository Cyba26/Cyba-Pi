"""
CybOS Design Tokens
Toutes les constantes visuelles du Design System.
Source: Figma variables + styles du fichier CybOS.
"""


# --- Couleurs primitives ---

BLUE = {
    50: (230, 242, 241),
    100: (186, 227, 228),
    200: (125, 211, 213),
    300: (62, 190, 203),
    400: (0, 154, 189),
    500: (0, 109, 146),
    600: (8, 77, 109),
    700: (9, 53, 76),
    800: (8, 40, 55),
}

RED = {
    50: (255, 228, 220),
    100: (255, 193, 183),
    200: (237, 150, 143),
    300: (207, 111, 109),
    400: (172, 70, 75),
    500: (130, 41, 53),
    600: (93, 19, 34),
    700: (58, 6, 19),
    800: (25, 1, 5),
}


# --- Couleurs sémantiques ---

class Colors:
    # Titres
    TITLE_PRIMARY = BLUE[500]
    TITLE_SECONDARY = RED[400]

    # Texte
    TEXT_PRIMARY = BLUE[500]
    TEXT_SECONDARY = RED[400]
    TEXT_PRIMARY_DISABLE = BLUE[300]
    TEXT_SECONDARY_DISABLE = RED[200]

    # Actions / inputs
    ACTION_PRIMARY = BLUE[500]
    ACTION_SECONDARY = RED[400]
    ACTION_PRIMARY_DISABLE = BLUE[200]

    # Icônes
    ICON_PRIMARY = BLUE[500]
    ICON_SECONDARY = RED[400]
    ICON_SECONDARY_DARK = RED[600]
    ICON_SECONDARY_LIGHT = RED[100]

    # Blocs
    BLOC_BG_LIGHT = (230, 242, 241, 26)  # blue-50 à 10% opacité
    BLOC_STROKE = BLUE[50]

    # Barres de progression
    BAR_LIGHT = BLUE[300]
    BAR_MEDIUM = BLUE[500]
    BAR_BACKGROUND = BLUE[50]

    # Éléments décoratifs
    CIRCLE_TRANSPARENT = BLUE[200]


# --- Typographie ---

class Fonts:
    TITLE_FAMILY = "DM Serif Text"
    TEXT_FAMILY = "Helvetica Neue"

    # Tailles
    TITLE_XL = 112
    TITLE_MD = 48
    TEXT_MEDIUM = 32
    TEXT_SMALL = 20

    # Weights (pour référence, Pygame ne gère pas le weight nativement)
    TITLE_WEIGHT = 400  # Regular
    TEXT_WEIGHT = 700  # Bold


# --- Spacings ---

class Spacing:
    SP_8 = 8
    SP_12 = 12
    SP_16 = 16
    SP_20 = 20
    SP_32 = 32
    SP_48 = 48


# --- Border radius ---

class Radius:
    DEFAULT = 12
    FULL = 9999  # Cercle parfait


# --- Résolution ---

class Screen:
    WIDTH = 800
    HEIGHT = 480
    FPS = 60


# --- Effets (neumorphisme) ---

class Effects:
    # Window - Default
    BLUR_RADIUS = 24  # arrondi de 23.7

    SHADOW_DEFAULT = {
        "dark": {
            "color": (8, 77, 109, 128),  # #084D6D80
            "offset": (1, 1),
            "blur": 3,
        },
        "light": {
            "color": (230, 242, 241, 229),  # #E6F2F1E5
            "offset": (-1, -1),
            "blur": 3,
        },
    }

    SHADOW_SELECT = {
        "dark_outer": {
            "color": (8, 77, 109, 77),  # #084D6D4D
            "offset": (4, 4),
            "blur": 12,
        },
        "light_outer": {
            "color": (230, 242, 241, 178),  # #E6F2F1B2
            "offset": (-4, -4),
            "blur": 12,
        },
        "dark_inner": {
            "color": (8, 77, 109, 128),  # #084D6D80
            "offset": (1, 1),
            "blur": 3,
        },
        "light_inner": {
            "color": (230, 242, 241, 229),  # #E6F2F1E5
            "offset": (-1, -1),
            "blur": 3,
        },
    }


# --- Spécifiques layout ---

class Layout:
    GAP = 32
    MARGIN = 32
    BLOC_RESPONSIVE_WEIGHT_MAX = 900


# --- Gradients (tuples de couleurs pour interpolation) ---

class Gradients:
    TYPOGRAPHY = (BLUE[300], BLUE[400])
    ACTION = (BLUE[300], BLUE[500])
    BACKGROUND = (BLUE[50], BLUE[100])
    LIGHT = (BLUE[50], BLUE[50])


# --- Animations ---

class Animations:
    LOADER_CYCLE = 3.0  # secondes
    APP_LOADING_MIN = 2.0  # secondes
    WELCOME_BAR_FAKE = 3.0  # secondes si chargement < 3s
    LONG_PRESS = 2.0  # secondes pour déclencher move app

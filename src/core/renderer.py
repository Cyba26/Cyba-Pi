"""
CybOS Renderer
Fonctions utilitaires pour le rendu Pygame : formes, texte, effets.
"""

import os
import pygame
from src.core.tokens import Colors, Fonts, Radius, Effects, BLUE, RED


# Cache des fonts chargées
_font_cache = {}

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")


def get_font(family, size, bold=False, italic=False):
    """Charge et met en cache une font."""
    key = (family, size, bold, italic)
    if key not in _font_cache:
        font_path = _find_font_file(family, bold, italic)
        if font_path and os.path.exists(font_path):
            _font_cache[key] = pygame.font.Font(font_path, size)
        else:
            _font_cache[key] = pygame.font.SysFont(family, size, bold=bold, italic=italic)
    return _font_cache[key]


def _find_font_file(family, bold=False, italic=False):
    """Trouve le fichier de font correspondant dans assets/fonts/."""
    if not os.path.exists(FONTS_DIR):
        return None

    family_lower = family.lower().replace(" ", "")
    suffix = ""
    if bold and italic:
        suffix = "bolditalic"
    elif bold:
        suffix = "bold"
    elif italic:
        suffix = "italic"
    else:
        suffix = "regular"

    for f in os.listdir(FONTS_DIR):
        f_lower = f.lower().replace("-", "").replace("_", "")
        if family_lower in f_lower and suffix in f_lower:
            return os.path.join(FONTS_DIR, f)

    # Fallback : n'importe quel fichier de cette famille
    for f in os.listdir(FONTS_DIR):
        f_lower = f.lower().replace("-", "").replace("_", "")
        if family_lower in f_lower:
            return os.path.join(FONTS_DIR, f)

    return None


def draw_text(surface, text, x, y, font_family, size, color, bold=False, italic=False, anchor="topleft"):
    """Dessine du texte avec ancrage configurable."""
    font = get_font(font_family, size, bold=bold, italic=italic)
    text_surface = font.render(text, True, color[:3])
    rect = text_surface.get_rect(**{anchor: (x, y)})
    surface.blit(text_surface, rect)
    return rect


def draw_rounded_rect(surface, rect, color, radius=Radius.DEFAULT, border=0, border_color=None):
    """Dessine un rectangle arrondi avec optionnel border."""
    r = pygame.Rect(rect)

    if len(color) == 4:
        # Couleur avec alpha
        temp = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
        pygame.draw.rect(temp, color, (0, 0, r.width, r.height), border_radius=radius)
        surface.blit(temp, r.topleft)
    else:
        pygame.draw.rect(surface, color, r, border_radius=radius)

    if border > 0 and border_color:
        pygame.draw.rect(surface, border_color[:3], r, width=border, border_radius=radius)


def draw_bloc(surface, rect, state="default"):
    """Dessine un bloc style CybOS (fond semi-transparent + stroke + neumorphisme)."""
    r = pygame.Rect(rect)

    # Ombres neumorphiques
    shadow_config = Effects.SHADOW_SELECT if state == "select" else Effects.SHADOW_DEFAULT
    _draw_neumorphic_shadows(surface, r, shadow_config)

    # Fond semi-transparent
    draw_rounded_rect(surface, r, Colors.BLOC_BG_LIGHT, radius=Radius.DEFAULT)

    # Stroke
    draw_rounded_rect(surface, r, (0, 0, 0, 0), radius=Radius.DEFAULT,
                       border=1, border_color=Colors.BLOC_STROKE)


def _draw_neumorphic_shadows(surface, rect, shadow_config):
    """Dessine les ombres neumorphiques autour d'un rect."""
    for key, shadow in shadow_config.items():
        offset = shadow["offset"]
        color = shadow["color"]
        blur = shadow["blur"]

        shadow_rect = rect.move(offset[0], offset[1])
        temp = pygame.Surface((shadow_rect.width + blur * 2, shadow_rect.height + blur * 2), pygame.SRCALPHA)

        alpha = color[3] if len(color) == 4 else 255
        shadow_color = (color[0], color[1], color[2], alpha // 3)

        pygame.draw.rect(temp, shadow_color,
                         (blur, blur, shadow_rect.width, shadow_rect.height),
                         border_radius=Radius.DEFAULT)

        surface.blit(temp, (shadow_rect.x - blur, shadow_rect.y - blur))


def draw_progress_bar(surface, rect, fill_ratio, bar_color=Colors.BAR_MEDIUM, bg_color=Colors.BAR_BACKGROUND):
    """Dessine une barre de progression."""
    r = pygame.Rect(rect)

    # Fond
    pygame.draw.rect(surface, bg_color, r, border_radius=r.height // 2)

    # Remplissage
    if fill_ratio > 0:
        fill_width = max(r.height, int(r.width * fill_ratio))
        fill_rect = pygame.Rect(r.x, r.y, fill_width, r.height)
        pygame.draw.rect(surface, bar_color, fill_rect, border_radius=r.height // 2)


def draw_gradient_vertical(surface, rect, color_top, color_bottom):
    """Dessine un dégradé vertical."""
    r = pygame.Rect(rect)
    for y in range(r.height):
        t = y / max(1, r.height - 1)
        color = (
            int(color_top[0] + (color_bottom[0] - color_top[0]) * t),
            int(color_top[1] + (color_bottom[1] - color_top[1]) * t),
            int(color_top[2] + (color_bottom[2] - color_top[2]) * t),
        )
        pygame.draw.line(surface, color, (r.x, r.y + y), (r.x + r.width - 1, r.y + y))


def load_svg(filename, size=None):
    """Charge un SVG depuis le dossier assets. Retourne une Surface."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        # Fallback : surface rouge pour signaler l'asset manquant
        s = pygame.Surface(size or (24, 24), pygame.SRCALPHA)
        s.fill((255, 0, 0, 128))
        return s

    try:
        surface = pygame.image.load(path)
        if size:
            surface = pygame.transform.smoothscale(surface, size)
        return surface
    except pygame.error:
        s = pygame.Surface(size or (24, 24), pygame.SRCALPHA)
        s.fill((255, 0, 0, 128))
        return s

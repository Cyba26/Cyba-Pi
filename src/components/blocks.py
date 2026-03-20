"""
CybOS Components — Blocks
Bloc style (neumorphic cards), application bloc, quickaction bar.
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius, Effects
from src.core.renderer import draw_text, draw_rounded_rect, draw_bloc, load_svg


def draw_bloc_style(surface, x, y, size=128, state="default", typ="default",
                     contrast="light", stroke=True):
    """Bloc carré neumorphique (128x128 par défaut)."""
    r = Radius.DEFAULT

    # Couleur de fond selon le type
    if typ == "default":
        bg = BLUE[50]
    else:  # light
        bg = (230, 242, 241, 40)  # très transparent

    # Intensité des ombres selon le contraste
    shadow_alpha_mult = {"light": 0.5, "medium": 1.0, "heavy": 1.8}
    mult = shadow_alpha_mult.get(contrast, 1.0)

    # Dessin des ombres
    if state == "clic":
        _draw_clic_shadows(surface, x, y, size, size, r, mult)
    elif state == "select":
        _draw_select_shadows(surface, x, y, size, size, r, mult)
    else:
        _draw_default_shadows(surface, x, y, size, size, r, mult)

    # Fond
    if isinstance(bg, tuple) and len(bg) == 4:
        temp = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(temp, bg, (0, 0, size, size), border_radius=r)
        surface.blit(temp, (x, y))
    else:
        pygame.draw.rect(surface, bg, (x, y, size, size), border_radius=r)

    # Stroke
    if stroke:
        pygame.draw.rect(surface, BLUE[50], (x, y, size, size), width=1, border_radius=r)


def draw_app_bloc(surface, x, y, icon_surface=None, name="App", state="default", moving=False):
    """Bloc application pour le home screen."""
    if moving:
        if state == "select":
            w, h = 216, 216
        else:
            w, h = 112, 112
    else:
        if state in ("select", "clic"):
            w, h = 256, 256
        elif state == "loading":
            w, h = 256, 256
        else:
            w, h = 176, 256

    r = Radius.DEFAULT
    draw_bloc(surface, (x, y, w, h), state="select" if state in ("select", "clic") else "default")

    # Icône centrée
    if icon_surface:
        icon_w, icon_h = icon_surface.get_size()
        if state in ("select", "clic") and not moving:
            # Plus grande
            scaled = pygame.transform.smoothscale(icon_surface, (int(icon_w * 1.2), int(icon_h * 1.2)))
            ix = x + (w - scaled.get_width()) // 2
            iy = y + (h - scaled.get_height()) // 2 - 20
            surface.blit(scaled, (ix, iy))
        else:
            ix = x + (w - icon_w) // 2
            iy = y + (h - icon_h) // 2 - (20 if not moving else 0)
            surface.blit(icon_surface, (ix, iy))

    # Bouton play en bas à droite (état select/clic)
    if state in ("select", "clic") and not moving:
        from src.components.buttons import draw_button_icon
        draw_button_icon(surface, x + w - 48, y + h - 48, "play", "small",
                          "select" if state == "select" else "clic")

    # Loader (état loading)
    if state == "loading":
        cx, cy = x + w // 2, y + h - 40
        arc_rect = pygame.Rect(cx - 12, cy - 12, 24, 24)
        pygame.draw.arc(surface, RED[400], arc_rect, 0, 4.2, 3)

    # Indicateur de drop (moving + select)
    if moving and state == "select":
        # Flèche vers le bas
        cx = x + w // 2
        by = y + h + 8
        pts = [(cx - 10, by), (cx, by + 12), (cx + 10, by)]
        pygame.draw.polygon(surface, RED[400], pts)


def draw_quickaction_bar(surface, x, y, typ="audio", on_screen=False):
    """Barre d'action rapide verticale."""
    if on_screen:
        w, h = 128, 418
        draw_bloc(surface, (x, y, w, h), state="default")
        # Icône en haut
        icon_cx = x + w // 2
        if typ == "audio":
            from src.components.bars import _draw_speaker_icon
            _draw_speaker_icon(surface, icon_cx - 12, y + 16, BLUE[500])
        else:
            from src.components.bars import _draw_sun_icon
            _draw_sun_icon(surface, icon_cx - 12, y + 16, BLUE[500])
        # Barre verticale
        bar_x = icon_cx - 4
        bar_h = h - 80
        draw_rounded_rect(surface, (bar_x, y + 56, 8, bar_h), BLUE[50], radius=4)
        fill_h = int(bar_h * 0.6)
        draw_rounded_rect(surface, (bar_x, y + 56 + bar_h - fill_h, 8, fill_h), BLUE[500], radius=4)
    else:
        w, h = 24, 308
        # Icône en haut
        if typ == "audio":
            from src.components.bars import _draw_speaker_icon
            _draw_speaker_icon(surface, x, y, BLUE[500])
        else:
            from src.components.bars import _draw_sun_icon
            _draw_sun_icon(surface, x, y, BLUE[500])
        # Barre verticale fine
        bar_h = h - 40
        draw_rounded_rect(surface, (x + 8, y + 32, 8, bar_h), BLUE[50], radius=4)
        fill_h = int(bar_h * 0.6)
        draw_rounded_rect(surface, (x + 8, y + 32 + bar_h - fill_h, 8, fill_h), BLUE[500], radius=4)


# --- Helpers ombres ---

def _draw_default_shadows(surface, x, y, w, h, r, mult=1.0):
    """Ombres neumorphiques default."""
    alpha_dark = min(255, int(80 * mult))
    alpha_light = min(255, int(180 * mult))
    temp = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
    pygame.draw.rect(temp, (8, 77, 109, alpha_dark), (3, 3, w, h), border_radius=r)
    surface.blit(temp, (x - 2, y - 2))
    temp2 = pygame.Surface((w + 10, h + 10), pygame.SRCALPHA)
    pygame.draw.rect(temp2, (230, 242, 241, alpha_light), (0, 0, w, h), border_radius=r)
    surface.blit(temp2, (x - 3, y - 3))


def _draw_select_shadows(surface, x, y, w, h, r, mult=1.0):
    """Ombres neumorphiques select (plus prononcées)."""
    alpha_dark = min(255, int(60 * mult))
    alpha_light = min(255, int(140 * mult))
    temp = pygame.Surface((w + 30, h + 30), pygame.SRCALPHA)
    pygame.draw.rect(temp, (8, 77, 109, alpha_dark), (12, 12, w, h), border_radius=r)
    surface.blit(temp, (x - 4, y - 4))
    temp2 = pygame.Surface((w + 30, h + 30), pygame.SRCALPHA)
    pygame.draw.rect(temp2, (230, 242, 241, alpha_light), (0, 0, w, h), border_radius=r)
    surface.blit(temp2, (x - 8, y - 8))


def _draw_clic_shadows(surface, x, y, w, h, r, mult=1.0):
    """Ombres inversées pour effet clic."""
    alpha = min(255, int(40 * mult))
    temp = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(temp, (8, 77, 109, alpha), (0, 0, w, h), border_radius=r)
    surface.blit(temp, (x, y))

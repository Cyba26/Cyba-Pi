"""
CybOS Components — Bars
Big bar (dot slider), bar with icon, small progress bars.
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius
from src.core.renderer import draw_text, draw_rounded_rect


def draw_bar_big(surface, x, y, fill=5, state="default", width=266):
    """Barre horizontale avec 10 positions de dots + handle (266x32)."""
    h = 32
    num_dots = 10
    dot_radius = 5
    handle_radius = 10

    # Couleurs selon l'état
    if state == "select":
        track_bg = RED[50]
        dot_color = RED[200]
        handle_color = RED[400]
        track_fill = RED[300]
    else:
        track_bg = BLUE[50]
        dot_color = BLUE[200]
        handle_color = BLUE[500]
        track_fill = BLUE[300]

    # Track (fond)
    draw_rounded_rect(surface, (x, y, width, h), track_bg, radius=h // 2)

    # Remplissage jusqu'au handle
    if fill > 0:
        fill_w = max(h, int((width - 20) * fill / num_dots) + 10)
        draw_rounded_rect(surface, (x, y, fill_w, h), track_fill, radius=h // 2)

    # Dots
    margin = 14
    spacing = (width - margin * 2) / (num_dots - 1) if num_dots > 1 else 0

    for i in range(num_dots):
        dx = x + margin + int(i * spacing)
        dy = y + h // 2
        if i == fill:
            # Handle (plus grand)
            pygame.draw.circle(surface, handle_color, (dx, dy), handle_radius)
            # Highlight
            pygame.draw.circle(surface, (255, 255, 255, 60), (dx - 2, dy - 2), 4)
        else:
            pygame.draw.circle(surface, dot_color, (dx, dy), dot_radius)


def draw_bar_big_icon(surface, x, y, fill=5, state="default", typ="audio"):
    """Bar big avec icône à gauche (316x32)."""
    icon_size = 24
    icon_x = x
    bar_x = x + icon_size + 8

    # Icône
    icon_color = BLUE[500] if state != "disable" else BLUE[200]
    if state == "select":
        icon_color = RED[400]

    if typ == "audio":
        _draw_speaker_icon(surface, icon_x, y + 4, icon_color, muted=(state == "disable"))
    elif typ == "luminosity":
        _draw_sun_icon(surface, icon_x, y + 4, icon_color, off=(state == "disable"))

    # Bar
    if state == "disable":
        draw_bar_big(surface, bar_x, y, fill, "default", 266)
        # Overlay semi-transparent pour effet disable
        overlay = pygame.Surface((266, 32), pygame.SRCALPHA)
        overlay.fill((230, 242, 241, 140))
        surface.blit(overlay, (bar_x, y))
    else:
        draw_bar_big(surface, bar_x, y, fill, state, 266)


def draw_bar_small(surface, x, y, filled_pct=0.5, width=276, typ="simple"):
    """Barre de progression fine (276x8)."""
    h = 8

    # Fond
    draw_rounded_rect(surface, (x, y, width, h), BLUE[50], radius=h // 2)

    if typ == "simple":
        # Remplissage simple
        if filled_pct > 0:
            fw = max(h, int(width * filled_pct))
            draw_rounded_rect(surface, (x, y, fw, h), BLUE[500], radius=h // 2)

    elif typ == "double":
        # Deux tons : blue-500 puis blue-300
        if filled_pct > 0:
            fw = max(h, int(width * filled_pct))
            # Partie foncée (2/3 du fill)
            dark_w = max(h, int(fw * 0.6))
            draw_rounded_rect(surface, (x, y, fw, h), BLUE[300], radius=h // 2)
            draw_rounded_rect(surface, (x, y, dark_w, h), BLUE[500], radius=h // 2)


def draw_bar_specific(surface, x, y, start_pct=0.0, end_pct=1.0, width=276):
    """Barre avec segment highlight entre start% et end%."""
    h = 8

    # Fond
    draw_rounded_rect(surface, (x, y, width, h), BLUE[50], radius=h // 2)

    # Segment
    sx = x + int(width * start_pct)
    ew = int(width * (end_pct - start_pct))
    if ew > 0:
        # Partie foncée
        dark_end = sx + int(ew * 0.5)
        draw_rounded_rect(surface, (sx, y, ew, h), BLUE[300], radius=h // 2)
        draw_rounded_rect(surface, (sx, y, max(h, dark_end - sx), h), BLUE[500], radius=h // 2)


def draw_bar_info(surface, x, y, text_left, fill_pct, text_right="",
                   width=484, details_right=True):
    """Barre avec texte gauche + droite (484x24)."""
    h = 24
    bar_h = 8
    text_w = 80

    draw_text(surface, text_left, x, y + 2,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[500], bold=True)

    bar_x = x + text_w
    bar_w = width - text_w * 2 if details_right else width - text_w
    draw_bar_small(surface, bar_x, y + (h - bar_h) // 2, fill_pct, bar_w, "double")

    if details_right and text_right:
        draw_text(surface, text_right, x + width, y + 2,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[500], bold=True, anchor="topright")


# --- Icônes inline pour les barres ---

def _draw_speaker_icon(surface, x, y, color, muted=False):
    """Icône speaker simplifiée."""
    # Corps du speaker
    pygame.draw.rect(surface, color, (x + 4, y + 7, 6, 10))
    pygame.draw.polygon(surface, color, [(x + 10, y + 4), (x + 18, y + 0), (x + 18, y + 24), (x + 10, y + 20)])

    if not muted:
        # Ondes
        pygame.draw.arc(surface, color, (x + 16, y + 4, 8, 16), -1.0, 1.0, 2)
    else:
        # X pour muted
        pygame.draw.line(surface, RED[400], (x + 18, y + 6), (x + 24, y + 18), 2)
        pygame.draw.line(surface, RED[400], (x + 24, y + 6), (x + 18, y + 18), 2)


def _draw_sun_icon(surface, x, y, color, off=False):
    """Icône soleil simplifiée."""
    cx, cy = x + 12, y + 12
    # Cercle central
    pygame.draw.circle(surface, color, (cx, cy), 6, 2 if off else 0)

    if not off:
        # Rayons
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            sx = cx + int(9 * math.cos(rad))
            sy = cy + int(9 * math.sin(rad))
            ex = cx + int(12 * math.cos(rad))
            ey = cy + int(12 * math.sin(rad))
            pygame.draw.line(surface, color, (sx, sy), (ex, ey), 2)

"""
CybOS Components — Buttons
Icon buttons, text buttons (primary/secondary).
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius
from src.core.renderer import draw_text, draw_rounded_rect, draw_bloc


BUTTON_SIZES = {
    "small": {"icon": (40, 40), "text": (165, 48)},
    "medium": {"icon": (56, 56), "text": (227, 71)},
}


def draw_button_icon(surface, x, y, icon_name="arrow_r", size="small", state="default"):
    """Bouton icône rond/carré arrondi."""
    w, h = BUTTON_SIZES[size]["icon"]
    r = Radius.DEFAULT

    if state == "clic":
        _draw_pressed_bloc(surface, x, y, w, h, r)
    elif state == "select":
        draw_bloc(surface, (x, y, w, h), state="select")
    else:
        draw_bloc(surface, (x, y, w, h), state="default")

    icon_color = BLUE[500] if state != "select" else BLUE[600]
    cx, cy = x + w // 2, y + h // 2
    _draw_inline_icon(surface, cx, cy, icon_name, icon_color, size)


def draw_button_text(surface, x, y, text="Button", size="small", state="default", style="primary"):
    """Bouton texte avec chevrons < text >."""
    w, h = BUTTON_SIZES[size]["text"]
    r = Radius.DEFAULT
    font_size = Fonts.TEXT_SMALL if size == "small" else Fonts.TEXT_MEDIUM

    if style == "primary":
        text_color = BLUE[500]
    else:
        text_color = RED[400]

    if state == "clic":
        _draw_pressed_bloc(surface, x, y, w, h, r)
    elif state == "select":
        draw_bloc(surface, (x, y, w, h), state="select")
    else:
        draw_bloc(surface, (x, y, w, h), state="default")

    if state == "loading":
        draw_bloc(surface, (x, y, w, h), state="default")
        _draw_loader_spinner(surface, x + w // 2, y + h // 2, BLUE[300])
        return

    cx, cy = x + w // 2, y + h // 2
    draw_text(surface, f"<  {text}  >", cx, cy,
              Fonts.TEXT_FAMILY, font_size, text_color, bold=True, anchor="center")


def _draw_pressed_bloc(surface, x, y, w, h, r):
    """Bloc avec effet pressé (ombres inversées)."""
    draw_rounded_rect(surface, (x, y, w, h), Colors.BLOC_BG_LIGHT, radius=r)
    draw_rounded_rect(surface, (x, y, w, h), (0, 0, 0, 0), radius=r,
                       border=1, border_color=BLUE[100])
    inner = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(inner, (8, 77, 109, 30), (0, 0, w, h), border_radius=r)
    surface.blit(inner, (x, y))


def _draw_loader_spinner(surface, cx, cy, color, radius=10):
    """Spinner de chargement."""
    arc_rect = pygame.Rect(cx - radius, cy - radius, radius * 2, radius * 2)
    pygame.draw.arc(surface, color, arc_rect, 0, 4.2, 3)


def _draw_inline_icon(surface, cx, cy, name, color, size="small"):
    """Icône inline simple."""
    s = 8 if size == "small" else 12

    if name in ("arrow_r", "chevron_r"):
        pts = [(cx - s // 2, cy - s), (cx + s // 2, cy), (cx - s // 2, cy + s)]
        pygame.draw.lines(surface, color, False, pts, 2)
    elif name in ("arrow_l", "chevron_l"):
        pts = [(cx + s // 2, cy - s), (cx - s // 2, cy), (cx + s // 2, cy + s)]
        pygame.draw.lines(surface, color, False, pts, 2)
    elif name == "setting":
        pygame.draw.circle(surface, color, (cx, cy), s, 2)
        pygame.draw.circle(surface, color, (cx, cy), s // 2)
    elif name == "play":
        pts = [(cx - s // 2, cy - s), (cx + s, cy), (cx - s // 2, cy + s)]
        pygame.draw.polygon(surface, color, pts)
    elif name == "valid":
        pts = [(cx - s, cy), (cx - s // 3, cy + s // 2), (cx + s, cy - s // 2)]
        pygame.draw.lines(surface, color, False, pts, 2)
    elif name == "download":
        pygame.draw.line(surface, color, (cx, cy - s), (cx, cy + s // 2), 2)
        pts = [(cx - s // 2, cy), (cx, cy + s), (cx + s // 2, cy)]
        pygame.draw.lines(surface, color, False, pts, 2)
    else:
        pygame.draw.rect(surface, color, (cx - s // 2, cy - s // 2, s, s), 2)

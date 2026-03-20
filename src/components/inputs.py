"""
CybOS Components — Inputs
Text fields, sliders.
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius
from src.core.renderer import draw_text, draw_rounded_rect, draw_bloc


def draw_text_field(surface, x, y, label="Label", text="", state="default", navigation=False):
    """Champ de saisie texte (400x105)."""
    w, h = 400, 105
    r = Radius.DEFAULT

    # Fond
    if navigation:
        draw_bloc(surface, (x, y, w, h), state="select")
    else:
        draw_bloc(surface, (x, y, w, h), state="default")

    # Label
    draw_text(surface, label, x + 20, y + 16,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[300], bold=True)

    if state == "text_input" and text:
        # Texte saisi + curseur
        text_rect = draw_text(surface, text, x + 20, y + 50,
                               Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, BLUE[500], bold=True)
        # Curseur rouge
        cursor_x = text_rect.right + 2
        pygame.draw.line(surface, RED[400], (cursor_x, y + 48), (cursor_x, y + 82), 3)
    elif state == "text_input":
        # Juste le curseur
        pygame.draw.line(surface, RED[400], (x + 20, y + 48), (x + 20, y + 82), 3)


def draw_slider_component(surface, x, y, typ="all_select"):
    """Composant slider individuel (dot)."""
    if typ == "all_select":
        # Pill sélectionné (48x12)
        draw_rounded_rect(surface, (x, y, 48, 12), RED[400], radius=6)
    elif typ == "default_app":
        # Point app (12x12)
        pygame.draw.circle(surface, BLUE[500], (x + 6, y + 6), 6)
    elif typ == "default_setting":
        # Point setting (12x12)
        pygame.draw.circle(surface, BLUE[300], (x + 6, y + 6), 6)


def draw_slider(surface, x, y, amount=3, selected_index=0):
    """Slider composé : rangée de dots avec un sélectionné."""
    dot_size = 12
    selected_w = 48
    gap = 8

    cx = x
    for i in range(amount):
        if i == selected_index:
            draw_slider_component(surface, cx, y, "all_select")
            cx += selected_w + gap
        else:
            draw_slider_component(surface, cx, y, "default_app")
            cx += dot_size + gap

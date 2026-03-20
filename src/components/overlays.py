"""
CybOS Components — Overlays
Pop-ups, snackbars, scan blocs.
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius
from src.core.renderer import draw_text, draw_rounded_rect, draw_bloc, draw_progress_bar


def draw_popup(surface, x, y, title="Title", description="Description",
               button_texts=("Annuler", "Confirmer"), icon=None, progress=None):
    """Pop-up modal (550x~455)."""
    w = 550
    padding = 32
    content_y = y + padding

    # Calculer la hauteur
    h = padding  # top padding
    if icon:
        h += 40  # icon
    h += 48  # title
    if progress is not None:
        h += 24  # progress bar
    h += 30  # description
    h += 20  # gap
    h += 71  # buttons
    h += padding  # bottom padding

    # Fond du popup
    draw_bloc(surface, (x, y, w, h), state="default")

    cy = content_y

    # Icône optionnelle (checkmark)
    if icon == "valid":
        pygame.draw.circle(surface, BLUE[500], (x + padding + 14, cy + 14), 14)
        # Checkmark
        pts = [(x + padding + 6, cy + 14), (x + padding + 12, cy + 20), (x + padding + 22, cy + 8)]
        pygame.draw.lines(surface, (255, 255, 255), False, pts, 3)
        cy += 40

    # Titre
    draw_text(surface, title, x + padding, cy,
              Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, BLUE[500], bold=True)
    cy += 42

    # Barre de progression optionnelle
    if progress is not None:
        draw_progress_bar(surface, (x + padding, cy, w - padding * 2, 8), progress)
        cy += 24

    # Description
    draw_text(surface, description, x + padding, cy,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[500], bold=True)
    cy += 40

    # Boutons
    btn_w = (w - padding * 3) // 2
    btn_h = 56
    from src.components.buttons import draw_button_text
    if len(button_texts) >= 1:
        draw_button_text(surface, x + padding, cy, button_texts[0],
                         "small", "default", "secondary")
    if len(button_texts) >= 2:
        draw_button_text(surface, x + padding + btn_w + padding, cy, button_texts[1],
                         "small", "default", "primary")


def draw_snackbar(surface, x, y, text="Label", undo=True, fill_pct=0.4, width=420):
    """Toast notification (420x74)."""
    h = 74
    r = Radius.DEFAULT

    # Fond
    draw_bloc(surface, (x, y, width, h), state="default")

    # Texte
    draw_text(surface, text, x + 20, y + 12,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[500], bold=True)

    # Barre de progression
    bar_w = width - 40 if not undo else width // 2
    draw_progress_bar(surface, (x + 20, y + 40, bar_w, 8), fill_pct)

    # Undo
    if undo:
        draw_text(surface, "L+R to Undo", x + width - 20, y + 12,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, RED[400], bold=True, anchor="topright")


def draw_scan_bloc(surface, x, y, typ="scanning", text="Recherche en cours..."):
    """Zone de scan (338x193)."""
    w, h = 338, 193
    r = Radius.DEFAULT

    # Fond
    draw_bloc(surface, (x, y, w, h), state="default")

    cx = x + w // 2

    if typ == "scanning":
        # Loader
        arc_rect = pygame.Rect(cx - 15, y + 50, 30, 30)
        pygame.draw.arc(surface, BLUE[500], arc_rect, 0, 4.2, 3)
        # Texte
        draw_text(surface, text, cx, y + 110,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[500], bold=True, anchor="midtop")
    else:
        # No data
        draw_text(surface, "Aucune donnée", cx, y + h // 2,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[300], bold=True, anchor="center")

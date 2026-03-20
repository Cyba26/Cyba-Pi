"""
CybOS Components — Header
Status bar, title header, back button.
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius
from src.core.renderer import draw_text, draw_rounded_rect, draw_bloc


def draw_header(surface, x, y, width=800, state="default", time_str="12:34",
                wifi=True, bluetooth=True, battery_level=5):
    """Barre de statut en haut (width x 56)."""
    h = 56

    # Heure à gauche
    time_color = BLUE[500] if state == "default" else BLUE[200]
    draw_text(surface, time_str, x + 20, y + 16,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, time_color, bold=True)

    # Icônes à droite
    icon_x = x + width - 20
    icon_y = y + 16
    icon_color = BLUE[500] if state == "default" else BLUE[200]
    icon_off_color = BLUE[200] if state == "default" else BLUE[100]

    # Batterie
    icon_x -= 28
    _draw_battery_icon(surface, icon_x, icon_y, battery_level, icon_color)

    # Bluetooth
    icon_x -= 28
    bt_color = icon_color if bluetooth else icon_off_color
    _draw_bluetooth_icon(surface, icon_x, icon_y, bt_color, connected=bluetooth)

    # Wifi
    icon_x -= 28
    wifi_color = icon_color if wifi else icon_off_color
    _draw_wifi_icon(surface, icon_x, icon_y, wifi_color, connected=wifi)


def draw_title_header(surface, x, y, icon_name="setting", title="Title", back_text=""):
    """En-tête de page avec titre et bouton retour optionnel."""
    cx = x

    # Bouton retour
    if back_text:
        draw_back_button(surface, cx, y, back_text)
        cx += 160

    # Icône du titre
    _draw_page_icon(surface, cx, y + 8, icon_name, RED[400])
    cx += 40

    # Titre
    draw_text(surface, title, cx, y + 4,
              Fonts.TITLE_FAMILY, Fonts.TITLE_MD, RED[400])


def draw_back_button(surface, x, y, text="Accueil", state="default"):
    """Bouton de retour (< text)."""
    font = pygame.font.SysFont(Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, bold=True)
    tw = font.size(text)[0]
    w = tw + 48
    h = 40
    r = Radius.DEFAULT

    draw_bloc(surface, (x, y + 8, w, h), state="select" if state == "select" else "default")

    # Chevron <
    chevron_x = x + 16
    cy = y + 28
    pts = [(chevron_x + 6, cy - 6), (chevron_x, cy), (chevron_x + 6, cy + 6)]
    pygame.draw.lines(surface, BLUE[500], False, pts, 2)

    # Texte
    draw_text(surface, text, x + 28, y + 18,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[500], bold=True)


# --- Icônes du header ---

def _draw_wifi_icon(surface, x, y, color, connected=True):
    """Icône wifi."""
    cx = x + 12
    if connected:
        # 3 arcs
        for i, radius in enumerate([10, 7, 4]):
            rect = pygame.Rect(cx - radius, y + 12 - radius, radius * 2, radius * 2)
            pygame.draw.arc(surface, color, rect, 0.5, 2.6, 2)
        pygame.draw.circle(surface, color, (cx, y + 14), 2)
    else:
        # Barré
        for i, radius in enumerate([10, 7, 4]):
            rect = pygame.Rect(cx - radius, y + 12 - radius, radius * 2, radius * 2)
            pygame.draw.arc(surface, color, rect, 0.5, 2.6, 2)
        pygame.draw.circle(surface, color, (cx, y + 14), 2)
        pygame.draw.line(surface, color, (x + 2, y + 2), (x + 22, y + 22), 2)


def _draw_bluetooth_icon(surface, x, y, color, connected=True):
    """Icône bluetooth."""
    cx = x + 12
    cy = y + 12
    # Forme B simplifiée
    pts_top = [(cx - 4, cy - 8), (cx + 4, cy - 2), (cx - 4, cy + 2)]
    pts_bot = [(cx - 4, cy - 2), (cx + 4, cy + 4), (cx - 4, cy + 10)]
    pygame.draw.lines(surface, color, False, pts_top, 2)
    pygame.draw.lines(surface, color, False, pts_bot, 2)
    pygame.draw.line(surface, color, (cx, cy - 10), (cx, cy + 12), 2)

    if not connected:
        pygame.draw.line(surface, color, (x + 2, y + 2), (x + 22, y + 22), 2)


def _draw_battery_icon(surface, x, y, level=5, color=None):
    """Icône batterie (7 niveaux)."""
    if color is None:
        color = BLUE[500]
    w, h = 22, 12
    # Contour
    pygame.draw.rect(surface, color, (x, y + 4, w, h), 1, border_radius=2)
    # Borne
    pygame.draw.rect(surface, color, (x + w, y + 7, 3, 6))
    # Remplissage
    fill_w = max(0, int((w - 4) * level / 7))
    if fill_w > 0:
        pygame.draw.rect(surface, color, (x + 2, y + 6, fill_w, h - 4), border_radius=1)


def _draw_page_icon(surface, x, y, name, color):
    """Icône de page pour le title header."""
    s = 16
    cx, cy = x + s, y + s

    if name == "setting":
        # Engrenage
        pygame.draw.circle(surface, color, (cx, cy), s, 3)
        pygame.draw.circle(surface, color, (cx, cy), s // 2)
        # Dents
        import math
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            dx = cx + int((s + 2) * math.cos(rad))
            dy = cy + int((s + 2) * math.sin(rad))
            pygame.draw.circle(surface, color, (dx, dy), 4)
    elif name == "bluetooth":
        _draw_bluetooth_icon(surface, x, y, color)
    elif name == "wifi":
        _draw_wifi_icon(surface, x, y, color)
    elif name == "system":
        pygame.draw.circle(surface, color, (cx, cy), s, 3)
        pygame.draw.circle(surface, color, (cx, cy), s // 2)
    elif name == "download":
        pygame.draw.line(surface, color, (cx, cy - s), (cx, cy + s // 2), 3)
        pts = [(cx - s // 2, cy), (cx, cy + s), (cx + s // 2, cy)]
        pygame.draw.polygon(surface, color, pts)
    else:
        pygame.draw.circle(surface, color, (cx, cy), s, 2)

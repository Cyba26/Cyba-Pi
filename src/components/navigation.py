"""
CybOS Components — Navigation
Select cursor, menu selection, title menu, line state, line navigation.
"""

import pygame
from src.core.tokens import BLUE, RED, Colors, Fonts, Spacing, Radius
from src.core.renderer import draw_text, draw_rounded_rect, get_font


def draw_select_cursor(surface, x, y, state="default", navigation="select"):
    """Petit indicateur vertical de sélection (16x34)."""
    w, h = 16, 34

    if navigation == "area_select":
        # Petit point bleu
        pygame.draw.circle(surface, BLUE[300], (x + w // 2, y + h // 2), 5)
        return

    if state == "selected" and navigation == "select":
        # Pill plein rouge
        draw_rounded_rect(surface, (x, y, w, h), RED[400], radius=w // 2)
    elif state == "selected" and navigation == "no_select":
        # Pill plein bleu
        draw_rounded_rect(surface, (x, y, w, h), BLUE[500], radius=w // 2)
    elif state == "default" and navigation == "select":
        # Pill outline bleu
        draw_rounded_rect(surface, (x, y, w, h), BLUE[50], radius=w // 2,
                           border=2, border_color=BLUE[300])
    else:
        # default + no_select: petit point
        pygame.draw.circle(surface, BLUE[300], (x + w // 2, y + h // 2), 4)


def draw_menu_selection(surface, x, y, text, state="default", navigation="select"):
    """Item de menu avec texte (largeur ~91px)."""
    cursor_w = 16
    text_x = x

    if state == "selected":
        if navigation == "select":
            draw_select_cursor(surface, x, y, "selected", "select")
            text_color = RED[400]
        else:
            draw_select_cursor(surface, x, y, "selected", "no_select")
            text_color = BLUE[500]
        text_x = x + cursor_w + 4
    else:
        if navigation == "select":
            # Petit point
            pygame.draw.circle(surface, BLUE[300], (x + 6, y + 17), 4)
            text_color = BLUE[500]
        else:
            pygame.draw.circle(surface, BLUE[200], (x + 6, y + 17), 3)
            text_color = BLUE[300]
        text_x = x + cursor_w + 4

    draw_text(surface, text, text_x, y + 2,
              Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, text_color, bold=True)


def draw_title_menu(surface, x, y, text, state="default"):
    """Titre de section de menu."""
    if state == "select":
        draw_select_cursor(surface, x, y, "selected", "select")
        draw_text(surface, text, x + 20, y + 2,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, BLUE[500], bold=True)
    else:
        draw_text(surface, text, x, y + 2,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, BLUE[500], bold=True)


def draw_line_state(surface, x, y, status="none"):
    """Indicateur de statut (loading, valid, error, none)."""
    if status == "valid":
        # Cercle bleu avec checkmark
        pygame.draw.circle(surface, BLUE[500], (x + 12, y + 12), 10)
        # Checkmark simplifié
        pts = [(x + 7, y + 12), (x + 11, y + 16), (x + 17, y + 8)]
        pygame.draw.lines(surface, (255, 255, 255), False, pts, 2)
    elif status == "error":
        # Cercle rouge avec X
        pygame.draw.circle(surface, RED[400], (x + 12, y + 12), 10)
        pygame.draw.line(surface, (255, 255, 255), (x + 8, y + 8), (x + 16, y + 16), 2)
        pygame.draw.line(surface, (255, 255, 255), (x + 16, y + 8), (x + 8, y + 16), 2)
    elif status == "loading":
        # Arc de cercle (loader simplifié)
        rect = pygame.Rect(x + 2, y + 2, 20, 20)
        pygame.draw.arc(surface, BLUE[500], rect, 0, 4.5, 2)
    else:
        # None : petit texte
        draw_text(surface, "-", x + 8, y + 2,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[200], bold=True)


def draw_line_navigation(surface, x, y, width, typ="1_text", state="default",
                          state_info=True, text1="Text", text2="Text", status="valid"):
    """Ligne de navigation complète (width x 39px)."""
    h = 39
    text_x = x
    right_x = x + width

    # Curseur de sélection à gauche
    if state == "selected":
        draw_select_cursor(surface, x, y + 2, "selected", "select")
        text1_color = BLUE[500]
        text_x = x + 20
    else:
        text1_color = BLUE[500]
        text_x = x

    if typ == "1_text":
        draw_text(surface, text1, text_x, y + 4,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, text1_color, bold=True)
        if state_info and text2:
            draw_text(surface, text2, text_x + 160, y + 10,
                      Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[300], bold=True)
            draw_line_state(surface, right_x - 30, y + 8, status)

    elif typ == "2_text":
        draw_text(surface, text1, text_x, y + 4,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, text1_color, bold=True)
        if state_info:
            # Texte d'action à droite en rouge
            action_color = RED[400] if state == "selected" else BLUE[300]
            draw_text(surface, text2, right_x - 10, y + 4,
                      Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, action_color, bold=True, anchor="topright")

    elif typ == "button":
        draw_text(surface, text1, text_x, y + 4,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, text1_color, bold=True)
        # Icônes bouton à droite
        from src.components.buttons import draw_button_icon
        btn_state = "select" if state == "selected" else "default"
        draw_button_icon(surface, right_x - 80, y, "setting", "small", "default")
        draw_button_icon(surface, right_x - 36, y, "arrow_r", "small", btn_state)

    elif typ == "bar":
        draw_text(surface, text1, text_x, y + 4,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, text1_color, bold=True)
        from src.components.bars import draw_bar_big_icon
        bar_state = "select" if state == "selected" else "default"
        draw_bar_big_icon(surface, text_x + 160, y + 4, 4, bar_state, "audio")

    elif typ == "loading":
        draw_text(surface, text1, text_x, y + 4,
                  Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, text1_color, bold=True)
        if state_info:
            draw_text(surface, text2, text_x + 160, y + 10,
                      Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, BLUE[300], bold=True)
        # Loader à droite
        draw_line_state(surface, right_x - 30, y + 8, "loading")


def draw_line_navigation_choice(surface, x, y, texts, selected_index=0):
    """Ligne de choix horizontal (ex: Amount=1 ou Amount=2)."""
    gap = 24
    cx = x
    for i, text in enumerate(texts):
        if i == selected_index:
            draw_menu_selection(surface, cx, y, text, "selected", "select")
        else:
            draw_menu_selection(surface, cx, y, text, "default", "select")
        font = get_font(Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, bold=True)
        tw = font.size(text)[0]
        cx += 20 + tw + gap

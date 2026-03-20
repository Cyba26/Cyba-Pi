"""
CybOS Styleguide — Page complète de démonstration du Design System.
Navigation : flèches haut/bas pour scroller, Escape pour quitter.
"""

import pygame
from src.core.tokens import (
    BLUE, RED, Colors, Fonts, Spacing, Radius, Screen, Gradients,
)
from src.core.renderer import (
    draw_text, draw_rounded_rect, draw_bloc, draw_progress_bar,
    draw_gradient_vertical, get_font, load_svg,
)
from src.components.navigation import (
    draw_select_cursor, draw_menu_selection, draw_title_menu,
    draw_line_state, draw_line_navigation, draw_line_navigation_choice,
)
from src.components.bars import (
    draw_bar_big, draw_bar_big_icon, draw_bar_small, draw_bar_specific, draw_bar_info,
)
from src.components.buttons import draw_button_icon, draw_button_text
from src.components.inputs import draw_text_field, draw_slider, draw_slider_component
from src.components.overlays import draw_popup, draw_snackbar, draw_scan_bloc
from src.components.blocks import draw_bloc_style, draw_app_bloc, draw_quickaction_bar
from src.components.header import draw_header, draw_title_header, draw_back_button


SECTION_GAP = 48
LABEL_COLOR = BLUE[600]
SUBLABEL_COLOR = BLUE[400]
BG_COLOR = BLUE[50]
M = Spacing.SP_32  # Marge


def run_styleguide():
    pygame.init()
    screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
    pygame.display.set_caption("CybOS — Styleguide")
    clock = pygame.time.Clock()

    content_height = 6000
    content = pygame.Surface((Screen.WIDTH, content_height), pygame.SRCALPHA)
    scroll_y = 0
    scroll_speed = 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_y = min(scroll_y + scroll_speed, max(0, content_height - Screen.HEIGHT))
                elif event.key == pygame.K_UP:
                    scroll_y = max(scroll_y - scroll_speed, 0)
                elif event.key == pygame.K_PAGEDOWN:
                    scroll_y = min(scroll_y + Screen.HEIGHT, max(0, content_height - Screen.HEIGHT))
                elif event.key == pygame.K_PAGEUP:
                    scroll_y = max(scroll_y - Screen.HEIGHT, 0)

        content.fill(BG_COLOR)
        y = _draw_all_sections(content)

        if y + 100 != content_height:
            content_height = y + 100
            content = pygame.Surface((Screen.WIDTH, content_height), pygame.SRCALPHA)
            continue

        screen.blit(content, (0, -scroll_y))

        # Scrollbar
        max_scroll = max(1, content_height - Screen.HEIGHT)
        if max_scroll > 0:
            bar_h = max(20, int(Screen.HEIGHT * Screen.HEIGHT / content_height))
            bar_y = int(scroll_y / max_scroll * (Screen.HEIGHT - bar_h))
            pygame.draw.rect(screen, BLUE[300], (Screen.WIDTH - 6, bar_y, 4, bar_h), border_radius=2)

        pygame.display.flip()
        clock.tick(Screen.FPS)

    pygame.quit()


def _section(surface, y, title):
    y += SECTION_GAP
    draw_text(surface, title, M, y, Fonts.TITLE_FAMILY, Fonts.TITLE_MD, Colors.TITLE_PRIMARY)
    y += Fonts.TITLE_MD + 12
    pygame.draw.line(surface, BLUE[200], (M, y), (Screen.WIDTH - M, y), 1)
    y += Spacing.SP_16
    return y


def _label(surface, y, text):
    draw_text(surface, text, M, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, SUBLABEL_COLOR, bold=True)
    return y + Fonts.TEXT_SMALL + Spacing.SP_8


def _draw_all_sections(surface):
    y = M

    # ============================================================
    # 1. COULEURS PRIMITIVES
    # ============================================================
    y = _section(surface, y, "Couleurs primitives")

    y = _label(surface, y, "Blue")
    swatch, gap = 56, 8
    for i, (shade, color) in enumerate(sorted(BLUE.items())):
        x = M + i * (swatch + gap)
        draw_rounded_rect(surface, (x, y, swatch, swatch), color, radius=8)
        draw_text(surface, str(shade), x + swatch // 2, y + swatch + 4,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="midtop")
    y += swatch + 28

    y = _label(surface, y, "Red")
    for i, (shade, color) in enumerate(sorted(RED.items())):
        x = M + i * (swatch + gap)
        draw_rounded_rect(surface, (x, y, swatch, swatch), color, radius=8)
        draw_text(surface, str(shade), x + swatch // 2, y + swatch + 4,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="midtop")
    y += swatch + 28

    # ============================================================
    # 2. COULEURS SEMANTIQUES (par catégorie)
    # ============================================================
    y = _section(surface, y, "Couleurs sémantiques")

    categories = [
        ("Texte", [
            ("title-primary", Colors.TITLE_PRIMARY),
            ("title-secondary", Colors.TITLE_SECONDARY),
            ("text-primary", Colors.TEXT_PRIMARY),
            ("text-secondary", Colors.TEXT_SECONDARY),
            ("text-primary-disable", Colors.TEXT_PRIMARY_DISABLE),
            ("text-secondary-disable", Colors.TEXT_SECONDARY_DISABLE),
        ]),
        ("Actions / Inputs", [
            ("action-primary", Colors.ACTION_PRIMARY),
            ("action-secondary", Colors.ACTION_SECONDARY),
            ("action-primary-disable", Colors.ACTION_PRIMARY_DISABLE),
        ]),
        ("Icônes", [
            ("icon-primary", Colors.ICON_PRIMARY),
            ("icon-secondary", Colors.ICON_SECONDARY),
            ("icon-secondary-dark", Colors.ICON_SECONDARY_DARK),
            ("icon-secondary-light", Colors.ICON_SECONDARY_LIGHT),
        ]),
        ("Blocs & Barres", [
            ("bloc-stroke", Colors.BLOC_STROKE),
            ("bar-light", Colors.BAR_LIGHT),
            ("bar-medium", Colors.BAR_MEDIUM),
            ("bar-background", Colors.BAR_BACKGROUND),
        ]),
    ]

    for cat_name, items in categories:
        y = _label(surface, y, cat_name)
        for i, (name, color) in enumerate(items):
            x = M + (i % 4) * 180
            row_y = y + (i // 4) * 48
            rgb = color[:3]
            draw_rounded_rect(surface, (x, row_y, 32, 32), rgb, radius=6)
            draw_text(surface, name, x + 40, row_y + 8,
                      Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        rows = (len(items) + 3) // 4
        y += rows * 48 + 8

    # ============================================================
    # 3. TYPOGRAPHIE
    # ============================================================
    y = _section(surface, y, "Typographie")

    draw_text(surface, "Title XL", M, y, Fonts.TITLE_FAMILY, 56, Colors.TITLE_PRIMARY)
    y += 64
    draw_text(surface, "Title MD (48px)", M, y, Fonts.TITLE_FAMILY, Fonts.TITLE_MD, Colors.TITLE_PRIMARY)
    y += 56
    draw_text(surface, "Title MD Secondary", M, y, Fonts.TITLE_FAMILY, Fonts.TITLE_MD, Colors.TITLE_SECONDARY)
    y += 56
    draw_text(surface, "Text Medium (32px)", M, y, Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_PRIMARY, bold=True)
    y += 40
    draw_text(surface, "Text Medium Italic", M, y, Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_PRIMARY, bold=True, italic=True)
    y += 40
    draw_text(surface, "Text Small (20px)", M, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY, bold=True)
    y += 28

    y = _label(surface, y, "Couleurs texte")
    draw_text(surface, "Primary", M, y, Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_PRIMARY, bold=True)
    draw_text(surface, "Secondary", M + 180, y, Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_SECONDARY, bold=True)
    draw_text(surface, "Disable", M + 380, y, Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_PRIMARY_DISABLE, bold=True)
    y += 40
    draw_text(surface, "Primary", M, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY, bold=True)
    draw_text(surface, "Secondary", M + 180, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_SECONDARY, bold=True)
    draw_text(surface, "Disable", M + 380, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY_DISABLE, bold=True)
    draw_text(surface, "Disable", M + 540, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_SECONDARY_DISABLE, bold=True)
    y += 32

    # ============================================================
    # 4. SPACINGS
    # ============================================================
    y = _section(surface, y, "Spacings")
    for name, val in [("sp-8", 8), ("sp-12", 12), ("sp-16", 16), ("sp-20", 20), ("sp-32", 32), ("sp-48", 48)]:
        draw_text(surface, f"{name} ({val}px)", M, y + 2, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        draw_rounded_rect(surface, (200, y, val * 4, 18), BLUE[300], radius=4)
        y += 26

    # ============================================================
    # 5. BORDER RADIUS
    # ============================================================
    y = _section(surface, y, "Border radius")
    draw_rounded_rect(surface, (M, y, 120, 80), BLUE[200], radius=Radius.DEFAULT, border=2, border_color=BLUE[500])
    draw_text(surface, "12px", M + 60, y + 40, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="center")
    draw_rounded_rect(surface, (M + 160, y, 80, 80), BLUE[200], radius=Radius.FULL, border=2, border_color=BLUE[500])
    draw_text(surface, "full", M + 200, y + 40, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="center")
    y += 100

    # ============================================================
    # 6. GRADIENTS
    # ============================================================
    y = _section(surface, y, "Gradients")
    for i, (name, (c1, c2)) in enumerate([("Typography", Gradients.TYPOGRAPHY), ("Action", Gradients.ACTION), ("Background", Gradients.BACKGROUND)]):
        gx = M + i * 240
        draw_text(surface, name, gx, y, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        draw_gradient_vertical(surface, (gx, y + 20, 200, 40), c1, c2)
    y += 80

    # ============================================================
    # 7. HEADER
    # ============================================================
    y = _section(surface, y, "Header")
    y = _label(surface, y, "Default")
    draw_header(surface, M, y, 736, "default", "12:34", True, True, 5)
    y += 60
    y = _label(surface, y, "Disable")
    draw_header(surface, M, y, 736, "disable", "12:34", False, False, 2)
    y += 60

    # ============================================================
    # 8. TITLE HEADER
    # ============================================================
    y = _section(surface, y, "Title header")
    draw_title_header(surface, M, y, "setting", "Paramètres", "Accueil")
    y += 70
    draw_title_header(surface, M, y, "bluetooth", "Bluetooth", "Système")
    y += 70

    # ============================================================
    # 9. SELECT CURSOR
    # ============================================================
    y = _section(surface, y, "Select cursor")
    cursors = [
        ("Selected + Select", "selected", "select"),
        ("Default + Select", "default", "select"),
        ("Selected + No sel.", "selected", "no_select"),
        ("Default + No sel.", "default", "no_select"),
        ("Area select", "default", "area_select"),
    ]
    for i, (label, state, nav) in enumerate(cursors):
        cx = M + i * 140
        draw_select_cursor(surface, cx, y, state, nav)
        draw_text(surface, label, cx, y + 40, Fonts.TEXT_FAMILY, 12, LABEL_COLOR, bold=True)
    y += 64

    # ============================================================
    # 10. MENU SELECTION
    # ============================================================
    y = _section(surface, y, "Menu selection")
    selections = [
        ("Selected + Select", "selected", "select"),
        ("Default + Select", "default", "select"),
        ("Selected + No sel.", "selected", "no_select"),
        ("Default + No sel.", "default", "no_select"),
    ]
    for i, (label, state, nav) in enumerate(selections):
        cx = M + (i % 2) * 360
        cy = y + (i // 2) * 48
        draw_menu_selection(surface, cx, cy, "Text", state, nav)
    y += 100

    # ============================================================
    # 11. TITLE MENU
    # ============================================================
    y = _section(surface, y, "Title menu")
    draw_title_menu(surface, M, y, "Text", "select")
    draw_title_menu(surface, M + 200, y, "Text", "default")
    y += 48

    # ============================================================
    # 12. LINE STATE
    # ============================================================
    y = _section(surface, y, "Line state")
    for i, (label, status) in enumerate([("Loading", "loading"), ("Valid", "valid"), ("Error", "error"), ("None", "none")]):
        cx = M + i * 120
        draw_line_state(surface, cx, y, status)
        draw_text(surface, label, cx, y + 30, Fonts.TEXT_FAMILY, 12, LABEL_COLOR, bold=True)
    y += 56

    # ============================================================
    # 13. LINE NAVIGATION
    # ============================================================
    y = _section(surface, y, "Line navigation")

    y = _label(surface, y, "1 text — Selected + State info")
    draw_line_navigation(surface, M, y, 454, "1_text", "selected", True, "Text", "Text", "valid")
    y += 48
    y = _label(surface, y, "1 text — Default + State info")
    draw_line_navigation(surface, M, y, 454, "1_text", "default", True, "Text", "Text", "valid")
    y += 48
    y = _label(surface, y, "1 text — Selected, no state info")
    draw_line_navigation(surface, M, y, 454, "1_text", "selected", False, "Text")
    y += 48
    y = _label(surface, y, "2 text — Selected")
    draw_line_navigation(surface, M, y, 454, "2_text", "selected", True, "Text", "Text")
    y += 48
    y = _label(surface, y, "2 text — Default")
    draw_line_navigation(surface, M, y, 454, "2_text", "default", True, "Text", "Text")
    y += 48
    y = _label(surface, y, "Button — Selected")
    draw_line_navigation(surface, M, y, 454, "button", "selected", True, "Text")
    y += 48
    y = _label(surface, y, "Button — Default")
    draw_line_navigation(surface, M, y, 454, "button", "default", True, "Text")
    y += 48
    y = _label(surface, y, "Bar — Selected")
    draw_line_navigation(surface, M, y, 454, "bar", "selected", False, "Text")
    y += 48
    y = _label(surface, y, "Loading — Selected")
    draw_line_navigation(surface, M, y, 454, "loading", "selected", True, "Text", "Text")
    y += 48
    y = _label(surface, y, "Loading — Default")
    draw_line_navigation(surface, M, y, 454, "loading", "default", True, "Text", "Text")
    y += 48

    # ============================================================
    # 14. BAR BIG (dot slider)
    # ============================================================
    y = _section(surface, y, "Bar - Big")
    y = _label(surface, y, "Default (blue)")
    for fill in range(0, 11, 2):
        draw_bar_big(surface, M, y, fill, "default")
        draw_text(surface, f"Fill {fill}", M + 280, y + 6, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        y += 40
    y = _label(surface, y, "Select (red)")
    for fill in [0, 5, 10]:
        draw_bar_big(surface, M, y, fill, "select")
        draw_text(surface, f"Fill {fill}", M + 280, y + 6, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        y += 40

    # ============================================================
    # 15. BAR BIG + ICON
    # ============================================================
    y = _section(surface, y, "Bar - Big + Icon")
    for typ in ["audio", "luminosity"]:
        y = _label(surface, y, typ.capitalize())
        for state in ["default", "select", "disable"]:
            draw_bar_big_icon(surface, M, y, 4, state, typ)
            draw_text(surface, state, M + 330, y + 6, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
            y += 40

    # ============================================================
    # 16. BAR SMALL
    # ============================================================
    y = _section(surface, y, "Bar - Small")
    y = _label(surface, y, "Simple")
    for pct in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        draw_bar_small(surface, M, y, pct, 276, "simple")
        draw_text(surface, f"{int(pct*100)}%", M + 290, y - 2, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        y += 18
    y += 8
    y = _label(surface, y, "Double")
    for pct in [0.2, 0.6, 1.0]:
        draw_bar_small(surface, M, y, pct, 276, "double")
        y += 18
    y += 8
    y = _label(surface, y, "Specific indication")
    for start, end in [(0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 1.0)]:
        draw_bar_specific(surface, M, y, start, end, 276)
        draw_text(surface, f"{int(start*100)}%-{int(end*100)}%", M + 290, y - 2, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        y += 18
    y += 8
    y = _label(surface, y, "Bar + information")
    draw_bar_info(surface, M, y, "System", 0.4, "20% / 16go", 500)
    y += 32
    draw_bar_info(surface, M, y, "Apps", 0.6, "40% / 32go", 500)
    y += 32

    # ============================================================
    # 17. BLOC STYLE
    # ============================================================
    y = _section(surface, y, "Bloc style")
    y = _label(surface, y, "Default + Stroke")
    for i, (state_label, state) in enumerate([("Default", "default"), ("Select", "select"), ("Clic", "clic")]):
        for j, contrast in enumerate(["light", "medium", "heavy"]):
            bx = M + (i * 3 + j) * 86
            if bx + 80 > Screen.WIDTH:
                continue
            draw_bloc_style(surface, bx, y, 76, state, "default", contrast, True)
        draw_text(surface, state_label, M + i * 258, y + 82, Fonts.TEXT_FAMILY, 12, LABEL_COLOR, bold=True)
    y += 104

    y = _label(surface, y, "Light + Stroke")
    for i, state in enumerate(["default", "select", "clic"]):
        for j, contrast in enumerate(["light", "medium", "heavy"]):
            bx = M + (i * 3 + j) * 86
            if bx + 80 > Screen.WIDTH:
                continue
            draw_bloc_style(surface, bx, y, 76, state, "light", contrast, True)
    y += 100

    y = _label(surface, y, "Light + No stroke")
    for i, state in enumerate(["default", "select", "clic"]):
        for j, contrast in enumerate(["light", "medium", "heavy"]):
            bx = M + (i * 3 + j) * 86
            if bx + 80 > Screen.WIDTH:
                continue
            draw_bloc_style(surface, bx, y, 76, state, "light", contrast, False)
    y += 100

    # ============================================================
    # 18. BUTTONS
    # ============================================================
    y = _section(surface, y, "Boutons")

    y = _label(surface, y, "Icon — Small")
    for i, state in enumerate(["default", "select", "clic"]):
        draw_button_icon(surface, M + i * 56, y, "arrow_r", "small", state)
    y += 52

    y = _label(surface, y, "Icon — Medium")
    for i, state in enumerate(["default", "select", "clic"]):
        draw_button_icon(surface, M + i * 72, y, "arrow_r", "medium", state)
    y += 72

    y = _label(surface, y, "Text Primary — Small")
    for i, state in enumerate(["default", "select", "clic", "loading"]):
        draw_button_text(surface, M + i * 178, y, "Button", "small", state, "primary")
    y += 60

    y = _label(surface, y, "Text Primary — Medium")
    for i, state in enumerate(["default", "select", "clic"]):
        draw_button_text(surface, M + i * 244, y, "Button", "medium", state, "primary")
    y += 84

    y = _label(surface, y, "Text Secondary — Small")
    for i, state in enumerate(["default", "select", "clic", "loading"]):
        draw_button_text(surface, M + i * 178, y, "Button", "small", state, "secondary")
    y += 60

    y = _label(surface, y, "Text Secondary — Medium")
    for i, state in enumerate(["default", "select", "clic"]):
        draw_button_text(surface, M + i * 244, y, "Button", "medium", state, "secondary")
    y += 84

    # ============================================================
    # 19. TEXT FIELD
    # ============================================================
    y = _section(surface, y, "Text field")
    y = _label(surface, y, "Default — no navigation")
    draw_text_field(surface, M, y, "Label", "", "default", False)
    y += 116
    y = _label(surface, y, "Text input — no navigation")
    draw_text_field(surface, M, y, "Label", "Text", "text_input", False)
    y += 116
    y = _label(surface, y, "Default — navigation")
    draw_text_field(surface, M, y, "Label", "", "default", True)
    y += 116
    y = _label(surface, y, "Text input — navigation")
    draw_text_field(surface, M, y, "Label", "Text", "text_input", True)
    y += 116

    # ============================================================
    # 20. SLIDER
    # ============================================================
    y = _section(surface, y, "Slider")
    y = _label(surface, y, "Composants")
    draw_slider_component(surface, M, y, "all_select")
    draw_slider_component(surface, M + 60, y, "default_app")
    draw_slider_component(surface, M + 80, y, "default_setting")
    y += 24

    y = _label(surface, y, "Composé")
    for amount in [2, 3, 4, 5, 6, 7]:
        draw_slider(surface, M, y, amount, 0)
        draw_text(surface, f"Amount={amount}", M + 200, y, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        y += 22

    # ============================================================
    # 21. POP-UP
    # ============================================================
    y = _section(surface, y, "Pop-up")
    y = _label(surface, y, "Default")
    draw_popup(surface, M, y, "Éteindre le système",
               "Vous êtes sur le point d'éteindre le système, continuer ?",
               ("Annuler", "Éteindre"))
    y += 300

    y = _label(surface, y, "Avec icône + progression")
    draw_popup(surface, M, y, "Téléchargement en cours",
               "Estimation : 2 minutes",
               ("Annuler",), icon="valid", progress=0.4)
    y += 320

    # ============================================================
    # 22. SNACKBAR
    # ============================================================
    y = _section(surface, y, "Snackbar")
    y = _label(surface, y, "Avec undo")
    draw_snackbar(surface, M, y, "Suppression effectuée", undo=True)
    y += 88
    y = _label(surface, y, "Sans undo")
    draw_snackbar(surface, M, y, "Action effectuée", undo=False)
    y += 88

    # ============================================================
    # 23. SCAN BLOC
    # ============================================================
    y = _section(surface, y, "Scan bloc")
    draw_scan_bloc(surface, M, y, "scanning", "Recherche en cours...")
    draw_scan_bloc(surface, M + 360, y, "no_data")
    y += 210

    # ============================================================
    # 24. APP BLOC
    # ============================================================
    y = _section(surface, y, "Application bloc")
    app_icon = load_svg("apps/cybulateur-red-large.png", (120, 120))

    y = _label(surface, y, "Default / Select / Clic")
    draw_app_bloc(surface, M, y, app_icon, "Cybulateur", "default")
    draw_app_bloc(surface, M + 200, y, app_icon, "Cybulateur", "select")
    draw_app_bloc(surface, M + 480, y, app_icon, "Cybulateur", "clic")
    y += 270

    y = _label(surface, y, "Moving / Loading")
    draw_app_bloc(surface, M, y, app_icon, "Cybulateur", "select", moving=True)
    draw_app_bloc(surface, M + 250, y, app_icon, "Cybulateur", "default", moving=True)
    draw_app_bloc(surface, M + 400, y, app_icon, "Cybulateur", "loading")
    y += 280

    # ============================================================
    # 25. QUICKACTION BAR
    # ============================================================
    y = _section(surface, y, "Quickaction bar")
    draw_quickaction_bar(surface, M, y, "audio", on_screen=False)
    draw_quickaction_bar(surface, M + 50, y, "light", on_screen=False)
    draw_quickaction_bar(surface, M + 120, y, "audio", on_screen=True)
    y += 340

    # ============================================================
    # 26. ICÔNES
    # ============================================================
    y = _section(surface, y, "Icônes")

    icon_names = [
        "wifi", "bluetooth", "system", "setting", "arrow-l", "arrow-r",
        "audio", "audio-off", "light", "light-off", "valid", "error",
        "download", "play", "move", "loader",
    ]

    y = _label(surface, y, "Blue — Primary")
    icon_size = 32
    for i, name in enumerate(icon_names):
        ix = M + i * (icon_size + 12)
        if ix + icon_size > Screen.WIDTH - M:
            break
        icon = load_svg(f"icons/{name}-blue-primary.png", (icon_size, icon_size))
        surface.blit(icon, (ix, y))
    y += icon_size + 16

    y = _label(surface, y, "Red — Secondary")
    for i, name in enumerate(icon_names[:12]):
        ix = M + i * (icon_size + 12)
        icon = load_svg(f"icons/{name}-red-secondary.png", (icon_size, icon_size))
        surface.blit(icon, (ix, y))
    y += icon_size + 16

    y = _label(surface, y, "Blue — Disable")
    for i, name in enumerate(icon_names[:12]):
        ix = M + i * (icon_size + 12)
        icon = load_svg(f"icons/{name}-blue-disable.png", (icon_size, icon_size))
        surface.blit(icon, (ix, y))
    y += icon_size + 16

    # Battery levels
    y = _label(surface, y, "Battery (1-7)")
    for i in range(1, 8):
        ix = M + (i - 1) * (icon_size + 12)
        icon = load_svg(f"icons/battery-{i}-blue-primary.png", (icon_size, icon_size))
        surface.blit(icon, (ix, y))
    y += icon_size + 16

    # ============================================================
    # 27. LOADERS
    # ============================================================
    y = _label(surface, y, "Loaders")
    for i in range(1, 4):
        for j, (sz_name, sz) in enumerate([("default", 32), ("large", 56)]):
            for k, color in enumerate(["blue", "red"]):
                lx = M + ((i - 1) * 4 + j * 2 + k) * 68
                loader = load_svg(f"loaders/loader-{i}-{sz_name}-{color}.png", (sz, sz))
                surface.blit(loader, (lx, y))
    y += 72

    # ============================================================
    # 28. APP ILLUSTRATIONS
    # ============================================================
    y = _label(surface, y, "App illustrations")
    apps = ["cybulateur", "hue", "setting"]
    for i, app in enumerate(apps):
        for j, color in enumerate(["red", "blue"]):
            ax = M + (i * 2 + j) * 100
            icon = load_svg(f"apps/{app}-{color}-large.png", (80, 80))
            surface.blit(icon, (ax, y))
    y += 100

    return y


if __name__ == "__main__":
    run_styleguide()

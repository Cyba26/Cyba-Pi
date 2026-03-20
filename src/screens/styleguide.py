"""
CybOS Styleguide
Page de démonstration visuelle de tous les tokens et composants du DS.
Navigation verticale avec flèches haut/bas pour scroller.
"""

import pygame
from src.core.tokens import (
    BLUE, RED, Colors, Fonts, Spacing, Radius, Screen,
    Gradients, Animations,
)
from src.core.renderer import (
    draw_text, draw_rounded_rect, draw_bloc, draw_progress_bar,
    draw_gradient_vertical, get_font, load_svg,
)


SECTION_GAP = 48
LABEL_COLOR = BLUE[600]
BG_COLOR = BLUE[50]


def run_styleguide():
    """Lance la page styleguide en standalone."""
    pygame.init()
    screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))
    pygame.display.set_caption("CybOS — Styleguide")
    clock = pygame.time.Clock()

    # Surface scrollable (plus grande que l'écran)
    content_height = 2400
    content = pygame.Surface((Screen.WIDTH, content_height), pygame.SRCALPHA)

    scroll_y = 0
    max_scroll = content_height - Screen.HEIGHT

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_y = min(scroll_y + 40, max_scroll)
                elif event.key == pygame.K_UP:
                    scroll_y = max(scroll_y - 40, 0)
                elif event.key == pygame.K_PAGEDOWN:
                    scroll_y = min(scroll_y + Screen.HEIGHT, max_scroll)
                elif event.key == pygame.K_PAGEUP:
                    scroll_y = max(scroll_y - Screen.HEIGHT, 0)

        # Rendu du contenu
        content.fill(BG_COLOR)
        y = _draw_all_sections(content)

        # Ajuster la hauteur scrollable si nécessaire
        if y > content_height:
            content_height = y + 100
            content = pygame.Surface((Screen.WIDTH, content_height), pygame.SRCALPHA)
            max_scroll = content_height - Screen.HEIGHT

        # Afficher la portion visible
        screen.blit(content, (0, -scroll_y))

        # Indicateur de scroll
        if max_scroll > 0:
            bar_h = max(20, int(Screen.HEIGHT * Screen.HEIGHT / content_height))
            bar_y = int(scroll_y / max_scroll * (Screen.HEIGHT - bar_h))
            pygame.draw.rect(screen, BLUE[300], (Screen.WIDTH - 6, bar_y, 4, bar_h), border_radius=2)

        pygame.display.flip()
        clock.tick(Screen.FPS)

    pygame.quit()


def _draw_all_sections(surface):
    """Dessine toutes les sections du styleguide. Retourne la hauteur totale."""
    y = Spacing.SP_32

    y = _draw_section_title(surface, y, "Couleurs primitives")
    y = _draw_colors(surface, y)

    y = _draw_section_title(surface, y, "Couleurs sémantiques")
    y = _draw_semantic_colors(surface, y)

    y = _draw_section_title(surface, y, "Typographie")
    y = _draw_typography(surface, y)

    y = _draw_section_title(surface, y, "Spacings")
    y = _draw_spacings(surface, y)

    y = _draw_section_title(surface, y, "Border radius")
    y = _draw_radius(surface, y)

    y = _draw_section_title(surface, y, "Blocs (neumorphisme)")
    y = _draw_blocs(surface, y)

    y = _draw_section_title(surface, y, "Barres de progression")
    y = _draw_progress_bars(surface, y)

    y = _draw_section_title(surface, y, "Gradients")
    y = _draw_gradients(surface, y)

    y = _draw_section_title(surface, y, "Icônes")
    y = _draw_icons(surface, y)

    return y


def _draw_section_title(surface, y, title):
    """Dessine un titre de section."""
    y += SECTION_GAP
    draw_text(surface, title, Spacing.SP_32, y,
              Fonts.TITLE_FAMILY, Fonts.TITLE_MD, Colors.TITLE_PRIMARY)
    y += Fonts.TITLE_MD + Spacing.SP_16
    # Ligne de séparation
    pygame.draw.line(surface, BLUE[200], (Spacing.SP_32, y), (Screen.WIDTH - Spacing.SP_32, y), 1)
    y += Spacing.SP_16
    return y


def _draw_colors(surface, y):
    """Affiche les palettes blue et red."""
    x_start = Spacing.SP_32
    swatch_size = 56
    gap = 8

    # Blue
    draw_text(surface, "Blue", x_start, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, LABEL_COLOR, bold=True)
    y += Fonts.TEXT_SMALL + Spacing.SP_8
    for i, (shade, color) in enumerate(sorted(BLUE.items())):
        x = x_start + i * (swatch_size + gap)
        draw_rounded_rect(surface, (x, y, swatch_size, swatch_size), color, radius=8)
        draw_text(surface, str(shade), x + swatch_size // 2, y + swatch_size + 4,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="midtop")
    y += swatch_size + 24

    # Red
    draw_text(surface, "Red", x_start, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, LABEL_COLOR, bold=True)
    y += Fonts.TEXT_SMALL + Spacing.SP_8
    for i, (shade, color) in enumerate(sorted(RED.items())):
        x = x_start + i * (swatch_size + gap)
        draw_rounded_rect(surface, (x, y, swatch_size, swatch_size), color, radius=8)
        draw_text(surface, str(shade), x + swatch_size // 2, y + swatch_size + 4,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="midtop")
    y += swatch_size + 24

    return y


def _draw_semantic_colors(surface, y):
    """Affiche les couleurs sémantiques avec leur nom."""
    x_start = Spacing.SP_32
    swatch_size = 40
    items = [
        ("title-primary", Colors.TITLE_PRIMARY),
        ("title-secondary", Colors.TITLE_SECONDARY),
        ("text-primary", Colors.TEXT_PRIMARY),
        ("text-secondary", Colors.TEXT_SECONDARY),
        ("text-primary-disable", Colors.TEXT_PRIMARY_DISABLE),
        ("text-secondary-disable", Colors.TEXT_SECONDARY_DISABLE),
        ("action-primary", Colors.ACTION_PRIMARY),
        ("action-secondary", Colors.ACTION_SECONDARY),
        ("action-primary-disable", Colors.ACTION_PRIMARY_DISABLE),
        ("bar-light", Colors.BAR_LIGHT),
        ("bar-medium", Colors.BAR_MEDIUM),
        ("bar-background", Colors.BAR_BACKGROUND),
        ("bloc-stroke", Colors.BLOC_STROKE),
    ]

    col_width = 240
    for i, (name, color) in enumerate(items):
        col = i % 3
        row = i // 3
        x = x_start + col * col_width
        cy = y + row * (swatch_size + Spacing.SP_8)

        rgb = color[:3]
        draw_rounded_rect(surface, (x, cy, swatch_size, swatch_size), rgb, radius=6)
        draw_text(surface, name, x + swatch_size + 8, cy + swatch_size // 2,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="midleft")

    rows = (len(items) + 2) // 3
    y += rows * (swatch_size + Spacing.SP_8) + Spacing.SP_8
    return y


def _draw_typography(surface, y):
    """Affiche les styles typographiques."""
    samples = [
        ("Title XL (112px)", Fonts.TITLE_FAMILY, 56, Colors.TITLE_PRIMARY, False, False),  # Réduit pour la démo
        ("Title MD (48px)", Fonts.TITLE_FAMILY, Fonts.TITLE_MD, Colors.TITLE_PRIMARY, False, False),
        ("Text Medium (32px)", Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_PRIMARY, True, False),
        ("Text Medium Italic", Fonts.TEXT_FAMILY, Fonts.TEXT_MEDIUM, Colors.TEXT_PRIMARY, True, True),
        ("Text Small (20px)", Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY, True, False),
    ]

    for label, family, size, color, bold, italic in samples:
        draw_text(surface, label, Spacing.SP_32, y, family, size, color, bold=bold, italic=italic)
        y += size + Spacing.SP_12

    # Couleurs de texte
    y += Spacing.SP_8
    draw_text(surface, "Primary", Spacing.SP_32, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY, bold=True)
    draw_text(surface, "Secondary", 180, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_SECONDARY, bold=True)
    draw_text(surface, "Disable", 360, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY_DISABLE, bold=True)
    draw_text(surface, "Disable", 500, y, Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_SECONDARY_DISABLE, bold=True)
    y += Fonts.TEXT_SMALL + Spacing.SP_8

    return y


def _draw_spacings(surface, y):
    """Affiche les spacings sous forme de barres proportionnelles."""
    spacings = [
        ("sp-8", Spacing.SP_8),
        ("sp-12", Spacing.SP_12),
        ("sp-16", Spacing.SP_16),
        ("sp-20", Spacing.SP_20),
        ("sp-32", Spacing.SP_32),
        ("sp-48", Spacing.SP_48),
    ]

    for name, value in spacings:
        draw_text(surface, f"{name} ({value}px)", Spacing.SP_32, y + 2,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        bar_x = 200
        draw_rounded_rect(surface, (bar_x, y, value * 4, 20), BLUE[300], radius=4)
        y += 28

    return y


def _draw_radius(surface, y):
    """Affiche les différents border radius."""
    # radius-default (12px)
    draw_rounded_rect(surface, (Spacing.SP_32, y, 120, 80), BLUE[200], radius=Radius.DEFAULT,
                       border=2, border_color=BLUE[500])
    draw_text(surface, "12px", Spacing.SP_32 + 60, y + 40,
              Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="center")

    # radius-full
    draw_rounded_rect(surface, (200, y, 80, 80), BLUE[200], radius=Radius.FULL,
                       border=2, border_color=BLUE[500])
    draw_text(surface, "full", 240, y + 40,
              Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True, anchor="center")

    y += 100
    return y


def _draw_blocs(surface, y):
    """Affiche les blocs neumorphiques dans leurs différents états."""
    # Default
    draw_text(surface, "Default", Spacing.SP_32, y, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
    y += 20
    draw_bloc(surface, (Spacing.SP_32, y, 300, 100), state="default")
    draw_text(surface, "Bloc default", Spacing.SP_32 + 150, y + 50,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY, bold=True, anchor="center")

    # Select
    draw_text(surface, "Select", 400, y - 20, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
    draw_bloc(surface, (400, y, 300, 100), state="select")
    draw_text(surface, "Bloc select", 550, y + 50,
              Fonts.TEXT_FAMILY, Fonts.TEXT_SMALL, Colors.TEXT_PRIMARY, bold=True, anchor="center")

    y += 120
    return y


def _draw_progress_bars(surface, y):
    """Affiche les barres de progression à différents niveaux."""
    fills = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

    for fill in fills:
        label = f"{int(fill * 100)}%"
        draw_text(surface, label, Spacing.SP_32, y + 2,
                  Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        draw_progress_bar(surface, (100, y, 300, 8), fill)

        # Version bar-light
        draw_progress_bar(surface, (440, y, 300, 8), fill, bar_color=Colors.BAR_LIGHT)
        y += 20

    return y


def _draw_gradients(surface, y):
    """Affiche les gradients définis."""
    gradients = [
        ("Typography", Gradients.TYPOGRAPHY),
        ("Action", Gradients.ACTION),
        ("Background", Gradients.BACKGROUND),
    ]

    x = Spacing.SP_32
    for name, (c1, c2) in gradients:
        draw_text(surface, name, x, y, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
        draw_gradient_vertical(surface, (x, y + 20, 200, 40), c1, c2)
        x += 240

    y += 80
    return y


def _draw_icons(surface, y):
    """Affiche un échantillon d'icônes."""
    icon_names = [
        "icons/wifi-blue-primary.svg",
        "icons/bluetooth-blue-primary.svg",
        "icons/setting-blue-primary.svg",
        "icons/system-blue-primary.svg",
        "icons/audio-blue-primary.svg",
        "icons/light-blue-primary.svg",
        "icons/download-blue-primary.svg",
        "icons/play-blue-primary.svg",
        "icons/move-blue-primary.svg",
        "icons/valid-blue-primary.svg",
        "icons/error-blue-primary.svg",
        "icons/arrow-l-blue-primary.svg",
        "icons/arrow-r-blue-primary.svg",
        "icons/loader-blue-primary.svg",
    ]

    x_start = Spacing.SP_32
    icon_size = 32
    gap = 16

    for i, name in enumerate(icon_names):
        x = x_start + i * (icon_size + gap)
        if x + icon_size > Screen.WIDTH - Spacing.SP_32:
            break
        icon = load_svg(name, (icon_size, icon_size))
        surface.blit(icon, (x, y))

    y += icon_size + Spacing.SP_16

    # Icônes en rouge
    red_icons = [
        "icons/wifi-red-secondary.svg",
        "icons/bluetooth-red-secondary.svg",
        "icons/setting-red-secondary.svg",
        "icons/audio-red-secondary.svg",
        "icons/valid-red-secondary.svg",
        "icons/error-red-secondary.svg",
    ]

    for i, name in enumerate(red_icons):
        x = x_start + i * (icon_size + gap)
        icon = load_svg(name, (icon_size, icon_size))
        surface.blit(icon, (x, y))

    y += icon_size + Spacing.SP_16

    # App illustrations
    draw_text(surface, "App illustrations", x_start, y, Fonts.TEXT_FAMILY, 14, LABEL_COLOR, bold=True)
    y += 20
    app_icons = [
        "apps/cybulateur-red-large.svg",
        "apps/hue-red-large.svg",
        "apps/setting-red-large.svg",
        "apps/cybulateur-blue-large.svg",
        "apps/hue-blue-large.svg",
        "apps/setting-blue-large.svg",
    ]
    for i, name in enumerate(app_icons):
        x = x_start + i * (80 + gap)
        icon = load_svg(name, (80, 80))
        surface.blit(icon, (x, y))

    y += 100
    return y


if __name__ == "__main__":
    run_styleguide()

"""
CybOS - Point d'entrée principal
Usage : python main.py [--styleguide]
"""

import sys


def main():
    if "--styleguide" in sys.argv:
        from src.screens.styleguide import run_styleguide
        run_styleguide()
    else:
        print("CybOS — Utilise --styleguide pour afficher le design system")
        print("Le hub principal sera implémenté en Phase 3.")


if __name__ == "__main__":
    main()

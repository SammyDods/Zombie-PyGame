"""Platform helpers for desktop vs pygbag (browser) builds."""
import sys

IS_WEB = sys.platform == "emscripten"


def quit_game():
    """Exit the game (desktop and browser)."""
    import pygame

    pygame.quit()
    raise SystemExit

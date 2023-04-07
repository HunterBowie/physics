import pygame

from windowgui.constants import RootPosition


class PygameDisplayUninitialized(Exception):
    """The Pygame Display was not initialized using set_mode()."""


def root(rect: pygame.Rect, pos: RootPosition) -> pygame.Rect:
    """
    Position a rect relative to specific position on the screen.

    The Pygame display must be initialized before calling this function.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        raise PygameDisplayUninitialized(
            "The root function cannot be called \
                                          unless the display is initialized"
        )
    screen_width, screen_height = screen.get_size()
    center_pos = int(screen_width / 2), int(screen_height / 2)

    x, y = 0, 0
    match pos:
        case RootPosition.CENTER:
            x = center_pos[0] - int(rect.width / 2)
            y = center_pos[1] - int(rect.height / 2)
        case RootPosition.LEFT_CENTER:
            x = 0
            y = center_pos[1] - int(rect.height / 2)
        case RootPosition.RIGHT_CENTER:
            x = screen_width - rect.width
            y = center_pos[1] - int(rect.height / 2)
        case RootPosition.TOP_CENTER:
            x = center_pos[0] - int(rect.width / 2)
            y = 0
        case RootPosition.TOP_LEFT:
            x = 0
            y = 0
        case RootPosition.TOP_RIGHT:
            x = screen_width - rect.width
            y = 0
        case RootPosition.BOTTOM_CENTER:
            y = screen_height - rect.height
            x = center_pos[0] - int(rect.width / 2)
        case RootPosition.BOTTOM_LEFT:
            x = 0
            y = screen_height - rect.height
        case RootPosition.BOTTOM_RIGHT:
            y = screen_height - rect.height
            x = screen_width - rect.width
        case other:
            ValueError("Invalid RootPosition argument")
    rect.x += x
    rect.y += y
    return rect

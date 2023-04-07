from dataclasses import dataclass

import pygame

from windowgui.constants import Color


@dataclass
class Window:
    """
    A class for handling window settings.
    """

    screen_size: tuple[int, int]
    caption: str = "Window"
    icon: pygame.Surface = None
    force_quit: bool = False
    resizable: bool = False
    max_fps: int = 60
    bg_color: pygame.Color = Color.WHITE

    def __post_init__(self):
        if self.resizable:
            self.screen: pygame.Surface = pygame.display.set_mode(
                self.screen_size, pygame.RESIZABLE
            )
        else:
            self.screen: pygame.Surface = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.caption)
        if self.icon is not None:
            pygame.display.set_icon(self.icon)
        self._clock: pygame.time.Clock = pygame.time.Clock()

    def update(self):
        pygame.display.flip()
        self._clock.tick(self.max_fps)
        self.screen.fill(self.bg_color)

        if self.force_quit and pygame.event.get(eventtype=pygame.QUIT):
            quit()

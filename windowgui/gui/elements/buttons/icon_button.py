from dataclasses import dataclass

import pygame

from windowgui.assets import Icon
from windowgui.constants import ButtonImageShape, ColorStyle, RootPosition
from windowgui.gui.elements.buttons.button import MARGIN, Button


@dataclass
class IconButton(Button):
    icon: Icon = Icon.ARROW_UP
    image_shape: ButtonImageShape = ButtonImageShape.SQUARE

    def __post_init__(self):
        self.width = self.icon.value.get_width() + MARGIN
        self.height = self.icon.value.get_height() + MARGIN
        super().__post_init__()

    def render(self, surface: pygame.Surface):
        super().render(surface)
        if self.is_down():
            surface.blit(self.icon.value, self.rect.topleft)
        else:
            surface.blit(self.icon.value, (self.x, self.y - 4))

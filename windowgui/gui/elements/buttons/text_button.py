from dataclasses import dataclass
from typing import Optional

import pygame

from windowgui.assets import Icon
from windowgui.constants import ButtonImageShape, ColorStyle, RootPosition
from windowgui.gui.elements.buttons.button import MARGIN, Button
from windowgui.util import Text


@dataclass
class TextButton(Button):
    text: Optional[Text] = None

    def __post_init__(self):
        super().__post_init__()
        if self.text is None:
            self.text = Text("")
        self.text.center(self.rect)
        self.text.y -= MARGIN

    def render(self, surface: pygame.Surface):
        super().render(surface)
        if self.is_down():
            surface.blit(self.text.surface, (self.text.x, self.text.y + MARGIN))
        else:
            self.text.render(surface)

from dataclasses import dataclass

import pygame

from windowgui.assets import load_button_image
from windowgui.constants import (
    ButtonImageShape,
    ButtonStatus,
    ColorStyle,
    EventType,
    RootPosition,
)
from windowgui.gui.elements.gui_element import GUIElement

MARGIN = 4


@dataclass
class Button(GUIElement):
    """
    A GUI element for buttons.
    """

    x: int = 0
    y: int = 0
    width: int = 250
    height: int = 50
    tag: str = ""
    root_pos: RootPosition = RootPosition.TOP_LEFT
    color_style: ColorStyle = ColorStyle.WHITE
    image_shape: ButtonImageShape = ButtonImageShape.LONG

    def __post_init__(self):
        self.clicked = False

        self.image_up = load_button_image(
            ButtonStatus.UP,
            (self.width, self.height),
            self.color_style,
            self.image_shape,
        )
        self.image_down = load_button_image(
            ButtonStatus.DOWN,
            (self.width, self.height - MARGIN),
            self.color_style,
            self.image_shape,
        )

        self.force_down = False
        super().__post_init__()

    def eventloop(self, event: pygame.event.Event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                self.clicked = True
                self.post_event(EventType.BUTTON_CLICKED)

    def update(self):
        if not pygame.mouse.get_pressed() == (1, 0, 0) and self.clicked:
            self.clicked = False
            self.post_event(EventType.BUTTON_RELEASED)

    def is_down(self) -> bool:
        return self.clicked or self.force_down

    def render(self, surface: pygame.Surface):
        if self.is_down():
            surface.blit(self.image_down, self.rect.topleft)
        else:
            surface.blit(self.image_up, (self.x, self.y - MARGIN))

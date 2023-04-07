from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import pygame

from windowgui.constants import RootPosition
from windowgui.util import root


@dataclass
class GUIElement(ABC):
    """A GUI element."""

    x: int
    y: int
    tag: str
    root_pos: RootPosition
    width: int = field(init=False)
    height: int = field(init=False)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def __post_init__(self):
        self.root(self.root_pos)

    def post_event(self, event_type: int, **kwargs):
        event_data = {"tag": self.tag}
        pygame.event.post(pygame.event.Event(event_type, event_data), **kwargs)

    def root(self, pos: RootPosition):
        self.x, self.y = root(self.rect, pos).topleft

    @abstractmethod
    def eventloop(self, event: pygame.event.Event):
        """Allow GUI element to process event."""

    @abstractmethod
    def update(self):
        """Update GUI element."""

    @abstractmethod
    def render(self, surface: pygame.Surface):
        "Render GUI element on the given surface."

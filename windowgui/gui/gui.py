import pygame

from windowgui.constants import RootPosition
from windowgui.gui.elements import GUIElement


class GUI:
    """
    A class for managing GUI elements.
    """

    def __init__(self, *args: list[GUIElement]):
        self.elements: list[GUIElement] = list(args)

    def __str__(self):
        return str(self.elements)

    def eventloop(self, event: pygame.event.Event):
        """Allow GUI elements to process an event."""
        for element in self.elements:
            element.eventloop(event)

    def update(self):
        """Updates all elements in the GUI."""
        for element in self.elements:
            element.update()

    def render(self, surface: pygame.Surface):
        """Renders all elements in the GUI."""
        elements = self.elements.copy()
        elements.reverse()
        for element in elements:
            element.render(surface)

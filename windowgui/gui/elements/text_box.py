from dataclasses import dataclass

import pygame
import pyperclip

from windowgui.constants import Color, EventType, RootPosition
from windowgui.gui.elements.gui_element import GUIElement
from windowgui.util import Text, Timer

MARGIN = 5
CURSOR_BLINK_TIME = 0.45
BACKSPACE_START_DELAY = 0.4
BACKSPACE_DELAY = 0.05
BORDER_WIDTH = 4
SHIFT_CHARS = {
    "1": "!",
    "2": "@",
    "3": "#",
    "4": "$",
    "5": "%",
    "6": "^",
    "7": "&",
    "8": "*",
    "9": "(",
    "0": ")",
    "-": "_",
    "=": "+",
    "`": "~",
    "/": "?",
    ";": ":",
    "\\": "\|",
}


@dataclass
class TextBox(GUIElement):
    """
    A GUI element for getting text from the user.
    """

    x: int = 0
    y: int = 0
    tag: str = ""
    root_pos: RootPosition = RootPosition.TOP_LEFT
    width: int = 250
    height: int = 50
    text: Text = None
    border_size: int = 3

    def __post_init__(self):
        if self.text is None:
            self.text = Text("")
        self.text.style

        self.selected = False
        self.show_cursor = True
        self.cursor_timer = Timer()
        self.cursor_timer.start()
        self.backspace_timer = Timer()
        self.held_backspace_timer = Timer()
        super().__post_init__()

    def hide_cursor(self):
        self.cursor_timer.start()
        self.cursor_blink = True

    def is_appendable(self, string: str):
        text_size = Text.get_pygame_text_size(
            self.text.string + string, self.text.style
        )
        if text_size[0] >= (self.rect.width - MARGIN * 2):
            return False
        return True

    def enter(self, string: str):
        """Attempt to enter text into the text box."""
        if self.is_appendable(string):
            self.text.add(string)

        self.hide_cursor()

    def backspace(self):
        """Attempt to remove a single text character."""
        if self.text.string:
            self.text.pop()

        self.hide_cursor()

    def process_input(self, key_name: str):
        """Process keyboard input."""
        match key_name:
            case "space":
                self.enter(" ")
                return
            case "backspace":
                self.backspace_timer.start()
                self.held_backspace_timer.start()
                self.backspace()
                return
            case "return":
                self.post_event(EventType.TEXTBOX_POSTED, data=self.text.string)
                return
            case "v":
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_META and not mods & pygame.KMOD_ALT:
                    self.enter(pyperclip.paste())
                    return

        if len(key_name) != 1:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if key_name in SHIFT_CHARS.keys():
                self.enter(SHIFT_CHARS[key_name])
                return

        self.enter(key_name)
        return

    def eventloop(self, event: pygame.event.Event):
        pos = pygame.mouse.get_pos()

        # Is the text box selected?
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pos):
                if not self.selected:
                    self.selected = True
                    self.post_event(EventType.TEXTBOX_SELECTED)
            else:
                self.selected = False

        # Get input from keyboard
        if self.selected:
            if event.type == pygame.KEYDOWN:
                self.process_input(pygame.key.name(event.key))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_timer.reset()

    def update(self):
        self.text.center_y(pygame.Rect(0, 0, self.rect.width, self.rect.height))

        if self.cursor_timer.passed(CURSOR_BLINK_TIME):
            self.cursor_timer.start()
            self.show_cursor = not self.show_cursor

        keys = pygame.key.get_pressed()
        if self.selected and keys[pygame.K_BACKSPACE]:
            if self.backspace_timer.passed(BACKSPACE_START_DELAY):
                if self.held_backspace_timer.passed(BACKSPACE_DELAY):
                    self.held_backspace_timer.start()
                    self.backspace()

    def get_surface(self) -> pygame.Surface:
        surface = pygame.Surface((self.rect.width, self.rect.height))
        surface.fill(Color.BLACK)
        inner_surface = pygame.Surface(
            (
                self.rect.width - self.border_size * 2,
                self.rect.height - self.border_size * 2,
            )
        )
        inner_surface.fill(Color.WHITE)
        surface.blit(inner_surface, (self.border_size, self.border_size))

        surface.blit(self.text.surface, (MARGIN, MARGIN * 2))

        if self.selected and self.show_cursor:
            cursor_text = Text(string="|", x=self.text.get_width() + MARGIN)
            cursor_text.y = self.rect.height // 2 - cursor_text.get_height() // 2
            cursor_text.render(surface)

        return surface

    def render(self, surface: pygame.Surface):
        surface.blit(self.get_surface(), self.rect.topleft)

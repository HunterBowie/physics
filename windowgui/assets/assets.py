from enum import Enum, auto
from os import path

import pygame

from windowgui.constants import ButtonImageShape, ButtonStatus, ColorStyle
from windowgui.util import load_image

CURRENT_DIR = path.dirname(__file__)
IMAGES_DIR = path.join(CURRENT_DIR, "images")
SOUNDS_DIR = path.join(CURRENT_DIR, "sounds")
FOUNTS_DIR = path.join(CURRENT_DIR, "fonts")

FONTS = {
    "regular": pygame.font.get_default_font(),
    "rounded": path.join(FOUNTS_DIR, "rounded.ttf"),
    "future": path.join(FOUNTS_DIR, "future.ttf"),
}


class Icon(Enum):
    ARROW_DOWN: pygame.Surface = load_image("arrowDown", IMAGES_DIR)
    ARROW_LEFT: pygame.Surface = load_image("arrowLeft", IMAGES_DIR)
    ARROW_RIGHT: pygame.Surface = load_image("arrowRight", IMAGES_DIR)
    ARROW_UP: pygame.Surface = load_image("arrowUp", IMAGES_DIR)
    AUDIO_OFF: pygame.Surface = load_image("audioOff", IMAGES_DIR)
    AUDIO_ON: pygame.Surface = load_image("audioOn", IMAGES_DIR)
    BACKWARD: pygame.Surface = load_image("backward", IMAGES_DIR)
    BARS_HORIZONTAL: pygame.Surface = load_image("barsHorizontal", IMAGES_DIR)
    BARS_VERTICAL: pygame.Surface = load_image("barsVertical", IMAGES_DIR)
    BASKET: pygame.Surface = load_image("basket", IMAGES_DIR)


def load_button_image(
    status: ButtonStatus,
    scale: tuple[int, int],
    color_style: ColorStyle,
    shape: ButtonImageShape,
) -> pygame.Surface:
    image_name = color_style.value + "_button_" + status.value + "_" + shape.value
    image = load_image(image_name, IMAGES_DIR)
    return pygame.transform.scale(image, scale)


def load_slider_image(direction, color_style):
    image_name = color_style + "_slider"
    direction = direction[0].upper() + direction[1:]
    image_name = image_name + direction
    image = load_image(image_name, IMAGES_DIR)
    return image


def load_checkbox_image(filled, color_style, symbol, scale):
    if filled:
        symbol = symbol[0].upper() + symbol[1:]
        return load_image(f"{color_style}_box{symbol}", IMAGES_DIR, scale=scale)

    if symbol != "tick":
        return load_image("white_box", IMAGES_DIR, scale=scale)
    return load_image("white_circle", IMAGES_DIR, scale=scale)

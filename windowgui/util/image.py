from os import path

import pygame

from windowgui.constants import Color


def load_image(
    img_name: str,
    img_dir: str,
    ext: str = ".png",
    colorkey: tuple[int, int, int] = None,
    convert: bool = False,
    scale: tuple[int, int] = None,
) -> pygame.Surface:
    full_path = path.join(img_dir, img_name) + ext
    try:
        img = pygame.image.load(full_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"No image for path {full_path}")
    if scale is not None:
        img = pygame.transform.scale(img, scale)
    if convert:
        img = img.convert_alpha()
    if colorkey:
        img.set_colorkey(Color.BLACK)
    return img

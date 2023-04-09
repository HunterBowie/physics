from os import path

import windowgui

CURRENT_DIR = path.dirname(__file__)
IMAGES_DIR = path.join(CURRENT_DIR, "images")
SOUND_DIR = path.join(CURRENT_DIR, "sound")


IMAGES = {
    "green_round_alien": windowgui.load_image(
        "Aliens/alienGreen_round", IMAGES_DIR, scale=(20, 20)
    ),
    "green_square_alien": windowgui.load_image(
        "Aliens/alienGreen_square", IMAGES_DIR, scale=(20, 20)
    ),
    "blue_square_alien": windowgui.load_image(
        "Aliens/alienBlue_square", IMAGES_DIR, scale=(20, 20)
    ),
}


def convert_images():
    for name, image in IMAGES.items():
        IMAGES[name] = image.convert_alpha()

from enum import Enum, auto

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

RESTITUTION = 0.5


class BodyType(Enum):
    DYNAMIC = auto()
    STATIC = auto()

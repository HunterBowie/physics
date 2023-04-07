from dataclasses import dataclass, field

import pygame


@dataclass
class PhysicsObject:
    x: float
    y: float
    width: int
    height: int
    density: int = 1

    def __post_init__(self):
        self.velocity: list[int, int] = [0, 0]

    @property
    def mass(self) -> int:
        return self.width * self.height * self.density

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def accelerate(self, acceleration: tuple[float, float]):
        self.velocity[0] += acceleration[0]
        self.velocity[1] += acceleration[1]

    def apply_force(self, pytons: tuple[float, float]):
        """
        Apply a force to the object in pytons.

        A pyton is the force it takes to accelerate a 1
        pygram object to 1 pixel / second / second
        """
        acceleration = pytons[0] / self.mass, pytons[1] / self.mass
        self.accelerate(acceleration)

    def update(self, delta):
        self.x += self.velocity[0] / delta
        self.y += self.velocity[1] / delta

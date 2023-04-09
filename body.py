from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from constants import RESTITUTION, BodyType


@dataclass
class Body:
    x: float = 0.0
    y: float = 0.0
    mask: pygame.Mask = pygame.Mask((1, 1), True)
    body_type: BodyType = BodyType.DYNAMIC
    density: float = 1

    def __post_init__(self):
        self.velocity: list[float, float] = [0, 0]

    @property
    def area(self) -> int:
        return self.mask.overlap_area(self.mask.copy(), (0, 0))

    @property
    def mass(self) -> float:
        if self.body_type == BodyType.STATIC:
            return float("inf")
        return self.area * self.density

    @property
    def width(self):
        return self.mask.get_size()[0]

    @property
    def height(self):
        return self.mask.get_size()[1]

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def accelerate(self, acceleration: tuple[float, float]):
        """Change the speed of the object."""
        self.velocity[0] += acceleration[0]
        self.velocity[1] += acceleration[1]

    def apply_force(self, pytons: tuple[float, float]):
        """Apply a force to the body in pytons."""
        acceleration_x = (pytons[0] * 10) / (self.mass / 1000)
        acceleration_y = (pytons[1] * 10) / (self.mass / 1000)
        self.accelerate((acceleration_x, acceleration_y))

    def collided(self, body: Body) -> bool:
        offset = round(body.x) - round(self.x), round(body.y) - round(self.y)
        if self.mask.overlap(body.mask, offset):
            return True
        return False

    @staticmethod
    def _one_dimesional_elastic_collision(
        v1i: float, v2i: float, m1: float, m2: float
    ) -> tuple[int, int]:
        v1f = (m1 - m2) / (m1 + m2) * v1i + 2 * m2 / (m1 + m2) * v2i
        v2f = 2 * m1 / (m1 + m2) * v1i + (m2 - m1) / (m1 + m2) * v2i
        return v1f, v2f

    @staticmethod
    def _one_dimesional_inelastic_collision(
        v1i: float, v2i: float, m1: float, m2: float
    ) -> tuple[int, int]:
        v1f = (RESTITUTION * m2 * (v2i - v1i) + m1 * v1i + m2 * v2i) / (m1 + m2)
        v2f = (RESTITUTION * m1 * (v1i - v2i) + m1 * v1i + m2 * v2i) / (m1 + m2)
        return v1f, v2f

    def _collision(self, body: Body):
        if body.body_type == BodyType.STATIC:
            self.velocity[0] = -RESTITUTION * self.velocity[0]
            self.velocity[1] = -RESTITUTION * self.velocity[1]
            return
        self.velocity[0], body.velocity[0] = self._one_dimesional_inelastic_collision(
            self.velocity[0], body.velocity[0], self.mass, body.mass
        )
        self.velocity[1], body.velocity[1] = self._one_dimesional_inelastic_collision(
            self.velocity[1], body.velocity[1], self.mass, body.mass
        )

    def move_and_collide(self, delta: float, bodies: list[Body]):
        collided_bodies = []
        if self.velocity[0] != 0:
            self.x += self.velocity[0] * delta
            for body in bodies:
                if self.collided(body):
                    collided_bodies.append(body)
                    if self.velocity[0] > 0:  # right
                        self.x = body.rect.left - self.width
                    else:
                        self.x = body.rect.right

        if self.velocity[1] != 0:
            self.y += self.velocity[1] * delta
            for body in bodies:
                if self.collided(body):
                    collided_bodies.append(body)
                    if self.velocity[1] > 0:  # down
                        self.y = body.rect.top - self.height
                    else:
                        self.y = body.rect.bottom

        for body in collided_bodies:
            self._collision(body)

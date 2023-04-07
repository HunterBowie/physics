import pygame

import windowgui
from constants import SCREEN_SIZE
from physics_object import PhysicsObject

pygame.init()

window = windowgui.Window(SCREEN_SIZE, force_quit=True, caption="Physics Simulation")


def main():
    box = PhysicsObject(50, 400, 100, 100)
    box.velocity = [50, -50]
    pos = set()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    box.apply_force((0, -100))
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    box.apply_force((0, 100))
        box.accelerate((0, 9.8 / window.max_fps))
        box.update(window.max_fps)
        pos.add(box.rect.center)
        pygame.draw.rect(window.screen, windowgui.Color.GOLD, box.rect)
        for p in pos:
            window.screen.set_at(p, windowgui.Color.RED)
        window.update()


if __name__ == "__main__":
    main()

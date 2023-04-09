import pygame

import assets
import windowgui
from body import Body
from constants import SCREEN_HEIGHT, SCREEN_SIZE, SCREEN_WIDTH, BodyType

pygame.init()

window = windowgui.Window(SCREEN_SIZE, force_quit=True, caption="Physics Simulation")

assets.convert_images()

alien_image = assets.IMAGES["green_square_alien"]


def main():
    box = Body(50, 400, pygame.mask.from_surface(alien_image))
    box2 = Body(300, 400, pygame.mask.from_surface(alien_image))
    pygame.Surface((SCREEN_WIDTH - 20, 50))
    floor = Body(
        10,
        SCREEN_HEIGHT - 60,
        pygame.Mask((SCREEN_WIDTH, 50), True),
        body_type=BodyType.STATIC,
    )
    while True:
        newtons = 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    box.apply_force((-newtons, 0))
                if event.key == pygame.K_d:
                    box.apply_force((newtons, 0))
                if event.key == pygame.K_w:
                    box.apply_force((0, -newtons))
                if event.key == pygame.K_s:
                    box.apply_force((0, newtons))
                if event.key == pygame.K_LEFT:
                    box2.apply_force((-newtons, 0))
                if event.key == pygame.K_RIGHT:
                    box2.apply_force((newtons, 0))
                if event.key == pygame.K_DOWN:
                    box2.apply_force((0, newtons))
                if event.key == pygame.K_UP:
                    box2.apply_force((0, -newtons))
                if event.key == pygame.K_SPACE:
                    box.x, box.y = 100, 100
                    box2.x, box2.y = 200, 200
        box.accelerate((0, 98.1 / window.max_fps))
        box2.accelerate((0, 98.1 / window.max_fps))
        box.move_and_collide(1 / window.max_fps, [box2, floor])
        box2.move_and_collide(1 / window.max_fps, [box, floor])
        # pygame.draw.rect(window.screen, windowgui.Color.RED, box.rect)
        window.screen.blit(assets.IMAGES["green_square_alien"], box.rect.topleft)
        window.screen.blit(assets.IMAGES["blue_square_alien"], box2.rect.topleft)
        pygame.draw.rect(window.screen, windowgui.Color.GREEN, floor.rect)
        window.update()


if __name__ == "__main__":
    main()

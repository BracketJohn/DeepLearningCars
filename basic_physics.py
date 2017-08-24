"""First go at simulating some cars in an enclosed area."""
import math
import random
import sys

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

import pymunk
import pymunk.pygame_util


CAR_MASS = 2
CAR_RADIUS = 1
CAR_SIZE = 37.5, 15

WINDOW_SIZE = 600


def add_car(space):
    """Add car to space."""
    inertia = pymunk.moment_for_box(CAR_MASS, size=CAR_SIZE)
    body = pymunk.Body(CAR_MASS, inertia)
    body.position = WINDOW_SIZE/2, WINDOW_SIZE/2
    body.velocity = [100, 0]
    body.angle = math.radians(random.randint(0, 359))

    body.velocity = body.velocity.rotated(body.angle)

    shape = pymunk.Poly.create_box(body, size=CAR_SIZE, radius=CAR_RADIUS)
    shape.filter = pymunk.ShapeFilter(categories=1, mask=pymunk.ShapeFilter.ALL_MASKS ^ 1)
    shape.elasticity = 0.95

    # body.apply_force_at_local_point((0, 10000), (0, CAR_SIZE[1]/2))

    space.add(body, shape)

    return shape


def create_walls(space):
    """Create walls in space."""
    wall = pymunk.Body(body_type=pymunk.Body.STATIC)

    walls = [
        pymunk.Segment(wall, (0, 0), (0, WINDOW_SIZE), 3),
        pymunk.Segment(wall, (0, 0), (WINDOW_SIZE, 0), 3),
        pymunk.Segment(wall, (0, WINDOW_SIZE), (WINDOW_SIZE, WINDOW_SIZE), 3),
        pymunk.Segment(wall, (WINDOW_SIZE, 0), (WINDOW_SIZE, WINDOW_SIZE), 3)
        ]

    for wall in walls:
        wall.elasticity = 0.95

    space.add(walls)


def main():
    """Start simulation."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Car simulation")
    clock = pygame.time.Clock()

    space = pymunk.Space()

    create_walls(space)

    sprites = [add_car(space) for car in range(700)]
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_ESCAPE, 113]):
                sys.exit(0)

        screen.fill((255, 255, 255))

        space.debug_draw(draw_options)

        space.step(1/50.0)
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    main()

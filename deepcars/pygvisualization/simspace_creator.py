"""Module which provides a standardized simulation Space, Screen, Clock and draw_options, which can then be used by all other modules."""
from typing import Any, Callable, Tuple

from deepcars.pygvisualization import WINDOW_SIZE

import pygame

import pymunk
import pymunk.pygame_util


def create_sim(caption: str='Basic Simulation') -> Tuple[Any]:
    """Create Simulation Space which can be used by all other classes."""
    pygame.init()
    space = pymunk.Space()

    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption(caption)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    clock = pygame.time.Clock()

    return space, screen, draw_options, clock


def sim_loop(space: pymunk.Space, clock: pygame.time.Clock, screen: pygame.display, draw_options: pymunk.pygame_util.DrawOptions) -> Callable[[Any], Any]:
    """Decorate functionality with a Simulation Loop."""
    def ev_loop(func, *args, **kwargs):
        def loop():
            while True:
                screen.fill((255, 255, 255))

                if func(*args, **kwargs) is 0:
                    break

                space.debug_draw(draw_options)
                pygame.display.flip()
                space.step(1/50.0)
                clock.tick(50)

        return loop

    return ev_loop

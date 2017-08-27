"""Module which provides game like menu for the Car Deep Learn Sim."""
from deepcars.pygvisualization import Coordinate, create_new_map, create_sim, is_pressed, sim_loop, simple_text_menu
import pygame


def main_menu():
    """Run Deep Learn Sim."""
    caption = 'Car Deep Learn Simulation v0.1'
    space, screen, draw_options, clock = create_sim(caption)

    @sim_loop(space, clock, screen, draw_options)
    def sim_menu():
        for event in pygame.event.get():
            if is_pressed(event, [*list('qQ'), 'quit']):
                return 0

            if is_pressed(event, 'sS'):
                sim_map = select_map(caller_caption=caption)

            if is_pressed(event, 'cC'):
                create_new_map(caller_caption=caption)

        simple_text_menu(screen, ['Start Simulation', 'Create a Map', 'Quit'])

    return sim_menu()

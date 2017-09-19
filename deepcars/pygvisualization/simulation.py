"""Run the actual Simulation, including Map select."""
import os
import pickle
import string

import pygame

from pygvisualization import COLLISION_TYPES, MAP_DIR, SimMap
from pygvisualization.object_generator import create_border, Car, create_segment, mark_startingpoint
from pygvisualization.pyg_utils import caption_manager, is_pressed, simple_text
from pygvisualization.simspace_creator import create_sim, sim_loop

from pymunk.vec2d import Vec2d

@caption_manager
def simulation(sim_map: SimMap) -> int:
    """Start Simulation."""
    caption = 'Simulation'
    space, screen, draw_options, clock = create_sim(caption)
    h = space.add_wildcard_collision_handler(COLLISION_TYPES['car'])
    h.begin = Car.car_collions_h

    cars = [Car(space, sim_map['starting_point']) for i in range(10)]

    mark_startingpoint(space, sim_map['starting_point'])
    create_border(space)

    for segment in sim_map['segments']:
        create_segment(space, segment)
    
    @sim_loop(space, clock, screen, draw_options)
    def run_simulation() -> int:
        for event in pygame.event.get():
            if is_pressed(event, 'qQ'):
                return 0

        simple_text(screen, ['Quit'], pos='middle')
        simple_text(screen, ['Fitness: ', 'Speed: ', 'Angle: '], pos='topleft')
        simple_text(screen, ['nth Iteration'], pos='topright')     

        # for car in cars:
        #     car.shape.body.velocity = car.shape.body.velocity.rotated_degrees(0.1)
        #     car.shape.body.angle = Vec2d.get_angle(car.shape.body.velocity)

    return run_simulation()


@caption_manager
def select_map() -> int:
    """Select Map."""
    caption = 'Map Selection'
    space, screen, draw_options, clock = create_sim(caption)

    if not os.path.isdir(MAP_DIR):
        opts = ['Cancel - Please create a Map first!']
    else:
        opts = []

        cur_map_no = 0
        while os.path.exists(f'{MAP_DIR}/map_{cur_map_no}.map'):
            opts.append(f'map_{cur_map_no}.map')
            cur_map_no += 1
        opts = [' '.join([hotkey, mapname]) for hotkey, mapname in zip(string.ascii_uppercase.replace('C', ''), opts)]


    @sim_loop(space, clock, screen, draw_options)
    def select() -> int:
        for event in pygame.event.get():
            if is_pressed(event, 'cC'):
                return 0

            for idx, option in enumerate(opts):
                hotkeys = ''.join([option[0].lower(), option[0]])
                if is_pressed(event, hotkeys):
                    try:
                        with open(f'{MAP_DIR}/{option.split()[1]}', 'rb') as m:
                            sim_map: SimMap = pickle.load(m)
                    except (IndexError, AttributeError):
                        return 1
                    return simulation(sim_map, caller_caption=caption)

        simple_text(screen, ['Cancel'] + opts, pos='middle')

    return select()

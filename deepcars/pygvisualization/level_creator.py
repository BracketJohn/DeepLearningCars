"""Module which allows Simulation User to draw a map for the Simulation to be run on."""
import os
import pickle
from typing import Generator, List, Tuple

from pygvisualization import Coordinate, MAP_DIR, Segment, SegmentPart, SimMap
from pygvisualization.object_generator import create_segment
from pygvisualization.pyg_utils import caption_manager, is_pressed, simple_text
from pygvisualization.simspace_creator import create_sim, sim_loop

import pygame

import pymunk


@caption_manager
def create_new_map() -> int:
    """Start Map Creator."""
    space, screen, draw_options, clock = create_sim('Map Creator')

    segment_g: Generator[Segment, Tuple[str, Coordinate], None] = segment_gen(space)
    next(segment_g)

    sim_map: SimMap = {'segments': []}

    @sim_loop(space, clock, screen, draw_options)
    def draw_map() -> int:
        for event in pygame.event.get():
            if is_pressed(event, 'cC'):
                return 0

            if is_pressed(event, 'sS'):
                if sim_map.get('starting_point'):
                    new_map_number = 0

                    if not os.path.isdir(MAP_DIR):
                        os.makedirs(MAP_DIR)

                    while os.path.exists(f'{MAP_DIR}/map_{new_map_number}.map'):
                        new_map_number += 1

                    with open(f'{MAP_DIR}/map_{new_map_number}.map', 'wb') as new_map:
                        pickle.dump(sim_map, new_map)

                return 0

            if is_pressed(event, ['lmouse_down', 'rmouse_down']):
                segment_g.send(['start', pygame.mouse.get_pos()])

            if is_pressed(event, ['mouse_move']):
                segment_g.send(['continue', pygame.mouse.get_pos()])

            if is_pressed(event, ['lmouse_up', 'rmouse_up']):
                segment: Segment = segment_g.send(['stop', pygame.mouse.get_pos()])
                next(segment_g)
                if is_pressed(event, ['lmouse_up']):
                    sim_map['segments'].append(segment)
                    create_segment(space, segment)
                else:
                    try:
                        sp = SegmentPart(segment[:1][0].start, segment[-1:][0].end)
                        sim_map['starting_point'] = sp
                    except IndexError:
                        return 1

        simple_text(screen, ['Cancel', 'Save'], pos='middle')
        simple_text(screen, ['Left Click and Drag to draw Wall.', 'Right Click and Drag for Start.',
                             'Walls will appear on Release.'], pos='topleft')
        sp = sim_map.get('starting_point')
        simple_text(screen,
                    [f'Start: ({sp.start.x}, {sp.start.y})', f'End: ({sp.end.x}, {sp.end.y})'] if sp else ['Startpoint not set, Map will not save.'],
                    pos='topright')

    return draw_map()


def segment_gen(space: pymunk.Space) -> Generator[Segment, Tuple[str, Coordinate], None]:
    """Generate dynamic, hand drawn Segments, which are stored as a list of Coordinates."""
    drawing: bool = False
    pts: List[Coordinate] = []

    while True:
        status, mouse_pos = yield

        if status == 'start':
            drawing = True

        if drawing:
            pts.append(mouse_pos)

        if drawing and status == 'stop':
            yield Segment([SegmentPart(Coordinate(*seg_start), Coordinate(*seg_end))
                           for seg_start, seg_end in zip(pts, pts[1:])])

            pts = []
            drawing = False

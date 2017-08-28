"""Create Bodys and Shapes from a set of directions and add them to the Screen and Space."""
from pygvisualization import Coordinate, Segment, SegmentPart, WINDOW_SIZE
from pygvisualization.pyg_utils import to_pygame

import pymunk


WALLS = [
    Segment([SegmentPart(Coordinate(0, 0), Coordinate(0, WINDOW_SIZE))]),
    Segment([SegmentPart(Coordinate(0, 0), Coordinate(WINDOW_SIZE, 0))]),
    Segment([SegmentPart(Coordinate(0, WINDOW_SIZE), Coordinate(WINDOW_SIZE, WINDOW_SIZE))]),
    Segment([SegmentPart(Coordinate(WINDOW_SIZE, 0), Coordinate(WINDOW_SIZE, WINDOW_SIZE))])
    ]


def create_border(space: pymunk.Space) -> None:
    """Shorthand to create Walls around Map."""
    for wall in WALLS:
        create_segment(space, wall)


def mark_startingpoint(space: pymunk.Space, sp: SegmentPart) -> None:
    """Draw Car Simulation Starting point and indicate Starting Direction."""
    start_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    start_shape = pymunk.Circle(start_body, 10, offset=(to_pygame(sp.start)))
    space.add(start_shape)


def create_segment(space: pymunk.Space, segment: Segment) -> None:
    """Create walls in space."""
    seg_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    seg_body.elasticity = 1
    seg_body.collision_type = 'wall'

    for seg_part in segment:
        seg_shape = pymunk.Segment(seg_body, to_pygame(seg_part.start), to_pygame(seg_part.end), 3)
        space.add(seg_shape)

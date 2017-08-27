"""Create Bodys and Shapes from a set of directions and add them to the Screen and Space."""
from deepcars.pygvisualization import Coordinate, Segment, SegmentPart, WINDOW_SIZE

import pymunk

from deepcars.pygvisualization.pyg_utils import to_pygame


WALLS = [
    Segment([SegmentPart(Coordinate(0, 0), Coordinate(0, WINDOW_SIZE))]),
    Segment([SegmentPart(Coordinate(0, 0), Coordinate(WINDOW_SIZE, 0))]),
    Segment([SegmentPart(Coordinate(0, WINDOW_SIZE), (WINDOW_SIZE, WINDOW_SIZE))]),
    Segment([SegmentPart(Coordinate(WINDOW_SIZE, 0), Coordinate(WINDOW_SIZE, WINDOW_SIZE))])
    ]


def create_border(space: pymunk.Space) -> None:
    """Shorthand to create Walls around Map."""
    for wall in WALLS:
        create_segment(space, wall)


def create_segment(space: pymunk.Space, segment: Segment) -> None:
    """Create walls in space."""
    seg_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    seg_body.elasticity = 1
    seg_body.collision_type = 'wall'

    for seg_part in segment:
        seg_shape = pymunk.Segment(seg_body, to_pygame(seg_part.start), to_pygame(seg_part.end), 3)
        space.add(seg_shape)

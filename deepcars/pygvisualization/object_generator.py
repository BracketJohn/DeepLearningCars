"""Create Bodys and Shapes from a set of directions and add them to the Screen and Space."""
from pygvisualization import CAR_SIZE, COLLISION_TYPES, Coordinate, Segment, SegmentPart, WINDOW_SIZE
from pygvisualization.pyg_utils import to_pygame

import pymunk
from pymunk.vec2d import Vec2d

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
    start_dot = pymunk.Circle(start_body, 7, offset=(to_pygame(sp.start)))
    start_direction = pymunk.Segment(start_body, to_pygame(sp.start), to_pygame(sp.end), 2)
    start_dot.collision_type, start_direction.collision_type = COLLISION_TYPES['start'], COLLISION_TYPES['start']
    space.add([start_dot, start_direction])


def create_segment(space: pymunk.Space, segment: Segment) -> None:
    """Create walls in space."""
    seg_body = pymunk.Body(body_type=pymunk.Body.STATIC)

    for seg_part in segment:
        seg_shape = pymunk.Segment(seg_body, to_pygame(seg_part.start), to_pygame(seg_part.end), 3)
        seg_shape.elasticity = 0
        seg_shape.collision_type = COLLISION_TYPES['wall']
        space.add(seg_shape)


class Car:
    """Class to manage one specific car."""

    def __init__(self, space, start):
        """Initialize car and it's sensors."""
        self._shape = self.create_car(space, start)

    def create_car(self, space: pymunk.Space, sp: SegmentPart, mass=20):
        """Create a car body and add to Space."""
        from random import randint
        from math import cos, sin
        vertices = [(0, 0), (CAR_SIZE[0], 0), (CAR_SIZE[0], CAR_SIZE[1]), (0, CAR_SIZE[1])]
        inertia = pymunk.moment_for_poly(mass, vertices)

        body = pymunk.Body(mass, inertia)
        body.position = to_pygame(Coordinate(randint(0, 600), randint(0, 600)))

        shape = pymunk.Poly(body, vertices)

        angle_ = Vec2d.get_angle_between(Vec2d(sp.end), Vec2d(sp.start))
        shape.body.velocity = Vec2d(cos(angle_), sin(angle_))*20
        shape.body.angle = angle_
        shape.elasticity = 0
        shape.collision_type = COLLISION_TYPES['car']

        space.add(body, shape)

        return shape

    @staticmethod
    def car_collions_h(arbiter, space, data):
        """Handle Car Collisions."""
        s1, s2 = arbiter.shapes

        if s1.collision_type == COLLISION_TYPES['wall'] or s2.collision_type == COLLISION_TYPES['wall']:
            if s1.collision_type == COLLISION_TYPES['car']:
                s1.body.velocity = 0, 0
            if s2.collision_type == COLLISION_TYPES['car']:
                s2.body.velocity = 0, 0

        return False

    @property
    def shape(self):
        """Give easy Access to Car Shape."""
        return self._shape

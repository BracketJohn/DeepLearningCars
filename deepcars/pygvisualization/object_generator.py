"""Create Bodys and Shapes from a set of directions and add them to the Screen and Space."""
from math import radians

import pygame

from pygvisualization import CAR_SIZE, COLLISION_TYPES, Coordinate, Segment, SegmentPart, WINDOW_SIZE
from pygvisualization.pyg_utils import to_pygame

from pymphysics.pym_utils import calc_heading_vector, calc_radians_between, rotate_around_center

import pymunk


WALLS = [
    Segment([SegmentPart(Coordinate(0, 0), Coordinate(0, WINDOW_SIZE))]),
    Segment([SegmentPart(Coordinate(0, 0), Coordinate(WINDOW_SIZE, 0))]),
    Segment([SegmentPart(Coordinate(0, WINDOW_SIZE), Coordinate(WINDOW_SIZE, WINDOW_SIZE))]),
    Segment([SegmentPart(Coordinate(WINDOW_SIZE, 0), Coordinate(WINDOW_SIZE, WINDOW_SIZE))])
    ]
SENSORS = [
    radians(30),
    radians(60),
    radians(90),
    radians(120),
    radians(150)
    ]


def create_border(space: pymunk.Space) -> None:
    """Shorthand to create Walls around Map."""
    for wall in WALLS:
        create_segment(space, wall)


def mark_startingpoint(space: pymunk.Space, sp: SegmentPart) -> None:
    """Draw Car Simulation Starting point and indicate Starting Direction."""
    start_body = pymunk.Body(body_type=pymunk.Body.STATIC)

    starting_dot = pymunk.Circle(start_body, 6, offset=to_pygame(sp.start))
    starting_dot.collision_type = COLLISION_TYPES['start']

    space.add(starting_dot)


# def create_circle(space: pymunk.Space, position: Coordinate, color: str='blue') -> None:
#     """Draw a Circle at certain Position with certain Color."""
#     body = pymunk.Body(body_type=pymunk.Body.STATIC)
#     circle = pymunk.Circle(body, 6, offset=position)
#     circle.color = pygame.color.THECOLORS[color]
#     circle.collision_type = COLLISION_TYPES['start']

#     space.add(circle)


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
        """Initialize car and it's Sensors."""
        self._shape = self.create_car(space, start)
        self._sensors = [Sensor(self, space, angle) for angle in SENSORS]

    def create_car(self, space: pymunk.Space, sp: SegmentPart, mass=20):
        """Create a car body and add to Space."""
        vertices = [(0, 0), (CAR_SIZE[0], 0), (CAR_SIZE[0], CAR_SIZE[1]), (0, CAR_SIZE[1])]
        inertia = pymunk.moment_for_poly(mass, vertices)
        angle = calc_radians_between(sp.start, sp.end)

        body = pymunk.Body(mass, inertia)
        body.angle = angle
        body.position = to_pygame(sp.start)
        body.velocity = calc_heading_vector(angle)*0

        shape = pymunk.Poly(body, vertices)
        shape.elasticity = 0
        shape.collision_type = COLLISION_TYPES['car']

        space.add(body, shape)

        return shape

    def create_sensors(space: pymunk.Space, car: pymunk.Shape, position: Coordinate):
        """Initialize Cars Sensors."""
        pass

    @staticmethod
    def car_collions_h(arbiter, space, data):
        """Handle Car Collisions."""
        s1, s2 = arbiter.shapes

        if s1.collision_type == COLLISION_TYPES['wall'] or s2.collision_type == COLLISION_TYPES['wall']:
            if s1.collision_type == COLLISION_TYPES['car']:
                s1.body.velocity = 0, 0
                s1.color = pygame.color.THECOLORS['red']
            if s2.collision_type == COLLISION_TYPES['car']:
                s2.color = pygame.color.THECOLORS['red']
                s2.body.velocity = 0, 0

        return False

    @property
    def shape(self):
        """Give easy Access to Car Shape."""
        return self._shape

    @property
    def vertices(self):
        """Get Position of all vertices in Real life Coordinates."""
        return [Coordinate(*(v.rotated(self.shape.body.angle) + self.shape.body.position)) for v in self.shape.get_vertices()]

    @property
    def sensors(self):
        """Get all Sensors attached to car."""
        return self._sensors

    @property
    def sensor_anchor(self):
        """Calculate Front Center of Car, from where the Sensors will measure."""
        front_left, front_right = self.vertices[1], self.vertices[2]
        anchor = Coordinate(*(front_left + front_right)) / 2
        return anchor


class Sensor:
    """Class for a Sensor."""

    def __init__(self, car: Car, space: pymunk.Space, angle: float, max_measure_dist: int=60):
        """Initialize Sensors."""
        self._car = car
        self._angle = angle + self._car.shape.body.angle - radians(90)  # as car is rotated along long side, sensors at short end.
        self._max_measure_dist = max_measure_dist
        self._line_one, self._line_two = self.draw_sensor(space)

    def draw_sensor(self, space: pymunk.Space, sensor_size: int=10) -> pymunk.Shape:
        """Create Cross for Car Sensors."""
        cross_body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)

        line_one = pymunk.Segment(cross_body, self.position + Coordinate(0, sensor_size), self.position + Coordinate(sensor_size, 0), 2)
        line_two = pymunk.Segment(cross_body, self.position, self.position + Coordinate(sensor_size, sensor_size), 2)

        line_one.color, line_two.color = pygame.color.THECOLORS['green'], pygame.color.THECOLORS['green']
        line_one.collision_type, line_two.collision_type = COLLISION_TYPES['sensor'], COLLISION_TYPES['sensor']
        line_one.sensor, line_two.sensor = True, True

        space.add([line_one, line_two])

        return line_one, line_two

    def update_position(sensor) -> Coordinate:
        """Update Sensor Position, based on Car Position and max. Wall Distance before Collision."""
        anchor = sensor.car.sensor_anchor
        return Coordinate(*rotate_around_center(anchor, anchor + Coordinate(*(sensor._max_measure_dist, 0)), sensor._angle))

    @staticmethod
    def interset_tester_collision_h(arbiter, space, data):
        """Handle collisions of Sensor Segment tests and calculate the Sensors maximal possible Distance."""
        s1, s2 = arbiter.shapes
        return False

    @property
    def car(self):
        """Return Car Sensor is attached to."""
        return self._car

    @property
    def position(self) -> Coordinate:
        """Return Position of Sensor."""
        if not hasattr(self, '_position'):
            self._position = self.update_position()
        return self._position

    @position.setter
    def position(self, new_pos: Coordinate) -> None:
        """Set new Position for Sensor."""
        self._position = new_pos
        self._line_one.body.position, self._line_two.body.position = new_pos, new_pos

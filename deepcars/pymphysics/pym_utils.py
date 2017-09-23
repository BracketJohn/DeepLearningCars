"""Module which provides some nice pymunk/Vec2d functionalities that make development easier."""
from math import atan2, cos, pi, sin

from pygvisualization import Coordinate

from pymunk.vec2d import Vec2d


def calc_radians_between(p1: Coordinate, p2: Coordinate):
    """Calculate angle of a line in radians."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    rads = atan2(-dy, dx)
    rads %= 2*pi

    return rads


def calc_heading_vector(angle: float):
    """Calculate heading vector from angle in radians."""
    return Vec2d(cos(angle), sin(angle))


def rotate_around_center(center, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given center.

    The angle should be given in radians.
    """
    ox, oy = center
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy

import math

from shapely.geometry import Point


def add_polar_vector(point: Point, angle: float, magnitude: float):
    """
    :param point:
        the point to start from
    :param angle:
        the angle of the vector to apply to the point
    :param magnitude:
        the length of the vector to apply to the point
    :return:
        a new point at the new position
    """
    d_x = math.cos(angle) * magnitude
    d_y = math.sin(angle) * magnitude
    return Point(point.x + d_x, point.y + d_y)

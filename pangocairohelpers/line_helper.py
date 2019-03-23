import math
from typing import Tuple, Optional
Coordinate = Tuple[float, float]


def coords_length(coord_a: Coordinate, coord_b: Coordinate) -> float:
    """
    :param coord_a:
        the first coordinate
    :param coord_b:
        the second coordinate
    :return:
        the length between two coordinates
    """
    return math.sqrt(
        (coord_a[0] - coord_b[0]) ** 2 +
        (coord_a[1] - coord_b[1]) ** 2
    )


def coords_are_left_to_right(coord_a, coord_b) -> Optional[bool]:
    """
    :param coord_a:
        the first coordinate
    :param coord_b:
        the second coordinate
    :return:
        if the coordinates are going left to right, or right to left.
        In cases where the line is going vertical, ``None`` is returned.
    """
    if coord_b[0] - coord_a[0] == 0:
        return None
    return coord_b[0] > coord_a[0]

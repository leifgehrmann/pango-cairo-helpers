"""
    Functions to help with a single line segments.
"""

import math
from typing import Optional, Tuple
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


def coords_are_left_to_right(
        coord_a: Coordinate,
        coord_b: Coordinate
) -> Optional[bool]:
    """
    :param coord_a:
        the first coordinate
    :param coord_b:
        the second coordinate
    :return:
        ``True`` if the coordinates are going left to right, ``False`` if right
        to left. If the line is vertical, ``None`` is returned.
    """
    if coord_b[0] - coord_a[0] == 0:
        return None
    return coord_b[0] > coord_a[0]

from shapely.geometry import LineString
from typing import Dict, Optional, Tuple
from pangocairohelpers.line_helper import coords_are_left_to_right
from pangocairohelpers.line_helper import coords_length
Coordinate = Tuple[float, float]


def directional_length(
        line_string: LineString,
        aggregate_rule: Dict[Optional[bool], bool]
) -> float:
    """
    :return:
        the length of all the line segments that go left (-x) to
        right (+x)d
    """
    last_coord = None
    length = 0

    for coord in line_string.coords:
        if last_coord is None:
            last_coord = coord
            continue

        should_aggregate = aggregate_rule.get(
            coords_are_left_to_right(last_coord, coord),
            False
        )
        if should_aggregate:
            length += coords_length(last_coord, coord)
        last_coord = coord

    return length


def left_to_right_length(line_string: LineString) -> float:
    """
    :return:
        the length of all the line segments that go left (-x) to
        right (+x)d
    """
    direction_aggregator = {
        True: True,
        False: False,
        None: True,
    }

    return directional_length(line_string, direction_aggregator)


def right_to_left_length(line_string: LineString) -> float:
    """
    :return:
        the length of all the line segments that go right (+x) to
        left (-x)
    """
    direction_aggregator = {
        True: False,
        False: True,
        None: True,
    }

    return directional_length(line_string, direction_aggregator)

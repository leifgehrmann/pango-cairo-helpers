"""
    Functions to help with Shapely's ``LineString`` class.
"""
import math

from shapely.geometry import LineString, Point, LinearRing, MultiPoint, \
    JOIN_STYLE
from typing import Dict, Optional, List, Tuple

from pangocairohelpers import Side
from pangocairohelpers.line_helper import coords_are_left_to_right
from pangocairohelpers.line_helper import coords_length


def _directional_length(
        line_string: LineString,
        aggregate_rule: Dict[Optional[bool], bool]
) -> float:
    """
    :param line_string:
        the ``LineString`` to measure
    :param aggregate_rule:
        a mapping of ``True``, ``False`` and ``None`` to whether the length
        should be aggregated or not (``True`` if it should be aggregated)
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
    :param line_string:
        the ``LineString`` to measure
    :return:
        the length of all the line segments in ``line_string`` that go
        left (-x) to right (+x)
    """
    direction_aggregator = {
        True: True,
        False: False,
        None: True,
    }

    return _directional_length(line_string, direction_aggregator)


def right_to_left_length(line_string: LineString) -> float:
    """
    :param line_string:
        the ``LineString`` to measure
    :return:
        the length of all the line segments in ``line_string`` that go
        right (+x) to left (-x)
    """
    direction_aggregator = {
        True: False,
        False: True,
        None: True,
    }

    return _directional_length(line_string, direction_aggregator)


def interpolated_distance_of_point(
        line_string: LineString,
        point: Point
) -> float:
    """
    :param line_string:
        the ``LineString`` to find the distance on
    :param point:
        the point to find on the line
    :return:
        the interpolation distance to calculate the position of the point on
        the line string
    """
    return line_string.project(point)


def points_at_distance_from_point_on_line_string(
        line_string: LineString,
        point: Point,
        distance: float
) -> List[Point]:
    """
    :param line_string:
        the ``LineString`` to find points on
    :param point:
        the circle's center point to find intersections on the line
    :param distance:
        the circle's radius to find intersections on the line
    :return:
        a list of points that exist in the ``line_string`` and intersect the
        circle at ``point`` with the radius ``distance``
    """
    circle = LinearRing(point.buffer(distance).exterior.coords)
    intersections = line_string.intersection(circle)

    if isinstance(intersections, Point):
        return [intersections]
    elif isinstance(intersections, MultiPoint):
        return list(intersections.geoms)
    elif intersections.is_empty:
        return []
    else:
        raise ValueError('Unexpected intersection type returned')


def next_offset_from_offset_in_line_string(
        line_string: LineString,
        current_offset: float,
        distance: float
) -> Optional[float]:
    """
    Used to find the next point on a line_string that is at a certain distance
    away from the current point on the line.

    :param line_string:
        the ``LineString`` to find the offset on
    :param current_offset:
        the offset to start at
    :param distance:
        the distance the next offset should be
    :return:
        the next offset that is ``distance`` units away from the current
        offset on the ``line_string``
    """
    current_offset_point = line_string.interpolate(current_offset)
    points_at_distance = points_at_distance_from_point_on_line_string(
        line_string,
        current_offset_point,
        distance
    )

    next_minimum_point_offset = None
    for point in points_at_distance:
        point_offset = interpolated_distance_of_point(
            line_string,
            point
        )
        if point_offset < current_offset:
            continue
        if next_minimum_point_offset is None or \
                next_minimum_point_offset > point_offset:
            next_minimum_point_offset = point_offset

    return next_minimum_point_offset


def angles_at_offsets(
        line_string: LineString
) -> List[Tuple[float, float]]:
    """
    :param line_string:
        the ``LineString`` to read values from
    :return:
        a list of angle values, indexed by the offset within
        the ``line_string``
    """
    angles = []
    offsets = []
    coords = line_string.coords
    offset = 0
    for i in range(len(coords) - 1):
        coord_a = coords[i]
        coord_b = coords[i + 1]
        distance = math.hypot(coord_b[0] - coord_a[0], coord_b[1] - coord_a[1])
        angle = math.atan2(coord_b[1] - coord_a[1], coord_b[0] - coord_a[0])
        angles.append(angle)
        offsets.append(offset)
        offset += distance
    return list(zip(offsets, angles))


def angle_at_offset(
        angles_at_offsets_list: List[Tuple[float, float]],
        offset: float
) -> float:
    """
    :param angles_at_offsets_list:
        a list of angle values, indexed by the offset
    :param offset:
        the offset value to look for
    :return:
        the angle at a specific offset in the ``angles_at_offsets``
    """
    if offset < 0:
        raise ValueError("offset cannot be less than 0")
    for i in range(len(angles_at_offsets_list)):
        angle_offset, angle = angles_at_offsets_list[i]
        _, previous_angle = angles_at_offsets_list[i - 1]
        if angle_offset > offset:
            return previous_angle
    return angles_at_offsets_list[-1][1]


def reverse(line_string: LineString) -> LineString:
    return LineString(list(line_string.coords)[::-1])


def parallel_offset_with_matching_direction(
        line_string: LineString,
        distance: float,
        side: Side = Side.RIGHT,
        resolution: int = 16,
        join_style: int = JOIN_STYLE.round,
        mitre_limit: float = 5,
        is_flipped: bool = True
) -> Tuple[Optional[LineString], bool]:
    if is_flipped:
        side = side.flipped
    result = line_string.parallel_offset(
        distance,
        side=side.value,
        resolution=resolution,
        join_style=join_style,
        mitre_limit=mitre_limit
    )

    result_reverse = reverse(result)

    input_position_start = line_string.coords[0]
    output_position_start = result.coords[0]
    output_position_end = result_reverse.coords[0]

    position_diff_start = coords_length(
        input_position_start,
        output_position_start
    )
    position_diff_end = coords_length(
        input_position_start,
        output_position_end
    )

    _, input_angle_start = angles_at_offsets(line_string)[0]
    _, output_angle_start = angles_at_offsets(result)[0]
    _, output_angle_end = angles_at_offsets(result_reverse)[0]

    # Is the start position and angle of the output line similar to the input
    # line?
    if position_diff_start == distance and \
       output_angle_start == input_angle_start:
        return result, True

    # Is the start position and angle of the reverse output line similar to the
    # input line?
    if position_diff_end == distance and \
       output_angle_end == input_angle_start:
        return result_reverse, True

    # Is the start position of the output line similar to the input line?
    if position_diff_start == distance:
        return result, True

    # Is the start position of the reverse output line similar to the input
    # line?
    if position_diff_end == distance:
        return result_reverse, True

    # Give up, there is no other precise way to know exactly what the correct
    # direction should be.
    return result, False

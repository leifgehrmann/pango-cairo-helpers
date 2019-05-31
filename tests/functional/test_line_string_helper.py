from typing import List, Tuple, Optional

import pytest
from shapely.geometry import LineString, Point, JOIN_STYLE, MultiLineString
from pangocairohelpers import line_string_helper as helper, Side
import math


test_get_lrt_and_rtl_length_data = [
    (LineString([[0, 0], [1, 0], [2, 0]]), 2, 0),
    (LineString([[2, 0], [1, 0], [0, 0]]), 0, 2),
    (LineString([[0, 0], [1, 0], [0, 1], [1, 1]]), 2, math.sqrt(2)),
]


@pytest.mark.parametrize(
    "line_string,expected_lrt,expected_rtl",
    test_get_lrt_and_rtl_length_data
)
def test_get_lrt_and_rtl_length(
        line_string: LineString,
        expected_lrt: float,
        expected_rtl: float
):
    assert helper.left_to_right_length(line_string) == expected_lrt
    assert helper.right_to_left_length(line_string) == expected_rtl


def test_get_rtl_length_is_inverse_ltr_length_for_vertical_lines():
    """
    When the line segments of the LineString are going vertical, it is
    ambiguous whether a line going up is "lrt" or "rtl". Therefore, the
    LineStrings length should be identical regardless of direction.
    """
    line_string = LineString([[0, 0], [0, 1], [0, 2]])
    ltr_length = helper.left_to_right_length(line_string)
    rtl_length = helper.right_to_left_length(line_string)
    assert ltr_length == rtl_length

    # invert the line_string coordinates
    line_string.coords = list(line_string.coords)[::-1]
    ltr_length = helper.left_to_right_length(line_string)
    rtl_length = helper.right_to_left_length(line_string)
    assert ltr_length == rtl_length


test_interpolated_distance_of_point_on_line_data = [
    # On line
    (LineString([[0, 0], [0, 1], [0, 2]]), Point([0, 0.5]), 0.5),
    (LineString([[0, 0], [0.5, 1], [0, 2]]), Point([0.5, 1]), math.sqrt(1.25)),
    (LineString([[0, 0], [0, 1], [0, 2]]), Point([0, 3]), 2),
    # Off line
    (LineString([[0, 0], [0.5, 1], [0, 2]]), Point([1, 1]), math.sqrt(1.25)),
]


@pytest.mark.parametrize(
    "line_string,point,expected_distance",
    test_interpolated_distance_of_point_on_line_data
)
def test_interpolated_distance_of_point_on_line(
        line_string: LineString,
        point: Point,
        expected_distance: float
):
    distance = helper.interpolated_distance_of_point(line_string, point)
    assert isinstance(distance, float)
    assert distance == expected_distance


test_points_at_distance_from_point_on_line_string_data = [
    (LineString([[0, 0], [0, 1], [0, 2]]), Point([0, 1]), 0.5, 2),
    (LineString([[0, 0], [0, 1], [0, 2]]), Point([0, 2]), 0.5, 1),
    (LineString([[0, 0], [0, 1], [0, 2]]), Point([0, 3]), 0.5, 0)
]


@pytest.mark.parametrize(
    "line_string,point,distance,expected_count",
    test_points_at_distance_from_point_on_line_string_data
)
def test_points_at_distance_from_point_on_line_string(
        line_string: LineString,
        point: Point,
        distance: float,
        expected_count: int
):
    intersections = helper.points_at_distance_from_point_on_line_string(
        line_string,
        point,
        distance
    )

    assert len(intersections) == expected_count
    for intersection in intersections:
        assert isinstance(intersection, Point)


def test_points_at_distance_from_point_on_line_string_raises_value_error():
    line_string = LineString(Point([0, 0]).buffer(1).exterior.coords)
    point = Point([0, 0])
    distance = 1
    with pytest.raises(ValueError):
        helper.points_at_distance_from_point_on_line_string(
            line_string,
            point,
            distance
        )


test_next_offset_from_offset_in_line_string_data = [
    # Basic x-axis tests
    (LineString([[0, 0], [10, 0]]), 3, 1, 4),
    (LineString([[2, 0], [10, 0]]), 9, 1.5, None),
    (LineString([[0, 0], [10, 0]]), 0, 10, 10),
    # Test x-y axis
    (LineString([[0, 0], [0, 1], [1, 0], [3, 0]]), 0, 2, math.sqrt(2) + 2),
    # Test multiple choice example
    (LineString([[0, 0], [2, 0], [0, 1], [2, 1]]), 1, 0.5, 1.5),
]


@pytest.mark.parametrize(
    "line_string,current_offset,distance,expected_next_offset",
    test_next_offset_from_offset_in_line_string_data
)
def test_next_offset_from_offset_in_line_string(
        line_string: LineString,
        current_offset: float,
        distance: float,
        expected_next_offset: float
):
    next_offset = helper.next_offset_from_offset_in_line_string(
        line_string,
        current_offset,
        distance
    )
    if expected_next_offset is None:
        assert next_offset is None
    else:
        assert next_offset == expected_next_offset


test_angles_at_offsets_data = [
    # Horizontal
    (
        LineString([[0, 0], [2, 0], [0, 0]]), [(0, 0), (2, math.pi)]
    ),
    # Vertical
    (
        LineString([[0, 0], [0, 2], [0, 0]]),
        [(0, math.pi / 2), (2, -math.pi / 2)]
    ),
    # Diagonal
    (
        LineString([[0, 0], [1, 1], [0, 0]]),
        [(0, math.pi / 4), (math.sqrt(2), -math.pi * 3 / 4)]
    ),
    # Multiple
    (
        LineString([[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]]),
        [(0, 0), (1, 0), (2, 0), (3, 0)]
    ),
]


@pytest.mark.parametrize(
    "line_string,expected_angles_at_offsets",
    test_angles_at_offsets_data
)
def test_angles_at_offsets(
        line_string: LineString,
        expected_angles_at_offsets: List[Tuple[float, float]],
):
    angles_at_offsets = helper.angles_at_offsets(
        line_string,
    )
    assert angles_at_offsets == expected_angles_at_offsets


test_angle_at_offset_data = [
    ([(0, 0), (2, math.pi)], 0, 0),
    ([(0, 0), (2, math.pi)], 1, 0),
    ([(0, 0), (2, math.pi)], 2, math.pi),
    ([(0, 0), (2, math.pi)], 3, math.pi),
    ([(0, math.pi / 2), (2, -math.pi / 2)], 1, math.pi / 2),
    ([(0, math.pi / 2), (2, -math.pi / 2)], 2, -math.pi / 2),
    ([(0, 0), (1, 1), (2, 0), (3, 1)], 3, 1),
    ([(0, 0), (1, 1), (2, 0), (3, 1)], 2.4223, 0),
]


@pytest.mark.parametrize(
    "angles_at_offsets,offset,expected_angle",
    test_angle_at_offset_data
)
def test_angle_at_offset(
        angles_at_offsets: List[Tuple[float, float]],
        offset: float,
        expected_angle: float
):
    angle_at_offset = helper.angle_at_offset(
        angles_at_offsets,
        offset
    )
    assert angle_at_offset == expected_angle


def test_angle_at_offset_raises_error_on_invalid_offset():
    with pytest.raises(ValueError):
        helper.angle_at_offset(
            [(0, 1), (1, 2), (3, 1)],
            -1.34
        )


test_reverse_data = [
    (
        LineString([[0, 0], [10, 10], [20, 0]]),
        LineString([[20, 0], [10, 10], [0, 0]])
    )
]


@pytest.mark.parametrize(
    "line_string,expected_output",
    test_reverse_data
)
def test_reverse(line_string: LineString, expected_output: LineString):
    output = helper.reverse(line_string)
    assert list(expected_output.coords) == list(output.coords)


test_substring_data = [
    (
        LineString([[0, 0], [10, 10], [20, 0]]),
        0,
        None,
        LineString([[0, 0], [10, 10], [20, 0]])
    )
]


@pytest.mark.parametrize(
    "line_string,start,end,expected_output",
    test_substring_data
)
def test_substring(
        line_string: LineString,
        start: float,
        end: Optional[float],
        expected_output: LineString
):
    output = helper.substring(line_string, start, end)
    assert list(output.coords) == list(expected_output.coords)


test_parallel_offset_with_matching_direction_data = [
    (
        LineString([[10, 10], [20, 10]]),
        10,
        Side.LEFT,
        LineString([[10, 0], [20, 0]]),
        True
    ),
    (
        LineString([[10, 10], [10, 20]]),
        10,
        Side.LEFT,
        LineString([[20, 10], [20, 20]]),
        True
    ),
    (
        LineString([[10, 10], [0, 10]]),
        10,
        Side.LEFT,
        LineString([[10, 20], [0, 20]]),
        True
    ),
    (
        LineString([[10, 10], [10, 0]]),
        10,
        Side.LEFT,
        LineString([[0, 10], [0, 0]]),
        True
    ),
    (
        LineString([[0, 0], [10, 0], [10, 20]]),
        10,
        Side.RIGHT,
        LineString([[0, 10], [0, 20]]),
        True
    ),
    (
        LineString([[10, 20], [20, 20], [20, 0], [0, 0]]),
        10,
        Side.RIGHT,
        LineString([[10, 30], [30, 30], [30, -10], [0, -10]]),
        True
    ),
    (
        LineString([[0, 0], [40, 0], [40, 30], [10, 30], [10, 10], [0, 10]]),
        10,
        Side.RIGHT,
        LineString([[20, 10], [30, 10], [30, 20], [20, 20], [20, 10]]),
        False
    ),
    (
        LineString([[10, 50], [50, 50], [90, 90]]),
        -10.0,
        Side.RIGHT,
        LineString([
            [10, 40],
            [54.14213562373096, 40],
            [97.07106781186548, 82.92893218813452]
        ]),
        True
    )
]


@pytest.mark.parametrize(
    "line_string,distance,side,expected_output,expected_correct_direction",
    test_parallel_offset_with_matching_direction_data
)
def test_parallel_offset_with_matching_direction(
        line_string: LineString,
        distance: float,
        side: Side,
        expected_output: LineString,
        expected_correct_direction: bool
):
    offset_line_string, correct_direction = helper.\
        parallel_offset_with_matching_direction(
            line_string,
            distance,
            side=side,
            join_style=JOIN_STYLE.mitre,
            is_flipped=True
        )

    assert expected_correct_direction is correct_direction

    if correct_direction is True:
        assert list(offset_line_string.coords) == list(expected_output.coords)
    else:
        assert list(offset_line_string.coords) == list(expected_output.coords)\
         or \
         list(helper.reverse(offset_line_string).coords) == \
         list(expected_output.coords)

    # Now assert the inverse direction
    line_string = helper.reverse(line_string)
    expected_output = helper.reverse(expected_output)
    offset_line_string, correct_direction = helper.\
        parallel_offset_with_matching_direction(
            line_string,
            distance,
            side=side.flipped,
            join_style=JOIN_STYLE.mitre,
            is_flipped=True
        )

    assert expected_correct_direction is correct_direction

    if correct_direction is True:
        assert list(offset_line_string.coords) == list(expected_output.coords)
    else:
        assert list(offset_line_string.coords) == list(expected_output.coords)\
               or \
               list(helper.reverse(offset_line_string).coords) == \
               list(expected_output.coords)


def test_parallel_offset_with_matching_direction_empty():
    line_string = LineString([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
    ])
    distance = 1

    offset_line_string, correct_direction = helper.\
        parallel_offset_with_matching_direction(
            line_string,
            distance,
            side=Side.RIGHT,
            join_style=JOIN_STYLE.mitre,
            is_flipped=True
        )

    assert offset_line_string.is_empty and correct_direction is False


def test_parallel_offset_with_matching_direction_multi_linear_ring():
    line_string = LineString([
        [0, 0],
        [2, 0],
        [1.2, 1],
        [2, 2],
        [0, 2],
        [0.8, 1],
        [0, 0],
    ])
    distance = 0.2

    offset_line_string, correct_direction = helper.\
        parallel_offset_with_matching_direction(
            line_string,
            distance,
            side=Side.RIGHT,
            join_style=JOIN_STYLE.mitre,
            is_flipped=True
        )

    assert isinstance(offset_line_string, MultiLineString) and \
        correct_direction is False

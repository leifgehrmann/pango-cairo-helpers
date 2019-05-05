from typing import List, Tuple

import pytest
from shapely.geometry import LineString, Point
from pangocairohelpers import line_string_helper as helper
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

import pytest
from shapely.geometry import LineString
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

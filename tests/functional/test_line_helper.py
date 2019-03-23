from pangocairohelpers import line_helper
import math


def test_coords_length():
    assert line_helper.coords_length((0, 0), (1, 0)) == 1
    assert line_helper.coords_length((0, 0), (0, 1)) == 1
    assert line_helper.coords_length((0, 0), (1, 1)) == math.sqrt(2)


def test_are_coords_left_to_right():
    assert line_helper.coords_are_left_to_right((0, 0), (1, 0)) is True
    assert line_helper.coords_are_left_to_right((1, 0), (0, 0)) is False
    assert line_helper.coords_are_left_to_right((0, 0), (0, 0)) is None
    assert line_helper.coords_are_left_to_right((2, 0), (2, 1)) is None

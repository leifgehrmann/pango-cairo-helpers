import math

import pytest
from shapely.geometry import Point

from pangocairohelpers.point_helper import add_polar_vector

test_add_polar_vector_data = [
    # All directions (from -2pi to 2pi)
    (Point([1, 1]), math.pi * -4 / 2, 1, Point(2, 1)),
    (Point([1, 1]), math.pi * -3 / 2, 1, Point(1, 2)),
    (Point([1, 1]), math.pi * -2 / 2, 1, Point(0, 1)),
    (Point([1, 1]), math.pi * -1 / 2, 1, Point(1, 0)),
    (Point([1, 1]), math.pi * 0 / 2, 1, Point(2, 1)),
    (Point([1, 1]), math.pi * 1 / 2, 1, Point(1, 2)),
    (Point([1, 1]), math.pi * 2 / 2, 1, Point(0, 1)),
    (Point([1, 1]), math.pi * 3 / 2, 1, Point(1, 0)),
    (Point([1, 1]), math.pi * 4 / 2, 1, Point(2, 1)),
    # Various magnitudes
    (Point([1, 1]), 0, 0.123, Point(1.123, 1)),
    (Point([1, 1]), 0, 123.4, Point(124.4, 1)),
]


@pytest.mark.parametrize(
    "point,angle,magnitude,expected_output",
    test_add_polar_vector_data
)
def test_add_polar_vector(
        point: Point,
        angle: float,
        magnitude: float,
        expected_output: Point
):
    output = add_polar_vector(point, angle, magnitude)
    assert math.isclose(output.x, expected_output.x)
    assert math.isclose(output.y, expected_output.y)

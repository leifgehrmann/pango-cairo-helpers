import unittest
from shapely.geometry import LineString
from pangocairohelpers import LineStringHelper


class TestLineStringHelper(unittest.TestCase):

    def test_get_left_to_right_length(self):
        line_string = LineString([[0, 0], [1, 0]])
        helper = LineStringHelper(line_string)
        assert helper.get_left_to_right_length() == 1

        line_string = LineString([[1, 0], [0, 0]])
        helper = LineStringHelper(line_string)
        # assert helper.get_left_to_right_length() == 0

    def test_get_right_to_left_length(self):
        line_string = LineString([[0, 0], [1, 0]])
        helper = LineStringHelper(line_string)
        # assert helper.get_right_to_left_length() == 0

        line_string = LineString([[1, 0], [0, 0]])
        helper = LineStringHelper(line_string)
        assert helper.get_right_to_left_length() == 1

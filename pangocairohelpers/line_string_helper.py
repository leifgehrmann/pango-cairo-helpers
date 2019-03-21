from shapely.geometry import LineString


class LineStringHelper:

    def __init__(self, line_string: LineString):
        self.line_string = line_string

    def get_left_to_right_length(self) -> float:
        """
        :return:
            the length of all the line segments that go left (-x) to
            right (+x)
        """
        return self.line_string.length

    def get_right_to_left_length(self) -> float:
        """
        :return:
            the length of all the line segments that go right (+x) to
            left (-x)
        """
        return self.line_string.length

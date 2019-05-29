from abc import ABCMeta

from pangocffi import Layout
from shapely.geometry import LineString


class TextPathAbstract(object, metaclass=ABCMeta):

    def __init__(
            self,
            line_string: LineString,
            layout: Layout
    ):
        self._layout = layout
        self._input_line_string = line_string

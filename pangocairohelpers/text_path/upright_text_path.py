from pangocffi import Layout
from typing import Optional

from cairocffi import Context
from shapely.geometry import MultiPolygon, LineString

from pangocairohelpers import line_string_helper
from pangocairohelpers.text_path import TextPathAbstract, TextPath


class UprightTextPath(TextPathAbstract):
    """
    A TextPath that when drawn, will always try to make sure the glyphs are
    never rendered upside down for poor readability.
    """

    def __init__(self, line_string: LineString, layout: Layout):
        super().__init__(line_string, layout)
        self._text_path = None  # type: Optional[TextPath]

    def _compute_best_text_path(self):
        text_path_a = TextPath(self._input_line_string, self._layout)
        text_path_a.side = self._side
        text_path_a.alignment = self._alignment
        text_path_a.start_offset = self._start_offset
        text_path_a.vertical_offset = self._vertical_offset
        text_path_a.layout_engine_class = self._layout_engine_class

        text_path_b = TextPath(self._input_line_string, self._layout)
        text_path_b.side = self._side.flipped
        text_path_b.alignment = self._alignment
        text_path_b.start_offset = self._start_offset
        text_path_b.vertical_offset = self._vertical_offset
        text_path_b.layout_engine_class = self._layout_engine_class

        baseline_a = text_path_a.compute_baseline()
        baseline_b = text_path_b.compute_baseline()

        ltr_length_a = line_string_helper.left_to_right_length(baseline_a)
        ltr_length_b = line_string_helper.left_to_right_length(baseline_b)

        if ltr_length_a > ltr_length_b:
            self._text_path = text_path_a
        else:
            self._text_path = text_path_b

    def text_fits(self) -> bool:
        self._compute_best_text_path()
        return self._text_path.text_fits()
        pass

    def compute_baseline(self) -> Optional[LineString]:
        self._compute_best_text_path()
        return self._text_path.compute_baseline()

    def compute_boundaries(self) -> MultiPolygon:
        self._compute_best_text_path()
        return self._text_path.compute_boundaries()

    def draw(self, context: Context):
        self._compute_best_text_path()
        return self._text_path.draw(context)

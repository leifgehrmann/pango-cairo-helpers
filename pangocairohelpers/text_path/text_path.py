from typing import Optional, List

from cairocffi import Context
from pangocffi import Layout
from shapely.geometry import LineString, MultiPolygon
from pangocairocffi.render_functions import show_glyph_item

from pangocairohelpers import Side, point_helper
from pangocairohelpers.line_string_helper import reverse, substring, \
    parallel_offset_with_matching_direction
from pangocairohelpers.text_path import TextPathAbstract, TextPathGlyphItem


class TextPath(TextPathAbstract):
    """
    Renders text similar to the behaviour found in SVG's ``<textPath>``.

    ``line_string`` behaves as the baseline for the text in the layout.

    Multi-line layouts are not supported and will throw an error.

    Left-to-right text is assumed.
    """

    def __init__(
            self,
            line_string: LineString,
            layout: Layout
    ):
        """
        :param line_string:
            a ``LineString`` for the text to follow
        :param layout:
            the layout to apply to the ``line_string``
        """
        super().__init__(line_string, layout)

        self._modified_line_string = None  # type: Optional[LineString]
        self._text_path_glyph_items = None  \
            # type: Optional[List[TextPathGlyphItem]]

    def _generate_modified_line_string(self):
        self._modified_line_string = self._input_line_string
        if self._side == Side.RIGHT:
            self._modified_line_string = reverse(self._modified_line_string)

        if self._vertical_offset != 0:
            self._modified_line_string, matched_direction = \
                parallel_offset_with_matching_direction(
                    self._modified_line_string,
                    self._vertical_offset,
                    side=Side.LEFT
                )

            if not isinstance(self._modified_line_string, LineString) or \
                    self._modified_line_string.is_empty:
                self._modified_line_string = None
                raise RuntimeError("Failed to offset linestring. "
                                   "Non-linestring object returned.")

            if not matched_direction:
                self._modified_line_string = None
                raise RuntimeError("Failed to offset linestring. "
                                   "Direction could not be established.")

    def _generate_layout_engine(self):
        self._generate_modified_line_string()

        if not isinstance(self._layout_engine, self._layout_engine_class) or \
                self._layout_engine is None:
            self._layout_engine = self.layout_engine_class(
                self._modified_line_string,
                self._layout_clusters
            )

        if self._layout_engine.alignment != self._alignment:
            self._layout_engine.alignment = self._alignment

        if self._layout_engine.start_offset != self._start_offset:
            self._layout_engine.start_offset = self._start_offset

    def _compute_text_path_glyph_items(self) -> List[TextPathGlyphItem]:
        self._generate_layout_engine()
        self._text_path_glyph_items = self._layout_engine. \
            generate_text_path_glyph_items()
        return self._text_path_glyph_items

    def text_fits(self) -> bool:
        text_path_glyph_items = self._compute_text_path_glyph_items()
        number_of_laid_out_glyphs = len(text_path_glyph_items)
        number_of_total_glyphs = len(self._layout_clusters.get_clusters())
        return number_of_laid_out_glyphs == number_of_total_glyphs

    def compute_baseline(self) -> Optional[LineString]:
        text_path_glyph_items = self._compute_text_path_glyph_items()

        # Get the start position
        start_point = text_path_glyph_items[0].position

        # Get the end position
        end_glyph = text_path_glyph_items[-1]
        end_point = point_helper.add_polar_vector(
            end_glyph.position,
            end_glyph.rotation,
            end_glyph.logical_extent.width
        )

        start_offset = self._modified_line_string.project(start_point)
        end_offset = self._modified_line_string.project(end_point)

        return substring(self._modified_line_string, start_offset, end_offset)

    def compute_boundaries(self) -> Optional[MultiPolygon]:
        pass

    def draw(self, context: Context):
        text_path_glyph_items = self._compute_text_path_glyph_items()
        for text_path_glyph_item in text_path_glyph_items:
            glyph_position = text_path_glyph_item.position
            glyph_rotation = text_path_glyph_item.rotation

            context.save()
            context.translate(glyph_position.x, glyph_position.y)
            context.rotate(glyph_rotation)
            show_glyph_item(
                context,
                self._layout_text,
                text_path_glyph_item.glyph_item
            )
            context.restore()

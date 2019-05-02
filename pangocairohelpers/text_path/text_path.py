from typing import List

from cairocffi import Context
from pangocffi import Layout, Alignment
from shapely.geometry import LineString, MultiPolygon
from pangocairocffi.render_functions import show_glyph_item

from pangocairohelpers import LayoutClusters
from pangocairohelpers.text_path import TextPathGlyphItem


class TextPath:
    """
    Renders text similar to the behaviour found in SVG's ``<textPath>``.

    ``line_string`` behaves as the baseline for the text in the layout.

    Multi-line layouts are not supported and will throw an error.

    Left-to-right text is assumed.
    """

    def __init__(
            self,
            line_string: LineString,
            layout: Layout,
            alignment: Alignment = Alignment.LEFT
    ):
        if layout.get_line_count() > 1:
            raise ValueError('layout cannot be more than one line.')

        self.layout = layout
        self.layout_text = layout.get_text()
        self.line_string = line_string
        self.layout_clusters = LayoutClusters(self.layout)
        self.alignment = alignment

    def text_fits(self) -> bool:
        # Todo: is this algorithm realistic?
        last_position = self.layout_clusters.get_logical_positions()[-1]
        return last_position.x < self.line_string.length

    def get_text_path_glyph_items(self) -> List[TextPathGlyphItem]:
        # Todo: Make this function correct
        glyph_items = self.layout_clusters.get_clusters()
        logical_positions = self.layout_clusters.get_logical_positions()
        text_path_glyph_items = []
        for glyph_item, logical_position in zip(glyph_items, logical_positions):
            glyph_start_position = self.line_string.interpolate(
                logical_position.x
            )
            text_path_glyph_item = TextPathGlyphItem(
                glyph_item,
                glyph_start_position,
                0
            )
            text_path_glyph_items.append(text_path_glyph_item)
        return text_path_glyph_items

    def compute_boundaries(self) -> MultiPolygon:
        # Todo:
        pass

    def draw(self, context: Context):
        text_path_glyph_items = self.get_text_path_glyph_items()
        for text_path_glyph_item in text_path_glyph_items:
            glyph_position = text_path_glyph_item.position
            glyph_rotation = text_path_glyph_item.rotation

            context.save()
            context.translate(glyph_position.x, glyph_position.y)
            context.rotate(glyph_rotation)
            show_glyph_item(
                context,
                self.layout_text,
                text_path_glyph_item.glyph_item
            )
            context.restore()


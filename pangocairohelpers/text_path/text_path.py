from typing import List

from cairocffi import Context
from pangocffi import Layout
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

    def __init__(self, line_string: LineString, layout: Layout):
        self.layout = layout
        self.layout_text = layout.get_text()
        self.line_string = line_string
        self.layout_clusters = LayoutClusters(self.layout)

        # Todo: throw an error if the layout is multi-lined

    def text_fits(self) -> bool:
        last_position = self.layout_clusters.get_logical_positions()[-1]
        return last_position.x < self.line_string.length

    def get_text_path_glyph_items(self) -> List[TextPathGlyphItem]:
        glyph_items = self.layout_clusters.get_clusters()
        logical_positions = self.layout_clusters.get_logical_positions()
        text_path_glyph_items = []
        for glyph_item, logical_position in zip(glyph_items, logical_positions):
            text_path_glyph_item = TextPathGlyphItem(
                glyph_item,
                logical_position,
                0
            )
            text_path_glyph_items.append(text_path_glyph_item)
        return text_path_glyph_items

    def compute_boundaries(self) -> MultiPolygon:
        pass

    def draw(self, context: Context):
        text_path_glyph_items = self.get_text_path_glyph_items()
        for text_path_glyph_item in text_path_glyph_items:
            show_glyph_item(
                context,
                self.layout_text,
                text_path_glyph_item.glyph_item
            )


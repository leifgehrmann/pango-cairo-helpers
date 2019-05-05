from typing import List, Tuple

from pangocffi import Alignment
from shapely.geometry import LineString

from pangocairohelpers import LayoutClusters
from pangocairohelpers import line_string_helper
from pangocairohelpers.text_path import TextPathGlyphItem


class StandardLayoutEngine:

    def __init__(
            self,
            line_string: LineString,
            layout_clusters: LayoutClusters,
            alignment: Alignment = Alignment.LEFT
    ):
        self.line_string = line_string
        self.layout_clusters = layout_clusters
        self.alignment = alignment
        self.start_offset = 0

    # def _find_

    def generate_text_path_glyph_items(self) -> List[TextPathGlyphItem]:
        text_path_glyph_items = []

        angles_at_offsets = line_string_helper.angles_at_offsets(
            self.line_string
        )

        line_string_length = self.line_string.length

        glyph_items = self.layout_clusters.get_clusters()
        extents = self.layout_clusters.get_logical_extents()
        glyph_items_and_extents = zip(glyph_items, extents)
        for glyph_item, extent in glyph_items_and_extents:

            offset = self.start_offset + extent.x

            # Cut off rendering the rest of the text if there no more space
            # to layout the text
            if line_string_length < offset:
                break

            position = self.line_string.interpolate(offset)
            rotation = line_string_helper.angle_at_offset(
                angles_at_offsets, offset
            )

            text_path_glyph_item = TextPathGlyphItem(
                glyph_item,
                position,
                rotation
            )
            text_path_glyph_items.append(text_path_glyph_item)

        return text_path_glyph_items

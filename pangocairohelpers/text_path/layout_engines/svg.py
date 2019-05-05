import math
from typing import List

from pangocffi import Alignment
from shapely.geometry import LineString

from pangocairohelpers import LayoutClusters, point_helper
from pangocairohelpers import line_string_helper
from pangocairohelpers.text_path import TextPathGlyphItem


class Svg:

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

            glyph_width = extent.width
            offset = self.start_offset + extent.x + glyph_width / 2

            # Cut off rendering the rest of the text if there no more space
            # to layout the text
            if line_string_length < offset:
                break

            center_position = self.line_string.interpolate(offset)
            rotation = line_string_helper.angle_at_offset(
                angles_at_offsets, offset
            )

            left_position = point_helper.add_polar_vector(
                center_position, rotation + math.pi, glyph_width / 2
            )

            text_path_glyph_item = TextPathGlyphItem(
                glyph_item,
                left_position,
                rotation
            )
            text_path_glyph_items.append(text_path_glyph_item)

        return text_path_glyph_items

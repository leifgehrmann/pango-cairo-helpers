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
            layout_clusters: LayoutClusters
    ):
        self.line_string = line_string
        self.layout_clusters = layout_clusters
        self._alignment = Alignment.LEFT
        self._start_offset = 0

    @property
    def alignment(self) -> Alignment:
        return self._alignment

    @alignment.setter
    def alignment(self, value: Alignment):
        self._alignment = value

    @property
    def start_offset(self) -> float:
        return float(self._start_offset)

    @start_offset.setter
    def start_offset(self, value: float):
        self._start_offset = float(value)

    def _get_aligned_start_offset(self) -> float:
        """
        :return:
            the offset along the line_string where the first character should
            begin.
        """
        if self._alignment == Alignment.CENTER:
            return self._get_center_aligned_start_offset()
        if self._alignment == Alignment.RIGHT:
            return self._get_right_aligned_start_offset()
        # Default to left
        return self._get_left_aligned_start_offset()

    def _get_left_aligned_start_offset(self) -> float:
        # Todo: This assumes we don't allow clipping of text at the beginning
        return self.start_offset

    def _get_center_aligned_start_offset(self) -> float:
        layout_extent = self.layout_clusters.get_max_logical_extent()
        # Todo: This assumes we don't allow clipping of text at the beginning
        if layout_extent.width > self.line_string.length:
            return self._get_left_aligned_start_offset()
        return (self.line_string.length - layout_extent.width) / 2 + \
            self.start_offset

    def _get_right_aligned_start_offset(self) -> float:
        layout_extent = self.layout_clusters.get_max_logical_extent()
        # Todo: This assumes we don't allow clipping of text at the beginning
        if layout_extent.width > self.line_string.length:
            return self._get_left_aligned_start_offset()
        return self.line_string.length - layout_extent.width + \
            self.start_offset

    def generate_text_path_glyph_items(self) -> List[TextPathGlyphItem]:
        text_path_glyph_items = []

        angles_at_offsets = line_string_helper.angles_at_offsets(
            self.line_string
        )

        line_string_length = self.line_string.length

        alignment_start_offset = self._get_aligned_start_offset()

        glyph_items = self.layout_clusters.get_clusters()
        extents = self.layout_clusters.get_logical_extents()
        glyph_items_and_extents = zip(glyph_items, extents)
        for glyph_item, extent in glyph_items_and_extents:

            glyph_width = extent.width
            offset = alignment_start_offset + extent.x + glyph_width / 2

            # Cut off rendering the rest of the text if there no more space
            # to layout the text
            if line_string_length < offset:
                break

            center_position = self.line_string.interpolate(offset)

            # Todo: hack
            if offset <= 0:
                continue

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

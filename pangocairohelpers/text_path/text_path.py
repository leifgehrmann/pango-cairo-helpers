import math
from typing import List, Optional, Tuple

from cairocffi import Context
from pangocffi import Layout, Alignment
from shapely.geometry import LineString, MultiPolygon
from pangocairocffi.render_functions import show_glyph_item

from pangocairohelpers import LayoutClusters
from pangocairohelpers.text_path import TextPathGlyphItem, StandardLayoutEngine
from pangocairohelpers import line_string_helper


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
        self.layout_engine = StandardLayoutEngine(
            self.line_string,
            self.layout_clusters,
            self.alignment
        )
        self.text_path_glyph_items = None

    def text_fits(self) -> bool:
        # Todo: is this algorithm realistic?
        last_position = self.layout_clusters.get_logical_extents()[-1]
        return last_position.x < self.line_string.length

    def _calculate_rotation_between_two_offsets(
            self,
            offset_a: float,
            offset_b: float
    ):
        """
        :param offset_a:
            the starting offset
        :param offset_b: 
            the ending offset
        :return:
            the rotation in radians relative to the positive x axis 
        """
        offset_a_point = self.line_string.interpolate(offset_a)
        offset_b_point = self.line_string.interpolate(offset_b)
        return math.atan2(
            offset_b_point.y - offset_a_point.y,
            offset_b_point.x - offset_a_point.x
        )

    def _calculate_rotation_for_glyph_item_at_offset(
            self,
            offset: float,
            distance: float
    ) -> Optional[float]:
        """
        :param offset:
        :param distance:

        :return:
            the angle that this glyph must use when following the path.
        """
        new_offset = line_string_helper.next_offset_from_offset_in_line_string(
            self.line_string,
            offset,
            distance
        )
        if new_offset is None:
            return None
        offset_point = self.line_string.interpolate(offset)
        new_offset_point = self.line_string.interpolate(new_offset)
        return math.atan2(
            new_offset_point.y - offset_point.y,
            new_offset_point.x - offset_point.x
        )
    
    def get_rotation_and_next_offset_for_glyph_item(
            self,
            logical_width: float,
            offset: float
    ) -> Optional[Tuple[float, float]]:
        """
        :param logical_width:
            the logical width of the glyph item
        :param offset: 
            the offset to start from
        :return:
            a tuple of rotation and the next offset to start the next
            glyph item. ``None`` if there are no more offsets to reach
        """
        new_offset = line_string_helper.next_offset_from_offset_in_line_string(
            self.line_string,
            offset,
            logical_width
        )
        if new_offset is None:
            return None
        
        rotation = self._calculate_rotation_for_glyph_item_at_offset(
            offset,
            new_offset
        )
        return rotation, new_offset

    def _compute_text_path_glyph_items(self):
        if self.text_path_glyph_items is None:
            self.text_path_glyph_items = self.layout_engine. \
                generate_text_path_glyph_items()
        return self.text_path_glyph_items

    def compute_boundaries(self) -> MultiPolygon:
        # Todo:
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
                self.layout_text,
                text_path_glyph_item.glyph_item
            )
            context.restore()


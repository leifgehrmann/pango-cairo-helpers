from pangocffi import GlyphItem
from shapely.geometry import Point

from pangocairohelpers import GlyphExtent


class TextPathGlyphItem:
    """
    An individual glyphItem component that is part of the TextPath
    """

    def __init__(
            self,
            glyph_item: GlyphItem,
            position: Point,
            rotation: float,
            logical_extent: GlyphExtent
    ):
        self.glyph_item = glyph_item
        self.position = position
        self.rotation = rotation
        self.logical_extent = logical_extent

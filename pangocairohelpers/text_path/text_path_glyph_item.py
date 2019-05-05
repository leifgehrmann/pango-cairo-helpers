from pangocffi import GlyphItem
from shapely.geometry import Point


class TextPathGlyphItem:
    """
    An individual glyphItem component that is part of the TextPath
    """

    def __init__(
            self,
            glyph_item: GlyphItem,
            position: Point,
            rotation: float
    ):
        self.glyph_item = glyph_item
        self.position = position
        self.rotation = rotation

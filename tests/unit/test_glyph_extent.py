import unittest

from pangocairohelpers import GlyphExtent


class TestGlyphExtent(unittest.TestCase):

    def test_constructor(self):
        glyph_extent = GlyphExtent(10, 20, 30, 40, 50)
        assert glyph_extent.x == 10
        assert glyph_extent.y == 20
        assert glyph_extent.width == 30
        assert glyph_extent.height == 40
        assert glyph_extent.baseline == 50

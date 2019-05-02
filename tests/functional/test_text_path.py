from cairocffi import Context, SVGSurface
import pangocairocffi
from shapely.geometry import LineString
import unittest

from pangocairohelpers.text_path import TextPath


class TestTextPath(unittest.TestCase):

    def test_error_is_raised_for_multi_line(self):
        surface = SVGSurface(None, 100, 100)
        cairo_context = Context(surface)
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語\nThis is a text')

        line_string = LineString([[0, 0], [100, 0]])

        with self.assertRaises(ValueError):
            TextPath(line_string, layout)

    def test_glyph(self):
        surface = SVGSurface(None, 100, 100)
        cairo_context = Context(surface)
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [100, 0]])

        text_path = TextPath(line_string, layout)

        surface.finish()

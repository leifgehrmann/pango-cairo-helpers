from typing import Tuple

from cairocffi import Context, SVGSurface, Surface
import pangocairocffi
from shapely.geometry import LineString
import unittest

from pangocairohelpers.text_path import TextPath


class TestTextPath(unittest.TestCase):

    def _create_void_surface(self) -> Tuple[Surface, Context]:
        surface = SVGSurface(None, 100, 100)
        cairo_context = Context(surface)
        return surface, cairo_context

    def _create_real_surface(self) -> Tuple[Surface, Context]:
        surface = SVGSurface('tests/output/test.svg', 100, 100)
        cairo_context = Context(surface)
        return surface, cairo_context

    def test_error_is_raised_for_multi_line(self):
        surface, cairo_context = self._create_void_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語\nThis is a text')

        line_string = LineString([[0, 0], [100, 0]])

        with self.assertRaises(ValueError):
            TextPath(line_string, layout)

    def test_glyph(self):
        surface, cairo_context = self._create_real_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語')

        line_string = LineString([[10, 30], [90, 30]])

        text_path = TextPath(line_string, layout)

        text_path.draw(cairo_context)

        surface.finish()

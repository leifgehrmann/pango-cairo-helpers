from typing import Tuple

from cairocffi import Context, SVGSurface, Surface
import pangocairocffi
from shapely.geometry import LineString
import unittest

from pangocairohelpers.text_path import TextPath
from . import debug


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

    def test_text_fits(self):
        surface, cairo_context = self._create_real_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [600, 0]])
        text_path = TextPath(line_string, layout)
        assert text_path.text_fits()

        line_string = LineString([[0, 0], [50, 0]])
        text_path = TextPath(line_string, layout)
        assert not text_path.text_fits()

    def test_compute_boundaries(self):
        surface, cairo_context = self._create_real_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [100, 0]])
        text_path = TextPath(line_string, layout)
        assert text_path.compute_boundaries() is None

    def test_glyph(self):
        surface, cairo_context = self._create_real_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.set_markup('Hi from Παν語')

        line_string = LineString([[10, 30], [90, 30]])
        text_path = TextPath(line_string, layout)
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        line_string = LineString([[10, 50], [50, 50], [90, 90]])
        text_path = TextPath(line_string, layout)
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        surface.finish()

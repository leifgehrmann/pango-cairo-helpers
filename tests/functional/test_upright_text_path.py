from typing import Tuple

from cairocffi import Context, SVGSurface, Surface
import pangocairocffi
from pangocffi import Alignment
from shapely.affinity import translate
from shapely.geometry import LineString
import unittest

from pangocairohelpers import Side
from pangocairohelpers.text_path import UprightTextPath
from . import debug


class TestUprightTextPath(unittest.TestCase):

    def _create_void_surface(self) -> Tuple[Surface, Context]:
        surface = SVGSurface(None, 100, 100)
        cairo_context = Context(surface)
        return surface, cairo_context

    def _create_real_surface(
            self,
            filename: str,
            width: int = 100,
            height: int = 100
    ) -> Tuple[Surface, Context]:
        surface = SVGSurface(
            'tests/output/text_path_%s' % filename,
            width,
            height
        )
        cairo_context = Context(surface)
        return surface, cairo_context

    def test_text_fits(self):
        surface, cairo_context = self._create_real_surface(
            'upright_text_path_text_fits.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [600, 0]])
        text_path = UprightTextPath(line_string, layout)
        assert text_path.text_fits()

        line_string = LineString([[0, 0], [50, 0]])
        text_path = UprightTextPath(line_string, layout)
        assert not text_path.text_fits()

    def test_compute_baseline(self):
        surface, cairo_context = self._create_real_surface(
            'upright_text_path_compute_baseline.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('<span font="8">Hi from Παν語</span>')

        line_string = LineString([[0, 10], [50, 20], [100, 10]])
        text_path = UprightTextPath(line_string, layout)
        text_path.alignment = Alignment.CENTER
        text_path.draw(cairo_context)

        baseline = text_path.compute_baseline()
        debug.draw_line_string(cairo_context, baseline)
        cairo_context.stroke()

        assert isinstance(baseline, LineString)
        assert baseline.length > 0
        assert baseline.length < line_string.length

        surface.finish()

    def test_compute_boundaries(self):
        surface, cairo_context = self._create_real_surface(
            'upright_text_path_compute_boundaries.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [100, 0]])
        text_path = UprightTextPath(line_string, layout)
        assert text_path.compute_boundaries() is None

    def test_draw(self):
        surface, cairo_context = self._create_real_surface(
            'upright_text_path_draw.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[10, 30], [90, 30]])
        text_path = UprightTextPath(line_string, layout)
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        line_string = LineString([[10, 50], [50, 50], [90, 90]])
        text_path = UprightTextPath(line_string, layout)
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        surface.finish()

    def test_side(self):
        surface, cairo_context = self._create_real_surface(
            'upright_text_path_side.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[10, 30], [50, 30], [90, 70]])
        text_path = UprightTextPath(line_string, layout)
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        line_string = translate(line_string, 0, 20)
        text_path = UprightTextPath(line_string, layout)
        text_path.side = Side.RIGHT
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        surface.finish()

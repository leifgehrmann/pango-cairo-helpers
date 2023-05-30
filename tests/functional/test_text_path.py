from typing import Tuple

from cairocffi import Context, SVGSurface, Surface
import pangocairocffi
from pangocffi import Alignment
from shapely.affinity import translate
from shapely.geometry import LineString
import unittest

from pangocairohelpers import Side
from pangocairohelpers.line_string_helper import \
    parallel_offset_with_matching_direction
from pangocairohelpers.text_path import TextPath
from pangocairohelpers.text_path.layout_engines import Svg
from . import debug


class TestTextPath(unittest.TestCase):

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

    def test_setters_getters(self):
        surface, cairo_context = self._create_void_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [600, 0]])
        text_path = TextPath(line_string, layout)

        assert isinstance(text_path.side, Side)
        assert isinstance(text_path.alignment, Alignment)
        assert isinstance(text_path.start_offset, float)
        assert isinstance(text_path.vertical_offset, float)

        text_path.side = Side.RIGHT
        text_path.alignment = Alignment.RIGHT
        text_path.start_offset = 12
        text_path.vertical_offset = 34

        assert isinstance(text_path.side, Side)
        assert isinstance(text_path.alignment, Alignment)
        assert isinstance(text_path.start_offset, float)
        assert isinstance(text_path.vertical_offset, float)

        text_path.layout_engine_class = Svg

    def test_error_is_raised_for_multi_line(self):
        surface, cairo_context = self._create_void_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語\nThis is a text')

        line_string = LineString([[0, 0], [100, 0]])

        with self.assertRaises(ValueError):
            TextPath(line_string, layout)

    def test_text_fits(self):
        surface, cairo_context = self._create_real_surface('text_fits.svg')
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [600, 0]])
        text_path = TextPath(line_string, layout)
        assert text_path.text_fits()

        line_string = LineString([[0, 0], [50, 0]])
        text_path = TextPath(line_string, layout)
        assert not text_path.text_fits()

    def test_compute_baseline(self):
        surface, cairo_context = self._create_real_surface(
            'compute_baseline.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('<span font="8">Hi from Παν語</span>')

        line_string = LineString([[0, 10], [50, 20], [100, 10]])
        text_path = TextPath(line_string, layout)
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
            'compute_boundaries.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [100, 0]])
        text_path = TextPath(line_string, layout)
        assert text_path.compute_boundaries() is None

    def test_draw(self):
        surface, cairo_context = self._create_real_surface('draw.svg')
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

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

    def test_side(self):
        surface, cairo_context = self._create_real_surface('side.svg')
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[10, 30], [50, 30], [90, 70]])
        text_path = TextPath(line_string, layout)
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        line_string = translate(line_string, 0, 20)
        text_path = TextPath(line_string, layout)
        text_path.side = Side.RIGHT
        text_path.draw(cairo_context)

        debug.draw_line_string(cairo_context, line_string)
        cairo_context.stroke()

        surface.finish()

    def test_alignment_when_no_space(self):
        surface, cairo_context = self._create_real_surface(
            'alignment_with_no_space.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[10, 30], [90, 30]])
        text_path = TextPath(line_string, layout)
        text_path.alignment = Alignment.CENTER
        text_path.draw(cairo_context)
        debug.draw_line_string(cairo_context, line_string)

        cairo_context.stroke()

        line_string = translate(line_string, 0, 25)
        text_path = TextPath(line_string, layout)
        text_path.alignment = Alignment.RIGHT
        text_path.draw(cairo_context)
        debug.draw_line_string(cairo_context, line_string)

        cairo_context.stroke()

        surface.finish()

    def test_alignment(self):
        surface, cairo_context = self._create_real_surface(
            'alignment.svg',
            300,
            100
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('<span font="8">Hi from Παν語</span>')

        start_offsets = [-10, 0, 10]
        alignments = [Alignment.LEFT, Alignment.CENTER, Alignment.RIGHT]

        for start_offset_index, start_offset in enumerate(start_offsets):
            for alignment_index, alignment in enumerate(alignments):
                line_string = LineString([
                    [5, 33 + alignment_index * 20],
                    [30, 23 + alignment_index * 20],
                    [50, 20 + alignment_index * 20],
                    [70, 23 + alignment_index * 20],
                    [95, 33 + alignment_index * 20]
                ])

                line_string = translate(
                    line_string,
                    start_offset_index * 100,
                    0
                )

                text_path = TextPath(line_string, layout)
                text_path.alignment = alignment
                text_path.start_offset = start_offset
                cairo_context.set_source_rgb(0, 0, 0)
                text_path.draw(cairo_context)

                cairo_context.set_source_rgba(0, 0, 0, 0.2)
                debug.draw_line_string(cairo_context, line_string)
                cairo_context.stroke()

        surface.finish()

    def test_vertical_offset_works(self):
        surface, cairo_context = self._create_real_surface(
            'vertical_offset_works.svg'
        )
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[5, 40], [45, 40], [90, 80]])

        for vertical_offset in [-13, 0, 13]:
            offset_linestring, _ = parallel_offset_with_matching_direction(
                line_string,
                vertical_offset,
                side=Side.LEFT
            )
            debug.draw_line_string(cairo_context, offset_linestring)
            red = max(0.0, vertical_offset / 13)
            green = max(0.0, -vertical_offset / 13)
            cairo_context.set_source_rgba(red, green, 0, 0.2)
            cairo_context.stroke()

            text_path = TextPath(line_string, layout)
            text_path.vertical_offset = vertical_offset
            cairo_context.set_source_rgb(red, green, 0)
            text_path.draw(cairo_context)

        surface.finish()

    def test_vertical_offset_fails_on_uncertain_direction(self):
        surface, cairo_context = self._create_void_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [1, 0], [0, 1]])
        text_path = TextPath(line_string, layout)
        text_path.vertical_offset = -10

        with self.assertRaises(RuntimeError):
            text_path.draw(cairo_context)

    def test_vertical_offset_fails_on_invalid_offset_shape(self):
        surface, cairo_context = self._create_void_surface()
        layout = pangocairocffi.create_layout(cairo_context)
        layout.apply_markup('Hi from Παν語')

        line_string = LineString([[0, 0], [40, 0], [40, 40], [0, 40], [0, 0]])
        text_path = TextPath(line_string, layout)
        text_path.vertical_offset = -10

        with self.assertRaises(RuntimeError):
            text_path.draw(cairo_context)

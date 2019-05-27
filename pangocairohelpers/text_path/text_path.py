from typing import TypeVar, Type

from cairocffi import Context
from pangocffi import Layout, Alignment
from shapely.geometry import LineString, MultiPolygon
from pangocairocffi.render_functions import show_glyph_item

from pangocairohelpers import LayoutClusters
from pangocairohelpers import Side
from pangocairohelpers.text_path.layout_engines import LayoutEngineAbstract
from pangocairohelpers.text_path.layout_engines import Svg as SvgLayoutEngine

LayoutEngine = TypeVar('LayoutEngine', bound=LayoutEngineAbstract)


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
            layout: Layout
    ):
        """
        :param line_string:
            a ``LineString`` for the text to follow
        :param layout:
            the layout to apply to the ``line_string``
        """
        if layout.get_line_count() > 1:
            raise ValueError('layout cannot be more than one line.')

        self._layout = layout
        self._layout_text = layout.get_text()
        self._line_string = line_string

        self._alignment = Alignment.LEFT
        self._start_offset = 0
        self._side = Side.LEFT

        self._layout_clusters = LayoutClusters(self._layout)
        self._layout_engine_class = SvgLayoutEngine
        self._layout_engine = None

        self._text_path_glyph_items = None

    @property
    def side(self) -> Side:
        return self._side

    @side.setter
    def side(self, value: Side):
        """
        :param value:
            what side the text should use. For example, for a line going
            left to right horizontally, the text will appear upright if the
            side is "left". If it's "right", the text will appear upside down.

            Defaults to ``'Left'``
        """
        if value != Side and value == Side.RIGHT:
            self._line_string.coords = list(self._line_string.coords)[::-1]
        self._side = value

    @property
    def alignment(self) -> Alignment:
        return self._alignment

    @alignment.setter
    def alignment(self, value: Alignment):
        """
        :param value:
            whether the text should be left, center, or right aligned

            Defaults to ``'Left'``
        """
        self._alignment = value

    @property
    def start_offset(self) -> float:
        return float(self._start_offset)

    @start_offset.setter
    def start_offset(self, value: float):
        """
        :param value:
            How far along the ``line_string`` the beginning character should be
            offset.

            Defaults to ``0``
        """
        self._start_offset = float(value)

    @property
    def layout_engine_class(self) -> Type[LayoutEngine]:
        return self._layout_engine_class

    @layout_engine_class.setter
    def layout_engine_class(self, value: Type[LayoutEngine]):
        """
        :param value:
            The layout engine class to use when positioning and orientating the
            text.

            Defaults to ``SvgLayoutEngine``
        """
        self._layout_engine_class = value

    def text_fits(self) -> bool:
        """
        :return:
            true if all the glyphs can be rendered on the line
        """
        text_path_glyph_items = self._compute_text_path_glyph_items()
        number_of_layed_out_glyphs = len(text_path_glyph_items)
        number_of_total_glyphs = len(self._layout_clusters.get_clusters())
        return number_of_layed_out_glyphs == number_of_total_glyphs

    def _generate_layout_engine(self):
        if not isinstance(self._layout_engine, self._layout_engine_class) or \
                self._layout_engine is None:
            self._layout_engine = self.layout_engine_class(
                self._line_string,
                self._layout_clusters
            )

        if self._layout_engine.alignment != self._alignment:
            self._layout_engine.alignment = self._alignment

        if self._layout_engine.start_offset != self._start_offset:
            self._layout_engine.start_offset = self._start_offset

    def _compute_text_path_glyph_items(self):
        self._generate_layout_engine()
        if self._text_path_glyph_items is None:
            self._text_path_glyph_items = self._layout_engine. \
                generate_text_path_glyph_items()
        return self._text_path_glyph_items

    def compute_boundaries(self) -> MultiPolygon:
        """
        Computes the combined glyph extents for the text path

        :return:
            a union of glyph extents
        """
        # Todo:
        pass

    def draw(self, context: Context):
        """
        Draws the text path on the context

        :param context:
            a cairo context
        """
        text_path_glyph_items = self._compute_text_path_glyph_items()
        for text_path_glyph_item in text_path_glyph_items:
            glyph_position = text_path_glyph_item.position
            glyph_rotation = text_path_glyph_item.rotation

            context.save()
            context.translate(glyph_position.x, glyph_position.y)
            context.rotate(glyph_rotation)
            show_glyph_item(
                context,
                self._layout_text,
                text_path_glyph_item.glyph_item
            )
            context.restore()

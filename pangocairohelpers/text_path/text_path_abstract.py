from abc import ABCMeta, abstractmethod

from cairocffi import Context
from typing import Type, TypeVar, Optional

from pangocffi import Layout, Alignment
from shapely.geometry import LineString, MultiPolygon

from pangocairohelpers import LayoutClusters, Side
from pangocairohelpers.text_path.layout_engines import LayoutEngineAbstract
from pangocairohelpers.text_path.layout_engines import Svg as SvgLayoutEngine

LayoutEngine = TypeVar('LayoutEngine', bound=LayoutEngineAbstract)


class TextPathAbstract(object, metaclass=ABCMeta):

    def __init__(
            self,
            line_string: LineString,
            layout: Layout
    ):
        if layout.get_line_count() > 1:
            raise ValueError('layout cannot be more than one line.')

        self._layout = layout
        self._input_line_string = line_string

        self._layout_text = layout.get_text()

        self._alignment = Alignment.LEFT
        self._start_offset = 0
        self._vertical_offset = 0
        self._side = Side.LEFT

        self._layout_clusters = LayoutClusters(self._layout)
        self._layout_engine_class = SvgLayoutEngine
        self._layout_engine = None

        self._text_path_glyph_items = None
        self._text_path_baseline = None

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
    def vertical_offset(self) -> float:
        return float(self._vertical_offset)

    @vertical_offset.setter
    def vertical_offset(self, value: float):
        """
        :param value:
            How many units the text should be offset vertically from the
            ``line_string``. If the line self_intersects, expect for the text
            path to not render at all.

            Defaults to ``0``
        """
        self._vertical_offset = float(value)

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

    @abstractmethod
    def text_fits(self) -> bool:
        """
        Todo

        :return:
            Todo
        """
        pass  # pragma: no cover

    @abstractmethod
    def compute_baseline(self) -> Optional[LineString]:
        """
        Computes the baseline that the text covers

        :return:
            a linestring representing the baseline of the text
        """
        pass  # pragma: no cover

    @abstractmethod
    def compute_boundaries(self) -> Optional[MultiPolygon]:
        """
        Computes the combined glyph extents for the text path

        :return:
            a union of glyph extents
        """
        pass  # pragma: no cover

    @abstractmethod
    def draw(self, context: Context):
        """
        Todo

        :return:
            Todo
        """
        pass  # pragma: no cover

from abc import ABCMeta, abstractmethod
from typing import List

from pangocffi import Alignment
from shapely.geometry import LineString

from pangocairohelpers import LayoutClusters
from pangocairohelpers.text_path import TextPathGlyphItem


class LayoutEngineAbstract:
    __metaclass__ = ABCMeta

    def __init__(
            self,
            line_string: LineString,
            layout_clusters: LayoutClusters
    ):
        self.line_string = line_string
        self.layout_clusters = layout_clusters
        self._alignment = Alignment.LEFT
        self._start_offset = 0

    @property
    def alignment(self) -> Alignment:
        return self._alignment

    @alignment.setter
    def alignment(self, value: Alignment):
        self._alignment = value

    @property
    def start_offset(self) -> float:
        return float(self._start_offset)

    @start_offset.setter
    def start_offset(self, value: float):
        self._start_offset = float(value)

    @abstractmethod
    def generate_text_path_glyph_items(self) -> List[TextPathGlyphItem]:
        pass

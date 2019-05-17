import unittest
from unittest.mock import patch

from pangocffi import Alignment
from shapely.geometry import LineString

from pangocairohelpers import LayoutClusters
from pangocairohelpers.text_path import Side
from pangocairohelpers.text_path.layout_engines import Svg


class TestLayoutEnginesSvg(unittest.TestCase):

    def testSvgProperties(self):
        line_string = LineString([[0, 0], [1, 0]])
        with patch.object(LayoutClusters, "__init__", lambda x, y: None):
            # noinspection PyTypeChecker
            layout_cluster = LayoutClusters(None)
            layout_engine = Svg(line_string, layout_cluster)
            assert isinstance(layout_engine.alignment, Alignment)
            assert isinstance(layout_engine.start_offset, float)

            layout_engine.alignment = Alignment.CENTER
            layout_engine.start_offset = 3.14

            assert layout_engine.alignment == Alignment.CENTER
            assert layout_engine.start_offset == 3.14

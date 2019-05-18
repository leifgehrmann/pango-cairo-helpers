import unittest
from unittest.mock import patch

import pytest
from shapely.geometry import LineString

from pangocairohelpers import LayoutClusters
from pangocairohelpers.text_path.layout_engines import LayoutEngineAbstract


class TestLayoutEngineAbstract(unittest.TestCase):

    def testAbstractRaisesError(self):
        line_string = LineString([[0, 0], [1, 0]])
        with patch.object(LayoutClusters, "__init__", lambda x, y: None):
            # noinspection PyTypeChecker
            layout_cluster = LayoutClusters(None)
            with pytest.raises(TypeError):
                _ = LayoutEngineAbstract(
                    line_string,
                    layout_cluster
                )

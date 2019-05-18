import unittest

from pangocairohelpers import Extent


class TestExtent(unittest.TestCase):

    def test_constructor(self):
        extent = Extent(10, 20, 30, 40)
        assert extent.x == 10
        assert extent.y == 20
        assert extent.width == 30
        assert extent.height == 40

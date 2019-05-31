from typing import Optional

from cairocffi import Context
from shapely.geometry import MultiPolygon, LineString

from pangocairohelpers.text_path import TextPathAbstract


class UprightTextPath(TextPathAbstract):
    """
    A TextPath that when drawn, will always try to make sure the glyphs are
    never rendered upside down for poor readability.
    """

    def text_fits(self) -> bool:
        pass

    def compute_baseline(self) -> Optional[LineString]:
        pass

    def compute_boundaries(self) -> MultiPolygon:
        pass

    def draw(self, context: Context):
        pass

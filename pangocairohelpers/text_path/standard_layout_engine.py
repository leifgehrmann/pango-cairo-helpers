from typing import List, Tuple

from pangocffi import Alignment
from shapely.geometry import LineString

from pangocairohelpers import LayoutClusters


class StandardLayoutEngine:

    def __init__(
            self,
            line_string: LineString,
            layout_clusters: LayoutClusters,
            alignment: Alignment = Alignment.LEFT
    ):
        self.line_string = line_string
        self.layout_clusters = layout_clusters
        self.alignment = alignment
        self.start_offset = 0

    def generate_positions_and_rotations(self) -> List[Tuple[float, float]]:
        positions = []
        rotations = []

        extents = self.layout_clusters.get_logical_extents()
        for extent in extents:
            position = self.line_string.interpolate(
                self.start_offset + extent.x
            )
            rotation =


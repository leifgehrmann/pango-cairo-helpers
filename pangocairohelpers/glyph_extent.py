from pangocairohelpers import Extent


class GlyphExtent(Extent):

    def __init__(
            self,
            x: float = 0,
            y: float = 0,
            width: float = 0,
            height: float = 0,
            baseline: float = 0
    ):
        super().__init__(x, y, width, height)
        self.baseline = baseline

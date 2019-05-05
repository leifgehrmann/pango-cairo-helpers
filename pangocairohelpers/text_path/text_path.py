from cairocffi import Context
from pangocffi import Layout, Alignment
from shapely.geometry import LineString, MultiPolygon
from pangocairocffi.render_functions import show_glyph_item

from pangocairohelpers import LayoutClusters
from pangocairohelpers.text_path.layout_engines import Svg as SvgLayoutEngine


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
            layout: Layout,
            alignment: Alignment = Alignment.LEFT,
            layout_engine=SvgLayoutEngine
    ):
        if layout.get_line_count() > 1:
            raise ValueError('layout cannot be more than one line.')

        self.layout = layout
        self.layout_text = layout.get_text()
        self.line_string = line_string
        self.layout_clusters = LayoutClusters(self.layout)
        self.alignment = alignment
        self.layout_engine = layout_engine(
            self.line_string,
            self.layout_clusters,
            self.alignment
        )
        self.text_path_glyph_items = None

    def text_fits(self) -> bool:
        """
        :return:
            true if all the glyphs can be rendered on the line
        """
        text_path_glyph_items = self._compute_text_path_glyph_items()
        number_of_layed_out_glyphs = len(text_path_glyph_items)
        number_of_total_glyphs = len(self.layout_clusters.get_clusters())
        return number_of_layed_out_glyphs == number_of_total_glyphs

    def _compute_text_path_glyph_items(self):
        if self.text_path_glyph_items is None:
            self.text_path_glyph_items = self.layout_engine. \
                generate_text_path_glyph_items()
        return self.text_path_glyph_items

    def compute_boundaries(self) -> MultiPolygon:
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
                self.layout_text,
                text_path_glyph_item.glyph_item
            )
            context.restore()

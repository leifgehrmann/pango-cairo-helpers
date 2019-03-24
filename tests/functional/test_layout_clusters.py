from cairocffi import Context, SVGSurface
import pangocairocffi
from pangocairohelpers import LayoutClusters


def test_layout_clusters_properties_have_same_length():
    surface = SVGSurface(None, 100, 100)
    cairo_context = Context(surface)
    layout = pangocairocffi.create_layout(cairo_context)
    layout.set_markup('Hi from Παν語')

    layout_clusters = LayoutClusters(layout)

    assert len(layout_clusters.get_clusters()) == 12
    assert len(layout_clusters.get_logical_positions()) == 12

    surface.finish()

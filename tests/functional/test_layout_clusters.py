from cairocffi import Context, SVGSurface
import pangocairocffi
from pangocairohelpers import LayoutClusters


def test_layout_clusters_properties_have_same_length():
    surface = SVGSurface(None, 100, 100)
    cairo_context = Context(surface)
    layout = pangocairocffi.create_layout(cairo_context)
    layout.set_markup('Hi from Παν語\nThis is a test')
    expected_length = len(layout.get_text()) - 1  # Subtract newline char

    layout_clusters = LayoutClusters(layout)

    assert layout_clusters.get_layout() is layout
    assert len(layout_clusters.get_clusters()) == expected_length
    assert len(layout_clusters.get_logical_extents()) == expected_length

    surface.finish()

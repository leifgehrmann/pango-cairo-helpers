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


def test_layout_clusters_get_max_logical_extents():
    surface = SVGSurface(None, 100, 100)
    cairo_context = Context(surface)

    layout_1 = pangocairocffi.create_layout(cairo_context)
    layout_1.set_markup('Text with one line')
    layout_1_clusters = LayoutClusters(layout_1)
    extent_1 = layout_1_clusters.get_max_logical_extents()

    layout_2 = pangocairocffi.create_layout(cairo_context)
    layout_2.set_markup('text with\ntwo lines')
    layout_2_clusters = LayoutClusters(layout_2)
    extent_2 = layout_2_clusters.get_max_logical_extents()

    assert extent_1.x == 0
    assert extent_1.y == 0
    assert extent_1.width > 0
    assert extent_1.height > 0

    assert extent_2.x == extent_1.x
    assert extent_2.y == extent_1.y
    assert extent_1.width != extent_2.width
    assert extent_1.height * 2 == extent_2.height

    surface.finish()

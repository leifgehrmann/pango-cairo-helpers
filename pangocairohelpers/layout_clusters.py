from pangocffi import Layout, GlyphItem, units_to_double
from typing import List, Optional

from pangocairohelpers import GlyphExtent


class LayoutClusters:
    """
    A decomposed representation of ``pangocffi.Layout`` as clusters (in other
    words ``pangocffi.GlyphItem``)

    This class is useful in scenarios where one wants to iterate over each
    individual cluster (commonly a single glyph or character).

    **Warning:** RTL directional text like Arabic or Hebrew is not supported
    for now.
    """

    def __init__(self, layout: Layout):
        """
        :param layout:
            a pango layout to decompose into clusters
        """
        self.layout = layout
        self.text = self.layout.get_text()
        self.clusters = []
        self.logical_extents = []
        self._extract_properties_from_layout()

    def _extract_properties_from_layout(self):
        """
        Iterates over each cluster

        Todo: This function uses two different iterators.
        This probably could do with a bit of refactoring
        """
        layout_run_iter = self.layout.get_iter()
        layout_cluster_iter = self.layout.get_iter()

        has_next_run = True
        while has_next_run:

            layout_run = layout_run_iter.get_run()
            layout_line_baseline = layout_run_iter.get_baseline()

            if layout_run is None:
                has_next_run = layout_run_iter.next_run()
                continue

            clusters = self._get_clusters_from_glyph_item(layout_run)
            for cluster in clusters:
                cluster_extents = layout_cluster_iter.get_cluster_extents()[1]
                layout_cluster_iter.next_cluster()
                self.clusters.append(cluster)
                self.logical_extents.append(GlyphExtent(
                    units_to_double(cluster_extents.x),
                    units_to_double(cluster_extents.y),
                    units_to_double(cluster_extents.width),
                    units_to_double(cluster_extents.height),
                    units_to_double(layout_line_baseline)
                ))

            has_next_run = layout_run_iter.next_run()

    def _split_glyph_item_at_first_cluster(
            self,
            glyph_item: GlyphItem,
    ) -> Optional[GlyphItem]:
        """
        :param glyph_item:
            the glyph item to split
        :return:
            the first cluster of the :param:`glyph_item`. The input parameter
            will also be split from the end of the first cluster.
        """
        i = 1
        while True:
            if i >= glyph_item.item.length:
                break
            try:
                return glyph_item.split(self.text, i)
            except ValueError:
                i += 1
                pass
        return None

    def _get_clusters_from_glyph_item(
            self,
            glyph_item: GlyphItem
    ) -> List[GlyphItem]:
        """
        Splits a glyph item (which is composed of multiple clusters) into
        an array of individual glyph items for each cluster.

        Warning: Does not support bidirectional text.

        :param glyph_item:
            the glyph item, or layout run, to split into individual glyphs
        :return:
            an array og individual glyph items
        """
        cluster_glyph_items = []
        glyph_item_copy = glyph_item.copy()
        while True:
            first_cluster = self._split_glyph_item_at_first_cluster(
                glyph_item_copy
            )
            if first_cluster is None:
                break
            cluster_glyph_items.append(first_cluster)
        cluster_glyph_items.append(glyph_item_copy)
        return cluster_glyph_items

    def get_layout(self) -> Layout:
        """
        :return:
            the layout on which this instance is based on
        """
        return self.layout

    def get_clusters(self) -> List[GlyphItem]:
        """
        :return:
            a list of ``GlyphItem`` for each cluster in the layout
        """
        return self.clusters

    def get_logical_extents(self) -> List[GlyphExtent]:
        """
        :return:
            a list of ``GlyphExtent`` for each cluster in the layout
        """
        return self.logical_extents

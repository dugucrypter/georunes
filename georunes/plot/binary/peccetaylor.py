import numpy as np
from matplotlib.colors import to_rgba

from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.language import format_chemical_formula as _fml, get_translator


# Peccerillo, A. and Taylor, S.R., 1976. Geochemistry of Eocene calc-alkaline volcanic rocks from the Kastamonu area,
# northern Turkey. Contributions to mineralogy and petrology, 58(1), pp.63-81.

class DiagramPecceTaylor(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title=_fml("K2O vs SiO2") + "classification diagram (Peccerillo and Taylor 1976)",
                 padding={"bottom": 0.20},
                 alpha_color=0.4, alpha_edge_color=0.8,
                 annotation=None,
                 **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, padding=padding, **kwargs)

        self.xlabel = _fml("SiO2 (wt%)")
        self.ylabel = _fml("K2O (wt%)")
        self.annotation = annotation
        self.alpha_color = alpha_color
        self.alpha_edge_color = alpha_edge_color

    def set_decoration(self):
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)
        _ = get_translator(self.lang_cfg)
        self.ax.set_xlim(45, 80)
        self.ax.set_ylim(0, 6)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        lx1 = np.array([48, 52, 56, 63, 70, 78])
        ly1 = np.array([0.3, 0.5, 0.7, 1, 1.3, 1.6])

        lx2 = np.array([48, 52, 56, 63, 70, 77])
        ly2 = np.array([1.2, 1.5, 1.8, 2.4, 3, 3.6])

        lx3 = np.array([48, 52, 56, 63, 70])
        ly3 = np.array([1.6, 2.4, 3.2, 4, 4.8])

        self.ax.plot(lx1, ly1, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, color=self.decor_line_col, linewidth=0.6)

        txt_series = [
            [58, 0.2, _("low-K tholeiite")],
            [53, 1, _("medium-K calc-alkaline")],
            [56, 2.6, _("high-K calc-alkaline")],
            [52, 3.6, _("shoshonitic")]
        ]
        for elt in txt_series:
            self.ax.text(*elt, fontsize="x-small")

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:
                label = list(group[self.label_column])[0] if self.label_defined else name
                zorder = 4
                if self.zorder_column:
                    zorder = list(group[self.zorder_column])[0]

                sample_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_edge_color)
                self.ax.scatter(group["SiO2"], group["K2O"], edgecolors=edge_color,
                                marker=list(group[self.marker_column])[0], label=label, facecolors=sample_color,
                                s=self.markersize,
                                zorder=zorder)

                if self.annotation:
                    for i, sample in group["SiO2"].items():
                        self.ax.annotate(group[self.annotation].get(i), (group["SiO2"].get(i), group["K2O"].get(i)),
                                         fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

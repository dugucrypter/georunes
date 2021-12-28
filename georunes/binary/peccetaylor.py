import numpy as np
from georunes.base.base import DiagramBase
from georunes.base.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.language import format_chemical_formula as _fml, get_translator


class DiagramPecceTaylor(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title=_fml("K2O vs SiO2") + "classification diagram (Peccerillo and Taylor 1976)",
                 padding={"bottom": 0.20}, annotation=None, **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, padding=padding, **kwargs)

        self.xlabel = _fml("SiO2 (wt%)")
        self.ylabel = _fml("K2O (wt%)")
        self.annotation = annotation

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
            [58, 0.2, _("low-K tholeite")],
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

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(group["SiO2"], group["K2O"], edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.9, zorder=zorder)

                if self.annotation:
                    for i, sample in group["SiO2"].iteritems():
                        self.ax.annotate(group[self.annotation].get(i), (group["SiO2"].get(i), group["K2O"].get(i)),
                                         fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

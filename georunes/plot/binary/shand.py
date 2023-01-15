from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.chemistry import molar_ratio
from georunes.tools.language import format_chemical_formula as _fml, get_translator


# Shand, S.J., 1943. Eruptive rocks: their genesis, composition, and classification, with a chapter on meteorites. J.
# Wiley & sons, Incorporated.

class DiagramShand(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="A/NK vs A/CNK diagram of Shand (1943)",
                 annotation=None,
                 xlim=None, ylim=None, **kwargs):

        DiagramBase.__init__(self, datasource=datasource, title=title, **kwargs)

        self.annotation = annotation
        if xlim:
            self.xlim = xlim
        else:
            self.xlim = (0.6, 1.4)
        if ylim:
            self.ylim = ylim
        else:
            self.ylim = (0.4, 2)

        self.xlabel = _fml("Al2O3/(NaO + K2O + CaO)")
        self.ylabel = _fml("Al2O3/(NaO + K2O)")

    def set_decoration(self):
        _ = get_translator(self.lang_cfg)
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)

        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        x1 = (1, 1)
        y1 = (-2, 2)

        x2 = (1.1, 1.1)
        y2 = (-2, 2)

        x3 = (-2, 2)
        y3 = (-2, 2)

        x4 = (-2, 2)
        y4 = (1, 1)

        self.ax.plot(x1, y1, self.decor_line_col, linewidth=0.8, zorder=1)
        self.ax.plot(x2, y2, self.decor_line_col, linewidth=0.4, zorder=1)
        self.ax.plot(x3, y3, self.decor_line_col, linewidth=0.8, zorder=1)
        self.ax.plot(x4, y4, self.decor_line_col, linewidth=0.8, zorder=1)

        self.ax.text(self.xlim[0] + 0.02, 0.85, _("Peralkaline"))
        self.ax.text(self.xlim[0] + 0.02, 1.85, _("Metaluminous"))
        self.ax.text(1.15, 1.85, _("Peraluminous"))

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                acnk = molar_ratio(group["Al2O3"]) / (
                        molar_ratio(group["Na2O"]) + molar_ratio(group["K2O"]) + molar_ratio(group["CaO"]))
                ank = molar_ratio(group["Al2O3"]) / (molar_ratio(group["Na2O"]) + molar_ratio(group["K2O"]))

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(acnk, ank, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.7, zorder=zorder)

                if self.annotation:
                    for i, sample in acnk.iteritems():
                        self.ax.annotate(group[self.annotation].get(i), (acnk.get(i), ank.get(i)), fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

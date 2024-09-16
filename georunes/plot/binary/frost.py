from georunes.plot.base import DiagramBase
from georunes.plot.helpers import ArrowDrawer, LegendDrawer
from georunes.tools.language import format_chemical_formula as _fml, get_translator


# Frost, B.R., Barnes, C.G., Collins, W.J., Arculus, R.J., Ellis, D.J. and Frost, C.D., 2001. A geochemical
# classification for granitic rocks. Journal of petrology, 42(11), pp.2033-2048.

class DiagramFrostSiFeNb(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title=_fml("SiO2 vs Fe# Frost diagram"), **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, **kwargs)
        if 'FeO' not in self.data.keys():
            raise Exception("FeO data missing. Check the table.")
        self.xlabel = _fml("SiO2 (wt %)")
        self.ylabel = "FeO/(FeO + MgO)"

    def set_decoration(self):
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)
        _ = get_translator(self.lang_cfg)
        self.ax.set_xlim(50, 80)
        self.ax.set_ylim(0.4, 1)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        x1 = (50, 80)
        y1 = (0.676, 0.814)

        self.ax.plot(x1, y1, self.decor_line_col, linewidth=0.6)

        self.ax.text(52, 0.8, _("ferroan"), size="small")
        self.ax.text(52, 0.6, _("magnesian"), size="small")

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):

                fenb = group["FeO"] / (group["FeO"] + group["MgO"])
                si = (group["SiO2"])

                label = list(group['label'])[0] if self.label_defined else name
                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(si, fenb, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=label, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.7, zorder=zorder)

        self.plot_arrows()
        self.plot_legend()


class DiagramFrostSiFeTotNb(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title=_fml("SiO2 vs Fe* Frost diagram"), calc_total_Fe=False, **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, **kwargs)
        if 'FeOt' not in self.data.keys():
            if calc_total_Fe:
                if 'FeO' not in self.data.keys():
                    raise Exception("FeO data missing. Cannot calculate total FeO.")
                elif 'Fe2O3' not in self.data.keys():
                    raise Exception("Fe2O3 data missing. Cannot calculate total FeO.")
                else:
                    self.data['FeOt'] = self.data['FeO'] + self.data["Fe2O3"] * 0.8998
            else:
                raise Exception("FeOt data missing. Check the table.")
        self.xlabel = _fml("SiO2 (wt %)")
        self.ylabel = "FeO$^{tot}$/(FeO$^{tot}$ + MgO)"

    def set_decoration(self):
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)
        _ = get_translator(self.lang_cfg)
        self.ax.set_xlim(50, 80)
        self.ax.set_ylim(0.4, 1)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        x1 = (50, 80)
        y1 = (0.716, 0.854)

        self.ax.plot(x1, y1, self.decor_line_col, linewidth=0.6)

        self.ax.text(52, 0.8, _("ferroan"), size="small")
        self.ax.text(52, 0.6, _("magnesian"), size="small")

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):

                fenb = group["FeOt"] / (group["FeOt"] + group["MgO"])
                si = (group["SiO2"])

                label = list(group['label'])[0] if self.label_defined else name
                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(si, fenb, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=label, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.7, zorder=zorder)

        self.plot_arrows()
        self.plot_legend()


class DiagramFrostSiMALI(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title=_fml("SiO2 vs modified alkali-lime index Frost diagram"), **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, **kwargs)
        self.xlabel = _fml("SiO2 (wt %)")
        self.ylabel = _fml("Na2O + K2O - CaO (wt %)")

    def set_decoration(self):
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)
        _ = get_translator(self.lang_cfg)
        self.ax.set_xlim(50, 80)
        self.ax.set_ylim(-8, 12)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        lx = [i for i in range(50, 75, 5)]

        ly1 = [-41.86 + 1.112 * x - 0.00572 * x * x for x in lx]
        ly2 = [-44.72 + 1.094 * x - 0.00527 * x * x for x in lx]
        ly3 = [-45.36 + 1.0043 * x - 0.00427 * x * x for x in lx]

        self.ax.plot(lx, ly1, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx, ly2, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx, ly3, self.decor_line_col, linewidth=0.6)

        self.ax.text(51, 2.5, _("alkalic"), size="small", )
        self.ax.text(51, -1.3, _("alkali-calcic"), size="small", rotation=30)
        self.ax.text(51, -3.5, _("calc-alkalic"), size="small", rotation=30)
        self.ax.text(51, -6.5, _("calcic"), size="small", )

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):

                mali = group["Na2O"] + group["K2O"] - group["CaO"]
                si = (group["SiO2"])

                label = list(group['label'])[0] if self.label_defined else name
                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(si, mali, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=label, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.7, zorder=zorder)

        self.plot_arrows()
        self.plot_legend()

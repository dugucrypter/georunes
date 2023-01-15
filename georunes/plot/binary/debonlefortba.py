import numpy as np
from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.chemistry import val_ox_to_mc
from georunes.tools.language import get_translator
from georunes.tools.plotting import get_spline


# Debon, F. and Le Fort, P., 1983. A chemical–mineralogical classification of common plutonic rocks and associations.
# Earth and Environmental Science Transactions of the Royal Society of Edinburgh, 73(3), pp.135-149.

class DiagramBA(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="B-A multicationic classification (Debon and Le Fort 1983)",
                 annotation=None, decor_set="Debon", legend_loc="upper right", **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, legend_loc=legend_loc, **kwargs)

        self.decor_set = decor_set
        self.annotation = annotation
        self.xlabel = "B = Fe + Mg + Ti"
        self.ylabel = "A = Al - (Na+ K + 2Ca)"

    def set_decoration(self):
        _ = get_translator(self.lang_cfg)
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(-100, 200)

        xax = (0, 200)
        yax = (0, 0)

        self.ax.plot(xax, yax, color=self.decor_line_col, linewidth=1.0)

        if self.decor_set is "Villaseca":

            lx1 = np.array([0, 13, 29, 37, 36, 32, 30])
            ly1 = np.array([100, 102, 98, 87, 54, 25, 0])

            lx2 = np.array([29, 45, 57, 78])
            ly2 = np.array([98, 148, 176, 200])

            lx3 = np.array([36, 92, 145, 167, 200])
            ly3 = np.array([54, 44, 39, 42, 53])

            lx4 = np.array([32, 57, 82, 105, 130])
            ly4 = np.array([25, 21, 14, 8, 0])

            x1, y1 = get_spline(lx1, ly1)
            x2, y2 = get_spline(lx2, ly2)
            x3, y3 = get_spline(lx3, ly3)
            x4, y4 = get_spline(lx4, ly4)

            self.ax.plot(x1, y1, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(x2, y2, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(x3, y3, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(x4, y4, color=self.decor_line_col, linewidth=0.6)

            self.ax.text(75, 110, "hP", size='x-small')
            self.ax.text(55, 40, "mP", size='x-small')
            self.ax.text(50, 10, "lP", size='x-small')
            self.ax.text(18, 60, _("felsic"), size='x-small')

        else:  # Default decor_set is from Debon and Le Fort 1983

            lx1 = np.array([0, 420])
            ly1 = np.array([0, -885])

            lx2 = np.array([0, 470])
            ly2 = np.array([0, -225])

            lx3 = np.array([0, 1500])
            ly3 = np.array([0, 0])

            lx4 = np.array([0, 600])
            ly4 = np.array([0, 250])

            lx5 = np.array([0, 435])
            ly5 = np.array([0, 500])

            self.ax.plot(lx1, ly1, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx2, ly2, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx3, ly3, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx4, ly4, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx5, ly5, color=self.decor_line_col, linewidth=0.6)

            self.ax.text(100, 150, "I", size='x-small')
            self.ax.text(175, 150, "II", size='x-small')
            self.ax.text(180, 25, "III", size='x-small')
            self.ax.text(180, -25, "IV", size='x-small')
            self.ax.text(75, -65, "V", size='x-small')
            self.ax.text(20, -75, "VI", size='x-small')

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:
            if self.is_group_allowed(name):

                al_mc = val_ox_to_mc(group["Al2O3"])
                na_mc = val_ox_to_mc(group["Na2O"])
                k_mc = val_ox_to_mc(group["K2O"])
                ca_mc = val_ox_to_mc(group["CaO"])
                fe_mc = val_ox_to_mc(group["Fe2O3"])
                mg_mc = val_ox_to_mc(group["MgO"])
                ti_mc = val_ox_to_mc(group["TiO2"])

                param_A = al_mc - na_mc - k_mc - 2 * ca_mc
                param_B = fe_mc + mg_mc + ti_mc

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(param_B, param_A, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.7, zorder=zorder)

                if self.annotation:
                    for i, sample in param_B.iteritems():
                        self.ax.annotate(group[self.annotation].get(i), (param_B.get(i), param_A[i]),
                                         fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

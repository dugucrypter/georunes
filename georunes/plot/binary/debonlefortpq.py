import numpy as np
from georunes.plot.base import DiagramBase
from georunes.plot.helpers import ArrowDrawer, LegendDrawer
from georunes.tools.chemistry import val_ox_to_mc


class DiagramPQ(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="P-Q multicationic classification (Debon and Le Fort 1983)",
                 padding={"bottom": 0.20}, annotation=None, **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, padding=padding, **kwargs)

        self.annotation = annotation
        self.xlabel = "P = K - (Na+Ca)"
        self.ylabel = "Q = Si/3 - (K+Na+2Ca/3)"

    def set_decorations(self):

        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        self.ax.set_xlim(-400, 110)
        self.ax.set_ylim(0, 260)

        lx1 = np.array([-377, -257, -205, -224, -311, -377])
        ly1 = np.array([0, 0, 55, 57, 57, 0])
        lx2 = np.array([-257, -188, -143, -205, -257])
        ly2 = np.array([0, 0, 48, 55, 0])
        lx3 = np.array([-188, -117, -88, -143, -188])
        ly3 = np.array([0, 0, 43, 48, 0])
        lx4 = np.array([-117, 16, 30, -40, -88, -117])
        ly4 = np.array([0, 0, 26, 38, 43, 0])
        lx5 = np.array([-311, -224, -205, -187, -172, -274, -311])
        ly5 = np.array([57, 57, 55, 79, 104, 100, 57])
        lx6 = np.array([-205, -143, -125, -103, -172, -187, -205])
        ly6 = np.array([55, 48, 70, 107, 104, 79, 55])
        lx7 = np.array([-143, -88, -69, -55, -103, -125, -143])
        ly7 = np.array([48, 43, 77, 109, 107, 70, 48])
        lx8 = np.array([-88, -40, 30, 64, -30, -55, -69, -88])
        ly8 = np.array([43, 38, 26, 110, 110, 109, 77, 43])
        lx9 = np.array([-274, -172, -156, -134, -119, -216, -230, -256, -274])
        ly9 = np.array([100, 104, 136, 190, 242, 238, 190, 132, 100])
        lx10 = np.array([-172, -103, -89, -71, -59, -119, -134, -156, -172])
        ly10 = np.array([104, 107, 137, 190, 244, 242, 190, 136, 104])
        lx11 = np.array([-103, -55, -44, -29, -17, -59, -71, -89, -103])
        ly11 = np.array([107, 109, 140, 190, 245, 244, 190, 137, 107])
        lx12 = np.array([-55, -30, 64, 75, 90, 105, -17, -29, -44, -55])
        ly12 = np.array([109, 110, 110, 140, 190, 250, 245, 190, 140, 109])

        self.ax.plot([0, 0], [0, 300], color=self.decor_line_col, linewidth=1)

        self.ax.plot(lx1, ly1, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx4, ly4, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx5, ly5, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx6, ly6, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx7, ly7, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx8, ly8, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx9, ly9, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx10, ly10, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx11, ly11, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx12, ly12, color=self.decor_line_col, linewidth=0.6)

        self.ax.text(-170, 230, "to", size='x-small', color=self.decor_text_col)
        self.ax.text(-100, 230, "gd", size='x-small', color=self.decor_text_col)
        self.ax.text(-45, 230, "ad", size='x-small', color=self.decor_text_col)
        self.ax.text(25, 230, "gr", size='x-small', color=self.decor_text_col)
        self.ax.text(-240, 90, "dq", size='x-small', color=self.decor_text_col)
        self.ax.text(-150, 90, "mzdq", size='x-small', color=self.decor_text_col)
        self.ax.text(-75, 90, "mzq", size='x-small', color=self.decor_text_col)
        self.ax.text(-20, 90, "sq", size='x-small', color=self.decor_text_col)
        self.ax.text(-300, 25, "go", size='x-small', color=self.decor_text_col)
        self.ax.text(-215, 25, "mzgo", size='x-small', color=self.decor_text_col)
        self.ax.text(-145, 25, "mz", size='x-small', color=self.decor_text_col)
        self.ax.text(-45, 25, "s", size='x-small', color=self.decor_text_col)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:

                si = val_ox_to_mc(group["SiO2"])
                na = val_ox_to_mc(group["Na2O"])
                k = val_ox_to_mc(group["K2O"])
                ca = val_ox_to_mc(group["CaO"])

                param_P = k - (na + ca)
                param_Q = si / 3 - (k + na + 2 * ca / 3)

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(param_P, param_Q, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.9, zorder=zorder)

                if self.annotation:
                    for i, sample in param_P.iteritems():
                        self.ax.annotate(group[self.annotation].get(i), (param_P.get(i), param_Q[i]),
                                         fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

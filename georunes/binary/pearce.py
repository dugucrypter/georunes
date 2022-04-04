import numpy as np

from georunes.base.base import DiagramBase
from georunes.base.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.language import get_translator


class PearceBase(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource,
                 x_formatter=None, y_formatter=None,
                 padding=None,
                 **kwargs
                 ):
        config_padding = {"left": 0.16}
        if padding:
            config_padding.update(padding)

        DiagramBase.__init__(self, datasource=datasource, padding=config_padding, **kwargs)
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        self.x_formatter = x_formatter
        self.y_formatter = y_formatter

    def set_decorations(self):
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        if self.ylim is not None:
            self.ax.set_ylim(self.ylim)

        if self.x_formatter:
            self.ax.xaxis.set_major_formatter(self.x_formatter)
        if self.y_formatter:
            self.ax.yaxis.set_major_formatter(self.y_formatter)


class DiagramPearceRYN(PearceBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="Pearce : Rb vs Y + Nb",
                 xlim=(2, 2000), ylim=(1, 2000),
                 **kwargs
                 ):
        PearceBase.__init__(self, datasource=datasource, title=title, **kwargs)
        self.xlim = xlim
        self.ylim = ylim
        self.xlabel = "Y + Nb (ppm)"
        self.ylabel = "Rb (ppm)"

    def set_decorations(self):
        PearceBase.set_decorations(self)
        _ = get_translator(self.lang_cfg)

        lx1 = np.array([2, 55])
        ly1 = np.array([80, 300])

        lx2 = np.array([55, 400])
        ly2 = np.array([300, 2000])

        lx3 = np.array([55, 51.5])
        ly3 = np.array([300, 8])

        lx4 = np.array([51.5, 50])
        ly4 = np.array([8, 1])

        lx5 = np.array([51.5, 2000])
        ly5 = np.array([8, 400])

        self.ax.plot(lx1, ly1, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx4, ly4, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx5, ly5, self.decor_line_col, linewidth=0.6)

        self.ax.text(6.3, 756, _("Syn-COLG"), color=self.decor_text_col)
        self.ax.text(210, 260, _("WPG"), color=self.decor_text_col)
        self.ax.text(4.36, 2.6, _("VAG"), color=self.decor_text_col)
        self.ax.text(277, 5, _("ORG"), color=self.decor_text_col)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:

                vx = group["Nb"] + group["Y"]
                vy = group["Rb"]

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(vx, vy, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.9, zorder=zorder)
        self.plot_arrows()
        self.plot_legend()
        self.adjust_padding()


class DiagramPearceRYT(PearceBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="Pearce : Rb vs Yb + Ta",
                 xlim=(0.5, 200), ylim=(1, 2000),
                 **kwargs
                 ):
        PearceBase.__init__(self, datasource=datasource, title=title, **kwargs)
        self.xlim = xlim
        self.ylim = ylim
        self.xlabel = "Yb + Ta (ppm)"
        self.ylabel = "Rb (ppm)"

    def set_decorations(self):
        PearceBase.set_decorations(self)
        _ = get_translator(self.lang_cfg)

        lx1 = np.array([6, 50])
        ly1 = np.array([200, 2000])

        lx2 = np.array([6, 6])
        ly2 = np.array([200, 8])

        lx3 = np.array([6, 6])
        ly3 = np.array([8, 1])

        lx4 = np.array([6, 200])
        ly4 = np.array([8, 400])

        lx5 = np.array([0.5, 6])
        ly5 = np.array([140, 200])

        self.ax.plot(lx1, ly1, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx4, ly4, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx5, ly5, self.decor_line_col, linewidth=0.6)

        self.ax.text(5.5, 1210, _("Syn-COLG"), color=self.decor_text_col)
        self.ax.text(54, 479, _("WPG"), color=self.decor_text_col)
        self.ax.text(2, 1.4, _("VAG"), color=self.decor_text_col)
        self.ax.text(24, 1.4, _("ORG"), color=self.decor_text_col)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:

                vx = group["Ta"] + group["Yb"]
                vy = group["Rb"]

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(vx, vy, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.9, zorder=zorder)

        self.plot_arrows()
        self.plot_legend()


class DiagramPearceNY(PearceBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="Pearce : Nb vs Y",
                 xlim=(1, 2000), ylim=(1, 2000),
                 **kwargs
                 ):
        PearceBase.__init__(self, datasource=datasource, title=title, **kwargs)
        self.xlim = xlim
        self.ylim = ylim
        self.xlabel = "Y (ppm)"
        self.ylabel = "Nb (ppm)"

    def set_decorations(self):
        PearceBase.set_decorations(self)
        _ = get_translator(self.lang_cfg)

        lx1 = np.array([40, 50])
        ly1 = np.array([1, 10])

        lx2 = np.array([50, 1000])
        ly2 = np.array([10, 100])

        lx3 = np.array([1, 50])
        ly3 = np.array([2000, 10])

        lx4 = np.array([25, 1000])
        ly4 = np.array([25, 400])

        self.ax.plot(lx1, ly1, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx4, ly4, color=self.decor_line_col, linewidth=0.6, linestyle='--')

        self.ax.text(2.3, 16.9, _("Syn-COLG") + " +\n" + _("VAG"), color=self.decor_text_col)
        self.ax.text(57, 301, _("WPG"), color=self.decor_text_col)
        self.ax.text(277, 5, _("ORG"), color=self.decor_text_col)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:

                vx = group["Y"]
                vy = group["Nb"]

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(vx, vy, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize, alpha=0.9, zorder=zorder)

        self.plot_arrows()
        self.plot_legend()


class DiagramPearceTY(PearceBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="Pearce : Ta vs Yb",
                 xlim=(0.1, 100), ylim=(0.05, 50),
                 **kwargs
                 ):
        PearceBase.__init__(self, datasource=datasource, title=title, **kwargs)
        self.xlim = xlim
        self.ylim = ylim
        self.xlabel = "Yb (ppm)"
        self.ylabel = "Ta (ppm)"

    def set_decorations(self):
        PearceBase.set_decorations(self)
        _ = get_translator(self.lang_cfg)

        lx1 = np.array([0.55, 3])
        ly1 = np.array([20, 2])

        lx2 = np.array([0.1, 3])
        ly2 = np.array([0.35, 2])

        lx3 = np.array([3, 5])
        ly3 = np.array([2, 1])

        lx4 = np.array([5, 5])
        ly4 = np.array([0.05, 1])

        lx5 = np.array([5, 100])
        ly5 = np.array([1, 7])

        lx6 = np.array([3, 100])
        ly6 = np.array([2, 20])

        self.ax.plot(lx1, ly1, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx5, ly5, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx4, ly4, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx6, ly6, color=self.decor_line_col, linewidth=0.6, linestyle='--')

        self.ax.text(0.16, 2.97, _("Syn-COLG"))
        self.ax.text(4.8, 11.3, _("WPG"), )
        self.ax.text(1.03, 0.08, _("VAG"), )
        self.ax.text(16.2, 0.19, _("ORG"), )

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:

                vx = group["Yb"]
                vy = group["Ta"]

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(vx, vy, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize, alpha=0.9, zorder=zorder)

        self.plot_legend()

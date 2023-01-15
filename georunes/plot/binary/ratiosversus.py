from matplotlib.colors import to_rgba
from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.plotting import normalize_marker_size


class DiagramRatiosVs(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource,
                 xnum, xdenom, ynum, ydenom, title=None, xlim=None, ylim=None,
                 xscale='linear', yscale='linear',
                 padding={"bottom": 0.20},
                 annotation=None,
                 marker='', alpha_color=0.4, alpha_edge_color=0.8,
                 x_formatter=None, y_formatter=None,
                 **kwargs
                 ):
        DiagramBase.__init__(self, datasource=datasource, title=title, padding=padding, **kwargs)

        self.xlabel = str(xnum) + "/" + str(xdenom)
        self.ylabel = str(ynum) + "/" + str(ydenom)
        if title:
            self.title = title
        else:
            self.title = 'Diagram ' + self.xlabel + " vs " + self.ylabel
        self.xlim = xlim
        self.ylim = ylim
        self.xnum = xnum
        self.xdenom = xdenom
        self.ynum = ynum
        self.ydenom = ydenom
        self.xscale = xscale
        self.yscale = yscale
        self.annotation = annotation
        self.marker = marker
        self.alpha_color = alpha_color
        self.alpha_edge_color = alpha_edge_color
        self.x_formatter = x_formatter
        self.y_formatter = y_formatter

    def set_decorations(self):

        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        if self.ylim is not None:
            self.ax.set_ylim(self.ylim)
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)
        self.ax.set_yscale(self.yscale)
        self.ax.set_xscale(self.xscale)
        self.ax.tick_params(axis='x', labelsize=self.fontsize)
        self.ax.tick_params(axis='y', labelsize=self.fontsize)
        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)
        if self.x_formatter:
            self.ax.xaxis.set_major_formatter(self.x_formatter)
        if self.y_formatter:
            self.ax.yaxis.set_major_formatter(self.y_formatter)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                if self.marker != '':
                    mrk = self.marker
                else:
                    mrk = list(group["marker"])[0]

                if self.marker_size_scaled():
                    size = normalize_marker_size(group[self.markersize['var_scale']], self.markersize['val_max'],
                                                 self.markersize['val_min'], self.markersize['size_max'],
                                                 self.markersize['size_min'])
                else:
                    size = self.markersize

                xvals = group[self.xnum] / group[self.xdenom]
                yvals = group[self.ynum] / group[self.ydenom]

                sample_color = to_rgba(list(group["color"])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group["color"])[0], alpha=self.alpha_edge_color)

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(xvals, yvals, edgecolors=edge_color,
                                marker=mrk, label=name, facecolors=sample_color,
                                s=size, zorder=zorder)

                if self.annotation:
                    for i, sample in xvals.iteritems():
                        self.ax.annotate(group[self.annotation].get(i), (xvals.get(i), yvals[i]), fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

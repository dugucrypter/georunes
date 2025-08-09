import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.chemistry import val_el_to_mol
from georunes.tools.plotting import normalize_marker_size


class DiagramScatter3D(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource,
                 xvar, yvar, zvar, xlim=None, ylim=None, zlim=None,
                 xlabel='', ylabel='', zlabel='',
                 annotation=None,
                 xscale='linear', yscale='linear', zscale='linear',
                 padding=None,
                 marker='',
                 xmolar=False, ymolar=False, zmolar=False,
                 alpha_color=0.4, alpha_edge_color=0.8,
                 x_formatter=None, y_formatter=None, z_formatter=None,
                 markersize=70,
                 **kwargs
                 ):
        config_padding = {"bottom": 0.20}
        if padding:
            config_padding.update(padding)
        self.xlabel = xlabel if xlabel else str(xvar)
        self.ylabel = ylabel if ylabel else str(yvar)
        self.zlabel = zlabel if zlabel else str(zvar)
        DiagramBase.__init__(self, datasource=datasource,
                             title=self.xlabel + " vs " + self.ylabel + " vs " + self.zlabel,
                             padding=config_padding,
                             markersize=markersize,
                             **kwargs)

        self.xlim = xlim
        self.ylim = ylim
        self.zlim = zlim
        self.xvar = xvar
        self.yvar = yvar
        self.zvar = zvar
        self.annotation = annotation
        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale
        self.marker = marker
        self.alpha_color = alpha_color
        self.alpha_edge_color = alpha_edge_color
        self.xmolar = xmolar
        self.ymolar = ymolar
        self.zmolar = zmolar
        self.x_formatter = x_formatter
        self.y_formatter = y_formatter
        self.z_formatter = z_formatter

    def init_plot(self):
        if self.h_ratio is None:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111, projection='3d')
        else:
            if isinstance(self.h_ratio, tuple):
                self.fig = plt.figure(figsize=self.h_ratio)
                self.ax = self.fig.add_subplot(111, projection='3d')
            else:
                self.fig = plt.figure(igsize=plt.figaspect(self.h_ratio))
                self.ax = self.fig.add_subplot(111, projection='3d')

    def set_decorations(self):

        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        if self.ylim is not None:
            self.ax.set_ylim(self.ylim)
        if self.zlim is not None:
            self.ax.set_ylim(self.zlim)

        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_yscale(self.yscale)
        self.ax.set_xscale(self.xscale)
        self.ax.set_zscale(self.zscale)
        self.ax.tick_params(axis='x', labelsize=self.fontsize)
        self.ax.tick_params(axis='y', labelsize=self.fontsize)
        self.ax.tick_params(axis='z', labelsize=self.fontsize)
        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)
        self.ax.set_zlabel(self.zlabel, fontsize=self.fontsize)
        if self.x_formatter:
            self.ax.xaxis.set_major_formatter(self.x_formatter)
        if self.y_formatter:
            self.ax.yaxis.set_major_formatter(self.y_formatter)
        if self.z_formatter:
            self.ax.yaxis.set_major_formatter(self.y_formatter)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group and marker
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                if self.marker != '':
                    marker = self.marker
                else:
                    marker = list(group[self.marker_column])[0]

                if self.marker_size_scaled():
                    size = normalize_marker_size(group[self.markersize['var_scale']], self.markersize['val_max'],
                                                 self.markersize['val_min'], self.markersize['size_max'],
                                                 self.markersize['size_min'])
                else:
                    size = self.markersize

                if self.xmolar:
                    xvals = val_el_to_mol(group[self.xvar])
                else:
                    xvals = group[self.xvar]
                if self.ymolar:
                    yvals = val_el_to_mol(group[self.yvar])
                else:
                    yvals = group[self.yvar]
                if self.zmolar:
                    zvals = val_el_to_mol(group[self.zvar])
                else:
                    zvals = group[self.zvar]

                label = list(group[self.label_column])[0] if self.label_defined else name
                zorder = 4
                if self.zorder_column:
                    zorder = list(group[self.zorder_column])[0]

                sample_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_edge_color)
                self.ax.scatter(
                    xvals, yvals, zvals,
                    edgecolors=edge_color,
                    marker=marker, label=label,
                    facecolors=sample_color,
                    s=size,
                    zorder=zorder)

                if self.annotation:
                    for i, sample in xvals.items():
                        self.ax.text(xvals.get(i), yvals.get(i), zvals.get(i),group[self.annotation].get(i), fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

import math

import matplotlib.pyplot as plt
import ternary

from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer
from georunes.tools.plotting import normalize_marker_size


class DiagramTernaryBase(DiagramBase, LegendDrawer):
    def __init__(self, datasource,
                 top_var='', left_var='', right_var='',
                 top_label='', left_label='', right_label='',
                 tscale='linear', left_scale='linear', right_scale='linear',
                 padding={"bottom": 0.14},
                 marker='', annotation=None,
                 alpha_color=0.8, legend_ncol=4,
                 no_ticks=False, no_ticks_label=False,
                 h_ratio=None, vertical_ticks=False,
                 scale=100,
                 **kwargs
                 ):
        self.scale = scale
        DiagramBase.__init__(self, datasource=datasource, h_ratio=h_ratio, legend_ncol=legend_ncol, padding=padding,
                             **kwargs)
        self.annotation = annotation
        self.top_label = top_label
        self.left_label = left_label
        self.right_label = right_label
        self.top_var = top_var
        self.left_var = left_var
        self.right_var = right_var
        self.top_scale = tscale
        self.left_scale = left_scale
        self.right_scale = right_scale
        self.marker = marker
        self.alpha_color = alpha_color
        self.no_ticks = no_ticks
        self.no_ticks_label = no_ticks_label
        self.vertical_ticks = vertical_ticks

    def init_plot(self):
        ratio_parameter = math.sqrt(3) / 2
        if self.h_ratio:
            ratio_parameter = self.h_ratio
        self.fig, self.ax = plt.subplots(figsize=plt.figaspect(ratio_parameter))  # Ratio figure size
        self.tax = ternary.TernaryAxesSubplot(ax=self.ax, scale=self.scale)

    def plot_config(self, no_gridline=False, no_ticks=False, no_ticks_label=False):
        DiagramBase.plot_config(self)

        if not no_gridline:
            self.tax.gridlines(color="black", multiple=10, linewidth=0.5)
        self.tax.boundary(linewidth=2.0)

        self.tax.left_corner_label(self.left_label)
        self.tax.right_corner_label(self.right_label)
        self.tax.top_corner_label(self.top_label)

        if not self.no_title:
            if self.title == "":
                self.title = 'Triangular diagram'
            self.tax.set_title(self.title, pad=25)

        lw = 0 if no_ticks else 1

        if not no_ticks:
            if no_ticks_label:
                self.tax.ticks(multiple=10, axis='lbr', linewidth=lw, linestyle='-', tick_formats="")
            else:
                self.tax.ticks(multiple=10, axis='lbr', linewidth=lw, linestyle='-', fontsize=10, offset=0.02)

        if self.vertical_ticks:
            self.ax.set_xlim()
            self.ax.spines['bottom'].set_visible(False)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.get_xaxis().set_visible(False)
        else:
            self.tax.get_axes().axis('off')

    def plot(self):
        self.plot_config(no_gridline=False, no_ticks=self.no_ticks, no_ticks_label=self.no_ticks_label)

        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                var_sum = group[self.top_var] + group[self.left_var] + group[self.right_var]
                norm_z = 100 * group[self.left_var] / var_sum
                norm_x = 100 * group[self.right_var] / var_sum
                norm_y = 100 * group[self.top_var] / var_sum

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

                zorder = None
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                # Convert points to tuples
                points = [(norm_x.get(i), norm_y.get(i), norm_z.get(i)) for i, sample in
                          group[self.top_var].iteritems()]

                self.tax.scatter(points, edgecolors=group["color"],
                                 marker=mrk, label=name, facecolors=group["color"], s=size,
                                 alpha=self.alpha_color, zorder=zorder)

        self.plot_legend()
        self.tax.clear_matplotlib_ticks()

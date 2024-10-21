import math
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer
from georunes.plot.piper.piper_axe_subplot import PiperAxesSubplot
from georunes.tools.plotting import normalize_marker_size


class DiagramPiper(DiagramBase, LegendDrawer):
    def __init__(self, datasource,
                 padding=None,
                 marker='', annotation=None,
                 alpha_color=0.4,  alpha_edge_color=0.8,
                 legend_ncol=4,
                 delta=0.1,
                 no_ticks=False, no_ticks_label=False,
                 ticks_number=6, ticks_fontsize="small", ticks_clockwise=True, ticks_offset=0.03,
                 nb_grid_separators=9, show_gridlines=True,
                 show_axis=False,
                 h_ratio=None,
                 **kwargs
                 ):
        self.delta = delta
        if padding is None:
            padding = {"left": 0.06, "right": 0.98}
        self.fig = None
        self.ax = None
        self.pax = None
        DiagramBase.__init__(self, datasource=datasource,  h_ratio=h_ratio, legend_ncol=legend_ncol, padding=padding,
                             **kwargs)
        self.annotation = annotation
        self.marker = marker
        self.alpha_color = alpha_color
        self.alpha_edge_color = alpha_edge_color
        self.no_ticks = no_ticks
        self.no_ticks_label = no_ticks_label
        self.ticks_number = ticks_number
        self.ticks_fontsize = ticks_fontsize
        self.ticks_clockwise = ticks_clockwise
        self.ticks_offset = ticks_offset
        self.show_gridlines = show_gridlines
        self.nb_grid_separators = nb_grid_separators
        self.show_axis = show_axis

    def init_plot(self):
        ratio_parameter = math.sqrt(3) / 2
        if self.h_ratio:
            ratio_parameter = self.h_ratio
        self.fig, self.ax = plt.subplots(figsize=plt.figaspect(ratio_parameter))  # Ratio figure size
        self.pax = PiperAxesSubplot(ax=self.ax, delta=self.delta)

    def plot_config(self):
        DiagramBase.plot_config(self)

        if self.show_gridlines:
            self.pax.gridlines(color="black", num_seps=self.nb_grid_separators, linewidth=0.5)
        self.pax.boundary(linewidth=1.0)

        if not self.no_title:
            if self.title == "":
                self.title = 'Piper diagram'
            self.pax.set_title(self.title)

        if not self.no_ticks:  # Show ticks
            self.pax.ticks(linewidth=1, num_ticks=self.ticks_number, clockwise=self.ticks_clockwise,
                           offset=self.ticks_offset, fontsize=self.ticks_fontsize)

        if not self.no_ticks_label:  # Show labels
            self.pax.set_labels_visible()

    def set_decorations(self, ):
        self.pax.set_xlim(-0.1, 1.1)
        self.pax.set_ylim(-0.08, 0.94)
        if not self.show_axis:
            self.pax.set_axis_off()

    def plot(self):
        self.plot_config()
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

                label = list(group['label'])[0] if self.label_defined else name
                zorder = None
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                # Convert points to tuples
                points = [(group["Ca"].get(i), group["Mg"].get(i), group["Na"].get(i), group["K"].get(i),
                           group["HCO3"].get(i), group["CO3"].get(i), group["SO4"].get(i), group["Cl"].get(i))
                          for i, sample in group["Ca"].items()]

                sample_color = to_rgba(list(group["color"])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group["color"])[0], alpha=self.alpha_edge_color)
                self.pax.scatter(points, edgecolors=edge_color,
                                 marker=mrk, label=label, facecolors=sample_color, s=size,
                                 zorder=zorder)

        self.plot_legend()

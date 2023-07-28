from functools import partial
import numpy as np
from matplotlib import pyplot
from georunes.plot.piper import lines
from georunes.plot.piper.helpers import project_left_triangle, project_right_triangle, project_diamond
from georunes.plot.piper.plotting import scatter, plot
from georunes.tools.language import format_chemical_formula as _fml


def figure(ax=None, delta=0.2):
    """
    Wraps a PiperAxesSubplot
    """
    piper_ax = PiperAxesSubplot(ax=ax, delta=delta)
    return piper_ax.get_figure(), piper_ax


def mpl_redraw_callback(event, pax):
    """
    Callback to properly rotate and redraw text labels when the plot is drawn
    or resized.

    Parameters
    ----------
    event: a matplotlib event
        either 'resize_event' or 'draw_event'
    pax: PiperAxesSubplot
         the PiperAxesSubplot
    """
    pax._redraw_labels()


class PiperAxesSubplot(object):
    """
    AxesSubplot for Piper diagram
    """

    def __init__(self, ax=None, delta=0.1, labels_fontsize=8):

        if ax:
            self.ax = ax
        else:
            _, self.ax = pyplot.subplots()

        # Container for the axis labels supplied by the user
        self._labels_fontsize = labels_fontsize
        self._ticks = dict()
        # Container for the redrawing of labels
        self._to_remove = []
        self._connect_callbacks()
        self._delta = delta
        self._hide_labels = True

    def _connect_callbacks(self):
        """Connect resize matplotlib callbacks."""
        fig = self.get_figure()
        callback = partial(mpl_redraw_callback, pax=self)
        event_names = ('resize_event', 'draw_event')
        for event_name in event_names:
            fig.canvas.mpl_connect(event_name, callback)

    def __repr__(self):
        return "PiperAxesSubplot: %s" % self.ax.__hash__()

    def get_axes(self):
        """Returns the underlying PiperAxesSubplot object."""
        return self.ax

    def get_figure(self):
        """Return the underlying matplotlib figure object."""
        ax = self.get_axes()
        return ax.get_figure()

    def set_axis_off(self):
        ax = self.get_axes()
        ax.set_axis_off()

    def set_title(self, title, **kwargs):
        """Sets the title on the underlying PiperAxesSubplot."""
        ax = self.get_axes()
        ax.set_title(title, **kwargs)

    def set_labels_visible(self):
        self._hide_labels = False

    def boundary(self, axes_colors=None, **kwargs):
        ax = self.get_axes()
        lines.boundary(ax=ax, axes_colors=axes_colors, delta=self._delta, **kwargs)

    def gridlines(self, num_seps=9, **kwargs):
        ax = self.get_axes()
        lines.gridlines(num_seps=num_seps, ax=ax, delta=self._delta, **kwargs)

    def close(self):
        fig = self.get_figure()
        pyplot.close(fig)

    def legend(self, *args, **kwargs):
        ax = self.get_axes()
        ax.legend(*args, **kwargs)

    def savefig(self, filename,  **kwargs):
        self._redraw_labels()
        fig = self.get_figure()
        fig.savefig(filename, **kwargs)

    def show(self):
        self._redraw_labels()
        pyplot.show()

    def ticks(self, ticks=None, num_ticks=6, locations=None, clockwise=False, axes_colors=None, tick_formats=None,
              **kwargs):
        if axes_colors is None:
            axes_colors = "black"
        ax = self.get_axes()
        delta = self._delta
        lines.ticks(ax, delta=delta, list_ticks=ticks, num_ticks=num_ticks, locations=locations,
                    clockwise=clockwise, axes_colors=axes_colors, tick_formats=tick_formats,
                    **kwargs)

    def set_xlim(self, xmin, xmax):
        ax = self.get_axes()
        return ax.set_xlim(xmin, xmax)

    def set_ylim(self, ymin, ymax):
        ax = self.get_axes()
        return ax.set_ylim(ymin, ymax)

    # Redrawing and resizing
    def _redraw_labels(self):
        """Redraw axis labels, typically after draw or resize events."""
        if not self._hide_labels:
            ax = self.get_axes()

            # Remove any previous labels
            for mpl_object in self._to_remove:
                mpl_object.remove()
            self._to_remove = []

            # Redraw the labels with the appropriate angles
            label_data = [
                ["Ca", project_left_triangle((1, 0, 0), delta=self._delta, drift=(0, -0.08)), "center", 0],
                ["Mg", project_left_triangle((0, 1, 0), delta=self._delta, drift=(-0.01, 0.05)), "center", 0],
                ["Na+K", project_left_triangle((0, 0, 1), delta=self._delta, drift=(0, -0.08)), "center", 0],
                [_fml("HCO3+CO3"), project_right_triangle((1, 0, 0),
                                                          delta=self._delta, drift=(0.03, -0.08)), "center", 0],
                [_fml("SO4"), project_right_triangle((0, 1, 0), delta=self._delta, drift=(0, 0.05)), "center", 0],
                ["Cl", project_right_triangle((0, 0, 1), delta=self._delta, drift=(0, -0.08)), "center", 0],
                [_fml("SO4+Cl"), project_diamond((0, 0.5), delta=self._delta, drift=(-0.07, 0)), "center", 60],
                ["Ca+Mg", project_diamond((0.5, 1), delta=self._delta, drift=(0.07, 0)), "center", -60],
            ]

            for label, position, halign, rotation in label_data:
                x, y = position[0], position[1]
                pos_a = np.array([x, y])
                new_rotation = ax.transData.transform_angles(np.array((rotation,)), pos_a.reshape((1, 2)))[0]
                text = ax.text(x, y, label, horizontalalignment=halign, rotation=new_rotation, transform=ax.transData,
                               fontsize=self._labels_fontsize, )
                self._to_remove.append(text)

    def scatter(self, points, **kwargs):
        delta = self._delta
        ax = self.get_axes()
        plot_ = scatter(points, ax=ax, delta=delta, **kwargs)
        return plot_

    def plot(self, points, **kwargs):
        ax = self.get_axes()
        plot(points, delta=self._delta, ax=ax, **kwargs)

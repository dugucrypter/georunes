from matplotlib.lines import Line2D
from matplotlib.ticker import StrMethodFormatter
from numpy import arange
from georunes.plot.piper.helpers import COS60, SIN60, COS45, project_two_triangles, project_diamond


class CustomFormatter(StrMethodFormatter):
    """
    A child of the StrMethodFormatter class with different formatting if the number is decimal or integer.
    """
    def __init__(self, fmt="%.2f", integer_fmt="%d"):
        super().__init__(fmt)
        self.integer_fmt = integer_fmt

    def format_value(self, value):
        value = round(value, 6)  # A trick to deal with numbers with not exactly precise decimals
        if isinstance(value, float) and value.is_integer():
            return self.integer_fmt % value
        else:
            return self.fmt % value


def line_ions(ax, p1, p2, delta, **kwargs):
    """
    Draws similar lines in the lower fields

    Parameters
    ----------
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    p1: 2-tuple
        The (x,y) starting coordinates
    p2: 2-tuple
        The (x,y) ending coordinates
    delta:
        The space separating the triangles (considering that the width of the diagram is scaled to 1).
    kwargs:
        Any kwargs to pass through to Matplotlib.
    """
    lp1, rp1 = project_two_triangles(p1, delta)
    lp2, rp2 = project_two_triangles(p2, delta)
    ax.add_line(Line2D((lp1[0], lp2[0]), (lp1[1], lp2[1]), **kwargs))
    ax.add_line(Line2D((rp1[0], rp2[0]), (rp1[1], rp2[1]), **kwargs))


def line_diamond(ax, p1, p2, delta, **kwargs):
    """
    Draws similar line in the diamond

    Parameters
    ----------
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    p1: 2-tuple
        The (x,y) starting coordinates
    p2: 2-tuple
        The (x,y) ending coordinates
    delta:
        The space separating the triangles (considering that the width of the diagram is scaled to 1).
    kwargs:
        Any kwargs to pass through to Matplotlib.
    """

    tp1 = project_diamond(p1, delta)
    tp2 = project_diamond(p2, delta)
    ax.add_line(Line2D((tp1[0], tp2[0]), (tp1[1], tp2[1]), **kwargs))


def boundary(ax, delta, axes_colors=None,  **kwargs):
    """
    Plots the boundary of the simplex. Creates and returns matplotlib axis if
    none given.

    Parameters
    ----------
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    delta:
        The space separating the triangles (considering that the width of the diagram is scaled to 1).
    kwargs:
        Any kwargs to pass through to matplotlib.
    axes_colors:
        Option for coloring boundaries different colors.
    """
    pos_top = (0, 1, 0)
    pos_left = (1, 0, 0)
    pos_right = (0, 0, 1)
    dm_left = (0, 0)
    dm_down = (1, 0)
    dm_right = (1, 1)
    dm_up = (0, 1)

    # Set default color as black.
    if axes_colors is None:
        axes_colors = 'black'

    # Horizontal
    line_ions(ax, (*pos_left, *pos_left,), (*pos_right, *pos_right), delta=delta, color=axes_colors, **kwargs)

    # Left
    line_ions(ax, (*pos_top, *pos_top), (*pos_left, *pos_left), delta=delta, color=axes_colors, **kwargs)
    line_diamond(ax, dm_left, dm_up, delta, color=axes_colors, **kwargs)
    line_diamond(ax, dm_down, dm_right, delta, color=axes_colors, **kwargs)

    # Right
    line_ions(ax, (*pos_top, *pos_top), (*pos_right, *pos_right), delta=delta, color=axes_colors, **kwargs)
    line_diamond(ax, dm_left, dm_down, delta=delta, color=axes_colors, **kwargs)
    line_diamond(ax, dm_up, dm_right, delta=delta, color=axes_colors, **kwargs)

    return ax


def gridlines(ax, num_seps=9, delta=0.1, **kwargs):
    """
    Plots grid lines excluding boundary.

    Parameters
    ----------
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    num_seps :
        The number of internal lines by parameter, inside triangles and diamond
    delta:
        The space separating the triangles (considering that the width of the diagram is scaled to 1).
    kwargs:
        Any kwargs to pass through to matplotlib
    """

    if 'linewidth' not in kwargs:
        kwargs["linewidth"] = 0.5
    if 'linestyle' not in kwargs:
        kwargs["linestyle"] = ':'

    interval = 1/(num_seps+1)

    # Draw grid-lines
    # Parallel to horizontal axis
    for i in arange(0, 1, interval):
        # In lower fields
        p1 = (1 - i, i, 0, 1 - i, i, 0)
        p2 = (0, i, 1 - i, 0, i, 1 - i)
        line_ions(ax, p1, p2, delta, **kwargs)

    # Parallel to left and right axes
    for i in arange(0, 1, interval):
        # Left lines
        # In lower fields
        p1 = (1 - i, 0, i, 1 - i, 0, i,)
        p2 = (0, 1 - i, i, 0, 1 - i, i,)
        line_ions(ax, p1, p2, delta, **kwargs)

        # In diamond
        pt1 = (i, 0)
        pt2 = (i, 1)
        line_diamond(ax, pt1, pt2, delta, **kwargs)

        # Right lines
        # In lower fields
        p1 = (i, 0, 1 - i, i, 0, 1 - i,)
        p2 = (i, 1 - i, 0, i, 1 - i, 0,)
        line_ions(ax, p1, p2, delta, **kwargs)
        line_ions(ax, p1, p2, delta, **kwargs)

        # In diamond
        pt1 = (0, i)
        pt2 = (1, i)
        line_diamond(ax, pt1, pt2, delta, **kwargs)

    return ax


def ticks(ax, delta, list_ticks=None, locations=None, num_ticks=6, offset=0.01, clockwise=False, axes_colors=None,
          fontsize=10, tick_formats=None, **kwargs):
    """
    Sets tick marks and labels.

    Parameters
    ----------
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    delta:
        The space separating the triangles (considering that the width of the diagram is scaled to 1).
    list_ticks: list of strings, None
        The tick labels
    locations: list of points, None
        The locations of the ticks
    num_ticks:
        The number of tick on each axis
    offset: float, 0.01
        controls the length of the ticks
    clockwise: bool, False
        Draw ticks marks clockwise or counterclockwise
    axes_colors:
        Option to color ticks differently for each axis,
    fontsize:
        Ticks label fontsize,
    tick_formats: None, Str
        If None, all axes will be labelled with ints.
    kwargs:
        Any kwargs to pass through to matplotlib.

    """
    if tick_formats is None:
        tick_formats = CustomFormatter()
    if axes_colors is None:
        axes_colors = "black"
    length = offset / 3

    if list_ticks and not locations:
        num_ticks = len(list_ticks)
        if num_ticks != 0:
            interval = 1 / (num_ticks - 1)
            locations = arange(0, 1 + interval, interval)

    if not list_ticks:
        interval = 1 / (num_ticks - 1)
        locations = arange(0, 1 + interval, interval)
        list_ticks = locations

    # Right axis
    for index, i in enumerate(locations):
        loc = (0, i, 1 - i)
        if clockwise:
            tick = list_ticks[-(index + 1)]
        else:
            tick = list_ticks[index]

        # Two lower fields
        tl, tr = project_two_triangles((*loc, *loc), delta)
        ax.add_line(
            Line2D((tl[0], tl[0] + length * COS60), (tl[1], tl[1] + length * SIN60), color=axes_colors, **kwargs))
        ax.add_line(
            Line2D((tr[0], tr[0] + length * COS60), (tl[1], tl[1] + length * SIN60), color=axes_colors, **kwargs))

        # Diamond field
        ttl = project_diamond((1 - i, 0), delta)
        ttr = project_diamond((1 - i, 1), delta)
        ax.add_line(Line2D(
            (ttl[0], ttl[0] + length * COS60), (ttl[1], ttl[1] + length * SIN60),
            color=axes_colors, **kwargs))
        ax.add_line(Line2D(
            (ttr[0], ttr[0] + length * COS60), (ttr[1], ttr[1] + length * SIN60),
            color=axes_colors, **kwargs))

        # Text
        pl, pr = project_two_triangles((*loc, *loc), delta)
        pt = project_diamond((1 - i, 1), delta)
        s = tick_formats.format_value(tick * 100)
        ax.text(pl[0] + 0.6 * offset * COS45, pl[1] + 0.6 * offset * COS45, s, horizontalalignment="left",
                color=axes_colors, fontsize=fontsize)
        ax.text(pr[0] + 0.6 * offset * COS45, pr[1] + 0.6 * offset * COS45, s, horizontalalignment="left",
                color=axes_colors, fontsize=fontsize)
        ax.text(pt[0] + 0.6 * offset * COS45, pt[1] + 0.6 * offset * COS45, s, horizontalalignment="left",
                color=axes_colors, fontsize=fontsize)

    # Left axis
    for index, i in enumerate(locations):
        loc = (1 - i, i, 0)
        if clockwise:
            tick = list_ticks[index]
        else:
            tick = list_ticks[-(index + 1)]

        # Two lower fields
        tl, tr = project_two_triangles((*loc, *loc), delta)
        ax.add_line(Line2D(
            (tl[0], tl[0] - length * COS60), (tl[1], tl[1] + length * SIN60),
            color=axes_colors, **kwargs))
        ax.add_line(Line2D(
            (tr[0], tr[0] - length * COS60), (tl[1], tl[1] + length * SIN60),
            color=axes_colors, **kwargs))

        # Diamond field
        ttl = project_diamond((0, 1 - i), delta)
        ttr = project_diamond((1, 1 - i), delta)
        ax.add_line(Line2D(
            (ttl[0], ttl[0] - length * COS60), (ttl[1], ttl[1] + length * SIN60),
            color=axes_colors, **kwargs))
        ax.add_line(Line2D(
            (ttr[0], ttr[0] - length * COS60), (ttr[1], ttr[1] + length * SIN60),
            color=axes_colors, **kwargs))

        # Text
        pl, pr = project_two_triangles((*loc, *loc), delta)
        pt = project_diamond((0, 1 - i), delta)
        s = tick_formats.format_value(tick * 100)
        ax.text(pl[0] - offset * COS45, pl[1], s, horizontalalignment="right",
                color=axes_colors, fontsize=fontsize)
        ax.text(pr[0] - offset * COS45, pr[1], s, horizontalalignment="right",
                color=axes_colors, fontsize=fontsize)
        ax.text(pt[0] - offset * COS45, pt[1], s, horizontalalignment="right",
                color=axes_colors, fontsize=fontsize)

    # Bottom axis
    for index, i in enumerate(locations):
        loc = (1-i, 0, i)
        if clockwise:
            # Right parallel
            tick = list_ticks[-index-1]
        else:
            tick = list_ticks[index]

        tl, tr = project_two_triangles((*loc, *loc), delta)
        ax.add_line(Line2D(
            (tl[0], tl[0]),  (tl[1], tl[1] - length*SIN60),
            color=axes_colors, **kwargs))
        ax.add_line(Line2D(
            (tr[0], tr[0]), (tl[1], tl[1] - length * SIN60),
            color=axes_colors, **kwargs))

        # Text
        pl, pr = project_two_triangles((*loc, *loc), delta)
        s = tick_formats.format_value(tick*100)
        ax.text(pl[0], pl[1]-1.4*offset, s, horizontalalignment="center",
                color=axes_colors, fontsize=fontsize)
        ax.text(pr[0], pr[1]-1.4*offset, s, horizontalalignment="center",
                color=axes_colors, fontsize=fontsize)

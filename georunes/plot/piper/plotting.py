from matplotlib import pyplot
from georunes.plot.piper import helpers as pip
from georunes.plot.piper.helpers import split_by_field
from georunes.tools.data import repeat_list


def scatter(points, delta, ax=None, edgecolors=None, facecolors=None, **kwargs):
    """
    Plots points of composition (Ca, Mg, Na + K, HCO3+ CO3, SO4, Cl) in a Piper diagram

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be scatter-plotted.
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    edgecolors :
        Colors of the marker's edges
    facecolors :
        Colors for filling the markers
    delta:
        The space separating the triangles (considering that the width of the diagram is scaled to 1).
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not ax:
        fig, ax = pyplot.subplots()
    xs, ys = pip.project_sequence(points, delta=delta)
    ax.scatter(xs, ys, edgecolors=repeat_list(edgecolors, len(xs)), facecolors=repeat_list(facecolors,  len(xs)),  **kwargs)
    return ax


def plot(points, delta, ax=None, **kwargs):
    """
    Plots trajectory points of composition (Ca, Mg, Na + K, HCO3+ CO3, SO4, Cl) in a Piper diagram

    Parameters
    ----------
    points: List of 3-tuples
        The list of tuples to be plotted as a connected curve.
    delta:
    ax: PiperAxesSubplot, None
        The subplot to draw on.
    kwargs:
        Any kwargs to pass through to matplotlib.
    """
    if not ax:
        fig, ax = pyplot.subplots()
    xs, ys = pip.project_sequence(points, delta)
    splitted = split_by_field(xs, ys)
    for xsp, ysp in splitted:
        ax.plot(xsp, ysp, **kwargs)
    return ax

import math
import numpy as np
from scipy import interpolate

sin60 = math.sqrt(3) / 2


def get_spline(x, y, prec=50):
    # get the cumulative distance along the contour
    dist = np.sqrt((x[:-1] - x[1:]) ** 2 + (y[:-1] - y[1:]) ** 2)
    dist_along = np.concatenate(([0], dist.cumsum()))

    # build a spline representation of the contour
    spline, u = interpolate.splprep([x, y], u=dist_along, s=0)

    # resample it at smaller distance intervals
    interp_d = np.linspace(dist_along[0], dist_along[-1], prec)
    interp_x, interp_y = interpolate.splev(interp_d, spline)
    return (interp_x, interp_y)


def tern_coords_to_bin_coords(rvar, tvar, lvar=None, scale=100):
    xvar = tvar / 2 + rvar
    yvar = tvar * sin60
    return (xvar, yvar)


def normalize_marker_size(serie, val_max, val_min, size_max, size_min):
    if size_max is None:
        size_max = 100
    if size_min is None:
        size_min = 1

    a = (size_max - size_min) / (val_max - val_min)

    b = size_max - a * val_max
    size_serie = serie * a + b

    return size_serie


def is_in_canvas(x, y, xlim, ylim):
    # Check if element is in canvas
    return ((x > xlim[0]) and (x < xlim[1]) and (y > ylim[0]) and (y < ylim[1]))

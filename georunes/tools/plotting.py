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
    return interp_x, interp_y


def tern_coords_to_bin_coords(rvar, tvar, lvar=None, scale=100):
    xvar = tvar / 2 + rvar
    yvar = tvar * sin60
    return xvar, yvar


def normalize_marker_size(serie, val_max, val_min, size_max, size_min, log_scale=True):
    if size_max is None:
        size_max = 18
    if size_min is None:
        size_min = 1

    serie = np.clip(serie, a_min=val_min, a_max=val_max)
    if log_scale:
        if val_min <= 0:
            raise ValueError("val_min must be > 0 when log_scale=True.")
        serie_scaled = np.log10(serie)
        val_min_scaled = np.log10(val_min)
        val_max_scaled = np.log10(val_max)
    else:
        serie_scaled = serie
        val_min_scaled = val_min
        val_max_scaled = val_max
    a = (size_max - size_min) / (val_max_scaled - val_min_scaled)
    b = size_min - a * val_min_scaled
    size_serie = a * serie_scaled + b

    return np.nan_to_num(size_serie, nan=0)


def is_in_canvas(x, y, xlim, ylim):
    # Check if element is in canvas
    return (x > xlim[0]) and (x < xlim[1]) and (y > ylim[0]) and (y < ylim[1])

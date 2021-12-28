import random
from matplotlib import colors as mplcol


def darken_color(color, percent=10):
    fcol = list(mplcol.to_rgba(color))
    for i in range(4):
        fcol[i] = max(0, fcol[i] * (1 - percent / 100))
    return fcol


def near_color(color):
    col = mplcol.to_rgba_array(color)[0]

    cr = col[0]
    cg = col[1]
    cb = col[2]

    cr = cr + (-100 + random.randint(0, 200)) / 255.
    cg = cg + (-100 + random.randint(0, 200)) / 255.
    cb = cb + (-100 + random.randint(0, 200)) / 255.

    return (cr, cg, cb, 1)

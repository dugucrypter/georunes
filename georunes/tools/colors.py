import random
import numpy as np
from matplotlib import colors as mplcol
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


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


def merge_colormaps(cmap1_name, cmap2_name, ratio=0.5, name='merged_cmap'):
    """
    Merge two matplotlib colormaps into one.

    Parameters:
        cmap1_name (str): Name of the first colormap (e.g., 'Blues')
        cmap2_name (str): Name of the second colormap (e.g., 'Oranges')
        ratio (float): Fraction of the output colormap to use from cmap1 (0 < ratio < 1)
        name (str): Name of the new colormap

    Returns:
        LinearSegmentedColormap: Merged colormap
    """
    assert 0 < ratio < 1, "Ratio must be between 0 and 1"

    n = 256
    n1 = int(n * ratio)
    n2 = n - n1

    cmap1 = plt.get_cmap(cmap1_name)
    cmap2 = plt.get_cmap(cmap2_name)

    colors1 = cmap1(np.linspace(0, 1, n1))
    colors2 = cmap2(np.linspace(0, 1, n2))
    combined = np.vstack((colors1, colors2))

    return LinearSegmentedColormap.from_list(name, combined)
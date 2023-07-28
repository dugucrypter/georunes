from itertools import chain
from math import sqrt
import numpy as np
from georunes.tools.chemistry import el_molar_mass as _mm

COS60 = 1 / 2
SIN60 = sqrt(3) / 2
COS45 = SIN45 = sqrt(2) / 2

ratio_meq = {
    "Ca2+": 2 / _mm["Ca"],
    "Mg2+": 2 / _mm["Mg"],
    "Na+": 1 / _mm["Na"],
    "K+": 1 / _mm["K"],
    "HCO3-": 1 / (_mm["H"] + _mm["C"] + _mm["O"] * 3),
    "CO3-": 1 / (_mm["C"] + _mm["O"] * 3),
    "SO42-": 2 / (_mm["S"] + _mm["O"] * 4),
    "Cl-": 1 / _mm["Cl"],
}


def ions_mgl_to_meq(p):
    _ca, _mg, _na, _k, _hco, _co, _so, _cl = p
    ca = cations_mgl_to_meq((_ca, _mg, _na, _k))
    an = anions_mgl_to_meq((_hco, _co, _so, _cl))
    return *ca, *an


def cations_mgl_to_meq(cations):
    _ca, _mg, _na, _k = cations
    ca = _ca * ratio_meq["Ca2+"]
    mg = _mg * ratio_meq["Mg2+"]
    nak = _na * ratio_meq["Na+"] + _k * ratio_meq["K+"]
    return ca, mg, nak


def anions_mgl_to_meq(anions):
    _hco, _co, _so, _cl = anions
    hco = _hco * ratio_meq["HCO3-"] + _co * ratio_meq["CO3-"]
    so = _so * ratio_meq["SO42-"]
    cl = _cl * ratio_meq["Cl-"]
    return hco, so, cl


def camg_mgl_to_meq(_ca, _mg):
    ca = _ca * ratio_meq["Ca2+"]
    mg = _mg * ratio_meq["Mg2+"]
    return ca + mg


def socl_mgl_to_meq(_so, _cl):
    so = _so * ratio_meq["SO42-"]
    cl = _cl * ratio_meq["Cl-"]
    return so + cl


def diamond_ox(delta):
    """ Get the X position of the left vertex of the diamond """
    width = (1 - delta) / 2
    return width / 2 + delta * COS60


def diamond_oy(delta):
    """ Get the Y position of the left vertex of the diamond """
    width = (1 - delta) / 2
    return width * SIN60 + delta * SIN60


def unzip(list_tuples):
    """[(a1, b1), ..., (an, bn)] ----> ([a1, ..., an], [b1, ..., bn])"""
    return list(zip(*list_tuples))


def project_sequence(seq, delta):
    """
    Projects a point or sequence of points using `project_point`.
    Returns the points in coordinates as two lists xs and ys
    """
    # Projection -> [ [[x1_cation, y1_cation], [x1_anion, y1_anion], [x1_diamond, y1_diamond]],
    #                 [[x2_cation, y2_cation], [x2_anion, y2_anion], [x2_diamond, y2_diamond]], ... ]
    projected = [project_points_piper(p, delta) for p in seq]

    # Group by coordinates
    #           -> [ [(x1_cation, x1_anion, x1_diamond), (y1_cation, y1_anion, y1_diamond)],
    #                [(x2_cation, x2_anion, x2_diamond), (y2_cation, y2_anion, y2_diamond)], ... ]
    list_tripoints = [unzip(pts) for pts in projected]

    # Merge in unique list for each coordinate
    #            -> [[x1_cation, x1_anion, x1_diamond, x2_cation, x2_anion, x2_diamond, ...],
    #                [y1_cation, y1_anion, y1_diamond, y2_cation, , y2_anion, y2_diamond, ...]]
    merged = [list(chain(*items)) for items in zip(*list_tripoints)]
    return merged


def project_points_piper(p, delta):
    """ Maps p = (ca, mg, na, k, hco3, co3, so, cl) coordinates to planar simplex. """
    width = (1 - delta) / 2
    ca, mg, nak, hco, so, cl = ions_mgl_to_meq(p)

    val_left = nak / (mg + ca + nak)
    val_right = (so + cl) / (so + hco + cl)

    tx = diamond_ox(delta) + val_left * width * COS60 + val_right * width * COS60
    ty = diamond_oy(delta) + width * val_left * (-1) * SIN60 + width * val_right * SIN60
    lx = width * (COS60 * (2 * nak + mg) / (mg + ca + nak))
    ly = width * SIN60 * mg / (mg + ca + nak)
    rx = width + delta + width * (COS60 * (2 * cl + so) / (so + hco + cl))
    ry = width * SIN60 * so / (so + hco + cl)

    return [[lx, ly], [rx, ry], [tx, ty]]


def project_ions_diamond(p, delta, drift=None):
    """ Get (ca,mg,so,cl) and return (x,y) position """
    if drift is None:
        drift = (0, 0)
    _ca, _mg, _so, _cl = p
    camg = camg_mgl_to_meq(_ca, _mg)
    socl = socl_mgl_to_meq(_so, _cl)
    width = (1 - delta) / 2
    tx = diamond_ox(delta) + camg * width * COS60 + socl * width * COS60
    ty = diamond_oy(delta) + camg * width * (-1) * SIN60 + socl * width * SIN60
    return [tx + drift[0], ty + drift[1]]


def project_two_triangles(p, delta, drift=None):
    """
    Maps p = (llf, ltp, lrt, rlf, rtp, rrt) to planar simplex in the anions and cations triangles,
    returns 2 couples (x,y)
    """
    if drift is None:
        drift = (0, 0)
    llf, ltp, lrt, rlf, rtp, rrt = p
    return [project_left_triangle(( llf, ltp, lrt), delta=delta, drift=drift),
            project_right_triangle((rlf, rtp, rrt), delta=delta, drift=drift)]


def project_left_triangle(p, delta, drift=None):
    """ Maps p = (left, top, right) composition to planar simplex in the cations triangle, returns a couple (x,y) """
    if drift is None:
        drift = (0, 0)
    lf, tp, rt = p
    width = (1 - delta) / 2
    lx = width * (0.5 * (2 * rt + tp) / (tp + lf + rt))
    ly = width * (sqrt(3) / 2) * tp / (tp + lf + rt)
    return [lx + drift[0], ly + drift[1]]


def project_right_triangle(p, delta, drift=None):
    """ Maps p = (left, top, right)  to planar simplex in the anions triangle, returns a couple (x,y) """
    if drift is None:
        drift = (0, 0)
    lf, tp, rt = p
    width = (1 - delta) / 2
    rx = width + delta + width * (0.5 * (2 * rt + tp) / (tp + lf + rt))
    ry = width * (sqrt(3) / 2) * tp / (tp + lf + rt)
    return [rx + drift[0], ry + drift[1]]


def project_diamond(p, delta, drift=None):
    """ Get (ca,mg,so,cl) and return (x,y) position """
    if drift is None:
        drift = (0, 0)
    down_left, down_right = p
    width = (1 - delta) / 2
    tx = diamond_ox(delta) + down_left * width * COS60 + down_right * width * COS60
    ty = diamond_oy(delta) + down_left * width * (-1) * SIN60 + down_right * width * SIN60
    return [tx + drift[0], ty + drift[1]]


def split_by_field(xs, ys):
    """ Get x and y list of points, return 3 lists for any a field (left, right and diamond). """
    x3 = np.array_split(xs, 3)
    xsp = list(zip(*x3))
    y3 = np.array_split(ys, 3)
    ysp = list(zip(*y3))
    return list(zip(xsp, ysp))

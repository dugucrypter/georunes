import math
import numpy as np


def nan_to_none(x, y):
    nx, ny = x, y
    if x is not None and math.isnan(x):
        nx = None
    if y is not None and math.isnan(y):
        ny = None
    return nx, ny


def min_wo_none(x, y):
    x, y = nan_to_none(x, y)
    if (x is None) and (y is None):
        return np.nan
    elif x is None:
        return y
    elif y is None:
        return x
    else:
        return min(x, y)


def gg_max(x, y):
    x, y = nan_to_none(x, y)
    if (x is None) and (y is None):
        return np.nan
    elif x is None:
        return y
    elif y is None:
        return x
    else:
        return max(x, y)


# Function to get min in each colum of two rows
def row_min(old_row, cur_row):
    if not old_row:
        return cur_row

        # Check if same length
    if len(old_row) != len(cur_row):
        raise ValueError('Two rows doesn\' have the same size !')

    new_row = []
    for x, y in zip(old_row, cur_row):
        new_row.append(min_wo_none(x, y))
    return new_row


# Function to get max in each colum of two rows
def row_max(old_row, cur_row):
    if not old_row:
        return cur_row

    # Check if same length
    if len(old_row) != len(cur_row):
        raise ValueError('Two rows doesn\' have the same size !')

    new_row = []
    for x, y in zip(old_row, cur_row):
        new_row.append(gg_max(x, y))

    return new_row


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def float_or_zero(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def linspace(start, stop, num, round_to=3):
    lns = np.linspace(start, stop, num)
    return [round(val, round_to) for val in lns]


def linspace_to_end(b, x, ndigits=5):
    if x <= 1:
        return [b] if x == 1 else []
    step = b / x  # divide into x equal parts, so we skip the 0
    return [round((i + 1) * step, ndigits) for i in range(x)]


def round_ceil_n_digits(value, n):
    multiplier = 10 ** n
    return math.ceil(value * multiplier) / multiplier


def round_floor_n_digits(value, n):
    multiplier = 10 ** n
    return math.floor(value * multiplier) / multiplier


# Get the key from a value in a dictionary
def get_key(dictionary, value):
    key_list = list(dictionary.keys())
    val_list = list(dictionary.values())
    position = val_list.index(value)
    return key_list[position]


def repeat_list(lst, n):
    return [lst] * n
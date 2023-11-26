import itertools
import warnings
from pathlib import Path
import pandas as pd
import matplotlib.cm as cm
from matplotlib.colors import to_hex
from georunes.tools.data import unique

_vtc = ('color', 'marker', 'order', 'zorder', 'label',)

_markers = ("o", "s", "p", "*", "<", ">", "^", "8", "h", "H", "+",
            "x", "X", "D", "d", "v", "1", "2" "3", "4", "|", "_", ".", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)


def check_data(dataset, group_name="group", supp_group=None, supp_vtc=None, ignore_checking_markers=False):
    if supp_group:
        list_group = [group_name, *supp_group]
    else:
        list_group = group_name

    if supp_vtc:
        vtc = itertools.chain(_vtc, supp_vtc)
    else:
        vtc = _vtc

    if ignore_checking_markers:
        a = list(vtc)
        a.remove('marker')
        vtc = tuple(a)

    if group_name not in dataset.keys():
        raise ValueError("Group name '" + str(group_name) + "' not found in dataset")

    groups = dataset.groupby(list_group)
    for name, group in groups:

        for field in vtc:
            if field in group.columns:

                test_value = list(group[field])[0]

                for val in group[field]:
                    if val != test_value:
                        raise ValueError("Different values for group " + str(name) +
                                         " and field " + str(field) + " : " +
                                         str(test_value) + " and " + str(val))


def _open_file(file, sheet=0, group_name='group', sep=",", delimiter=None):
    fext = Path(file).suffix
    if fext in (".xls", ".xlsx") and sheet == 0:
        warnings.warn("No sheet name specified, the first sheet of the Excel file will be used.")

    # Load data
    if fext in (".xls", ".xlsx"):
        data = pd.read_excel(file, sheet_name=sheet)
    elif fext in (".csv", ".txt"):
        data = pd.read_csv(file, sep=sep, delimiter=delimiter)
    if group_name not in data.columns:
        raise ValueError("The specified 'group_name' parameter is not in the excel sheet.")

    return data


def _save_file(data, file, sheet=0, output_suffix="_updated", sep=","):
    fext = Path(file).suffix
    parent_dir = Path(file).parent
    fname = Path(file).stem
    new_fname = str(parent_dir) + '\\' + fname + output_suffix + fext
    if fext in (".xls", ".xlsx"):
        new_sheet = sheet if sheet != 0 else "Sheet1"
        data.to_excel(new_fname, sheet_name=new_sheet, index=False)
    elif fext in (".csv", ".txt"):
        data.to_csv(new_fname, sep=sep)
    print("Edited file saved as '" + new_fname + "'")


def _check_graphic_preset(preset):
    # Check configuration
    attribs = preset.keys()
    if 'group' not in attribs:
        raise ValueError("The parameter 'group' is missing in the config dictionary.")

    categories = preset['group']  # All the categories to update in file
    if len(unique(categories)) < len(categories):
        raise ValueError("A doublon found in definition of group parameters in configuration.")

    card = len(preset['group'])
    for key in attribs:
        if key not in ('group', 'label') and len(preset[key]) != card:
            msg = "The length of the parameter '" + key + \
                  "' is different from the number of group defined in the config."
            raise ValueError(msg)

    return attribs, categories


def _find_graphics_preset(data, category_sequence, categories, cmap='viridis', pop_marker=True, pop_zorder=False,
                          pop_label=False):
    # Colors data to add
    i_cmap = cm.get_cmap(cmap, len(categories))
    rgbcolors = i_cmap(range(len(categories)))
    colors = [to_hex(i) for i in rgbcolors]

    markers = _markers[0:len(categories)]  # Markers data to add

    # Create dictionaries for data attribution
    dict_colors = dict(zip(categories, colors[0:len(categories)]))
    if pop_marker:
        dict_markers = dict(zip(categories, markers))
    if pop_zorder:
        dict_zorders = dict(zip(categories, range(4, 4 + len(categories))))
    if pop_label:
        dict_labels = dict(zip(categories, categories))

    # Create the new contents of the columns to edit
    color_data, marker_data, zorder_data, label_data = [], [], [], []
    for cat in category_sequence:
        color_data.append(dict_colors[cat])
        if pop_marker:
            marker_data.append(dict_markers[cat])
        if pop_zorder:
            zorder_data.append(dict_zorders[cat])
        if pop_label:
            label_data.append(dict_labels[cat])

    # Populate columns data
    data['color'] = color_data
    if pop_marker:
        data['marker'] = marker_data
    if pop_zorder:
        data['zorder'] = zorder_data
    if pop_label:
        data['label'] = label_data

    return data


def _data_from_sequence(data, preset, category_sequence, ):
    attribs = preset.keys()
    categories = preset['group']

    # Data to add
    if not all([x in preset['group'] for x in unique(category_sequence)]):
        raise ValueError("Some groups existing in data file miss their configuration.")
    if 'color' in attribs:
        colors = preset['color']
    if 'marker' in attribs:
        markers = preset['marker']
    if 'zorder' in attribs:
        zorders = preset['zorder']
    if 'label' in attribs:
        labels = preset['label']

    # Create dictionaries for data attribution
    if 'color' in attribs:
        dict_colors = dict(zip(categories, colors[0:len(categories)]))
    if 'marker' in attribs:
        dict_markers = dict(zip(categories, markers))
    if 'zorder' in attribs:
        dict_zorders = dict(zip(categories, zorders))
    if 'labels' in attribs:
        if labels == 'auto' or labels is None:
            dict_labels = dict(zip(categories, categories))
        else:
            dict_labels = dict(zip(categories, labels))

    # Create the new contents of the columns to edit
    color_data, marker_data, zorder_data, label_data = [], [], [], []
    for unit in category_sequence:
        if 'color' in attribs:
            color_data.append(dict_colors[unit])
        if 'marker' in attribs:
            marker_data.append(dict_markers[unit])
        if 'zorder' in attribs:
            zorder_data.append(dict_zorders[unit])
        if 'labels' in attribs:
            label_data.append(dict_labels[unit])

    # Populate columns data
    if 'color' in attribs:
        data['color'] = color_data
    if 'marker' in attribs:
        data['marker'] = marker_data
    if 'zorder' in attribs:
        data['zorder'] = zorder_data
    if 'labels' in attribs:
        data['label'] = label_data

    return data


def file_create_graphic_preset(file, sheet=0, group_name='group', cmap='viridis', pop_marker=True, pop_zorder=False,
                               pop_label=False, output_suffix="_updated", sep=",", delimiter=None):
    # Open file
    data = _open_file(file, sheet=sheet, group_name=group_name, sep=sep, delimiter=delimiter)

    category_sequence = data[group_name].tolist()  # Column of categories
    categories = unique(category_sequence)  # All the categories to update in file

    data = _find_graphics_preset(data, category_sequence, categories, cmap, pop_marker, pop_zorder, pop_label)

    # Save new file
    _save_file(data, file, sheet=sheet, output_suffix=output_suffix)


def data_create_graphic_preset(data, group_name='group', cmap='viridis', pop_marker=True, pop_zorder=False,
                               pop_label=False):
    category_sequence = data[group_name].tolist()  # Column of categories
    categories = unique(category_sequence)  # All the categories to update in file

    data = _find_graphics_preset(data, category_sequence, categories, cmap, pop_marker, pop_zorder, pop_label)

    return data


def file_set_graphic_preset(file, preset, sheet=0, group_name='group', output_suffix="cfg_update", sep=",",
                            delimiter=None, ):
    # Check preset
    _check_graphic_preset(preset)

    # Open file
    data = _open_file(file, sheet=sheet, group_name=group_name, sep=sep, delimiter=delimiter)

    category_sequence = data[group_name].tolist()  # Column of categories
    data = _data_from_sequence(data, preset, category_sequence, )

    # Save new file
    _save_file(data, file, sheet=sheet, output_suffix=output_suffix, sep=sep)


def data_set_graphic_preset(data, preset, group_name='group', ):
    # Check preset
    _check_graphic_preset(preset)

    # Load data
    if group_name not in data.columns:
        raise ValueError("The specified 'group_name' parameter is not in the excel sheet.")

    category_sequence = data[group_name].tolist()  # Column of categories
    data = _data_from_sequence(data, preset, category_sequence, )

    # Return data
    return data


def check_geochem_res(reservoir, listing=None):  # Listing for eventually required elements
    chklist = ['alias', 'color']
    if listing is not None:
        chklist = chklist.append(*listing)

    keys = reservoir.keys()
    for el in chklist:
        if el not in keys:
            raise ValueError("Key ", el, "not found in reservoir configuration.")

    return True

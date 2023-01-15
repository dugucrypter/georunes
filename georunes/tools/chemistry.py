name_ox_to_el = {
    'SiO2': 'Si',
    'TiO2': 'Ti',
    'Al2O3': 'Al',
    'Fe2O3': 'Fe',
    'FeOt': 'Fe',
    'MnO': 'Mn',
    'MgO': 'Mg',
    'CaO': 'Ca',
    'Li2O': 'Li',
    'Na2O': 'Na',
    'K2O': 'K',
    'Rb2O': 'Rb',
    'Cs2O': 'Cs',
    'BaO': 'Ba',
    'Cr2O3': 'Cr',
    'P2O5': 'P',
    'SnO': 'Sn',
    'Ta2O5': 'Ta',
    'Nb2O5': 'Nb'
}

name_el_to_def_ox = {
    'Si': 'SiO2',
    'Ti': 'TiO2',
    'Al': 'Al2O3',
    'Fe': 'FeOt',
    'Mn': 'MnO',
    'Mg': 'MgO',
    'Ca': 'CaO',
    'Li': 'Li2O',
    'Na': 'Na2O',
    'K': 'K2O',
    'Rb': 'Rb2O',
    'Cs': 'Cs2O',
    'Ba': 'BaO',
    'Cr': 'Cr2O3',
    'P': 'P2O5',
    'Sn': 'SnO',
    'Ta': 'Ta2O5',
    'Nb': 'Nb2O5'
}

ratio_el_to_ox = {
    'SiO2': 0.467,
    'TiO2': 0.600,
    'Al2O3': 0.529,
    'Fe2O3': 0.699,
    'FeO': 0.777,
    'MnO': 0.774,
    'MgO': 0.603,
    'CaO': 0.715,
    'Li2O': 0.464570,
    'Na2O': 0.742,
    'K2O': 0.830,
    'Rb2O': 0.914412,
    'Cs2O': 0.943226,
    'BaO': 0.895651,
    'Cr2O3': 0.684202,
    'P2O5': 0.436,
    'SnO': 0.881,
    'Ta2O5': 0.819,
    'NiO': 0.785797,
    'CoO': 0.786483,
    'SrO': 0.845595,
    'ZrO2': 0.740318,
    'V2O3': 0.684324,
    'SO3': 0.400504,
}

nb_cation = {
    'SiO2': 1,
    'TiO2': 1,
    'Al2O3': 2,
    'Fe2O3': 2,
    'Fe2O3t': 2,
    'FeO': 1,
    'FeOt': 1,
    'MnO': 1,
    'MgO': 1,
    'CaO': 1,
    'Li2O': 2,
    'Na2O': 2,
    'K2O': 2,
    'Rb2O': 2,
    'Cs2O': 2,
    'BaO': 1,
    'Cr2O3': 2,
    'P2O5': 2,
    'SnO': 1,
    'Ta2O5': 2
}

molar_mass = {
    'SiO2': 60.0843,  # a
    'TiO2': 79.8658,  # a
    'Al2O3': 101.961276,  # a
    'Fe2O3': 159.6882,  # a
    'Fe2O3t': 159.6882,  # a
    'FeO': 71.8444,  # a
    'FeOt': 71.8444,  # a
    'MnO': 70.937449,  # a
    'MgO': 40.3044,  # a
    'CaO': 56.0774,  # a
    'Li2O': 29.8814,  # a
    'Na2O': 61.97894,  # a
    'K2O': 94.1960,  # a
    'SrO': 103.6194,  # a
    'BaO': 153.3264,  # a
    'Rb2O': 186.935,  # a
    'Cs2O': 281.8103,  # a
    'ZrO2': 123.228,  # a
    'P2O5': 141.944522,  # a
    'NiO': 74.6928,  # a
    'CoO': 74.9326,  # a
    'Cr2O3': 151.9904,  # a
    'V2O3': 149.8812,  # a
    'CO2': 44.0095,  # a
    'SO3': 80.0642,  # a
    'SnO': 134.689,
    'Ta2O5': 441.891
}

el_molar_mass = {
    'F': 18.9984,  # a
    'O': 15.9994,  # a
    'Cl': 35.4527,  # a
    'S': 32.066,  # a
    'Nb': 92.90638,
    'Ta': 180.9479,
    'Nb_Ta': 92.90638 / 180.9479,
    'K': 39.0983,
    'Rb': 85.4678,
    'K_Rb': 39.0983 / 85.4678
}

all_elts = ("H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
            "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni",
            "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
            "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
            "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf",
            "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
            "Fr", "Ra", "Ac", "Th", "Pa", "U")


def val_ox_to_el(group):
    return group * ratio_el_to_ox[group.name]


def val_ox_to_el_ppm(ox_val, ox_formula):
    return (ox_val * ratio_el_to_ox[ox_formula]) * 10000


def val_ox_to_mc(group):
    return (1000 * group / molar_mass[group.name]) * nb_cation[group.name]


def val_el_to_mol(group):
    return group / el_molar_mass[group.name]


def molar_ratio(group):
    return group / molar_mass[group.name]


def molar_ratio_specified(group, group_name):
    return group / molar_mass[group_name]

# a. Verma, S.P., Torres-Alvarado, I.S. and Velasco-Tapia, F., 2003.
# A revised CIPW norm. Swiss Bulletin of Mineralogy and Petrology, 83(2), pp.197-216.

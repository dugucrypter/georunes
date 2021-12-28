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
    'Li2O': 0.465,
    'Na2O': 0.742,
    'K2O': 0.830,
    'Rb2O': 0.914,
    'Cs2O': 0.943,
    'BaO': 0.896,
    'Cr2O3': 0.684,
    'P2O5': 0.436,
    'SnO': 0.881,
    'Ta2O5': 0.819
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
    'SiO2': 60.0843,
    'TiO2': 79.8988,
    'Al2O3': 101.9613,
    'Fe2O3': 159.692,
    'Fe2O3t': 159.692,
    'FeO': 71.8464,
    'FeOt': 71.8464,
    'MnO': 70.9374,
    'MgO': 40.3114,
    'CaO': 56.0794,
    'Li2O': 29.882,
    'Na2O': 61.9788,
    'K2O': 94.2034,
    'Rb2O': 186.9356,
    'Cs2O': 281.8109,
    'BaO': 153.3391,
    'Cr2O3': 151.989,
    'P2O5': 141.943,
    'SnO': 134.689,
    'Ta2O5': 441.891
}

el_molar_mass = {
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

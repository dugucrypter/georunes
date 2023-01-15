import warnings
import numpy as np
from pandas import Series
from georunes.tools.chemistry import ratio_el_to_ox, molar_mass, el_molar_mass
from georunes.modmin.optim.base import BaseOptimizer

list_major_ox = ['SiO2', 'Na2O', 'K2O', 'CaO', 'MnO', 'FeO', 'Fe2O3', 'MgO', 'TiO2', 'Al2O3', 'P2O5']
list_minor_el = ['F', 'Cl', 'S', 'Ni', 'Co', 'Ba', 'Sr', 'Rb', 'Cs', 'Li', 'Zr', 'Cr', 'V']
list_ox_from_minor_el = ['SO3', 'NiO', 'CoO', 'BaO', 'SrO', 'Rb2O', 'Cs2O', 'Li2O', 'ZrO2', 'Cr2O3', 'V2O3']
list_all_ox_el = [*list_major_ox, 'CO2', 'F', 'Cl', 'S', *list_ox_from_minor_el]
final_list_min = ['Q', 'Or', 'Ab', 'An', 'C', 'Wo', 'Cs', 'Tn', 'Pf', 'Cc', 'Mt', 'Hm', 'Il', 'Ru',
                  'Ne', 'Th', 'Nc', 'Ac', 'Ns', 'Lc', 'Kp', 'Ks', 'Z', 'Hl', 'Fr', 'Pr', 'Cm']

oxide_corresp = {
    'Ni': 'NiO',
    'Co': 'CoO',
    'Ba': 'BaO',
    'Sr': 'SrO',
    'Rb': 'Rb2O',
    'Cs': 'Cs2O',
    'Li': 'Li2O',
    'Zr': 'ZrO2',
    'Cr': 'Cr2O3',
    'V': 'V2O3'
}

_mol_w = dict()
for _oxel in list_all_ox_el:
    if _oxel in molar_mass:
        _mol_w[_oxel] = molar_mass[_oxel]
    elif _oxel in el_molar_mass:
        _mol_w[_oxel] = el_molar_mass[_oxel]
for _oxel in ['O', 'Cl', 'S']:
    _mol_w[_oxel] = el_molar_mass[_oxel]

# Algorithm updated from Verma et al., 2003
# Verma, S.P., Torres-Alvarado, I.S. and Velasco-Tapia, F., 2003. A revised CIPW norm. Swiss Bulletin of Mineralogy
# and Petrology, 83(2), pp.197-216.

class CIPWNorm(BaseOptimizer):
    def __init__(self, **kwargs):
        BaseOptimizer.__init__(self, **kwargs)
        self.notif = ">>>>>> CIPW norm"

    def compute(self, raw_data, skip_cols, normalize_entry=False, minor_included=False, to_round=4,
                co2_cancrinite=False, co2_calcite=False):

        # 1 / Preparing data
        if self.verbose > 1: print("Step 1 - Prepare data")

        co2_cancrinite = float(co2_cancrinite)
        co2_calcite = float(co2_calcite)
        data = raw_data.iloc[:, :skip_cols].copy()
        raw_data_keys = raw_data.iloc[:, skip_cols:].keys()

        for oxel in raw_data_keys:
            if oxel in [*list_all_ox_el, *list_minor_el]:
                data[oxel] = raw_data[oxel]

        if 'Total' in raw_data_keys or 'Sum' in raw_data_keys:
            data['Total'] = raw_data['Total']
        else:
            warnings.warn("Total column not found.")

        data_keys = data.keys()
        filtered_columns = [oxel for oxel in raw_data_keys if oxel not in data_keys]
        if self.verbose: print('Ignored columns :', filtered_columns)

        for ox in list_major_ox:
            if ox not in data_keys:
                data[ox] = 0

        n_phase = data.iloc[:, :skip_cols].copy()
        next_step = Series(np.array([""] * len(data.index)))
        si_deff = data.iloc[:, :skip_cols].copy()
        prop = data.iloc[:, :skip_cols].copy()
        free = data.iloc[:, :skip_cols].copy()
        partitions = data.iloc[:, :skip_cols].copy()
        suppl = data.iloc[:, :skip_cols].copy()

        # Initializing columns for SiO2 deficiency calculation
        si_deff['Y'] = 0
        si_deff['D'] = 0

        # 2 / CO2 handling options
        if self.verbose > 1: print("Step 2 - CO2 handling options")

        if minor_included:
            if co2_cancrinite + co2_calcite != 1 and not (co2_cancrinite == co2_calcite == 0):
                raise Exception('Check the proportions of co2_cancrinite and co2_calcite.')
            if self.verbose > 1:
                print('CO2 proportion in calcite : ', co2_calcite, ' --- CO2 proportion in cancrinite:', co2_cancrinite)

        # 3 / Conversion of trace elements units
        if self.verbose > 1: print("Step 3 - Conversion of trace elements units")

        if minor_included:
            data_keys = data.keys()
            for oxel in data_keys:
                if oxel in list_minor_el and oxel not in ['F', 'Cl', 'S']:
                    oxide = oxide_corresp[oxel]
                    data[oxide] = data[oxel] / (ratio_el_to_ox[oxide] * 10000)
                    data = data.drop(columns=oxel)
                elif oxel in ['F', 'Cl', 'S']:
                    data[oxel] = data[oxel] / 10000

            # If some minor elements does not exist in data, add the corresponding oxide with zero values for
            # treatment. Also add other required elements that are missing.

            data_keys = data.keys()
            for ox in list_ox_from_minor_el:
                if ox not in data_keys:
                    data[ox] = 0
            if 'F' not in data_keys:
                data['F'] = 0

        # 4-5 / Adjust components to 100%
        if self.verbose > 1: print("Step 4, 5 - Adjust components to 100%")

        data_keys = data.keys()
        total_calculated = data.iloc[:, skip_cols:].sum(axis=1) - data['Total']
        if self.verbose > 1:
            print(">>> Total calculated")
            print(total_calculated.to_string())

        if normalize_entry:
            oxel_to_sum = list_major_ox if minor_included else list_major_ox
            for oxel in oxel_to_sum:
                if oxel in data_keys:
                    data[oxel] = 100 * data[oxel] / total_calculated
            total_normalized = data.iloc[:, skip_cols:].sum(axis=1) - data['Total']

            if self.verbose > 1:
                print(">>> Total normalized")
                print(total_normalized.to_string())
        else:
            total_normalized = total_calculated

        # Calculation of some petrogenetical parameters
        suppl['pp_FeOt/MgO'] = ((2 * _mol_w['FeO'] / _mol_w['Fe2O3']) * data['Fe2O3'] + data['FeO']) / data['MgO']
        suppl['pp_ratio_K2O_Na2O'] = data['K2O'] / data['Na2O']
        suppl['pp_SI'] = 100 * data['MgO'] / (data['MgO'] + data['FeO'] + data['Fe2O3'] + data['Na2O'] + data['K2O'])
        suppl['pp_Mg#'] = 100 * (data['MgO'] / _mol_w['MgO']) / (
                data['MgO'] / _mol_w['MgO'] + data['FeO'] / _mol_w['FeO'])

        for i in data.index:
            if data.loc[i, 'SiO2'] > 5 and 1 < suppl.loc[i, 'pp_ratio_K2O_Na2O'] < 2.5:
                suppl.loc[i, 'pp_AR'] = (data.loc[i, 'Al2O3'] + data.loc[i, 'CaO'] + 2 * data.loc[i, 'Na2O']) / (
                        data.loc[i, 'Al2O3'] + data.loc[i, 'CaO'] - 2 * data.loc[i, 'Na2O'])
            else:
                suppl.loc[i, 'pp_AR'] = (data.loc[i, 'Al2O3'] + data.loc[i, 'CaO'] + data.loc[i, 'Na2O'] + data.loc[
                    i, 'K2O']) / (data.loc[i, 'Al2O3'] + data.loc[i, 'CaO'] - data.loc[i, 'Na2O'] - data.loc[i, 'K2O'])

        # 6 / Mole computations
        if self.verbose > 1: print("Step 6 - Mole computations")

        data_n = data.copy().drop(['Total'], axis=1).fillna(0)

        if self.verbose > 1:
            print(">>> Initial compositions (wt %)")
            print(data_n.to_string())

        for oxel in data_n.keys():
            if oxel in list_all_ox_el:
                data_n[oxel] = data_n[oxel] / _mol_w[oxel]

        if self.verbose:
            print(">>> Initial molar concentrations (mol)")
            print(data_n.to_string())

        # 7-8 / Minor oxides combination and oxide molecular weight computations
        if self.verbose > 1: print(
            "Step 7, 8 - Minor oxides combination and oxide molecular weight computations")

        if minor_included:
            FeO_corr = data_n['FeO'] + data_n['MnO'] + data_n['NiO'] + data_n['CoO']
            CaO_corr = data_n['CaO'] + data_n['BaO'] + data_n['SrO']
            K2O_corr = data_n['K2O'] + data_n['Rb2O'] + data_n['Cs2O']
            Na2O_corr = data_n['Na2O'] + data_n['Li2O']
            Cr2O3_corr = data_n['Cr2O3'] + data_n['V2O3']
            xFeO = data_n['FeO'] / FeO_corr
            xMnO = data_n['MnO'] / FeO_corr
            xNiO = data_n['NiO'] / FeO_corr
            xCoO = data_n['CoO'] / FeO_corr
            xCaO = data_n['CaO'] / CaO_corr
            xBaO = data_n['BaO'] / CaO_corr
            xSrO = data_n['SrO'] / CaO_corr
            xK2O = data_n['K2O'] / K2O_corr
            xRb2O = data_n['Rb2O'] / K2O_corr
            xCs2O = data_n['Cs2O'] / K2O_corr
            xNa2O = data_n['Na2O'] / Na2O_corr
            xLi2O = data_n['Li2O'] / Na2O_corr
            xCr2O3 = data_n['Cr2O3'] / Cr2O3_corr
            xV2O3 = data_n['V2O3'] / Cr2O3_corr

            data_n['FeO'] = data_n['FeO'] + data_n['MnO'] + data_n['NiO'] + data_n['CoO']
            data_n['CaO'] = data_n['CaO'] + data_n['BaO'] + data_n['SrO']
            data_n['K2O'] = data_n['K2O'] + data_n['Rb2O'] + data_n['Cs2O']
            data_n['Na2O'] = data_n['Na2O'] + data_n['Li2O']
            data_n['Cr2O3'] = data_n['Cr2O3'] + data_n['V2O3']

            # Other oxides to zero
            for ox in ['MnO', 'NiO', 'CoO', 'BaO', 'SrO', 'Rb2O', 'Cs2O', 'Li2O', 'V2O3']:
                data_n[ox] = 0

        else:
            FeO_corr = data_n['MnO'] + data_n['FeO']
            xFeO = data_n['FeO'] / FeO_corr
            xMnO = data_n['MnO'] / FeO_corr
            data_n['FeO'] = data_n['FeO'] + data_n['MnO']
            data_n['MnO'] = 0

        if self.verbose:
            print(">>> Corrected molar concentrations (mol)")
            print(data_n.to_string())

        # Molecular weight correction
        corr_mol_w = _mol_w.copy()  # Each value will be a number of a list of number (for FeO for example)
        if minor_included:
            corr_mol_w['FeO'] = xFeO * _mol_w['FeO'] + xMnO * _mol_w['MnO'] + \
                                xNiO * _mol_w['NiO'] + xCoO * _mol_w['CoO']
            corr_mol_w['CaO'] = xCaO * _mol_w['CaO'] + xBaO * _mol_w['BaO'] + xSrO * _mol_w['SrO']
            corr_mol_w['K2O'] = xK2O * _mol_w['K2O'] + xRb2O * _mol_w['Cs2O'] + xCs2O * _mol_w['Cs2O']
            corr_mol_w['Na2O'] = xNa2O * _mol_w['Na2O'] + xLi2O * _mol_w['Li2O']
            corr_mol_w['Cr2O3'] = xCr2O3 * _mol_w['Cr2O3'] + xV2O3 * _mol_w['V2O3']

            corr_mol_w['FeO'] = corr_mol_w['FeO'].fillna(0)
            corr_mol_w['CaO'] = corr_mol_w['CaO'].fillna(0)
            corr_mol_w['K2O'] = corr_mol_w['K2O'].fillna(0)
            corr_mol_w['Na2O'] = corr_mol_w['Na2O'].fillna(0)
            corr_mol_w['Cr2O3'] = corr_mol_w['Cr2O3'].fillna(0)

        else:
            corr_mol_w['FeO'] = xFeO * _mol_w['FeO'] + xMnO * _mol_w['MnO']
            corr_mol_w['FeO'] = corr_mol_w['FeO'].fillna(0)

        # 9-10 / Correction of normative mineral molecular weights
        if self.verbose > 1: print("Step 9, 10 - Correction of normative mineral molecular weights")

        mol_w_min = {
            'Ab': corr_mol_w['Na2O'] + corr_mol_w['Al2O3'] + 6 * corr_mol_w['SiO2'],
            'Ne': corr_mol_w['Na2O'] + corr_mol_w['Al2O3'] + 2 * corr_mol_w['SiO2'],
            'Th': corr_mol_w['Na2O'] + corr_mol_w['SO3'],
            'Nc': corr_mol_w['Na2O'] + corr_mol_w['CO2'],
            'An': corr_mol_w['CaO'] + corr_mol_w['Al2O3'] + 2 * corr_mol_w['SiO2'],
            'Di-mg': corr_mol_w['CaO'] + corr_mol_w['MgO'] + 2 * corr_mol_w['SiO2'],
            'Di-fe': corr_mol_w['CaO'] + corr_mol_w['FeO'] + 2 * corr_mol_w['SiO2'],
            'Ac': corr_mol_w['Na2O'] + corr_mol_w['Fe2O3'] + 4 * corr_mol_w['SiO2'],
            'Ns': corr_mol_w['Na2O'] + corr_mol_w['SiO2'],
            'Or': corr_mol_w['K2O'] + corr_mol_w['Al2O3'] + 6 * corr_mol_w['SiO2'],
            'Lc': corr_mol_w['K2O'] + corr_mol_w['Al2O3'] + 4 * corr_mol_w['SiO2'],
            'Kp': corr_mol_w['K2O'] + corr_mol_w['Al2O3'] + 2 * corr_mol_w['SiO2'],
            'Ks': corr_mol_w['K2O'] + corr_mol_w['SiO2'],
            'Wo': corr_mol_w['CaO'] + corr_mol_w['SiO2'],
            'Cs': 2 * corr_mol_w['CaO'] + corr_mol_w['SiO2'],
            'Mt': corr_mol_w['FeO'] + corr_mol_w['Fe2O3'],
            'Il': corr_mol_w['FeO'] + corr_mol_w['TiO2'],
            'Tn': corr_mol_w['CaO'] + corr_mol_w['TiO2'] + corr_mol_w['SiO2'],
            'Pf': corr_mol_w['CaO'] + corr_mol_w['TiO2'],
            'Cc': corr_mol_w['CaO'] + corr_mol_w['CO2'],
            'Hy-fe': corr_mol_w['FeO'] + corr_mol_w['SiO2'],
            'Ol-fe': 2 * corr_mol_w['FeO'] + corr_mol_w['SiO2'],
            'Q': corr_mol_w['SiO2'],
            'C': corr_mol_w['Al2O3'],
            'Z': corr_mol_w['SiO2'] + corr_mol_w['ZrO2'],
            'Hy-mg': corr_mol_w['MgO'] + corr_mol_w['SiO2'],
            'Ol-mg': 2 * corr_mol_w['MgO'] + corr_mol_w['SiO2'],
            'Hm': corr_mol_w['Fe2O3'],
            'Ru': corr_mol_w['TiO2'],
            'Ap-F': 3 * corr_mol_w['CaO'] + corr_mol_w['P2O5'] + 1 / 3 * (
                    (corr_mol_w['CaO'] - _mol_w['O']) + 2 * corr_mol_w['F']),
            'Ap-O': 3 * corr_mol_w['CaO'] + corr_mol_w['P2O5'] + corr_mol_w['CaO'] * 1 / 3,
            'Cm': corr_mol_w['FeO'] + corr_mol_w['Cr2O3'],
            'Hl': (corr_mol_w['Na2O'] - _mol_w['O']) / 2 + _mol_w['Cl'],
            'Fr': (corr_mol_w['CaO'] - _mol_w['O']) + 2 * _mol_w['F'],
            'Pr': (corr_mol_w['FeO'] - _mol_w['O']) + 2 * _mol_w['S']
        }

        # 11 / Normative zircon
        if self.verbose > 1: print("Step 11 - Normative zircon")

        if minor_included:
            for i in data_n.index:
                if data_n.loc[i, 'SiO2'] > data_n.loc[i, 'ZrO2']:
                    n_phase.loc[i, 'Z'] = data_n.loc[i, 'ZrO2']
                    si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + n_phase.loc[i, 'Z']
                    data_n.loc[i, 'ZrO2'] = 0
                else:
                    print('WARNING : No further SiO2 after zircon attribution for composition ' + str(
                        i) + '. Check data.')

        # 12 / Normative apatite
        if self.verbose > 1: print("Step 12 - Normative apatite")

        temp_ap = np.zeros(shape=[len(data_n.index), 1])
        for i in data_n.index:
            if data_n.loc[i, 'CaO'] >= (3 + 1 / 3) * data_n.loc[i, 'P2O5']:
                temp_ap[i] = data_n.loc[i, 'P2O5']
                data_n.loc[i, 'CaO'] = data_n.loc[i, 'CaO'] - (3 + 1 / 3) * data_n.loc[i, 'P2O5']
            else:
                temp_ap[i] = data_n.loc[i, 'CaO'] / (3 + 1 / 3)
                data_n.loc[i, 'CaO'] = 0
                free.loc[i, 'P2O5'] = data_n.loc[i, 'P2O5'] - temp_ap[i]
            free.loc[i, 'P2O5'] = data_n.loc[i, 'P2O5'] - temp_ap[i]
            data_n.loc[i, 'P2O5'] = 0

        n_phase['Ap-F'] = 0
        n_phase['Ap-O'] = 0
        if minor_included:
            for i in data_n.index:
                if data_n.loc[i, 'F'] >= 2 / 3 * temp_ap[i]:
                    n_phase.loc[i, 'Ap-F'] = temp_ap[i]
                    free.loc[i, 'O_12b'] = 1 / 3 * n_phase.loc[i, 'Ap-F']
                    data_n.loc[i, 'F'] = data_n.loc[i, 'F'] - 2 / 3 * n_phase.loc[i, 'Ap-F']
                else:
                    n_phase.loc[i, 'Ap-F'] = 1.5 * data_n.loc[i, 'F']
                    n_phase.loc[i, 'Ap-O'] = temp_ap[i] - 1.5 * data_n.loc[i, 'F']
                    free.loc[i, 'O_12c'] = data_n.loc[i, 'F'] / 2
                    data_n.loc[i, 'F'] = 0
            n_phase['Ap'] = n_phase['Ap-F'] + n_phase['Ap-O']
        else:
            n_phase['Ap-O'] = temp_ap
        n_phase['Ap'] = n_phase['Ap-O'] + n_phase['Ap-F']

        # 13 / Normative fluorite
        if self.verbose > 1: print("Step 13 - Normative fluorite")

        if minor_included:
            for i in data_n.index:
                if data_n.loc[i, 'CaO'] >= data_n.loc[i, 'F'] / 2:
                    n_phase.loc[i, 'Fr'] = data_n.loc[i, 'F'] / 2
                    data_n.loc[i, 'CaO'] = data_n.loc[i, 'CaO'] - data_n.loc[i, 'F'] / 2
                    data_n.loc[i, 'F'] = 0
                else:
                    n_phase.loc[i, 'Fr'] = data_n.loc[i, 'CaO']
                    data_n.loc[i, 'CaO'] = 0
                    free.loc[i, 'F'] = data_n.loc[i, 'F'] - 2 * n_phase.loc[i, 'Fr']  # Unused F
                    data_n.loc[i, 'F'] = 0
                free.loc[i, 'O_13'] = n_phase.loc[i, 'Fr']

        # 14 / Normative halite
        if self.verbose > 1: print("Step 14 - Normative halite")

        if minor_included and 'Cl' in data_n.keys():
            for i in data_n.index:
                if data_n.loc[i, 'Na2O'] >= 2 * data_n.loc[i, 'Cl']:
                    n_phase.loc[i, 'Hl'] = data_n.loc[i, 'Cl']
                    data_n.loc[i, 'Na2O'] = data_n.loc[i, 'Na2O'] - n_phase.loc[i, 'Hl'] / 2
                    free.loc[i, 'O_14'] = n_phase.loc[i, 'Hl'] / 2
                    data_n.loc[i, 'Cl'] = 0
                else:
                    n_phase.loc[i, 'Hl'] = data_n.loc[i, 'Na2O'] / 2
                    free.loc[i, 'Cl'] = data_n.loc[i, 'Cl'] - n_phase.loc[i, 'Hl']
                    data_n.loc[i, 'Na2O'] = 0

        # 15 / Normative thenardite
        if self.verbose > 1: print("Step 15 - Normative thenardite")

        if minor_included and 'SO3' in data_n.keys():
            for i in data_n.index:
                if data_n.loc[i, 'Na2O'] >= 2 * data_n.loc[i, 'SO3']:
                    n_phase.loc[i, 'Th'] = data_n.loc[i, 'SO3']
                    data_n.loc[i, 'Na2O'] = data_n.loc[i, 'Na2O'] - n_phase.loc[i, 'Th']
                    data_n.loc[i, 'SO3'] = 0
                else:
                    n_phase.loc[i, 'Th'] = data_n.loc[i, 'Na2O']
                    free.loc[i, 'SO3'] = data_n.loc[i, 'SO3'] - n_phase.loc[i, 'Th']
                    data_n.loc[i, 'Na2O'] = 0

        # 16 / Normative pyrite
        if self.verbose > 1: print("Step 16 - Normative pyrite")

        if minor_included and 'S' in data_n.keys():
            for i in data_n.index:
                if data_n.loc[i, 'FeO'] >= 2 * data_n.loc[i, 'S']:
                    n_phase.loc[i, 'Pr'] = data_n.loc[i, 'S'] / 2
                    data_n.loc[i, 'FeO'] = data_n.loc[i, 'FeO'] - n_phase.loc[i, 'Pr']
                    data_n.loc[i, 'S'] = 0
                else:
                    n_phase.loc[i, 'Pr'] = data_n.loc[i, 'FeO']
                    free.loc[i, 'S'] = data_n.loc[i, 'S'] - 2 * n_phase.loc[i, 'Pr']
                    data_n.loc[i, 'FeO'] = 0
                free.loc[i, 'O_16'] = n_phase.loc[i, 'Pr']

        # 17 / Normative sodium carbonate or calcite
        if self.verbose > 1: print("Step 17 - Normative sodium carbonate or calcite")

        if minor_included:
            if 'CO2' in data_keys:
                free['CO2'] = 0
                if co2_cancrinite == co2_calcite == 0:
                    for i in data_n.index:
                        free.loc[i, 'CO2'] = data_n.loc[i, 'CO2']
                        data_n.loc[i, 'CO2'] = 0
                else:
                    # Cancrinite
                    for i in data_n.index:
                        if data_n.loc[i, 'CO2'] > 0:
                            if data_n.loc[i, 'Na2O'] >= data_n.loc[i, 'CO2'] * co2_cancrinite:
                                n_phase.loc[i, 'Nc'] = data_n.loc[i, 'CO2'] * co2_cancrinite
                                data_n.loc[i, 'Na2O'] = data_n.loc[i, 'Na2O'] - n_phase.loc[i, 'Nc']
                            else:
                                n_phase.loc[i, 'Nc'] = data_n.loc[i, 'Na2O']
                                data_n.loc[i, 'Na2O'] = 0
                                free.loc[i, 'CO2'] = free.loc[i, 'CO2'] + data_n.loc[i, 'CO2'] * co2_cancrinite \
                                                     - n_phase.loc[i, 'Nc']  # Free CO2
                            data_n.loc[i, 'CO2'] = data_n.loc[i, 'CO2'] * (1 - co2_cancrinite)

                    # Calcite, with all the rest of CO2
                    for i in data_n.index:
                        if data_n.loc[i, 'CO2'] > 0:
                            if data_n.loc[i, 'CaO'] > data_n.loc[i, 'CO2']:
                                n_phase.loc[i, 'Cc'] = data_n.loc[i, 'CO2']
                                data_n.loc[i, 'CaO'] = data_n.loc[i, 'CaO'] - n_phase.loc[i, 'Cc']
                            else:
                                n_phase.loc[i, 'Cc'] = data_n.loc[i, 'CaO']
                                data_n.loc[i, 'CaO'] = 0
                                free.loc[i, 'CO2'] = free.loc[i, 'CO2'] + data_n.loc[i, 'CO2'] - n_phase.loc[
                                    i, 'Cc']  # CO2 to free
                            data_n.loc[i, 'CO2'] = 0

        # 18 / Normative chromite
        if self.verbose > 1: print("Step 18 - Normative chromite")

        if minor_included:
            for i in data_n.index:
                if 0 < data_n.loc[i, 'Cr2O3'] <= data_n.loc[i, 'FeO']:
                    n_phase.loc[i, 'Cm'] = data_n.loc[i, 'Cr2O3']
                    data_n.loc[i, 'FeO'] = data_n.loc[i, 'FeO'] - n_phase.loc[i, 'Cm']
                    data_n.loc[i, 'Cr2O3'] = 0
                elif data_n.loc[i, 'FeO'] < data_n.loc[i, 'Cr2O3']:
                    n_phase.loc[i, 'Cm'] = data_n.loc[i, 'FeO']
                    free.loc[i, 'Cr2O3'] = data_n.loc[i, 'Cr2O3'] - n_phase.loc[i, 'Cm']
                    data_n.loc[i, 'FeO'] = 0
                    data_n.loc[i, 'Cr2O3'] = 0

        # 19 / Normative ilmenite
        if self.verbose > 1: print("Step 19 - Normative ilmenite")

        for i in data_n.index:
            if data_n.loc[i, 'FeO'] >= data_n.loc[i, 'TiO2']:
                n_phase.loc[i, 'Il'] = data_n.loc[i, 'TiO2']
                data_n.loc[i, 'FeO'] = data_n.loc[i, 'FeO'] - n_phase.loc[i, 'Il']
                data_n.loc[i, 'TiO2'] = 0
            else:
                n_phase.loc[i, 'Il'] = data_n.loc[i, 'FeO']
                data_n.loc[i, 'TiO2'] = data_n.loc[i, 'TiO2'] - n_phase.loc[i, 'Il']
                data_n.loc[i, 'FeO'] = 0

        # 20 / Normative orthoclase or potassium metasilicate
        if self.verbose > 1: print("Step 20 - Normative orthoclase or potassium metasilicate")

        for i in data_n.index:
            if data_n.loc[i, 'Al2O3'] >= data_n.loc[i, 'K2O']:
                n_phase.loc[i, 'Orp'] = data_n.loc[i, 'K2O']
                data_n.loc[i, 'Al2O3'] = data_n.loc[i, 'Al2O3'] - n_phase.loc[i, 'Orp']
                data_n.loc[i, 'K2O'] = 0
                si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 6 * n_phase.loc[i, 'Orp']
            else:
                n_phase.loc[i, 'Orp'] = data_n.loc[i, 'Al2O3']
                n_phase.loc[i, 'Ks'] = data_n.loc[i, 'K2O'] - n_phase.loc[i, 'Orp']  # Rest of K2O to Ks
                data_n.loc[i, 'Al2O3'] = 0
                data_n.loc[i, 'K2O'] = 0
                si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 6 * n_phase.loc[i, 'Orp'] + n_phase.loc[i, 'Ks']

        # 21 / Normative albite
        if self.verbose > 1: print("Step 21 - Normative albite")

        for i in data_n.index:
            if data_n.loc[i, 'Al2O3'] >= data_n.loc[i, 'Na2O']:
                n_phase.loc[i, 'Abp'] = data_n.loc[i, 'Na2O']
                data_n.loc[i, 'Al2O3'] = data_n.loc[i, 'Al2O3'] - n_phase.loc[i, 'Abp']
                data_n.loc[i, 'Na2O'] = 0
            else:
                n_phase.loc[i, 'Abp'] = data_n.loc[i, 'Al2O3']
                data_n.loc[i, 'Na2O'] = data_n.loc[i, 'Na2O'] - n_phase.loc[i, 'Abp']  # Rest of Na2O to Ab
                data_n.loc[i, 'Al2O3'] = 0
            si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 6 * n_phase.loc[i, 'Abp']

        # 22 / Normative acmite or sodium metasilicate
        if self.verbose > 1: print("Step 22 - Normative acmite or sodium metasilicate")

        for i in data_n.index:
            if data_n.loc[i, 'Na2O'] >= data_n.loc[i, 'Fe2O3']:
                n_phase.loc[i, 'Ac'] = data_n.loc[i, 'Fe2O3']
                n_phase.loc[i, 'Ns'] = data_n.loc[i, 'Na2O'] - n_phase.loc[i, 'Ac']  # Rest of Na2O to Ns
                data_n.loc[i, 'Na2O'] = 0
                data_n.loc[i, 'Fe2O3'] = 0
                si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 4 * n_phase.loc[i, 'Ac'] + n_phase.loc[i, 'Ns']
            else:
                n_phase.loc[i, 'Ac'] = data_n.loc[i, 'Na2O']
                data_n.loc[i, 'Fe2O3'] = data_n.loc[i, 'Fe2O3'] - n_phase.loc[i, 'Ac']
                data_n.loc[i, 'Na2O'] = 0
                si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 4 * n_phase.loc[i, 'Ac']

        # 23 / Normative anorthite or corundum
        if self.verbose > 1: print("Step 23 - Normative anorthite or corundum")

        for i in data_n.index:
            if data_n.loc[i, 'Al2O3'] >= data_n.loc[i, 'CaO']:
                n_phase.loc[i, 'An'] = data_n.loc[i, 'CaO']
                n_phase.loc[i, 'C'] = data_n.loc[i, 'Al2O3'] - data_n.loc[i, 'CaO']  # Rest of Al2O3 in C
                data_n.loc[i, 'CaO'] = 0
                data_n.loc[i, 'Al2O3'] = 0
            else:
                n_phase.loc[i, 'An'] = data_n.loc[i, 'Al2O3']
                data_n.loc[i, 'CaO'] = data_n.loc[i, 'CaO'] - n_phase.loc[i, 'An']
                data_n.loc[i, 'Al2O3'] = 0
            si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 2 * n_phase.loc[i, 'An']

        # 24 / Normative sphene / rutile
        if self.verbose > 1: print("Step 24 - Normative sphene / rutile")

        for i in data_n.index:
            if data_n.loc[i, 'CaO'] >= data_n.loc[i, 'TiO2']:
                n_phase.loc[i, 'Tnp'] = data_n.loc[i, 'TiO2']
                data_n.loc[i, 'CaO'] = data_n.loc[i, 'CaO'] - n_phase.loc[i, 'Tnp']
                data_n.loc[i, 'TiO2'] = 0
            else:
                n_phase.loc[i, 'Tnp'] = data_n.loc[i, 'CaO']
                n_phase.loc[i, 'Ru'] = data_n.loc[i, 'TiO2'] - n_phase.loc[i, 'Tnp']  # Rest of TiO2 in Ru
                data_n.loc[i, 'CaO'] = 0
                data_n.loc[i, 'TiO2'] = 0
            si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + n_phase.loc[i, 'Tnp']

        # 25 / Normative magnetite or hematite
        if self.verbose > 1: print("Step 25 - Normative magnetite or hematite")

        for i in data_n.index:
            if data_n.loc[i, 'Fe2O3'] >= data_n.loc[i, 'FeO']:
                n_phase.loc[i, 'Mt'] = data_n.loc[i, 'FeO']
                n_phase.loc[i, 'Hm'] = data_n.loc[i, 'Fe2O3'] - n_phase.loc[i, 'Mt']  # Rest of Fe2O3 in Mt
                data_n.loc[i, 'FeO'] = 0
                data_n.loc[i, 'Fe2O3'] = 0
            else:
                n_phase.loc[i, 'Mt'] = data_n.loc[i, 'Fe2O3']
                data_n.loc[i, 'FeO'] = data_n.loc[i, 'FeO'] - n_phase.loc[i, 'Mt']
                data_n.loc[i, 'Fe2O3'] = 0

        # 26 / Subdivision of Mg and Fe in some minerals
        if self.verbose > 1: print("Step 26 - Repartition of Mg and Fe in minerals")

        data_n['FeMgO'] = data_n['MgO'] + data_n['FeO']
        prop['xMg'] = data_n['MgO'] / (data_n['MgO'] + data_n['FeO'])
        prop['xFe'] = data_n['FeO'] / (data_n['MgO'] + data_n['FeO'])
        data_n['MgO'] = 0
        data_n['FeO'] = 0

        # 27 / Provisional normative diopside, wollastonite or hypersthene
        if self.verbose > 1: print("Step 27 - normative diopside, wollastonite or hypersthene")

        n_phase['Wop'] = 0
        for i in data_n.index:
            if data_n.loc[i, 'CaO'] >= data_n.loc[i, 'FeMgO']:
                n_phase.loc[i, 'Dip'] = data_n.loc[i, 'FeMgO']
                n_phase.loc[i, 'Wop'] = data_n.loc[i, 'CaO'] - n_phase.loc[i, 'Dip']
                data_n.loc[i, 'CaO'] = 0
                data_n.loc[i, 'FeMgO'] = 0
                si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 2 * n_phase.loc[i, 'Dip'] + n_phase.loc[i, 'Wop']
                n_phase.loc[i, 'Hyp'] = 0
            else:
                n_phase.loc[i, 'Dip'] = data_n.loc[i, 'CaO']
                n_phase.loc[i, 'Hyp'] = data_n.loc[i, 'FeMgO'] - n_phase.loc[i, 'Dip']
                data_n.loc[i, 'CaO'] = 0
                data_n.loc[i, 'FeMgO'] = 0
                si_deff.loc[i, 'Y'] = si_deff.loc[i, 'Y'] + 2 * n_phase.loc[i, 'Dip'] + n_phase.loc[i, 'Hyp']

        # 28 / Normative quartz and Si deficiency
        if self.verbose > 1: print("Step 28 - Normative quartz and Si deficiency")
        n_phase['Q'] = 0
        for i in data_n.index:
            if data_n.loc[i, 'SiO2'] >= si_deff.loc[i, 'Y']:
                n_phase.loc[i, 'Q'] = data_n.loc[i, 'SiO2'] - si_deff.loc[i, 'Y']
                data_n.loc[i, 'SiO2'] = 0
                next_step[i] = '36b'  # Instead of 36a which is obligatory in this algorithm
                if self.verbose: print("Si saturated for the composition", i)
            else:
                si_deff.loc[i, 'D'] = si_deff.loc[i, 'Y'] - data_n.loc[i, 'SiO2']
                data_n.loc[i, 'SiO2'] = 0
                next_step[i] = '29'

        # 29 / Normative olivine or hypersthene
        if self.verbose > 1: print("Step 29 - Normative olivine or hypersthene")
        for i in data_n.index:
            if next_step[i] == '29':
                if si_deff.loc[i, 'D'] < n_phase.loc[i, 'Hyp'] / 2:
                    n_phase.loc[i, 'Ol'] = si_deff.loc[i, 'D']
                    n_phase.loc[i, 'Hy'] = n_phase.loc[i, 'Hyp'] - 2 * si_deff.loc[i, 'D']
                    next_step[i] = '36b'
                else:
                    n_phase.loc[i, 'Ol'] = n_phase.loc[i, 'Hyp'] / 2
                    n_phase.loc[i, 'Hy'] = 0
                    si_deff.loc[i, 'D1'] = si_deff.loc[i, 'D'] - n_phase.loc[i, 'Hyp'] / 2
                    next_step[i] = '30'
            else:
                n_phase.loc[i, 'Hy'] = n_phase.loc[i, 'Hyp']
                n_phase.loc[i, 'Ol'] = 0

        # 30 / Normative sphene or perovskite
        if self.verbose > 1: print("Step 30 - Normative sphene or perovskite")

        for i in data_n.index:
            if next_step[i] == '30':
                if si_deff.loc[i, 'D1'] < n_phase.loc[i, 'Tnp']:
                    n_phase.loc[i, 'Tn'] = n_phase.loc[i, 'Tnp'] - si_deff.loc[i, 'D1']
                    n_phase.loc[i, 'Pf'] = si_deff.loc[i, 'D1']
                    next_step[i] = '36c'
                else:
                    n_phase.loc[i, 'Pf'] = n_phase.loc[i, 'Tnp']
                    n_phase.loc[i, 'Tn'] = 0
                    si_deff.loc[i, 'D2'] = si_deff.loc[i, 'D1'] - n_phase.loc[i, 'Tnp']
                    next_step[i] = '31'

        # 31 / Normative nepheline or albite
        if self.verbose > 1: print("Step 31 - Normative nepheline or albite")

        for i in data_n.index:
            if next_step[i] == '31':
                if si_deff.loc[i, 'D2'] < 4 * n_phase.loc[i, 'Abp']:
                    n_phase.loc[i, 'Ab'] = n_phase.loc[i, 'Abp'] - si_deff.loc[i, 'D2'] / 4
                    n_phase.loc[i, 'Ne'] = si_deff.loc[i, 'D2'] / 4
                    next_step[i] = '36d'
                else:
                    n_phase.loc[i, 'Ne'] = n_phase.loc[i, 'Abp']
                    n_phase.loc[i, 'Ab'] = 0
                    si_deff.loc[i, 'D3'] = si_deff.loc[i, 'D2'] - 4 * n_phase.loc[i, 'Abp']
                    next_step[i] = '32'

        # 32 / Normative leucite or orthoclase
        if self.verbose > 1: print("Step 32 - Normative leucite or orthoclase")

        n_phase['Lcp'] = 0
        for i in data_n.index:
            if next_step[i] == '32':
                if si_deff.loc[i, 'D3'] < 2 * n_phase.loc[i, 'Orp']:
                    n_phase.loc[i, 'Or'] = n_phase.loc[i, 'Orp'] - si_deff.loc[i, 'D3'] / 2
                    n_phase.loc[i, 'Lc'] = si_deff.loc[i, 'D3'] / 2
                    next_step[i] = '36e'
                else:
                    n_phase.loc[i, 'Lcp'] = n_phase.loc[i, 'Orp']
                    n_phase.loc[i, 'Or'] = 0
                    si_deff.loc[i, 'D4'] = si_deff.loc[i, 'D3'] - 2 * n_phase.loc[i, 'Orp']
                    next_step[i] = '33'

        # 33 / Normative dicalcium silicate or wollastonite
        if self.verbose > 1: print("Step 33 - Normative dicalcium silicate or wollastonite")

        for i in data_n.index:
            if next_step[i] == '33':
                if si_deff.loc[i, 'D4'] < 2 * n_phase.loc[i, 'Wop'] / 2:
                    n_phase.loc[i, 'Wo'] = n_phase.loc[i, 'Wop'] - 2 * si_deff.loc[i, 'D4']
                    n_phase.loc[i, 'Cs'] = si_deff.loc[i, 'D4']
                    next_step[i] = '36e'  # Instead of 36f
                else:
                    n_phase.loc[i, 'Cs'] = n_phase.loc[i, 'Wop'] / 2
                    n_phase.loc[i, 'Wo'] = 0
                    si_deff.loc[i, 'D5'] = si_deff.loc[i, 'D4'] - n_phase.loc[i, 'Wop'] / 2
                    next_step[i] = '34'

        # 34 / Normative dicalcium silicate or olivine
        if self.verbose > 1: print("Step 34 - Normative diopside or olivine adjustment")

        for i in data_n.index:
            if next_step[i] == '34':
                if si_deff.loc[i, 'D5'] < n_phase.loc[i, 'Dip']:
                    n_phase.loc[i, 'Cs'] = n_phase.loc[i, 'Cs'] + si_deff.loc[i, 'D5'] / 2
                    n_phase.loc[i, 'Ol'] = n_phase.loc[i, 'Ol'] + si_deff.loc[i, 'D5'] / 2
                    n_phase.loc[i, 'Di'] = n_phase.loc[i, 'Dip'] - si_deff.loc[i, 'D5']
                    next_step[i] = '36g'
                else:
                    n_phase.loc[i, 'Cs'] = n_phase.loc[i, 'Cs'] + n_phase.loc[i, 'Dip'] / 2
                    n_phase.loc[i, 'Ol'] = n_phase.loc[i, 'Ol'] + n_phase.loc[i, 'Dip'] / 2
                    n_phase.loc[i, 'Di'] = n_phase.loc[i, 'Di-fe'] = n_phase.loc[i, 'Di-mg'] = 0
                    si_deff.loc[i, 'D6'] = si_deff.loc[i, 'D5'] - n_phase.loc[i, 'Dip']
                    next_step[i] = '35'
            else:
                n_phase['Di'] = n_phase['Dip']

        # 35 / Normative kaliophilite or leucite
        if self.verbose > 1: print("Step 35 - Normative kaliophilite or leucite")

        for i in data_n.index:
            if next_step[i] == '35':
                if n_phase.loc[i, 'Lcp'] >= si_deff.loc[i, 'D6'] / 2:
                    n_phase.loc[i, 'Kp'] = si_deff.loc[i, 'D6'] / 2
                    n_phase.loc[i, 'Lc'] = n_phase.loc[i, 'Lcp'] - si_deff.loc[i, 'D6'] / 2
                    next_step[i] = '36g'
                else:
                    n_phase.loc[i, 'Kp'] = n_phase.loc[i, 'Lcp']
                    n_phase.loc[i, 'Lc'] = 0
                    suppl.loc[i, 'defSiO2'] = (si_deff.loc[i, 'D6'] - 2 * n_phase.loc[i, 'Kp']) * corr_mol_w['SiO2']
                    next_step[i] = '36g'

        # 36 / Definite mineral proportions

        for i in data_n.index:
            if self.verbose > 1: print("Step 36 - Solution", i)

            if next_step[i] == '36b':
                if self.verbose > 1: print("     36b")
                n_phase.loc[i, 'Tn'] = n_phase.loc[i, 'Tnp']
                next_step[i] = '36c'

            if next_step[i] == '36c':
                if self.verbose > 1: print("     36c")
                n_phase.loc[i, 'Ab'] = n_phase.loc[i, 'Abp']
                next_step[i] = '36d'

            if next_step[i] == '36d':
                if self.verbose > 1: print("     36d")
                n_phase.loc[i, 'Or'] = n_phase.loc[i, 'Orp']
                n_phase.loc[i, 'Lc'] = n_phase.loc[i, 'Lcp']
                next_step[i] = '36e'

            if next_step[i] == '36e':
                if self.verbose > 1: print("     36e")
                if 'Wop' in n_phase.keys():
                    n_phase.loc[i, 'Wo'] = n_phase.loc[i, 'Wop']

        # Steps of 36a and 36f, obligatory for this algorithm
        if self.verbose > 1: print("     Obilgatory 36a, 36f and Fe-Mg distribution in olivine")
        n_phase['Hy-fe'] = n_phase['Hy'] * prop['xFe']
        n_phase['Hy-mg'] = n_phase['Hy'] * prop['xMg']
        n_phase['Di-fe'] = n_phase['Di'] * prop['xFe']
        n_phase['Di-mg'] = n_phase['Di'] * prop['xMg']
        n_phase['Ol-fe'] = n_phase['Ol'] * prop['xFe']
        n_phase['Ol-mg'] = n_phase['Ol'] * prop['xMg']

        # 37 / Conversion of normative minerals in %, normative sum
        if self.verbose > 1: print("Step 37 - Conversion of normative minerals in %, normative sum")

        ignored_phases = []
        for mineral in n_phase.keys():
            if mineral in final_list_min:
                partitions[mineral] = n_phase[mineral] * mol_w_min[mineral]
            elif mineral == 'Ap':
                suppl['Ap-F'] = n_phase['Ap-F'] * mol_w_min['Ap-F']
                suppl['Ap-O'] = n_phase['Ap-O'] * mol_w_min['Ap-O']
                partitions['Ap'] = suppl['Ap-F'] + suppl['Ap-O']
            elif mineral == 'Ol':
                suppl['Ol-mg'] = n_phase['Ol-mg'] * mol_w_min['Ol-mg']
                suppl['Ol-fe'] = n_phase['Ol-fe'] * mol_w_min['Ol-fe']
                partitions['Ol'] = suppl['Ol-mg'] + suppl['Ol-fe']
            elif mineral == 'Hy':
                suppl['Hy-mg'] = n_phase['Hy-mg'] * mol_w_min['Hy-mg']
                suppl['Hy-fe'] = n_phase['Hy-fe'] * mol_w_min['Hy-fe']
                partitions['Hy'] = suppl['Hy-mg'] + suppl['Hy-fe']
            elif mineral == 'Di':
                suppl['Di-mg'] = n_phase['Di-mg'] * mol_w_min['Di-mg']
                suppl['Di-fe'] = n_phase['Di-fe'] * mol_w_min['Di-fe']
                partitions['Di'] = suppl['Di-mg'] + suppl['Di-fe']
            else:
                ignored_phases.append(mineral)

        if self.verbose > 1: print("Temporary phases ignored in final composition :", *ignored_phases[skip_cols:])

        # Add free CO2
        free = free.fillna(0)
        free_phases = free.keys()
        if 'CO2' in free_phases:
            partitions['CO2'] = free['CO2'] * corr_mol_w['CO2']

        # Add free O
        if minor_included:
            # Free O
            free['O_wt%'] = 0
            if 'O_12b' in free_phases:
                free['O_wt%'] = free['O_wt%'] + (1 + (0.1 * (mol_w_min['Ap-F'] / 328.8691887) - 1)) * \
                                corr_mol_w['O'] * free['O_12b']
            if 'O_12c' in free_phases:
                free['O_wt%'] = free['O_wt%'] + (
                        1 + 0.1 * (n_phase['Ap-F'] / n_phase['Ap']) * (mol_w_min['Ap-F'] / 328.8691887) - 1) * \
                                corr_mol_w['O'] * free['O_12c']
            if 'O_13' in free_phases:
                free['O_wt%'] = free['O_wt%'] + (1 + (corr_mol_w['CaO'] / 56.0774 - 1)) * corr_mol_w['O'] * free['O_13']
            if 'O_14' in free_phases:
                free['O_wt%'] = free['O_wt%'] + (1 + 0.5 * (corr_mol_w['Na2O'] / 61.97894 - 1)) * corr_mol_w['O'] * \
                                free['O_14']
            if 'O_16' in free_phases:
                free['O_wt%'] = free['O_wt%'] + (1 + (corr_mol_w['FeO'] / 71.8444 - 1)) * corr_mol_w['O'] * free['O_16']
            partitions['O'] = free['O_wt%']

        # Add free oxides
        partitions['free_Ox'] = 0
        free_keys = free.keys()
        for oxel in ['P2O5', 'F', 'Cl', 'SO3', 'Cr2O3']:
            if oxel in free_keys:
                partitions['free_oxides'] = partitions['free_Ox'] + free[oxel] * _mol_w[oxel]

        # Totals
        partitions['Sum_norm'] = partitions.iloc[:, skip_cols:].sum(axis=1)
        partitions = partitions.round(to_round)

        # 38 / Correctness of normative sum
        if self.verbose > 1: print("Step 38 - Correctness of normative sum")

        suppl['diff_sum'] = total_normalized - partitions['Sum_norm']

        # 39 / Other petrogenetical parameters
        if self.verbose > 1: print("Step 39 - Other petrogenetical parameters")

        suppl['pp_salic'] = n_phase['Q'] + n_phase['Or'] + n_phase['Ab'] + n_phase['An']
        suppl['pp_femic'] = suppl['Di-mg'] + suppl['Di-fe'] + suppl['Hy-mg'] + suppl['Hy-fe'] + suppl['Ol-mg'] + \
                            n_phase['Ol-fe'] + n_phase['Mt'] + n_phase['Il'] + n_phase['Hm']
        suppl['pp_CI'] = n_phase['An'] + 2.1570577 * suppl['Di-mg'] + suppl['Ol-mg'] + 0.7007616 * suppl['Hy-fe']
        suppl['pp_DI'] = n_phase['Q'] + n_phase['Or'] + n_phase['Ab'] + n_phase['An']

        partitions = partitions.fillna(0)
        partitions = partitions.loc[:, (partitions != 0).any(axis=0)]
        free = free.fillna(0)
        free = free.round(to_round)
        free = free.loc[:, (free != 0).any(axis=0)]
        suppl = suppl.round(to_round)
        suppl = suppl.fillna(0)

        if self.verbose:
            print(">>> Final compositions (wt %)")
            print(partitions.to_string())
            print(">>> Free phases (mol)")
            print(free.to_string())
            print(">>> Supplementary data")
            print(suppl.to_string())

        return partitions, (free, suppl)

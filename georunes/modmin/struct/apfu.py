import pandas as pd

from georunes.tools.chemistry import molar_mass, el_molar_mass, number_cations_per_oxygen, get_cation, \
    number_oxygen_in_oxide
from georunes.modmin.optim.base import BaseOptimizer

supported_oxides = ['SiO2', 'TiO2', 'CO2', 'Al2O3', 'Cr2O3', 'Fe2O3', 'FeO', 'Mn2O3', 'MnO', 'MgO', 'NiO', 'CaO', 'BaO',
                    'SrO', 'Li2O', 'Na2O', 'K2O', 'Rb2O', 'P2O5', 'H2O']
supported_anions = ['F', 'Cl']

custom_cation = {
    "Fe2O3": "Fe3+",
    "FeO": "Fe2+",
    "Mn2O3": "Mn3+",
    "MnO": "Mn2+"
}


class APFUCalc(BaseOptimizer):
    def __init__(self, **kwargs):
        BaseOptimizer.__init__(self, **kwargs)
        self.notif = ">>>>>> Atoms per formula unit (APFU) calculation"

    def compute(self, raw_data, skip_cols, oxygen_number=12, oxygen_equiv=False, to_round=3,
                ignored_columns=('LOI', 'H2O+', 'Total'), force_cation_number=None):
        if ignored_columns is None:
            ignored_columns = []

        # 1 / Preparing data
        if self.verbose > 1: print("Step 1 - Prepare data")

        data = raw_data.iloc[:, :skip_cols].copy()
        raw_data_keys = raw_data.iloc[:, skip_cols:].keys()
        supported_oxel = [*supported_oxides, *supported_anions]  # Limit the list of usable oxide
        for key in raw_data_keys:
            if key in supported_oxel and key not in ignored_columns:
                data[key] = raw_data[key]
        data = data.fillna(0)
        data_keys = data.keys()
        list_oxel = [ox for ox in data_keys if ox in supported_oxel]
        list_ox = [ox for ox in list_oxel if ox in supported_oxides]

        filtered_columns = [oxel for oxel in raw_data_keys if oxel not in data_keys]
        if self.verbose: print('Ignored columns :', filtered_columns)

        moles_oxides = data.iloc[:, :skip_cols].copy()
        moles_oxygen = data.iloc[:, :skip_cols].copy()
        ox_normalized = data.iloc[:, :skip_cols].copy()
        moles_cations = data.iloc[:, :skip_cols].copy()
        suppl = data.iloc[:, :skip_cols].copy()
        suppl["sum_cations"] = 0
        suppl["sum_anions"] = 0

        # 2 / Weight percent to moles number in oxides
        if self.verbose > 1: print("Step 2 - Calculate number of moles from weight percent of each oxide")
        for oxel in list_oxel:
            if oxel in supported_anions:
                moles_oxides[oxel] = data[oxel] / el_molar_mass[oxel]
            else:
                moles_oxides[oxel] = data[oxel] / molar_mass[oxel]

        # 3 / Moles number to oxygen moles number in oxides
        if self.verbose > 1: print("Step 3 - Calculate number of moles of oxygen in each oxide")

        for oxel in list_oxel:
            if oxel == 'H2O':
                moles_oxygen['H2O'] = moles_oxides['H2O']
            elif oxel in list_ox:
                moles_oxygen[oxel] = moles_oxides[oxel] * number_oxygen_in_oxide(oxel)
            else:
                moles_oxygen[oxel] = moles_oxides[oxel]

        # 4 / Normalization to the number of oxygen per formula
        if self.verbose > 1: print("Step 4 - Normalization to the number of oxygen per formula")

        _o = 'O'
        sum_o = moles_oxygen.iloc[:, skip_cols:].sum(axis=1)
        if oxygen_equiv:
            for element in supported_anions:
                if element in list_oxel:
                    sum_o = sum_o - moles_oxygen[element]/2  # 2 F,Cl for one O
                    _o = _o+'+'+str(element)

        oxygen_factor = oxygen_number / sum_o
        suppl["O_factor"] = oxygen_factor
        for oxel in list_oxel:
            ox_normalized[oxel] = moles_oxygen[oxel] * oxygen_factor

        # 5 / Normalized oxygen numbers to cations number
        if self.verbose > 1: print("Step 5 - Calculation of each cation number according to the normalized oxygen")

        for oxel in list_oxel:
            if oxel == 'H2O':
                moles_cations['OH'] = ox_normalized[oxel] * 2
                suppl["sum_anions"] = suppl["sum_anions"] + moles_cations['OH']
            elif oxel in supported_anions:
                moles_cations[oxel] = ox_normalized[oxel]
                suppl["sum_anions"] = suppl["sum_anions"] + moles_cations[oxel]
            elif oxel in custom_cation.keys():
                cat = custom_cation[oxel]
                moles_cations[cat] = ox_normalized[oxel] * number_cations_per_oxygen(oxel)
                suppl["sum_cations"] = suppl["sum_cations"] + moles_cations[cat]
            else:
                cat = get_cation(oxel)
                moles_cations[cat] = ox_normalized[oxel] * number_cations_per_oxygen(oxel)
                if cat not in ('P', 'C'):
                    suppl["sum_cations"] = suppl["sum_cations"] + moles_cations[cat]
        moles_cations[_o] = oxygen_number

        # If the cations number is fixed
        if isinstance(force_cation_number, int) and force_cation_number > 0:
            if self.verbose > 1: print("Number of cations forced to " + str(force_cation_number))
            moles_cations_cat_fixed = data.iloc[:, :skip_cols].copy()
            sum_cat = pd.Series([0] * len(moles_cations_cat_fixed), dtype=float, )
            list_atoms = moles_cations.iloc[:, skip_cols:].keys()
            for cat in list_atoms:
                if cat not in ('P', 'C', 'OH', 'O', 'O+F', 'O+Cl', 'O+F+Cl', 'O+Cl+F', *supported_anions):
                    sum_cat = sum_cat + moles_cations[cat]
            cations_factor = force_cation_number / sum_cat

            for cat in list_atoms:
                moles_cations_cat_fixed[cat] = moles_cations[cat] * cations_factor
            suppl["sum_anions_CF"] = suppl["sum_anions"] * cations_factor
            suppl["sum_cations_CF"] = suppl["sum_cations"] * cations_factor
            suppl['cations_factor'] = cations_factor
            moles_cations_cat_fixed = moles_cations_cat_fixed.round(to_round)

        # End
        moles_cations = moles_cations.round(to_round)

        suppl = suppl.round(to_round)
        suppl = suppl.fillna(0)
        if self.verbose:
            print(">>> Atoms")
            print(moles_cations.to_string())
        if self.verbose > 1:
            if isinstance(force_cation_number, int) and force_cation_number > 0:
                print(">>> Atoms (with cations normalized to " + str(force_cation_number) + ")")
                print(moles_cations_cat_fixed.to_string())
            print(">>> Supplementary data")
            print(suppl.to_string())

        return moles_cations, suppl

    def compute_oxygen_basis(self, raw_data, skip_cols, oxygen_number, **kwargs):
        return self.compute(raw_data, skip_cols, oxygen_number=oxygen_number, **kwargs)

    def compute_cation_basis(self, raw_data, skip_cols,  force_cation_number, oxygen_number=12, **kwargs):
        return self.compute(raw_data, skip_cols, force_cation_number=force_cation_number, oxygen_number=oxygen_number,
                            **kwargs)

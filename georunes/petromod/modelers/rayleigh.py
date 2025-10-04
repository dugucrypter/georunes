from georunes.petromod.modelers.partition import PartitionModeler


class RayleighCrystallization(PartitionModeler):
    def __init__(self, bulk_dist_coeffs):
        PartitionModeler.__init__(self, bulk_dist_coeffs)
        self.phases_labels = {"LIQ": "Instantaneous liquid",
                                 "SOL_INST": "Instantaneous solid",
                                 "SOL_TOT": "Accumulated solid", }
        self.modeler_name = "Fractionated crystallization"
        self.init_name = "Initial liquid composition (F=1)"

    def ratio_liq(self, liq_fract):
        if liq_fract == 0:
            liq_fract = 0.01
        ratio_liq = self.bulk_dist_coeffs.copy()
        for index, row in ratio_liq.items():
            ratio_liq[index] = liq_fract ** (self.bulk_dist_coeffs[index] - 1)
        ratio_liq = ratio_liq.drop(columns=['D', ])

        return ratio_liq

    def ratio_sol(self, liq_fract):
        """
        Calculate the ratio : instantaneous cumulate / initial concentration
        """
        return self.ratio_liq(liq_fract) * self.bulk_dist_coeffs

    def ratio_sol_avg(self, liq_fract):
        """
        Calculate the ratio : total cumulate / initial concentration
        """
        if liq_fract == 1:
            liq_fract = 0.99
        ratio_sol = self.bulk_dist_coeffs.copy()
        for index, row in ratio_sol.items():
            num = 1 - liq_fract ** (self.bulk_dist_coeffs[index])
            ratio_sol[index] = num / (1 - liq_fract)
        return ratio_sol

    def concentration_sol_avg_el(self, el, liq_fract, initial_c0):
        """
        Calculate the ratio for element : instantaneous cumulate / initial concentration
        """
        c_sol_el = initial_c0[el] * self.ratio_sol_avg(liq_fract)[el]
        return c_sol_el

    def get_phase_concentration_func(self, phase):
        if phase == 'LIQ':
            return self.concentration_liq_el
        elif phase == 'SOL_INST':
            return self.concentration_sol_el
        elif phase == 'SOL_TOT':
            return self.concentration_sol_avg_el
        raise Exception("Inapplicable phase : " + str(phase))

    @staticmethod
    def get_phases_labels():
        return {"LIQ": "Liquid", "SOL_INST": "Instantaneous solid", "SOL_TOT": "Accumulated solid"}


class RayleighMelting(PartitionModeler):
    def __init__(self, bulk_dist_coeffs):
        PartitionModeler.__init__(self, bulk_dist_coeffs)
        self.phases_labels = {"LIQ_INST": "Instantaneous liquid",
                                 "LIQ_TOT": "Accumulated liquid",
                                 "SOL": "Solid residue", }
        self.modeler_name = "Rayleigh melting"
        self.init_name = "Initial solid composition (F=0)"

    def ratio_liq(self, liq_fract):
        if liq_fract == 1:
            liq_fract = 0.99
        ratio_liq = self.bulk_dist_coeffs.copy()
        for index, row in ratio_liq.items():
            ratio_liq[index] = (1 / self.bulk_dist_coeffs[index]) * (1 - liq_fract) ** (
                        1 / self.bulk_dist_coeffs[index] - 1)
        return ratio_liq

    def ratio_sol(self, liq_fract):
        return self.ratio_liq(liq_fract) * self.bulk_dist_coeffs

    def ratio_liq_avg(self, liq_fract):
        if liq_fract == 0:
            liq_fract = 0.01
        ratio_liq_avg = self.bulk_dist_coeffs.copy()
        for index, row in ratio_liq_avg.items():
            num = 1 - (1 - liq_fract) ** (1 / self.bulk_dist_coeffs[index])
            ratio_liq_avg[index] = num / liq_fract
        return ratio_liq_avg

    def concentration_liq_avg_el(self, el, liq_fract, initial_conc):
        c_liq_el = initial_conc[el] * self.ratio_liq_avg(liq_fract)[el]
        return c_liq_el

    def get_phase_concentration_func(self, phase):
        if phase == 'LIQ_INST':
            return self.concentration_liq_el
        elif phase == 'SOL':
            return self.concentration_sol_el
        elif phase == 'LIQ_TOT':
            return self.concentration_liq_avg_el
        raise Exception("Inapplicable phase : " + str(phase))

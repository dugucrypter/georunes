from georunes.petromod.modelers.partition import PartitionModeler


class BatchModeler(PartitionModeler):
    def __init__(self,  bulk_dist_coeffs):
        PartitionModeler.__init__(self, bulk_dist_coeffs)
        self.phases_labels = {"LIQ": "Instantaneous/accumulated melt",
                             "SOL": "Total solid"}
        self.modeler_name = "Batch modeler"

    def ratio_liq(self, liq_fract):
        """
        Calculate the ratio : liquid / initial concentration
        """
        ratio_liq = 1 / (self.bulk_dist_coeffs * (1 - liq_fract) + liq_fract)
        return ratio_liq

    def ratio_sol(self, liq_fract):
        """
        Calculate the ratio : solid / initial concentration
        """
        return self.ratio_liq(liq_fract) * self.bulk_dist_coeffs


class BatchMelting(BatchModeler):
    def __init__(self,  bulk_dist_coeffs):
        BatchModeler.__init__(self, bulk_dist_coeffs)
        self.phases_labels = {"LIQ": "Instantaneous/accumulated melt",
                             "SOL": "Solid residue"}
        self.modeler_name = "Batch melting modeler"
        self.init_name = "Initial solid composition (F=0)"


class BatchCrystallization(BatchModeler):
    def __init__(self,  bulk_dist_coeffs):
        BatchModeler.__init__(self, bulk_dist_coeffs)
        self.phases_labels = {"LIQ": "Instantaneous/accumulated melt",
                             "SOL": "Solid cumulate"}
        self.modeler_name = "Batch crystallization model"
        self.init_name = "Initial liquid composition (F=1)"
        self.f_reverse = True

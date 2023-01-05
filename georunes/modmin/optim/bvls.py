import numpy as np
from pandas import DataFrame
from scipy.optimize import lsq_linear
from georunes.modmin.optim.base import Optimizer


class BVLS(Optimizer):
    def __init__(self, **kwargs):
        Optimizer.__init__(self, **kwargs)
        self.dist_func = "euclidian"
        self.notif = ">>>>>> Bounded Variable Least Squares Method"

    def _compute(self, raw_data, skip_cols, raw_minerals_data, to_round=4, max_minerals=None, min_minerals=None,
                 unfillable_partitions_allowed=True, ignore_oxides=None):
        if self.verbose > 1:
            print("Round digits :", to_round, " --  Oxides to ignore : " + str(ignore_oxides) if ignore_oxides else "")
        self.prepare_data(raw_data, skip_cols, raw_minerals_data, ignore_oxides)
        partitions = DataFrame(columns=self.list_minerals)
        deviation_name = "deviation_" + self.dist_func
        suppl = DataFrame(columns=[deviation_name])

        for i in self.data.index:
            if self.verbose: print(">>> Composition", i)
            list_minerals_i = self.list_minerals.copy()
            minerals_data_i = self.minerals_data.copy()
            bulk_chem = self.data.iloc[i].to_numpy()

            # Get maximum possible proportion for each mineral
            max_minerals_prop = []
            unnecessary_minerals = []
            for mineral in self.list_minerals:
                # Maximum proportion for each oxide equals Ox wt% in bulk chemistry / Ox wt% in mineral composition
                max_oxides_prop = self.data.iloc[i] / minerals_data_i[mineral].transpose()
                mineral_prop = max_oxides_prop.min()
                if np.isinf(mineral_prop) or mineral_prop == 0:
                    minerals_data_i = minerals_data_i.drop(columns=mineral)
                    list_minerals_i.remove(mineral)
                    unnecessary_minerals.append(mineral)
                else:
                    max_minerals_prop.append(mineral_prop)
            nb_minerals_i = len(list_minerals_i)
            min_minerals_prop = [0] * nb_minerals_i

            # Update minerals proportions with defined settings if provided
            if max_minerals:
                for key, value in max_minerals.items():
                    idx = list_minerals_i.index(key)
                    if idx:
                        max_minerals_prop[idx] = min(max_minerals_prop[idx], max_minerals[key])
            if min_minerals:
                for key, value in min_minerals.items():
                    idx = list_minerals_i.index(key)
                    if idx:
                        min_minerals_prop[idx] = max(min_minerals_prop[idx], min_minerals[key])
            if not unfillable_partitions_allowed and sum(max_minerals_prop) < 1.05:  # 5% tolerance
                raise Exception("Problem in composition " + str(i)
                                + ". The sum of the maximum proportions of minerals cannot complete to 100 "
                                  "(found " + str(100 * sum(max_minerals_prop)) + str(")."))

            if self.verbose and unnecessary_minerals:
                print("Unnecessary minerals :", *unnecessary_minerals)

            # Direct calculation of the result
            result = lsq_linear(minerals_data_i, bulk_chem, (min_minerals_prop, max_minerals_prop), method='bvls',
                                verbose=min(self.verbose, 2))
            dict_res = {list_minerals_i[i]: result.x[i] for i in range(len(list_minerals_i))}

            idx_new_row = len(partitions)
            for miner, prop in dict_res.items():
                partitions.loc[idx_new_row, miner] = prop
            partitions = partitions.fillna(0)
            partitions.iloc[idx_new_row] = 100 * partitions.iloc[idx_new_row]
            partitions = partitions.round(to_round)

            deviation = self.deviation(bulk_chem, np.dot(self.minerals_data, partitions.iloc[idx_new_row] / 100))
            chem = np.dot(self.minerals_data, partitions.loc[idx_new_row] / 100).round(to_round)
            suppl.loc[idx_new_row, deviation_name] = deviation
            suppl.loc[idx_new_row, "total_chem"] = sum(chem)

            if self.verbose:
                print("Solution", idx_new_row)
                print(partitions.loc[idx_new_row].to_dict())
                print("Corresponding composition")
                print([str(self.list_bulk_ox[i]) + " : " + str(chem[i]) for i in range(self.nb_oxides)])
                print("Deviation :", round(deviation, to_round), "%" if self.dist_func == "SMAPE" else "", "\n------")

        partitions["Total"] = partitions.sum(axis=1).round(to_round)
        suppl["diff_total_chem"] = suppl["total_chem"] - self.init_total

        return partitions, suppl

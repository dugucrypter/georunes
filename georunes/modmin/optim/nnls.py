import numpy as np
from pandas import DataFrame
from scipy.optimize import nnls
from georunes.modmin.optim.base import Optimizer


class NNLS(Optimizer):
    def __init__(self, verbose=False, **kwargs):
        Optimizer.__init__(self, verbose=verbose, **kwargs)
        self.dist_func = "euclidian"
        self.notif = ">>>>>> Non-Negative Least Squares method"

    def _compute(self, raw_data, skip_cols, raw_minerals_data, to_round=4, ignore_oxides=None,
                 max_iter=None):
        if self.verbose > 1:
            print("Round digits :", to_round, " --  Maximum iterations :", max_iter,
                  " --  Oxides to ignore : " + str(ignore_oxides) if ignore_oxides else "")
        self.prepare_data(raw_data, skip_cols, raw_minerals_data, ignore_oxides)

        partitions = DataFrame(columns=self.list_minerals)
        deviation_name = "deviation_" + self.dist_func
        suppl = DataFrame(columns=[deviation_name])
        for i in self.data.index:
            if self.verbose: print(">>> Composition", i)
            list_minerals_i = self.list_minerals.copy()
            minerals_data_i = self.minerals_data.copy()
            bulk_chem = self.data.iloc[i].to_numpy()

            # Ignore minerals missing some oxides
            unnecessary_minerals = []
            for ox in self.list_bulk_ox:
                if self.data.loc[i, ox] == 0:
                    for mineral in minerals_data_i:
                        if minerals_data_i.loc[ox, mineral] > 0:
                            minerals_data_i = minerals_data_i.drop(columns=mineral)
                            list_minerals_i.remove(mineral)
                            unnecessary_minerals.append(mineral)
            if self.verbose and unnecessary_minerals:
                print("Unnecessary minerals :", *unnecessary_minerals)

            # Direct calculation of the result
            result = nnls(minerals_data_i, bulk_chem, max_iter)
            dict_res = {list_minerals_i[i]: result[0][i] for i in range(len(list_minerals_i))}

            idx_new_row = len(partitions)
            for miner, prop in dict_res.items():
                partitions.loc[idx_new_row, miner] = prop
            partitions = partitions.fillna(0)
            partitions.iloc[idx_new_row] = 100 * partitions.iloc[idx_new_row]
            partitions = partitions.round(to_round)

            deviation = self.deviation(bulk_chem, np.dot(self.minerals_data, partitions.iloc[idx_new_row] / 100))
            suppl.loc[idx_new_row, deviation_name] = deviation

            if self.verbose:
                print("Solution", idx_new_row)
                print(partitions.loc[idx_new_row].to_dict())
                print("Corresponding composition")
                chem = np.dot(self.minerals_data, partitions.loc[idx_new_row] / 100).round(to_round)
                print([str(self.list_bulk_ox[i]) + " : " + str(chem[i]) for i in range(self.nb_oxides)])
                print("Deviation :", round(deviation, to_round), "%" if self.dist_func == "SMAPE" else "", "\n------")

        partitions["Total"] = partitions.sum(axis=1).round(to_round)
        suppl["Diff_total"] = partitions["Total"] - self.init_total

        return partitions, suppl

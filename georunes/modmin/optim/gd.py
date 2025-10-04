import warnings
import numpy as np
from pandas import DataFrame
from georunes.modmin.optim.base import Optimizer, is_in_bounds, random_part_with_bounds
from georunes.tools.warnings import FunctionParameterWarning


class GradientDescent(Optimizer):

    def __init__(self, dist_func="euclidian", filling_tolerance=0.05, **kwargs):
        Optimizer.__init__(self, **kwargs)
        self.dist_func = dist_func
        self.filling_tolerance = filling_tolerance
        self.notif = ">>>>>> Gradient Descent method / deviation function : " + dist_func

    @staticmethod
    def grad(x, y, A, total=1):
        B = A.copy()
        B.loc[len(B.index)] = np.array([1] * len(x))  # Row added to minerals_data (A) to keep a sum equals to total
        Bt = B.transpose()
        y = np.append(y, total)
        out = (np.dot(np.dot(Bt, B), x) - np.dot(Bt, y)) / (len(B.index))
        return out

    def _compute(self, raw_data, skip_cols, raw_minerals_data, to_round=4,
                 max_minerals=None, min_minerals=None, unfillable_partitions_allowed=True, ignore_oxides=None,
                 max_iter=int(1e6), learn_rate=None, tolerance=1e-08, starting_partition=None, force_totals=False,
                 residual_in_suppl=False):

        if not learn_rate:
            learn_rate = 1 * pow(10, -to_round)

        if self.verbose > 1:
            print("Round digits :", to_round, " --  Maximum iterations :", max_iter, " --  Learn rate :", learn_rate,
                  " --  Tolerance :", tolerance,
                  " --  Oxides to ignore : " + str(ignore_oxides) if ignore_oxides else "")
            if starting_partition: print("Starting partition :", starting_partition)

        self.prepare_data(raw_data, skip_cols, raw_minerals_data, ignore_oxides)
        partitions = DataFrame(columns=self.list_minerals)
        deviation_name = "deviation_" + self.dist_func
        suppl = DataFrame(columns=[deviation_name])
        bulk_chems = [0]*len(self.data.index)
        found_chems = [0]*len(self.data.index)

        if force_totals:
            if unfillable_partitions_allowed:
                warnings.warn("The parameter force_totals is True. Then, the parameter unfillable_partitions_allowed "
                                "will be set to False.", FunctionParameterWarning)
            target_totals = self.init_total
        else:
            target_totals = [100] * len(self.data.index)

        # Get maximum proportion for each mineral
        for i in self.data.index:
            if self.verbose: print(">>> Composition", i)
            list_minerals_i = self.list_minerals.copy()
            minerals_data_i = self.minerals_data.copy()
            bulk_chems[i] = self.data.iloc[i].to_numpy()

            # Get maximum possible proportion for each mineral
            max_minerals_prop = []
            unnecessary_minerals = []
            for mineral in self.list_minerals:
                # Maximum proportion for each oxide equals Ox wt% in bulk chemistry / ox wt% in mineral composition
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
            if not unfillable_partitions_allowed and sum(max_minerals_prop) < 1+self.filling_tolerance:  # % tolerance, default 5
                raise Exception("Problem in composition " + str(i)
                                + ". The sum of the maximum proportions of minerals cannot complete to 100 "
                                  "(found " + str(100 * sum(max_minerals_prop)) + str(")."))

            if self.verbose and unnecessary_minerals:
                print("Unnecessary minerals :", *unnecessary_minerals)

            # Gradient descent
            if self.verbose: print("Start calculations. Expected number of iterations :", max_iter)

            # Starting value
            if isinstance(starting_partition, dict):
                if not unfillable_partitions_allowed and sum(starting_partition.values()) != 100:
                    print("WARNING : The starting partition does not complete to 100. The calculations will be "
                          "started with a random composition.")
                    candidate = random_part_with_bounds(nb_minerals_i, max_minerals_prop, min_minerals_prop,
                                                        verbose=self.verbose)
                else:
                    # Check if all minerals in the config are present in minerals_data_i
                    if all(el in list_minerals_i for el in starting_partition.keys()):
                        candidate = []
                        for key in list_minerals_i:
                            val = starting_partition[key] / 100. if key in starting_partition.keys() else 0
                            candidate.append(val)
                        if not is_in_bounds(candidate, max_minerals_prop, min_minerals_prop):
                            print("WARNING : The starting partition does not respect the provided or the calculated "
                                  "bounds data : Minerals =", list_minerals_i, ", Max =", max_minerals_prop, ", Min =",
                                  min_minerals_prop, "The calculations will be started with a random composition.")
                            candidate = random_part_with_bounds(nb_minerals_i, max_minerals_prop, min_minerals_prop,
                                                                unfillable_partitions_allowed=unfillable_partitions_allowed, verbose=self.verbose)
                    else:
                        print("WARNING : Some minerals in starting partition are not present in mineral chemistry "
                              "data. The calculations will be started with a random composition.")
                        candidate = random_part_with_bounds(nb_minerals_i, max_minerals_prop, min_minerals_prop,
                                                            unfillable_partitions_allowed=unfillable_partitions_allowed,
                                                            verbose=self.verbose)
            else:
                candidate = random_part_with_bounds(nb_minerals_i, max_minerals_prop, min_minerals_prop,
                                                    unfillable_partitions_allowed=unfillable_partitions_allowed,
                                                    verbose=self.verbose)

            if self.verbose: print("Starting partition", dict(zip(list_minerals_i, candidate)))

            # Loop
            for k in range(max_iter):
                diff = -learn_rate * np.array(
                    self.grad(candidate, bulk_chems[i], minerals_data_i, total=target_totals[i] / 100))
                new_candidate = candidate + diff
                new_candidate = np.where(new_candidate < min_minerals_prop, min_minerals_prop, new_candidate)
                new_candidate = np.where(new_candidate > max_minerals_prop, max_minerals_prop, new_candidate)
                clean_diff = new_candidate - candidate

                if np.all(np.abs(clean_diff) <= tolerance):
                    if self.verbose: print("Tolerance condition reached after iteration", k)
                    break

                candidate = new_candidate
                if self.verbose > 2:
                    print("New solution at iteration", k)
                    print(dict(zip(list_minerals_i, candidate)))
                    corresp_chem = np.dot(minerals_data_i, candidate).round(decimals=to_round)
                    print("New deviation :", self.deviation(bulk_chems[i], corresp_chem),
                          "%" if self.dist_func == "SMAPE" else "")

            dict_res = {list_minerals_i[i]: round(candidate[i], to_round) for i in range(len(list_minerals_i))}

            idx_new_row = len(partitions)
            for miner, prop in dict_res.items():
                partitions.loc[idx_new_row, miner] = prop
            partitions = partitions.fillna(0).infer_objects(copy=False) # infer_objects prevent the downcasting of object dtype
            partitions.iloc[idx_new_row] = 100 * partitions.iloc[idx_new_row]
            partitions = partitions.round(to_round)

            deviation = self.deviation(bulk_chems[i], np.dot(self.minerals_data, partitions.iloc[idx_new_row] / 100.))
            found_chems[i] = np.dot(self.minerals_data, partitions.loc[idx_new_row] / 100.).round(to_round)
            suppl.loc[idx_new_row, deviation_name] = deviation
            suppl.loc[idx_new_row, "total_chem"] = sum(found_chems[i])

            if self.verbose:
                print("Solution", idx_new_row)
                print(partitions.loc[idx_new_row].to_dict())
                print("Corresponding composition")
                print([ str(a) + " : " + str(b) for a,b in zip(self.list_bulk_ox , found_chems[i])])
                print("Deviation :", round(deviation, to_round), "%" if self.dist_func == "SMAPE" else "", "\n------")

        partitions["Total"] = partitions.sum(axis=1).round(to_round)
        suppl["diff_total_chem"] = suppl["total_chem"] - self.init_total
        if residual_in_suppl:
            residuals = np.subtract(bulk_chems, found_chems)
            t_residuals = list(map(list, zip(*residuals)))  # Transposition
            for p, ox in enumerate(self.list_bulk_ox):
                print(t_residuals[p])
                suppl["resid_" + str(ox)] = t_residuals[p]

        return partitions, suppl

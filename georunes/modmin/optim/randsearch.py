import numpy as np
from pandas import DataFrame
from georunes.modmin.optim.base import Optimizer, is_in_bounds, random_part_with_bounds, random_part_in_hypercube


class RandomSearch(Optimizer):

    def __init__(self, dist_func="euclidian", **kwargs):
        Optimizer.__init__(self, **kwargs)
        self.dist_func = dist_func
        self.notif = ">>>>>> Random research Method / deviation function : " + dist_func

    def _compute(self, raw_data, skip_cols, raw_minerals_data, to_round=4,
                 max_minerals=None, min_minerals=None, unfillable_partitions_allowed=True, ignore_oxides=None,
                 max_iter=1000000, limit_deviation=1e-03, search_semiedge=1, scale_semiedge=None,
                 starting_partition=None, force_totals=False, residual_in_suppl=False):

        if self.verbose > 1:
            print("Round digits :", to_round, " --  Maximum iterations :", max_iter, " --  Limit deviation:",
                  limit_deviation,
                  " --  Semiegde of hypercube research :", search_semiedge,
                  " --  Oxides to ignore : " + str(ignore_oxides) if ignore_oxides else "")
            if starting_partition: print("Starting partition :", starting_partition)

        self.prepare_data(raw_data, skip_cols, raw_minerals_data, ignore_oxides)
        partitions = DataFrame(columns=self.list_minerals)
        deviation_name = "deviation_" + self.dist_func
        suppl = DataFrame(columns=[deviation_name])
        bulk_chems = [0] * len(self.data.index)
        found_chems = [0] * len(self.data.index)

        if force_totals:
            if unfillable_partitions_allowed:
                raise Exception("The parameter force_totals is True. The parameter unfillable_partitions_allowed "
                                "should be set to False. Check the computing configuration.")
            target_totals = self.init_total
        else:
            target_totals = [100] * len(self.data.index)

        if not scale_semiedge or scale_semiedge < 0 or scale_semiedge > 1:
            if self.verbose > 0:
                print("WARNING : The scale must be superior to 0 and inferior or equals to 1. Value set to 1.")
            scale_semiedge = 1

        # Get maximum proportion for each mineral
        for i in self.data.index:
            if self.verbose: print(">>> Composition", i)
            list_minerals_i = self.list_minerals.copy()
            minerals_data_i = self.minerals_data.copy()
            bulk_chems[i] = self.data.iloc[i].to_numpy()
            search_semiedge_i = search_semiedge

            # Get maximum possible proportion for each mineral
            max_minerals_prop = []
            unnecessary_minerals = []
            #print("min prop ", list(max_oxides_prop), "\n", mineral_prop)  # todo code to check if values present in all lines of a table, if there are doublond
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
            if not unfillable_partitions_allowed and sum(max_minerals_prop) < 1.05:  # 5% tolerance
                raise Exception("Problem in composition " + str(i)
                                + ". The sum of the maximum proportions of minerals cannot complete to 100 "
                                  "(found " + str(100 * sum(max_minerals_prop)) + str(")."))

            if self.verbose and unnecessary_minerals:
                print("Unnecessary minerals :", *unnecessary_minerals)

            # Random calculation
            if self.verbose: print("Start calculations. Expected number of iterations :", max_iter)
            min_deviation = 1e10
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
                            val = starting_partition[key] / 100 if key in starting_partition.keys() else 0
                            candidate.append(val)
                        if not is_in_bounds(candidate, max_minerals_prop, min_minerals_prop):
                            print("WARNING : The starting partition does not respect the provided and calculated "
                                  "bounds data : Minerals ,", list_minerals_i, "Max ,", max_minerals_prop, "Min ,",
                                  min_minerals_prop, "The calculations will be started with a random composition.")
                            candidate = random_part_with_bounds(nb_minerals_i, max_minerals_prop, min_minerals_prop,
                                                                unfillable_partitions_allowed=unfillable_partitions_allowed,
                                                                verbose=self.verbose)
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
                if search_semiedge_i > 1:
                    raise Exception("The variable search_semiedge_i must be inferior or equal to 1.")
                elif search_semiedge_i < 1 and candidate:
                    new_candidate = random_part_in_hypercube(candidate, search_semiedge_i, max_minerals_prop,
                                                             min_minerals_prop, total=target_totals[i] / 100,
                                                             unfillable_partitions_allowed=unfillable_partitions_allowed,
                                                             verbose=self.verbose)
                    if set(new_candidate) == set(candidate) and search_semiedge_i < 1:
                        search_semiedge_i = search_semiedge_i * scale_semiedge
                        if search_semiedge_i < pow(10, -to_round):
                            if self.verbose: print(
                                "Updated semiedge is inferior to the rounding precision. Search ended")
                            break
                        if self.verbose > 0:
                            print("In iteration", k, ", search_semiedge_i changed to", search_semiedge_i)

                else:
                    new_candidate = random_part_with_bounds(nb_minerals_i, max_minerals_prop, min_minerals_prop,
                                                            total=target_totals[i] / 100,
                                                            unfillable_partitions_allowed=unfillable_partitions_allowed,
                                                            verbose=self.verbose)

                corresp_chem = np.dot(minerals_data_i, new_candidate).round(decimals=to_round)
                dist = self.deviation(bulk_chems[i], corresp_chem)
                if dist < min_deviation:
                    min_deviation = dist
                    candidate = new_candidate
                    if min_deviation < limit_deviation:
                        if self.verbose: print("Bottom deviation condition reached after iteration", k)
                        break
                    if self.verbose > 1:
                        print("Better solution at iteration", k)
                        print(dict(zip(list_minerals_i, candidate)))
                        print("New deviation :", min_deviation, "%" if self.dist_func == "SMAPE" else "")

                if self.verbose and k == max_iter - 1:
                    print("Max iterations reached")

            dict_res = {list_minerals_i[i]: round(candidate[i], to_round) for i in range(len(list_minerals_i))}

            idx_new_row = len(partitions)
            for miner, prop in dict_res.items():
                partitions.loc[idx_new_row, miner] = prop
            partitions = partitions.fillna(0)
            partitions.iloc[idx_new_row] = 100 * partitions.iloc[idx_new_row]
            partitions = partitions.round(to_round)

            deviation = self.deviation(bulk_chems[i], np.dot(self.minerals_data, partitions.iloc[idx_new_row] / 100))
            found_chems[i] = np.dot(self.minerals_data, partitions.loc[idx_new_row] / 100).round(to_round).tolist()
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

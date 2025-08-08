import numpy as np
from numpy import linalg
from random import random


def is_in_bounds(partition, max_minerals_prop, min_minerals_prop):
    if any(partition[i] > max_minerals_prop[i] or partition[i] < min_minerals_prop[i] for i in range(len(partition))):
        return False
    return True


def random_part_in_hypercube(current_part, semiedge, max_minerals_prop=None, min_minerals_prop=None, total=1,
                             unfillable_partitions_allowed=True, max_iter=100, verbose=0):
    nb_minerals = len(current_part)
    if not min_minerals_prop:
        min_minerals_prop = [0] * nb_minerals
    if not max_minerals_prop:
        max_minerals_prop = [1] * nb_minerals
    if len(max_minerals_prop) != nb_minerals or len(min_minerals_prop) != nb_minerals:
        raise Exception("Wrong dimensions for max or min mineral compositions")

    it = 0
    prop = random()  # A random factor to allow smaller steps during the research of new values
    while it < max_iter:
        it += 1
        if unfillable_partitions_allowed :
            dec = np.random.uniform(-semiedge * prop, semiedge * prop, nb_minerals)
        else :
            dec = np.random.uniform(-semiedge * prop, semiedge * prop, nb_minerals - 1)
            dec = np.append(dec, total - sum(current_part) - sum(dec))  # To make sure that sum(new_partition) = total
        new_partition = [current_part[i] + dec[i] for i in range(nb_minerals)]
        if is_in_bounds(new_partition, max_minerals_prop, min_minerals_prop):
            # The new composition is found
            return new_partition

        if verbose > 1 and it == max_iter:
            print("WARNING : Maximum iteration reached in the research of a random composition.")

    return current_part


def random_part_with_bounds(nb_minerals, max_minerals_prop=None, min_minerals_prop=None, total=1,
                            unfillable_partitions_allowed=False, verbose=0, ):
    if not min_minerals_prop:
        min_minerals_prop = [0] * nb_minerals
    if not max_minerals_prop:
        max_minerals_prop = [1] * nb_minerals

    if len(max_minerals_prop) != nb_minerals or len(min_minerals_prop) != nb_minerals:
        raise Exception("Wrong dimensions for max or min mineral compositions")

    # Loop
    found = False
    k = 0
    while not found:
        k += 1
        new_partition = []
        for i in range(nb_minerals):
            new_partition.append(min_minerals_prop[i] + (max_minerals_prop[i] - min_minerals_prop[i]) * random())
        new_total = sum(new_partition)
        found = True
        if new_total > total:
            new_partition = [i * total / new_total for i in new_partition]
            # Check if minima conditions are respected
            for j in range(nb_minerals):
                if new_partition[j] < min_minerals_prop[j]:
                    found = False
                    break
        elif not unfillable_partitions_allowed:
            new_partition = [i * total / new_total for i in new_partition]
            for j in range(nb_minerals):
                if new_partition[j] > max_minerals_prop[j]:
                    found = False
                    break
        else:  # if unfillable partitions are authorized, nothing to do.
            # From its definition, new_partition respects the maxima and minima conditions
            pass
        if k > 1000:
            raise Exception("The algorithm struggles to find a coherent random partition. Please check the entry data.")
    if verbose > 2:
        print("Partition found after", k, "iterations.")

    return new_partition


def random_part(nb_minerals, verbose=0):
    return random_part_with_bounds(nb_minerals, verbose=verbose)


class BaseOptimizer:
    def __init__(self, verbose=None):
        if isinstance(verbose, (int, bool)):
            self.verbose = int(verbose)
        else:
            self.verbose = 0

    def deviation(self, part_a, part_b):
        if self.dist_func in ("euclidian", "L2-norm"):
            dist = np.linalg.norm(part_a - part_b)
        elif self.dist_func == "max":
            dist = np.linalg.norm(part_a - part_b, ord=np.inf)
        elif self.dist_func == "min":
            dist = np.linalg.norm(part_a - part_b, ord=-np.inf)
        elif self.dist_func == "MAE":  # Mean absolute error
            dist = np.absolute(part_a - part_b).mean()
        elif self.dist_func == "MSE":  # Mean square error
            dist = np.square(part_a - part_b).mean()
        elif self.dist_func == "RMSE":  # Root mean square error
            dist = np.sqrt(np.square(part_a - part_b).mean())
        elif self.dist_func == "SMAPE":  # Symmetric mean absolute percentage error
            sum_abs_a_b = np.abs(part_a) + np.abs(part_b)
            terms = np.divide(2 * np.abs(part_a - part_b), sum_abs_a_b, out=np.zeros_like(part_a),
                              where=sum_abs_a_b != 0)  # Put division to 0 when A = B = 0
            dist = 100 * terms.mean()
        else:
            raise Exception("Unknown parameter for distance function.")
        return dist


class Optimizer(BaseOptimizer):
    def __init__(self, **kwargs):
        BaseOptimizer.__init__(self, **kwargs)
        # self.norm defined in children classes

    def prepare_data(self, raw_data, skip_cols, raw_minerals_data, ignore_oxides):
        raw_data = raw_data.fillna(0)
        if 'Sum' in raw_data.keys():
            raw_data = raw_data.rename(columns={'Sum': 'Total'})
        if 'Total' in raw_data.keys():
            self.init_total = raw_data["Total"]
        else:
            raise Exception("Total column not found.")

        if ignore_oxides:
            el_ox_to_drop = [*ignore_oxides, 'Total']
        else:
            el_ox_to_drop = ['Total', ]

        for ox in el_ox_to_drop:
            if ox in raw_minerals_data.keys():
                raw_minerals_data = raw_minerals_data.drop(columns=ox)
            if ox in raw_data.keys():
                raw_data = raw_data.drop(columns=ox)

        raw_minerals_data = raw_minerals_data.fillna(0)
        raw_minerals_data = raw_minerals_data.set_index(raw_minerals_data.keys()[0])
        self.data = raw_data.iloc[:, skip_cols:].copy()
        self.list_bulk_ox = self.data.keys().tolist()
        raw_minerals_data = raw_minerals_data[[*list(self.list_bulk_ox)]]  # Order oxides as in source
        self.minerals_data = raw_minerals_data.transpose()
        self.list_minerals = self.minerals_data.keys().tolist()
        self.nb_minerals = len(self.list_minerals)

    def compute(self, raw_data, skip_cols, raw_minerals_data, to_round=4, ignore_oxides=None, ratios=None, **kwargs):
        if self.verbose:
            print(self.notif)

        if ratios:
            notif_cfg = ""
            rmd_t = raw_minerals_data.transpose()
            rmd_t.columns = rmd_t.iloc[0]
            df_t = rmd_t[1:].copy()
            for sol, cfg in ratios.items():
                if len(cfg) != 2:
                    print("WARNING : Incorrect configuration for the solution :", sol)
                elif len(cfg[0]) != len(cfg[1]):
                    print("WARNING : Missing data in the solution :", sol)
                else:
                    mins, parts = cfg[0], cfg[1]
                    if notif_cfg:
                        notif_cfg += " / " + str([mins, parts, ])
                    else:
                        notif_cfg += str([mins, parts, ])

                    # Calculation of mineral solutions and replacement in minerals_data
                    tot = sum(parts)
                    for miner, pa in zip(mins, parts):
                        df_t[miner] = df_t[miner] * pa / tot
                    df_t[sol] = df_t[mins].sum(axis=1)
                    df_t = df_t.drop(columns=mins)

            if self.verbose and len(notif_cfg) > 0:
                print("Considered mineral solutions :", notif_cfg)

                # Reset dataframe as raw table
                sub_data = df_t.transpose()
                sub_data.reset_index(drop=False, inplace=True)

                # Compute partitions
                partitions, suppl = self._compute(raw_data, skip_cols, sub_data, to_round=to_round,
                                                  ignore_oxides=ignore_oxides, **kwargs)

                # Component reconstitution
                for sol, cfg in ratios.items():
                    mins, parts = cfg[0], cfg[1]
                    tot = sum(parts)
                    suppl[sol] = partitions[sol]
                    for miner, pa in zip(mins, parts):
                        partitions[miner] = partitions[sol] * pa / tot
                    partitions = partitions.drop(columns=sol, axis=1)
                # Move Total to the last column
                cols = partitions.columns.tolist()
                cols.remove("Total")
                cols.append("Total")
                partitions = partitions[cols]
            else:
                partitions, suppl = self._compute(raw_data, skip_cols, raw_minerals_data, to_round=to_round,
                                                  ignore_oxides=ignore_oxides, **kwargs)

        else:
            partitions, suppl = self._compute(raw_data, skip_cols, raw_minerals_data, to_round=to_round,
                                              ignore_oxides=ignore_oxides, **kwargs)

        if self.verbose:
            self.show_results(partitions, suppl)

        return partitions, suppl

    @staticmethod
    def show_results(partitions, suppl):
        print(">>> Final compositions (wt %)")
        print(partitions.to_string())
        print(">>> Supplementary data")
        print(suppl.to_string())

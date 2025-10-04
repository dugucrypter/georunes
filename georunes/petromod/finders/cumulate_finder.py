import warnings
import pandas as pd
from georunes.modmin.optim.bvls import BVLS
from georunes.modmin.optim.gd import GradientDescent
from georunes.modmin.optim.nnls import NNLS
from georunes.modmin.optim.randsearch import RandomSearch
from georunes.tools.data import linspace_to_end, round_floor_n_digits
from georunes.tools.filemanager import FileManager
from georunes.tools.warnings import FunctionParameterWarning

filemanager = FileManager.get_instance()


def create_cumulate_finder_from_file(source, sheet_name, *args, **kwargs):
    raw_minerals_data = filemanager.read_file(source, sheet_name)
    return CumulateFinder(raw_minerals_data, *args, **kwargs)


class CumulateFinder:
    def __init__(self, raw_minerals_data, ignore_oxels=None, optimizer='BVLS', norm='euclidian', nb_results=5, verbose=0):
        self.ignore_oxels = ignore_oxels
        self.prepare_data(raw_minerals_data)
        self.nb_results = nb_results
        if optimizer in ('BVLS', 'NNLS') and norm != 'euclidian' :
            warnings.warn("BVLS and NNLS are specialized for euclidian norm. Distance function set to euclidian norm.", FunctionParameterWarning)
            norm = 'euclidian'
        self.optimizer = optimizer
        if self.optimizer == "BVLS":
            self.opt = BVLS(verbose=verbose)
        elif self.optimizer == "NNLS":
            self.opt = NNLS(verbose=verbose)
        elif self.optimizer == "RS":
            self.opt = RandomSearch(verbose=verbose, dist_func=norm)
        elif self.optimizer == "GD":
            self.opt = GradientDescent(verbose=verbose, dist_func=norm, filling_tolerance=0.01)

    def filter_oxels(self, comp, verbose=1):
        removed = []
        # list_keys = list()
        for elox in comp.keys():
            if elox not in self.oxel_list:
                del comp[elox]

        if len(removed) and verbose:
            print("Removed the oxels " + str(removed) + "from a composition.")

    def prepare_data(self, raw_minerals_data):
        if self.ignore_oxels:
            for ox in raw_minerals_data.columns.tolist()[1:]:
                if ox in self.ignore_oxels:
                    raw_minerals_data = raw_minerals_data.drop(columns=ox)
        raw_minerals_data = raw_minerals_data.fillna(0)
        raw_minerals_data = raw_minerals_data[(raw_minerals_data.iloc[:, 1:] != 0).any(axis=1)]
        self.raw_minerals_data = raw_minerals_data  # For optimization, index not needed
        raw_minerals_data = raw_minerals_data.set_index(raw_minerals_data.keys()[0])

        self.oxel_list = raw_minerals_data.columns.tolist()
        raw_minerals_data = raw_minerals_data[[*list(self.oxel_list)]]  # Order oxides as in source
        self.minerals_data = raw_minerals_data.transpose()
        self.list_minerals = self.minerals_data.keys().tolist()
        self.nb_minerals = len(self.list_minerals)

    def compute_beta_limit_removal(self, parent, child):
        div = parent / child
        self.max_beta = div.min()

    def find_cumulate_to_remove(self, parent_comp, child_comp, verbose=0):
        self.filter_oxels(parent_comp)
        self.filter_oxels(child_comp)
        data = pd.DataFrame(index=self.oxel_list, )
        self.compute_beta_limit_removal(parent_comp, child_comp)
        fracts_list = linspace_to_end(round_floor_n_digits(self.max_beta, 3), self.nb_results)[::-1]
        for beta in linspace_to_end(round_floor_n_digits(self.max_beta, 3), self.nb_results)[::-1]:
            x_df = self.get_cumulate_comp(parent_comp, child_comp, beta)
            data['alpha_' + str(round(1 - beta, 3))] = x_df

        data = data.T
        data = data.reset_index()
        data.rename(columns={'index': 'Sample'}, inplace=True)
        data['Total'] = data.iloc[:, 1:].sum(axis=1)

        p,s = None,None
        if self.optimizer in ("BVLS", "NNLS"):
            p, s = self.opt.compute(data, skip_cols=1, raw_minerals_data=self.raw_minerals_data)
        elif self.optimizer == 'RS':
            p, s = self.opt.compute(data, skip_cols=1, raw_minerals_data=self.raw_minerals_data,
                                    max_iter=100000, search_semiedge=0.2, scale_semiedge=0.75, force_totals=False,
                                    unfillable_partitions_allowed=True)  #
        elif self.optimizer == 'GD':
            self.opt.set_verbose(2)
            p, s = self.opt.compute(data, skip_cols=1, raw_minerals_data=self.raw_minerals_data,
                                    max_iter=10000, learn_rate=0.0001, force_totals=False)
        proportions, supplements = p, s

        return proportions, supplements, fracts_list

    @staticmethod
    def get_cumulate_comp(parent, child, beta):
        x_df = (parent - beta * child) / (1 - beta)
        return x_df

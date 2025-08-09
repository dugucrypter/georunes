from georunes.tools.filemanager import FileManager

filemanager = FileManager.get_instance()


class MassBalanceModalModeler:
    def __init__(self, data_minerals, ignore_oxides=None):
        raw_minerals_data = data_minerals
        self.ignore_oxels = ignore_oxides
        self.prepare_data(raw_minerals_data)
        self.modeler_name = "Mass balance modeler"
        self.init_name = 'Parental concentrations'

    def filter_elements(self, comp, verbose=1):
        removed = []
        for oxel in comp.keys():
            if oxel not in self.oxel_list:
                del comp[oxel]

        if len(removed) and verbose:
            print("Removed the oxels " + str(removed) + "from a composition.")

    def prepare_data(self, raw_minerals_data):

        if self.ignore_oxels:
            for ox in raw_minerals_data.columns.tolist()[1:]:
                if ox in self.ignore_oxels:
                    raw_minerals_data = raw_minerals_data.drop(columns=ox)
        raw_minerals_data = raw_minerals_data.fillna(0)

        # Remove row if all values are zeros
        raw_minerals_data = raw_minerals_data[(raw_minerals_data.iloc[:, 1:] != 0).any(axis=1)]
        self.raw_minerals_data = raw_minerals_data  # For optimization, index not needed
        raw_minerals_data = raw_minerals_data.set_index(raw_minerals_data.keys()[0])
        self.oxel_list = raw_minerals_data.columns.tolist()
        raw_minerals_data = raw_minerals_data[[*list(self.oxel_list)]]  # Order oxides as in source

        self.minerals_data = raw_minerals_data.transpose()
        self.default_minerals_data = raw_minerals_data.transpose()
        self.list_minerals = self.minerals_data.keys().tolist()
        self.nb_minerals = len(self.list_minerals)

    def get_elements_list(self):
        return self.minerals_data.index.tolist()

    def get_minerals_list(self):
        return self.minerals_data.columns

    def modal_props_to_concentration(self, modal_props):
        conc = dict()
        for oxel in self.oxel_list:
            sum_oxel = 0
            for mineral, fract in modal_props.items():
                sum_oxel += self.minerals_data[mineral][oxel] * fract
            conc[oxel] = sum_oxel / 100
        return conc

    def get_residual_liq_concentration(self, oxel, modal_cumulate, parent_conc, alpha_list):
        """
        Get the concentration of residual liquid for a list of alpha values (proportion of liquid)
        :param oxel: the oxide or the element (string)
        :param modal_cumulate: the modal mineral composition of the cumulate (dict)
        :param parent_conc: the concentrations of the parental melt (dict)
        :param alpha_list: the liquid proportions (list)
        :return: a list of the specified oxide/element concentration according to the liquid proportion
        """

        cumulate = self.modal_props_to_concentration(modal_cumulate)
        res = [(parent_conc[oxel] - alpha * cumulate[oxel]) / (1 - alpha) for alpha in alpha_list]
        return res

    def assimilate(self, parent, content, intake_ratio):
        """
        Calculate the assimilation of a content by a parental melt
        :param parent: the concentrations of the parental melt (dict)
        :param content: the concentrations of the assimilated component (dict)
        :param intake_ratio: the mass ratio of the assimilated content to the parental melt (float)
        :return: the concentrations of the mixed product (dict)
        """

    def set_minerals_data(self, minerals_data):
        self.minerals_data = minerals_data

    def reset_minerals_data(self):
        self.minerals_data = self.default_minerals_data.copy()

    @staticmethod
    def compute_alpha_limit_removal(parent, cumulate):
        div = parent / cumulate
        min_alpha = div.min()
        return min_alpha

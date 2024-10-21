import warnings
import pandas as pd
from georunes.tools.preprocessing import check_geochem_res

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

eml = pkg_resources.files('georunes.data').joinpath('reservoirs.csv')


# Singleton model, from github.com/pazdera/1098129
class Reservoirs:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Reservoirs.__instance is None:
            Reservoirs()
        return Reservoirs.__instance

    def __init__(self, source=eml):
        """ Virtually private constructor. """
        if Reservoirs.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Reservoirs.__instance = self

        data = pd.read_csv(source, )
        data.set_index("alias")
        self.model_list = list(data.loc[:, "alias"])
        self.compos = {}
        for model in self.model_list:
            self.compos[model] = data.loc[data['alias'] == model].squeeze()  # Convert to a Series

    def get_models_list(self):
        return self.model_list if self.model_list else None

    def get_label(self, model):
        return self.compos[model]["reservoir"]

    def get_color(self, model):
        return self.compos[model]["color"]

    def get_chondrite_compo(self, element):
        return self.compos['CI'][element]

    def register_model(self, model):
        alias = model['alias']
        self.model_list.append(alias)

        d = {}
        for el, val in model.items():
            if el != 'alias':
                d[el] = val

        self.compos[alias] = pd.Series(d)

        return self.compos[alias]


def chondrite_val(element):
    res = Reservoirs.get_instance()
    return res.get_chondrite_compo(element)


def get_reservoir_norm(norm_slug, default="CI"):
    res = Reservoirs.get_instance()
    if isinstance(norm_slug, dict) and check_geochem_res(norm_slug):
        norm = res.register_model(norm_slug)
    elif norm_slug in res.model_list:
        norm = res.compos[norm_slug]
    else:
        if norm_slug is not None:
            msg = "The data of reservoir " + norm_slug + " are not found. Check the figure configuration."
            warnings.warn(msg)
        norm = res.compos[default]
    return norm

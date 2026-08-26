import warnings
from pathlib import Path
import numpy as np
import pandas as pd


# Singleton model, from github.com/pazdera/1098129
class FileManager:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if FileManager.__instance is None:
            FileManager()
        return FileManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if FileManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            FileManager.__instance = self

        self.files = []
        self.datas = dict()

    def read_file(self, datasource, sheet_name=None, sep=",", delimiter=None, index=None):
        fext = Path(datasource).suffix

        if fext in (".xls", ".xlsx") and sheet_name == 0:
            warnings.warn("No sheet name specified, the first sheet of the Excel file will be used.")

        ref_end = '_' + str(sheet_name) if sheet_name and sheet_name != 0 else ''
        ref = str(datasource) + ref_end
        if ref in self.files:  # Check if already loaded
            return self.datas[ref]
        else:
            if fext in (".xls", ".xlsx"):
                data = pd.read_excel(datasource, sheet_name=sheet_name, index_col=index)
                # If multiples sheets in excel file and the sheet name is not provided, the first one will be taken.
                if isinstance(data, dict):
                    data = next(iter(data.items()))[1]
            elif fext in (".csv", ".txt"):
                data = pd.read_csv(datasource, sep=sep, delimiter=delimiter, index_col=index)
            else:
                msg = "Extension file " + fext + " not recognized."
                raise Exception(msg)

            if not data.empty:
                self.files.append(ref)

                # Preprocess
                data = data.replace('bdl', np.nan)

                self.datas[ref] = data
                print(ref + " data loaded.")
                return data


def load_subdata(datasource, filters=None, sheet=0):
    """
    Load data using GeoRUnes FileManager and filter rows.

    Parameters
    ----------
    datasource : str
        Path to the data file.

    filters : dict, optional
        Column/value filters. Values can be single values or lists.
        Multiple columns are combined with AND.
        Multiple values within a column are combined with OR.

    sheet : int or str, default 0
        Excel sheet index or name.

    Returns
    -------
    pandas.DataFrame
        Filtered dataframe.
    """

    data = FileManager.get_instance().read_file(datasource, sheet_name=sheet)
    if not filters:
        return data.copy()
    mask = True

    for column, values in filters.items():
        if column not in data.columns:
            raise KeyError(f"Column '{column}' not found in datasource.")
        if not isinstance(values, (list, tuple, set)):
            values = [values]
        mask &= data[column].isin(values)

    return data.loc[mask].copy()

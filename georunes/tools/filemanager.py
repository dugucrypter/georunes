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
            elif fext in (".csv", ".txt"):
                data = pd.read_csv(datasource, sep, delimiter, index_col=index)
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

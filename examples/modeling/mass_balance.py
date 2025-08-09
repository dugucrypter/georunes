import os

from georunes.petromod.modelers.mass_balance import MassBalanceModalModeler
from georunes.petromod.modelers.partition import initial_concentration_as_series
from georunes.petromod.viewer.tk.mass_balance_viewer import MassBalanceViewerTk
from georunes.tools.filemanager import FileManager

filemanager = FileManager.get_instance()

directory = os.path.dirname(os.path.realpath("mass_balance_dat.xlsx"))
data_minerals = filemanager.read_file(os.path.join(directory, "mass_balance_dat.xlsx"), 'Minerals')

list_oxides = ["SiO2", "Al2O3", "Fe2O3", "MgO", "CaO", "Na2O", "K2O", "TiO2", "MnO"]
_parental_magma_conc = [52.83, 16.69, 8.39, 9.74, 8.15, 3.24, 0.26, 0.83, 0.17]
_child_conc = [54.67, 16.73, 7.20, 7.64, 7.88, 3.52, 0.52, 0.79, 0.13]
parental_magma_conc = initial_concentration_as_series(list_oxides, _parental_magma_conc)
child = initial_concentration_as_series(list_oxides, _child_conc)

mb_model = MassBalanceModalModeler(data_minerals=data_minerals)

view = MassBalanceViewerTk(mb_model, parent_conc=parental_magma_conc, child_conc=child, verbose=1)
view.draw()
view.loop()

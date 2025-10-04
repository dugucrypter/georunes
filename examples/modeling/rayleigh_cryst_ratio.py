import os
from georunes.petromod.modelers.partition import initial_concentration_as_series, compute_bulk_coeffs
from georunes.petromod.modelers.rayleigh import RayleighCrystallization
from georunes.petromod.viewer.tk.fract_viewer import FractViewerTk
from georunes.tools.data import linspace
from georunes.tools.filemanager import FileManager


filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("model_db.xlsx"))
source = os.path.join(directory, "model_db.xlsx")

coeffs = filemanager.read_file(source, 'Hulsboschetal2014', index='Element')
starting_material = {'Quartz': 22, 'Plagioclase': 37.9, 'Zircon': 0.1, 'Alk-feldspar': 17.1, "Monazite": 0.1,
                     "Muscovite": 16.7, 'Tourmaline': 6.1}
bulk_coeffs = compute_bulk_coeffs(starting_material, coeffs)

rees = ["La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Dy", "Ho", "Er", "Yb", "Lu"]
rees_c0 = [12, 26, 4, 14.7, 3.5, 0.4, 3.1, 2.7, 0.5, 1.3, 1.1, 0.1]

initial_conc0 = initial_concentration_as_series(rees, rees_c0)
fract_values = linspace(0, 1, 20 + 1, )
rayleigh_model = RayleighCrystallization(bulk_coeffs)

ratio_viewer = FractViewerTk(rayleigh_model, solid_comp=starting_material, data_coeffs=coeffs,
                             initial_conc=initial_conc0,
                             liq_fract_values=fract_values, verbose=1)
ratio_viewer.draw()
ratio_viewer.loop()

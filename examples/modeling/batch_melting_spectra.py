import os
from georunes.petromod.modelers.batch import BatchMelting
from georunes.petromod.modelers.partition import initial_concentration_as_series, compute_bulk_coeffs
from georunes.petromod.viewer.tk.spider_viewer import SpiderViewerTk
from georunes.tools.data import linspace
from georunes.tools.filemanager import FileManager

filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("model_db.xlsx"))
source = os.path.join(directory, "model_db.xlsx")

coeffs = filemanager.read_file(source, 'ReichardtWeinberg2012', index='Element')
starting_material = {'Plagioclase': 35, "K-feldspar": 5, "Quartz": 7.5, "Hornblende": 25, "Biotite": 25,
                     "Titanite": 1.5, "Allanite": 0.4, "Apatite": 0.4, "Zircon": 0.2}
bulk_coeffs = compute_bulk_coeffs(starting_material, coeffs)

rees = ["La", "Ce", "Nd", "Sm", "Eu", "Gd", "Dy", "Er", "Yb", "Lu"]
rees_c0 = [49.825, 87.19, 32.408, 5.535, 1.378, 4.435, 3.555, 1.815, 1.693, 0.26]

initial_conc0 = initial_concentration_as_series(rees, rees_c0)
fract_values = linspace(0, 1, 20 + 1, )
batch_model = BatchMelting(bulk_coeffs)

batch_spectra_viewer = SpiderViewerTk(batch_model, solid_comp=starting_material, data_coeffs=coeffs,
                                      initial_conc=initial_conc0,
                                      liq_fract_values=fract_values, verbose=1)
batch_spectra_viewer.draw()
batch_spectra_viewer.loop()

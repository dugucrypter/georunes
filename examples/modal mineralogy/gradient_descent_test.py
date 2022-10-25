import os
from georunes.tools.filemanager import FileManager
from georunes.modmin.optim.gd import GradientDescent

filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("modalmin_test.csv"))
source_comp = os.path.join(directory, "modalmin_test.csv")
source_minerals = os.path.join(directory, "minerals.csv")
data = filemanager.read_file(source_comp)
minerals = filemanager.read_file(source_minerals)

gd = GradientDescent(verbose=2, dist_func="SMAPE")  # SMAPE = Symmetric mean absolute percentage error

# A starting composition used for the gradient descent method
starting_partition = {
    "Albite": 25,
    "Anorthite": 10,
    "Quartz": 28.999,
    "Hematite": 2,
    "Biotite": 6,
    "Muscovite": 8,
    "Orthoclase": 20,
    'Apatite-F': 0.001,
}

p, s = gd.compute(data, skip_cols=1, raw_minerals_data=minerals,
                  max_iter=100000, learn_rate=0.0001, starting_partition=starting_partition, force_totals=True)

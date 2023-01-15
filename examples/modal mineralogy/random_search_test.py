import os
from georunes.tools.filemanager import FileManager
from georunes.modmin.optim.randsearch import RandomSearch

filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("modalmin_test.csv"))
source_comp = os.path.join(directory, "modalmin_test.csv")
source_minerals = os.path.join(directory, "minerals.csv")
data = filemanager.read_file(source_comp)
minerals = filemanager.read_file(source_minerals)

rs = RandomSearch(verbose=1, dist_func='MAE')  # MAE = Mean absolute error
ratios = {"Plagioclase": [["Albite", "Anorthite"],
                          [76, 24]], }  # Define plagioclase as weigh proportions of 76% albite and 24% anorthite

# Optimize solution by checking random compositions in a defined hypercube. When no new random solution can be found
# (because of bound limits), the hypercube is reduced by multiplying the semi-edge with the parameter 'scale_semiedge'
p, s = rs.compute(data, skip_cols=1, raw_minerals_data=minerals, ratios=ratios,
                  max_iter=100000, search_semiedge=0.1, scale_semiedge=0.5, force_totals=True)

import os
from georunes.tools.filemanager import FileManager
from georunes.modmin.optim.bvls import BVLS
from georunes.modmin.optim.nnls import NNLS

filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("modalmin_test.csv"))
source_comp = os.path.join(directory, "modalmin_test.csv")
source_minerals = os.path.join(directory, "minerals.csv")
data = filemanager.read_file(source_comp)
minerals = filemanager.read_file(source_minerals)

bvls = BVLS(verbose=1)  # Bounded-variable least squares
nnls = NNLS(verbose=1)  # Non negative least squares

p1, s1 = bvls.compute(data, skip_cols=1, raw_minerals_data=minerals)
print("\n\n")
p2, s2 = nnls.compute(data, skip_cols=1, raw_minerals_data=minerals)

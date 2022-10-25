import os
from georunes.modmin.norm.cipw import CIPWNorm
from georunes.tools.filemanager import FileManager

filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("cipw_test.csv"))
source = os.path.join(directory, "cipw_test.csv")
data = filemanager.read_file(source)

cipw = CIPWNorm(verbose=1)
p, s = cipw.compute(data, skip_cols=1, minor_included=True, co2_calcite=0.8, co2_cancrinite=0.2)

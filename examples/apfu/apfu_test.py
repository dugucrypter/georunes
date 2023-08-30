import os

from georunes.modmin.struct.apfu import APFUCalc
from georunes.tools.filemanager import FileManager

filemanager = FileManager.get_instance()
directory = os.path.dirname(os.path.realpath("micas.csv"))
source_micas = os.path.join(directory, "micas.csv")
source_fsp = os.path.join(directory, "feldspars.csv")
data_micas = filemanager.read_file(source_micas)
data_fsp = filemanager.read_file(source_fsp)

apfu = APFUCalc(verbose=2,)

p_micas, s_micas = apfu.compute_oxygen_basis(data_micas, skip_cols=1, oxygen_number=12, oxygen_equiv=True)
p_fsp, s_fsp = apfu.compute_cation_basis(data_fsp, skip_cols=1, oxygen_number=8, force_cation_number=5)

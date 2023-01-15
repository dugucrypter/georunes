import os
import matplotlib.pyplot as plt
from georunes.plot.binary.versus import DiagramVs
from georunes.tools.preprocessing import populate_file, populate_file_with_config
from georunes.tools.language import format_chemical_formula as _fml

# Source file
directory = os.path.dirname(os.path.realpath("WAC_granitoids.csv"))
source = os.path.join(directory, "WAC_granitoids.csv")

# Attribute default colors (cmap) and and markers to the categories defined by 'group_name' parameter
populate_file(source, group_name='Lithology', output_suffix="_pop1", cmap='jet')

file1 = os.path.join(directory, "WAC_granitoids_pop1.csv")
test1 = DiagramVs(datasource=file1,
                  window_title="Test 1: 'WAC_granitoids_pop1.csv'",
                  xlabel=_fml("K2O"), ylabel=_fml("Na2O"),
                  group_name='Lithology',
                  xvar="K2O", yvar="Na2O",
                  legend_ncol=4,
                  )
test1.plot()

# Attribute a specific configuration of colors, markers, ... to the categories defined by 'group_name' parameter
cfg = {"group": ['Granite', 'Granodiorite', 'Monzonite', 'Trondhjemite'],
       "color": ['#ff5400', 'tab:green', '#ff0054', 'mediumblue'],
       "marker": ["o", "s", "^", "*"],
       "label": 'auto'
       }

populate_file_with_config(source, cfg, group_name='Lithology', output_suffix="_pop2")

file2 = os.path.join(directory, "WAC_granitoids_pop2.csv")
test2 = DiagramVs(datasource=file2,
                  window_title="Test 2: 'WAC_granitoids_pop2.csv'",
                  xlabel=_fml("K2O"), ylabel=_fml("Na2O"),
                  group_name='Lithology',
                  xvar="K2O", yvar="Na2O",
                  legend_ncol=4,
                  )
test2.plot()

plt.show()

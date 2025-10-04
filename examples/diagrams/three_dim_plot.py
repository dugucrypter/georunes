import os
import matplotlib.pyplot as plt
from georunes.plot.threed.scatter_3d import DiagramScatter3D

directory = os.path.dirname(os.path.realpath("WAC_granitoids_comp.xls"))
source = os.path.join(directory, "WAC_granitoids_comp.xls")
sheet = 'ggtest'

knaca = DiagramScatter3D(datasource=source,
                         sheet=sheet,
                         group_name='Lithology',
                         xvar='K2O', yvar='Na2O', zvar='CaO',
                         legend_ncol=4,
                         )

femgti = DiagramScatter3D(datasource=source, sheet=sheet,
                          group_name='Lithology',
                          xvar='Fe2O3t', yvar='MgO', zvar='TiO2',
                          annotation='Sample',
                          legend_ncol=4,
                          )


knaca.plot()
femgti.plot()

plt.show()

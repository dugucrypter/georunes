import os
import matplotlib.pyplot as plt
from georunes.ternary.anabor import DiagramAnAbOr
from georunes.ternary.jensen import DiagramJensen
from georunes.ternary.qap import DiagramQAP

# 'WAC_granitoids_pop2.csv' is created from WAC_granitoids.csv in the script preprocess_files.py
directory = os.path.dirname(os.path.realpath("WAC_granitoids_pop2.csv"))
source = os.path.join(directory, "WAC_granitoids_pop2.csv")
sheet = 'ggtest'

jensen = DiagramJensen(datasource=source, sheet=sheet,
                       group_name='Lithology',
                       legend_ncol=2,
                       alpha_color=0.8
                       )

qap = DiagramQAP(datasource=source, sheet=sheet,
                 group_name='Lithology',
                 legend_ncol=2,
                 alpha_color=0.8
                 )

barker = DiagramAnAbOr(datasource=source, sheet=sheet,
                       group_name='Lithology',
                       legend_ncol=2,
                       alpha_color=0.8,
                       )

jensen.plot()
qap.plot()
barker.plot()

plt.show()

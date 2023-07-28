import os
import matplotlib.pyplot as plt

from georunes.plot.piper.piper_diag import DiagramPiper
from georunes.plot.ternary.anabor import DiagramAnAbOr
from georunes.plot.ternary.jensen import DiagramJensen
from georunes.plot.ternary.qap import DiagramQAP

# 'WAC_granitoids_pop2.csv' is created from WAC_granitoids.csv in the script preprocess_files.py
directory = os.path.dirname(os.path.realpath("WAC_granitoids_pop2.csv"))
source = os.path.join(directory, "WAC_granitoids_pop2.csv")
sheet = 'ggtest'

jensen = DiagramJensen(datasource=source, sheet=sheet,
                       group_name='Lithology',
                        no_title=True,
                       legend_ncol=2,
                       alpha_color=0.8
                       )

qap = DiagramQAP(datasource=source, sheet=sheet,
                 group_name='Lithology',
                        no_title=True,
                 legend_ncol=2,
                 alpha_color=0.8
                 )

barker = DiagramAnAbOr(datasource=source, sheet=sheet,
                       group_name='Lithology',
                        no_title=True,
                       legend_ncol=2,
                       alpha_color=0.8,
                       )

# He, S., & Li, P. (2020). A MATLAB based graphical user interface (GUI) for quickly producing widely used
# hydrogeochemical diagrams. Geochemistry, 80(4), 125550.
source_piper = os.path.join(directory, "PiperHeLi2020.csv")
piper = DiagramPiper(datasource=source_piper,
                     delta=0.15,
                     )

jensen.plot()
qap.plot()
barker.plot()
piper.plot()

plt.show()

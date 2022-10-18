import os
import matplotlib.pyplot as plt
from georunes.binary.ratiosversus import DiagramRatiosVs
from georunes.binary.sialkali import DiagramSiAlkali
from georunes.binary.versus import DiagramVs
from georunes.tools.language import format_chemical_formula
from georunes.binary.pearce import DiagramPearceRYN

directory = os.path.dirname(os.path.realpath("WAC_granitoids_comp.xls"))
source = os.path.join(directory, "WAC_granitoids_comp.xls")
sheet = 'ggtest'

cox = DiagramSiAlkali(datasource=source,
                      sheet=sheet,
                      group_name='Lithology',
                      decor_set='Cox',
                      legend_ncol=4,
                      )

ntzh = DiagramRatiosVs(datasource=source, sheet=sheet,
                       xnum="Zr", xdenom="Hf", ynum="Nb", ydenom="Ta",
                       group_name='Lithology',
                       markersize={'var_scale': 'Nb', 'val_max': 20, 'val_min': 0.5},
                       annotation='Sample',
                       legend_ncol=4,
                       )

_fml = format_chemical_formula
femg = DiagramVs(datasource=source,
                 sheet=sheet,
                 xlim=(0, 12), ylim=(0, 7),
                 group_name='Lithology',
                 xvar="Fe2O3t", yvar="MgO",
                 xlabel=_fml("Fe2O3t"), ylabel=_fml("MgO"),
                 fontsize=16,
                 arrows=[[[7.6, 3.86], [2.73, 0.94]], ],
                 legend_in_axs=True,
                 legend_loc='lower right',
                 padding={"bottom": 0.14},
                 )

pearce_rynb = DiagramPearceRYN(datasource=source,
                               sheet=sheet,
                               group_name='Lithology',
                               legend_ncol=4,
                               padding={"bottom":0.17}
)

cox.plot()
ntzh.plot()
femg.plot()
pearce_rynb.plot()

plt.show()

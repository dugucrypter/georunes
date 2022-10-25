import os
import matplotlib.pyplot as plt
from georunes.plot.spider import DiagramSpider

# 'WAC_granitoids_pop2.csv' is created from WAC_granitoids.csv in the script preprocess_files.py
directory = os.path.dirname(os.path.realpath("WAC_granitoids_pop2.csv"))
source = os.path.join(directory, "WAC_granitoids_pop2.csv")

ree_chond = DiagramSpider(datasource=source,
                          window_title="REE normalized to chondrites (McDonough and Sun 1995)",
                          group_name='Lithology',
                          fillmode="enclosed-lines",
                          exclude_groups=('Trondhjemite', 'Monzonite'),
                          # no_legend=True,
                          show_reservoirs=['NMORB', 'CCRUST'],
                          h_ratio=[6.4, 4],
                          legend_ncol=2,
                          )

listing = ["Rb", "Ba", "Th", "U", "K", "Nb", "Ta", "La", "Sr", "Zr", "Hf", "Sm", "Gd", "Ti", "Dy", "Y", "Er"]
elts_crust = DiagramSpider(datasource=source,
                           window_title="Spider diagram normalized to bulk continental crust (Rudnick and Gao 2003)",
                           group_name='Lithology',
                           listing=listing,
                           markersize=4,
                           fillmode="marked-lines",
                           enclosed_in_bg=('Granodiorite', 'Granite',),
                           norm='CCRUST',
                           h_ratio=[6.4, 4],
                           legend_ncol=2,
                           )

ree_chond.plot()
elts_crust.plot()

plt.show()

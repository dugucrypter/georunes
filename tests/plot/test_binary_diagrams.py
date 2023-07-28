import os
from georunes.plot.binary.versus import DiagramVs

directory = os.path.dirname(os.path.realpath("WAC_granitoids_comp.xls"))
source = 'tests/WAC_granitoids_comp.xls'
sheet = 'ggtest'


def test_vs():
    vs_diag = DiagramVs(datasource=source,
                        sheet=sheet,
                        group_name='Lithology',
                        xvar='SiO2',
                        yvar='Al2O3')
    vs_diag.plot()

import numpy as np
from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.chemistry import val_ox_to_mc
from georunes.tools.language import get_translator


class DiagramR1R2(DiagramBase, ArrowDrawer, LegendDrawer):
    def __init__(self, datasource, title="R1-R2 multicationic classification (De La Roche et al. 1980)",
                 padding={"bottom": 0.20}, annotation=None, **kwargs):
        DiagramBase.__init__(self, datasource=datasource, title=title, padding=padding, **kwargs)
        self.annotation = annotation
        self.xlabel = "R1=4Si-11(Na+K)-2(Fe+Ti)"
        self.ylabel = "R2=6Ca+2Mg+Al"

    def set_decorations(self):
        _ = get_translator(self.lang_cfg)
        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        self.ax.set_xlim(-1000, 3500)
        self.ax.set_ylim(0, 2500)

        lx1 = np.array(
            [2613.42, 1432.92, 1446.06, 1480.64, 1542.88, 1595.44, 1714.38, 1854.77, 2165.28, 2583.68, 3051.87])
        ly1 = np.array([97.51, 147.33, 209.96, 299.64, 385.77, 451.25, 419.22, 392.17, 369.4, 331.67, 291.81])
        lx2 = np.array(
            [1432.92, 1446.06, 1480.64, 1542.88, 1595.44, 1504.84, 1407.33, 1309.82, 1246.89, 1192.25, 1149.38, 1062.24,
             954.36, 903.87, 1432.92])
        ly2 = np.array(
            [147.33, 209.96, 299.64, 385.77, 451.25, 488.26, 543.06, 619.93, 676.87, 759.43, 859.07, 632.74, 325.27,
             165.12, 147.33])
        lx3 = np.array(
            [112.03, 229.6, 359.61, 501.38, 654.22, 786.31, 921.85, 1056.02, 1149.38, 1062.24, 954.36, 903.87, 112.03])
        ly3 = np.array(
            [186.48, 385.77, 577.94, 757.3, 944.48, 910.32, 883.27, 866.9, 859.07, 632.74, 325.27, 165.12, 186.48])
        lx4 = np.array(
            [-878.98, -790.46, 112.03, 229.6, 359.61, 501.38, 654.22, 483.4, 312.59, 229.6, 69.85, -141.77, -324.34])
        ly4 = np.array(
            [227.05, 223.49, 186.48, 385.77, 577.94, 757.3, 944.48, 982.92, 1037.01, 1060.5, 1116.73, 1194.31, 1267.62])

        lx6 = np.array(
            [3062.93, 2465.42, 2139, 2031.12, 1951.59, 1834.72, 1769.02, 1700.55, 1639, 1595.44, 1714.38, 1854.77,
             2165.28, 2583.68, 3051.87])
        ly6 = np.array(
            [452.67, 525.98, 567.26, 586.48, 611.39, 646.98, 603.56, 548.75, 494.66, 451.25, 419.22, 392.17, 369.4,
             331.67, 291.81])
        lx7 = np.array(
            [1149.38, 1263.49, 1378.28, 1531.81, 1562.24, 1611.34, 1673.58, 1755.19, 1834.72, 1769.02, 1700.55, 1639,
             1595.44, 1504.84, 1407.33, 1309.82, 1246.89, 1192.25, 1149.38])
        ly7 = np.array(
            [859.07, 854.09, 858.36, 874.73, 829.18, 778.65, 733.1, 682.56, 646.98, 603.56, 548.75, 494.66, 451.25,
             488.26, 543.06, 619.93, 676.87, 759.43, 859.07])
        lx8 = np.array(
            [3062.93, 2465.42, 2139, 2031.12, 1951.59, 1834.72, 1964.73, 2085.75, 2232.37, 2426.69, 2611.34, 2818.81])
        ly8 = np.array([452.67, 525.98, 567.26, 586.48, 611.39, 646.98, 713.88, 766.55, 816.37, 869.04, 900.36, 930.96])
        lx9 = np.array(
            [2577.46, 2360.3, 2161.13, 1970.26, 1854.77, 1739.28, 1643.15, 1531.81, 1562.24, 1611.34, 1673.58, 1755.19,
             1834.72, 1964.73, 2085.75, 2232.37, 2426.69, 2611.34, 2818.81])
        ly9 = np.array(
            [1229.89, 1130.25, 1048.4, 982.92, 944.48, 916.73, 898.22, 874.73, 829.18, 778.65, 733.1, 682.56, 646.98,
             713.88, 766.55, 816.37, 869.04, 900.36, 930.96])

        lx10 = np.array(
            [2577.46, 2360.3, 2161.13, 1970.26, 1854.77, 1824.34, 1785.62, 1755.19, 1728.22, 1716.46, 1710.24, 1842.32,
             2017.29, 2254.5, 2484.09])
        ly10 = np.array(
            [1229.89, 1130.25, 1048.4, 982.92, 944.48, 972.95, 1020.64, 1066.9, 1114.59, 1177.94, 1238.43, 1266.19,
             1322.42, 1416.37, 1526.69])
        lx11 = np.array(
            [1854.77, 1739.28, 1643.15, 1531.81, 1441.91, 1411.48, 1396.96, 1396.96, 1506.22, 1710.24, 1716.46, 1728.22,
             1755.19, 1785.62, 1824.34, 1854.77])
        ly11 = np.array(
            [944.48, 916.73, 898.22, 874.73, 1020.64, 1100.36, 1160.85, 1210.68, 1212.81, 1238.43, 1177.94, 1114.59,
             1066.9, 1020.64, 972.95, 944.48])
        lx12 = np.array(
            [1138.31, 1127.25, 1123.1, 1120.33, 1133.47, 1149.38, 1263.49, 1378.28, 1531.81, 1441.91, 1411.48, 1396.96,
             1396.96, 1312.59, 1228.22, 1138.31])
        ly12 = np.array(
            [1243.42, 1175.8, 1100.36, 1012.81, 941.64, 859.07, 854.09, 858.36, 874.73, 1020.64, 1100.36, 1160.85,
             1210.68, 1215.66, 1228.47, 1243.42])
        lx13 = np.array(
            [708.85, 848.55, 978.56, 1071.92, 1138.31, 1127.25, 1123.1, 1120.33, 1133.47, 1149.38, 1056.02, 921.85,
             786.31, 654.22, 483.4, 312.59, 515.91, 708.85])
        ly13 = np.array(
            [1389.32, 1334.52, 1282.56, 1254.8, 1243.42, 1175.8, 1100.36, 1012.81, 941.64, 859.07, 866.9, 883.27,
             910.32, 944.48, 982.92, 1037.01, 1212.81, 1389.32])
        lx14 = np.array(
            [-324.34, -141.77, 69.85, 229.6, 312.59, 515.91, 708.85, 991.01, 869.29, 739.28, 611.34, 143.85, -50.48,
             -324.34])
        ly14 = np.array(
            [1267.62, 1194.31, 1116.73, 1060.5, 1037.01, 1212.81, 1389.32, 1660.5, 1735.94, 1829.89, 1940.93, 1682.56,
             1577.22, 1432.74])

        lx15 = np.array([-324.34, -50.48, 143.85, 611.34, 465.42, 325.03, 254.5, 174.97, 69.85, 22.13])
        ly15 = np.array([1432.74, 1577.22, 1682.56, 1940.93, 2067.62, 2210.68, 2288.26, 2392.17, 2550.89, 2646.98])

        lx16 = np.array(
            [2443.98, 2094.74, 1951.59, 1799.45, 1634.85, 1535.27, 1484.79, 1451.59, 1435.68, 1419.09, 1403.18, 1396.96,
             1506.22, 1710.24, 1842.32, 2017.29, 2254.5, 2484.09])
        ly16 = np.array(
            [1779.36, 1637.72, 1591.46, 1545.91, 1513.88, 1501.78, 1501.78, 1438.43, 1392.88, 1340.93, 1269.75, 1210.68,
             1212.81, 1238.43, 1266.19, 1322.42, 1416.37, 1526.69])
        lx17 = np.array(
            [1396.96, 1312.59, 1228.22, 1138.31, 1170.12, 1199.86, 1263.49, 1360.3, 1484.79, 1451.59, 1435.68, 1419.09,
             1403.18, 1396.96])
        ly17 = np.array(
            [1210.68, 1215.66, 1228.47, 1243.42, 1342.35, 1422.06, 1538.79, 1513.88, 1501.78, 1438.43, 1392.88, 1340.93,
             1269.75, 1210.68])
        lx18 = np.array(
            [1138.31, 1170.12, 1199.86, 1263.49, 1172.2, 1080.91, 991.01, 708.85, 848.55, 978.56, 1071.92, 1138.31])
        ly18 = np.array(
            [1243.42, 1342.35, 1422.06, 1538.79, 1568.68, 1609.96, 1660.5, 1389.32, 1334.52, 1282.56, 1254.8, 1243.42])
        lx20 = np.array(
            [2347.86, 2252.42, 2161.13, 2102.35, 2045.64, 2006.92, 1982.71, 1976.49, 1986.17, 2002.77, 2037.34, 2094.74,
             2443.98])
        ly20 = np.array(
            [2113.88, 2067.62, 2037.01, 2022.06, 1961.57, 1911.03, 1854.8, 1807.12, 1740.21, 1700.36, 1671.17, 1637.72,
             1779.36])
        lx21 = np.array(
            [1652.14, 1728.22, 1793.91, 1883.82, 2015.21, 2102.35, 2045.64, 2006.92, 1982.71, 1976.49, 1986.17, 2002.77,
             2037.34, 2094.74, 1951.59, 1799.45, 1634.85, 1535.27, 1484.79, 1360.3, 1263.49, 1338.17, 1407.33, 1474.41,
             1598.2, 1652.14])
        ly21 = np.array(
            [2001.42, 1987.19, 1977.94, 1980.07, 2003.56, 2022.06, 1961.57, 1911.03, 1854.8, 1807.12, 1740.21, 1700.36,
             1671.17, 1637.72, 1591.46, 1545.91, 1513.88, 1501.78, 1501.78, 1513.88, 1538.79, 1651.96, 1745.91, 1817.08,
             1947.33, 2001.42])
        lx22 = np.array(
            [1652.14, 1598.2, 1474.41, 1407.33, 1338.17, 1263.49, 1172.2, 1080.91, 991.01, 1423.24, 1476.49, 1529.05,
             1586.45, 1652.14])
        ly22 = np.array(
            [2001.42, 1947.33, 1817.08, 1745.91, 1651.96, 1538.79, 1568.68, 1609.96, 1660.5, 2096.09, 2065.48, 2039.15,
             2017.79, 2001.42])
        lx23 = np.array([991.01, 1423.24, 1376.9, 1316.04, 1261.41, 1215.08, 771.78, 611.34, 739.28, 869.29, 991.01])
        ly23 = np.array(
            [1660.5, 2096.09, 2130.96, 2185.05, 2243.42, 2307.47, 2037.01, 1940.93, 1829.89, 1735.94, 1660.5])
        lx24 = np.array([1100.97, 1123.1, 1161.13, 1215.08, 771.78, 611.34, 465.42, 325.03, 254.5, 1100.97])
        ly24 = np.array([2562.99, 2490.39, 2400.71, 2307.47, 2037.01, 1940.93, 2067.62, 2210.68, 2288.26, 2562.99])
        lx25 = np.array(
            [1090.59, 1100.97, 1123.1, 1161.13, 1215.08, 1261.41, 1316.04, 1376.9, 1423.24, 1476.49, 1529.05, 1586.45,
             1652.14, 1728.22, 1793.91, 1883.82, 2015.21, 2102.35, 2161.13, 2252.42, 2347.86])
        ly25 = np.array(
            [2628.47, 2562.99, 2490.39, 2400.71, 2307.47, 2243.42, 2185.05, 2130.96, 2096.09, 2065.48, 2039.15, 2017.79,
             2001.42, 1987.19, 1977.94, 1980.07, 2003.56, 2022.06, 2037.01, 2067.62, 2113.88])

        self.ax.plot(lx1, ly1, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx2, ly2, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx3, ly3, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx4, ly4, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx6, ly6, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx7, ly7, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx8, ly8, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx9, ly9, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx10, ly10, self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx11, ly11, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx12, ly12, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx13, ly13, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx14, ly14, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx15, ly15, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx16, ly16, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx17, ly17, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx18, ly18, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx20, ly20, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx21, ly21, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx22, ly22, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx23, ly23, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx24, ly24, color=self.decor_line_col, linewidth=0.6)
        self.ax.plot(lx25, ly25, color=self.decor_line_col, linewidth=0.6)

        self.ax.text(2700, 720, _("granodiorite"), size='x-small', color=self.decor_text_col)
        self.ax.text(1980, 495, _("granite"), size='x-small', rotation=-5, color=self.decor_text_col)
        self.ax.text(2280, 970, _("tonalite"), size='x-small', rotation=15, color=self.decor_text_col)
        self.ax.text(2100, 1220, _("diorite"), size='x-small', rotation=20, color=self.decor_text_col)
        self.ax.text(1450, 1020, _("monzo\n-diorite"), size='x-small', color=self.decor_text_col)
        self.ax.text(1155, 970, _("monzo-\nnite"), size='x-small', color=self.decor_text_col)

        self.ax.text(1680, 1360, _("gabbrodiorite"), size='x-small', rotation=20, color=self.decor_text_col)
        self.ax.text(1200, 1350, _("monzo-\ngabbro"), size='x-small', color=self.decor_text_col)
        self.ax.text(2150, 1950, _("gabbro-norite"), size='x-small', rotation=20, color=self.decor_text_col)
        self.ax.text(1620, 1700, _("gabbro"), size='x-small', color=self.decor_text_col)
        self.ax.text(780, 1910, _("theralite"), size='x-small', color=self.decor_text_col)
        self.ax.text(430, 2140, _("melteigite"), size='x-small', color=self.decor_text_col)

        self.ax.text(146, 1340, _("essexite"), size='x-small', color=self.decor_text_col)
        self.ax.text(-200, 1850, _("ijolite"), size='x-small', color=self.decor_text_col)

        self.ax.text(1300, 620, _("quartz\nmonzonite"), size='x-small', color=self.decor_text_col)
        self.ax.text(1074, 408, _("quartz\nsyenite"), size='x-small', color=self.decor_text_col)
        self.ax.text(420, 420, _("syenite"), size='x-small', color=self.decor_text_col)
        self.ax.text(-300, 600, _("nepheline\nsyenite"), size='x-small', color=self.decor_text_col)
        self.ax.text(1400, 2240, _("ultramafic rock"), size='x-small', color=self.decor_text_col)
        self.ax.text(850, 1390, _("syeno-\ngabbro"), size='x-small', color=self.decor_text_col)
        self.ax.text(1140, 1620, _("alkali-gabbro"), size='x-small', rotation=55, color=self.decor_text_col)
        self.ax.text(585, 1100, _("syeno-\ndiorite"), size='x-small', color=self.decor_text_col)
        self.ax.text(1700, 230, _("alkali-granite"), size='x-small', rotation=-5, color=self.decor_text_col)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:

                si = val_ox_to_mc(group["SiO2"])
                na = val_ox_to_mc(group["Na2O"])
                k = val_ox_to_mc(group["K2O"])
                fe = val_ox_to_mc(group["Fe2O3"])
                ti = val_ox_to_mc(group["TiO2"])
                ca = val_ox_to_mc(group["CaO"])
                mg = val_ox_to_mc(group["MgO"])
                al = val_ox_to_mc(group["Al2O3"])

                param_R1 = 4 * si - 11 * (na + k) - 2 * (fe + ti)
                param_R2 = 6 * ca + 2 * mg + al

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.ax.scatter(param_R1, param_R2, edgecolors=group["color"],
                                marker=list(group["marker"])[0], label=name, facecolors=group["color"],
                                s=self.markersize,
                                alpha=0.9, zorder=zorder)

                if self.annotation:
                    for i, sample in param_R1.iteritems():
                        self.ax.annotate(group[self.annotation].get(i), (param_R1.get(i), param_R2[i]),
                                         fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

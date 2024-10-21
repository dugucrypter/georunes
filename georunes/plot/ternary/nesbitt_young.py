import math
import numpy as np
from matplotlib.colors import to_rgba

from georunes.plot.helpers import ArrowDrawerTernary
from georunes.plot.ternary.ternbase import DiagramTernaryBase
from georunes.tools.chemistry import molar_ratio, molar_ratio_specified
from georunes.tools.language import format_chemical_formula as _fml
from georunes.tools.language import get_translator
from georunes.tools.plotting import normalize_marker_size

sin60 = math.sqrt(3) / 2
tan30 = 1 / math.sqrt(3)
tan60 = math.sqrt(3)


# Nesbitt, H.W. and Young, G.M., 1984.
# Prediction of some weathering trends of plutonic and volcanic rocks based on thermodynamic and
# kinetic considerations. Geochimica et cosmochimica acta, 48(7).

class DiagramNesbittYoung(DiagramTernaryBase, ArrowDrawerTernary):
    def __init__(self, datasource, title="Nesbitt and Young diagram",
                 markersize=20, ignore_apatite_correction=False, **kwargs):
        DiagramTernaryBase.__init__(self, datasource=datasource, title=title,
                                    markersize=markersize,
                                    top_label=_fml('A (Al2O3)'), left_label=_fml('CN (CaO+Na2O)'),
                                    right_label=_fml('K (K2O)'),
                                    no_ticks_label=True,
                                    **kwargs)

        self.ignore_apatite_correction = ignore_apatite_correction

    def set_decoration(self, ):
        _ = get_translator(self.lang_cfg)
        # Order for points : right var, top var, left var

        _ax = self.tax.get_axes()

        _ax.plot((0, 50 + 35 * sin60 * tan30), (sin60 * 65, sin60 * 65), linewidth=0.8, color=self.decor_line_col,
                 linestyle="--")
        _ax.plot((0, 50 + 15 * sin60 * tan30), (sin60 * 85, sin60 * 85), linewidth=0.8, color=self.decor_line_col,
                 linestyle="--")
        _ax.plot((0, 50 + 50 * sin60 * tan30), (sin60 * 50, sin60 * 50), linewidth=0.8, color=self.decor_line_col,
                 linestyle="--")

        self.ax.arrow(35, 50 * sin60, (30 * sin60) / tan60, 30 * sin60, linewidth=1, color="#222222",
                      head_width=3, head_length=3)

        _ax.annotate(_("Weak\nweathering"), (3, 45,), fontsize="small", color=self.decor_text_col, fontweight='bold')
        _ax.annotate(_("Intermediate\nweathering"), (3, 60,), fontsize="small", color=self.decor_text_col,
                     fontweight='bold')
        _ax.annotate(_("Strong\nweathering"), (3, 75,), fontsize="small", color=self.decor_text_col, fontweight='bold')
        self.tax.annotate(_("Hornblende"), (3, 16,), color=self.decor_text_col, fontsize="small")
        self.tax.annotate(_("Pyroxene"), (3, 6,), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("Plagioclase"), (3, sin60 * 46,), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("Smectite"), (25, sin60 * 80,), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("Kaolinite, gibbsite, chlorite"), (55, 85,), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("Illite"), (64, int(80 * sin60),), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("Muscovite"), (68, int(72 * sin60),), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("Biotite"), (74, int(58 * sin60),), color=self.decor_text_col, fontsize="small")
        _ax.annotate(_("K-feldspar"), (79, int(50 * sin60),), color=self.decor_text_col, fontsize="small")

        minerals = [
            (0, 8, 92),  # Clinopyroxene
            (0, 18, 82),  # Hornblende
            (0, 50, 50),  # Plagioclase
            (0, 80, 20),  # Smectite
            (0, 100, 0),  # Kaolininte, gibbsite, Chlorite
            (20, 80, 0),  # Illite
            (28, 72, 0),  # Muscovite
            (42, 58, 0),  # Biotite
            (50, 50, 0)  # K-feldspar
        ]

        self.tax.scatter(minerals, marker="o", facecolors="#333333", zorder=4, s=20)
        self.ax.arrow(0, 0, 0, 50 * tan60, head_width=3, head_length=3, fc='k', ec='k')

        # Draw vertical axis ticks
        cia_val = np.arange(0, 101, 10)
        for tick_value in cia_val:
            y_tick = tick_value * 50 * tan60 / 100
            self.ax.plot((0, 0.5), (y_tick, y_tick), linewidth=1, color=self.decor_line_col, )
            _ax.annotate(tick_value, (-3, y_tick - 2,), color=self.decor_text_col, fontsize="small", va="bottom",
                         ha="right")

        _ax.annotate("CIA", (2, 22,), color=self.decor_text_col, rotation=90, )

    def plot(self):
        DiagramTernaryBase.plot_config(self, no_gridline=True, no_ticks=self.no_ticks,
                                       no_ticks_label=self.no_ticks_label)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                top_var = molar_ratio(group['Al2O3'])
                if self.ignore_apatite_correction:
                    left_var = molar_ratio_specified(group['CaO'], "CaO") + molar_ratio(group['Na2O'])
                else:
                    left_var = molar_ratio_specified(group['CaO'] - 55.07 * group["P2O5"] / 41.85, "CaO") + molar_ratio(
                        group['Na2O'])

                right_var = molar_ratio(group['K2O'])

                var_sum = top_var + left_var + right_var
                norm_z = 100 * left_var / var_sum
                norm_x = 100 * right_var / var_sum
                norm_y = 100 * top_var / var_sum

                if self.marker != '':
                    mrk = self.marker
                else:
                    mrk = list(group["marker"])[0]

                if self.marker_size_scaled():
                    size = normalize_marker_size(group[self.markersize['var_scale']], self.markersize['val_max'],
                                                 self.markersize['val_min'], self.markersize['size_max'],
                                                 self.markersize['size_min'])
                else:
                    size = self.markersize

                # Convert points to tuples
                points = [(norm_x.get(i), norm_y.get(i), norm_z.get(i)) for i, sample in top_var.items()]

                label = list(group['label'])[0] if self.label_defined else name
                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                sample_color = to_rgba(list(group["color"])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group["color"])[0], alpha=self.alpha_edge_color)
                self.tax.scatter(points, edgecolors=edge_color,
                                 marker=mrk, label=label, facecolors=sample_color, s=size,
                                 zorder=zorder)

                if self.annotation:
                    for i, sample in group[self.top_var].items():
                        self.tax.annotate(group[self.annotation].get(i), (norm_x.get(i), norm_y.get(i)),
                                          fontsize='xx-small')

        self.plot_arrows()
        self.fig.subplots_adjust(right=0.92)
        self.plot_legend()

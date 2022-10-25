from georunes.plot.helpers import ArrowDrawerTernary
from georunes.plot.ternary.ternbase import DiagramTernaryBase
from georunes.tools.chemistry import val_ox_to_el, val_ox_to_mc
from georunes.tools.colors import darken_color
from georunes.tools.language import get_translator
from georunes.tools.plotting import normalize_marker_size


class DiagramJensen(DiagramTernaryBase, ArrowDrawerTernary):
    def __init__(self, datasource, title="Ternary plot of Jensen (1976)", **kwargs):
        DiagramTernaryBase.__init__(self, datasource=datasource, title=title,
                                    top_label='Fet + Ti', left_label='Al', right_label='Mg',
                                    **kwargs)

    def set_decoration(self, ):
        # Order for points : right var, top var, left var
        _ = get_translator(self.lang_cfg)

        p10 = (0, 10, 90)
        p11 = (100 - 29 - 53, 29, 53)
        p111 = (100 - 29.5 - 52, 29.5, 52)
        p12 = (100 - 29 - 51, 29, 51)
        p13 = (100 - 26 - 51, 26, 51)
        p14 = (100 - 12 - 51.5, 12, 51.5)

        p31 = (5, 15, 80)
        p32 = (20, 0, 80)

        p41 = (0, 30, 70)
        p42 = (30, 0, 70)

        p51 = (0, 40, 60)
        p52 = (30, 10, 60)

        p61 = (67 / 2, 33, 67 / 2)
        p62 = (100 - 25 - 51, 25, 51)

        p71 = (0, 50, 50)
        p72 = (17, 100 - 17 - 50, 50)
        p73 = (20, 29, 51)
        curve7 = [p71, p72, p73]

        p81 = (60, 40, 0)
        p82 = (60, 0, 40)

        p91 = (22, 56, 22)
        p92 = (50, 0, 50)

        curve = [p10, p11, p111, p12, p13, p14]

        self.tax.plot(curve, linewidth=1.0, color=self.decor_line_col)
        self.tax.plot(curve7, linewidth=1.0, color=self.decor_line_col, linestyle="--")
        self.tax.line(p31, p32, linewidth=1, color=self.decor_line_col, linestyle="--")
        self.tax.line(p41, p42, linewidth=1, color=self.decor_line_col, linestyle="--")
        self.tax.line(p51, p52, linewidth=1, color=self.decor_line_col, linestyle="--")
        self.tax.line(p61, p62, linewidth=1, color=self.decor_line_col, linestyle="--")
        self.tax.line(p81, p82, linewidth=1, color=self.decor_line_col, linestyle="--")
        self.tax.line(p91, p92, linewidth=1, color=self.decor_line_col)
        self.tax.annotate(_("TH"), (2, 45,), fontsize="small", color=darken_color(self.decor_text_col), rotation=30,
                          fontweight='bold')
        self.tax.annotate(_("Dacite"), (4, 25,), color=self.decor_text_col, fontsize="x-small", rotation=-60)
        self.tax.annotate(_("High-Fe\ntholeiite\nbasalt"), (16, 44,), ha="center", color=self.decor_text_col,
                          fontsize="x-small")
        self.tax.annotate(_("Andesite"), (9, 31,), color=self.decor_text_col, fontsize="x-small", rotation=-60)
        self.tax.annotate(_("Rhyolite"), (1, 21,), color=self.decor_text_col, fontsize="x-small", )

        self.tax.annotate(_("CA"), (40, 3), fontsize="small", color=darken_color(self.decor_text_col), rotation=30,
                          fontweight='bold')
        self.tax.annotate(_("Andesite"), (21, 7,), color=self.decor_text_col, fontsize="x-small", rotation=-60)
        self.tax.annotate(_("Dacite"), (15, 3,), color=self.decor_text_col, fontsize="x-small", rotation=-60)
        self.tax.annotate(_("Basalt"), (27, 12,), color=self.decor_text_col, fontsize="x-small", rotation=-60)
        self.tax.annotate(_("High-Mg\ntholeiite\nbasalt"), (40, 10,), ha="center", color=self.decor_text_col,
                          fontsize="x-small")
        self.tax.annotate(_("Komatiitic basalt"), (35, 35,), color=self.decor_text_col, fontsize="x-small")
        self.tax.annotate(_("Komatiite"), (70, 15,), color=self.decor_text_col, fontsize="x-small")

    def plot(self):
        DiagramTernaryBase.plot_config(self, no_gridline=True)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                top_var = val_ox_to_mc(group['Fe2O3t']) + val_ox_to_el(group['TiO2'])
                left_var = val_ox_to_mc(group['Al2O3'])
                right_var = val_ox_to_mc(group['MgO'])
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
                points = [(norm_x.get(i), norm_y.get(i), norm_z.get(i)) for i, sample in top_var.iteritems()]

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.tax.scatter(points, edgecolors=group["color"],
                                 marker=mrk, label=name, facecolors=group["color"], s=size,
                                 alpha=self.alpha_color, zorder=zorder)

                if self.annotation:
                    for i, sample in top_var.iteritems():
                        self.tax.annotate(group[self.annotation].get(i), (norm_x.get(i), norm_y.get(i)),
                                          fontsize='xx-small')

        self.plot_legend()

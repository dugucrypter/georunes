from georunes.plot.helpers import ArrowDrawerTernary
from georunes.plot.ternary.ternbase import DiagramTernaryBase
from georunes.tools.language import get_translator
from georunes.tools.plotting import normalize_marker_size


class DiagramAnAbOr(DiagramTernaryBase, ArrowDrawerTernary):
    def __init__(self, datasource, title="Ternary feldspar plot (anorthite, albite and orthoclase)",
                 decor_set="Barker79", padding={"bottom": 0.124}, **kwargs):

        if decor_set not in ("blank", "OConnor65", "Barker79"):
            raise ValueError("Parameter 'decor_set' must be 'blank', 'OConnor65' or 'Barker79'")

        DiagramTernaryBase.__init__(self, datasource=datasource, title=title,
                                    top_var='An', left_var='Ab', right_var='Or',
                                    top_label='An', left_label='Ab', right_label='Or',
                                    tscale='linear', left_scale='linear', right_scale='linear',
                                    padding=padding,
                                    **kwargs)

        self.decor_set = decor_set

    def set_decoration(self, ):
        _ = get_translator(self.lang_cfg)

        # Order for points : Or, An, Ab
        if self.decor_set == "blank":
            pass

        elif self.decor_set == "Barker79":

            p1 = (0, 30, 70)
            p2 = (24, 18, 58)

            p21 = (24, 18, 58)
            p22 = (34, 16, 50)

            p31 = (20, 20, 60)
            p32 = (20, 50, 30)

            p41 = (34, 16, 50)
            p42 = (34, 42, 24)

            p51 = (24, 18, 58)
            p52 = (30, 00, 70)

            self.tax.line(p1, p2, linewidth=1, color=self.decor_line_col)
            self.tax.line(p21, p22, linewidth=1, color=self.decor_line_col)
            self.tax.line(p31, p32, linewidth=1, color=self.decor_line_col)
            self.tax.line(p41, p42, linewidth=1, color=self.decor_line_col)
            self.tax.line(p51, p52, linewidth=1, color=self.decor_line_col)

            self.tax.annotate(_("Granite"), (30, 10,), fontsize="small")
            self.tax.annotate(_("Tonalite"), (55 * 0.08, 45, 55 * 0.92), fontsize="small", rotation=60)
            self.tax.annotate(_("Granodiorite"), (55 * 0.5, 45, 55 * 0.5), fontsize="small", rotation=60)
            self.tax.annotate(_("Trondhjemite"), (5, 5,), fontsize="small")

        elif self.decor_set == "OConnor65":
            p1 = (20, 0, 80)
            p2 = (20, 20, 60)

            p21 = (0, 25, 75)
            p22 = (60, 10, 30)

            p31 = (60, 10, 30)
            p32 = (100, 0, 0)
            p41 = (60, 10, 30)
            p42 = (60, 20, 20)
            p51 = (35, 16.25, 48.5)
            p52 = (35, 32.5, 32.5)
            p61 = (10, 22., 5, 67.5)
            p62 = (10, 45, 45)

            self.tax.line(p1, p2, linewidth=1, color=self.decor_line_col)
            self.tax.line(p21, p22, linewidth=1, color=self.decor_line_col)
            self.tax.line(p31, p32, linewidth=1, color=self.decor_line_col)
            self.tax.line(p41, p42, linewidth=1, color=self.decor_line_col)
            self.tax.line(p51, p52, linewidth=1, color=self.decor_line_col)
            self.tax.line(p61, p62, linewidth=1, color=self.decor_line_col)
            self.tax.annotate(_("Trondhjemite"), (5, 5,), fontsize="small")
            self.tax.annotate(_("Granite"), (35, 5,), fontsize="small")
            self.tax.annotate(_("Tonalite"), (4, 35,), fontsize="small", rotation=60)
            self.tax.annotate(_("Granodiorite"), (20, 35,), fontsize="small", rotation=60)
            self.tax.annotate(_("Quartz monzonite"), (45, 25,), fontsize="small", rotation=60)

    def plot(self):
        DiagramTernaryBase.plot_config(self, no_ticks=True)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                var_sum = group[self.top_var] + group[self.left_var] + group[self.right_var]
                norm_z = 100 * group[self.left_var] / var_sum
                norm_x = 100 * group[self.right_var] / var_sum
                norm_y = 100 * group[self.top_var] / var_sum

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

                points = [(norm_x.get(i), norm_y.get(i), norm_z.get(i)) for i, sample in
                          group[self.top_var].iteritems()]

                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                self.tax.scatter(points, edgecolors=group["color"],
                                 marker=mrk, label=name, facecolors=group["color"], s=size,
                                 alpha=self.alpha_color, zorder=zorder)

                if self.annotation:
                    for i, sample in group[self.top_var].iteritems():
                        self.tax.annotate(group[self.annotation].get(i), (norm_x.get(i), norm_y.get(i)),
                                          fontsize='xx-small')

        self.plot_legend()

from matplotlib.colors import to_rgba

from georunes.plot.helpers import ArrowDrawerTernary
from georunes.plot.ternary.ternbase import DiagramTernaryBase
from georunes.tools.language import get_translator
from georunes.tools.plotting import normalize_marker_size


# Streckeisen, A., 1974. Classification and nomenclature of plutonic rocks recommendations of the IUGS subcommission
# on the systematics of igneous rocks. Geologische Rundschau, 63(2), pp.773-786.
# Streckeisen, A., 1978. IUGS Subcommission on the Systematics of Igneous Rocks. Classification and Nomenclature of
# Volcanic Rocks, Lamprophyres, Carbonatites and Melilite Rocks. Recommendations and Suggestions. Neues Jahrbuch fur
# Mineralogie. Stuttgart. Abhandlungen, 143, pp.1-14.

class DiagramQAP(DiagramTernaryBase, ArrowDrawerTernary):
    def __init__(self, datasource, title="QAP ternary diagram", decor_set="Plut", decor_text_col="#777777", **kwargs):
        if decor_set not in ("Plut", "Volc"):
            raise ValueError("Parameter 'decor_set' must be 'Plut' or 'Volc'")

        DiagramTernaryBase.__init__(self, datasource=datasource,
                                    top_var='Qnorm', left_var='Anorm', right_var='Pnorm',
                                    title=title,
                                    top_label='Q', left_label='A', right_label='P',
                                    decor_text_col=decor_text_col,
                                    tscale='linear', left_scale='linear', right_scale='linear',
                                    **kwargs
                                    )

        self.decor_set = decor_set

    def check_parameters(self):
        chklist = ('Qnorm', 'Pnorm', 'Anorm')
        columns = self.data.columns
        missing = []
        for e in chklist:
            if e not in columns:
                missing.append(e)

        if len(missing) > 0:
            raise Exception("Parameters " + str(missing) + " are missing for QAP plot.")

    def set_decoration(self, ):
        _ = get_translator(self.lang_cfg)
        # Order for points : right var, top var, left var
        p01 = (80, 20, 0)
        p02 = (0, 20, 80)

        p21 = (40, 60, 0)
        p22 = (0, 60, 40)

        p31 = (10, 90, 0)
        p32 = (0, 90, 10)

        p41 = (40 * 0.1, 60, 40 * 0.9)
        p42 = (10, 0, 90)

        p51 = (80 * 0.35, 20, 80 * 0.65)
        p52 = (35, 00, 65)

        p61 = (40 * 0.65, 60, 40 * 0.35)
        p62 = (65, 00, 35)

        p621 = (40 * 0.65, 60, 40 * 0.35)
        p622 = (80 * 0.65, 20, 80 * 0.35)

        if self.decor_set == "Plut":
            p11 = (95, 5, 0)
            p12 = (0, 5, 95)

            q51 = (60 * 0.35, 40, 60 * 0.65)
            q52 = (80 * 0.35, 20, 80 * 0.65)

            p71 = (40 * 0.9, 60, 40 * 0.1)
            p72 = (90, 00, 10)

        elif self.decor_set == "Volc":
            p11 = (0, 5, 95)
            p12 = (65 * 0.95, 5, 35 * 0.95)

            q51 = (40 * 0.35, 60, 40 * 0.65)
            q52 = (80 * 0.35, 20, 80 * 0.65)

            p71 = (80 * 0.9, 20, 80 * 0.1)
            p72 = (40 * 0.9, 60, 40 * 0.1)

        self.tax.line(p01, p02, linewidth=1, color=self.decor_line_col)
        self.tax.line(p11, p12, linewidth=1, color=self.decor_line_col)
        self.tax.line(p21, p22, linewidth=1, color=self.decor_line_col)
        self.tax.line(p31, p32, linewidth=1, color=self.decor_line_col)
        self.tax.line(p41, p42, linewidth=1, color=self.decor_line_col)
        self.tax.line(p51, p52, linewidth=1, color=self.decor_line_col)
        self.tax.line(q51, q52, linewidth=1, linestyle="--", color=self.decor_line_col)
        self.tax.line(p61, p62, linewidth=1, color=self.decor_line_col)

        if self.decor_set == "Plut":
            self.tax.line(p621, p622, linewidth=1, color=self.decor_line_col)
            self.tax.line(p71, p72, linewidth=1, color=self.decor_line_col)

            # right, top
            self.tax.annotate(_("granite"), (12, 50), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("syeno-\ngranite"), (12, 25), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("monzo-\ngranite"), (31, 25), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("quartz-\nsyenite"), (21, 10), fontsize="small", ha="center", color=self.decor_text_col)
            self.tax.annotate(_("quartz-\nmonzonite"), (45, 10), fontsize="small", ha="center",
                              color=self.decor_text_col)
            self.tax.annotate(_("quartz-\nmonzodiorite"), (69, 10), fontsize="small", ha="center",
                              color=self.decor_text_col)
            self.tax.annotate(_("syenite"), (19, 1), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("monzonite"), (41, 1), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("granodiorite"), (41, 37), rotation=-70, fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("tonalite"), (45, 45), rotation=-65, fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("monzodiorite\nmonzogabbro"), (74, -14, 16), fontsize="small",
                              color=self.decor_text_col)

        if self.decor_set == "Volc":
            self.tax.line(p621, p622, linewidth=1, linestyle="--", color=self.decor_line_col)
            self.tax.line(p71, p72, linewidth=1, linestyle="--", color=self.decor_line_col)
            # right, top
            self.tax.annotate(_("rhyolite"), (14, 42), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("quartz-\ntrachyte"), (23, 10), fontsize="small", ha='center',
                              color=self.decor_text_col)
            self.tax.annotate(_("quartz-\nlatite"), (42, 10), fontsize="small", ha='center', color=self.decor_text_col)
            self.tax.annotate(_("dacite"), (40, 42), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("basalt\nandesite"), (73, 10), fontsize="small", ha='center', color=self.decor_text_col)
            self.tax.annotate(_("trachyte"), (18, 1), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("latite"), (43, 1), fontsize="small", color=self.decor_text_col)
            self.tax.annotate(_("monzodiorite\nmonzogabbro"), (74, -14, 16), fontsize="small",
                              color=self.decor_text_col)

    def plot(self):
        DiagramTernaryBase.plot_config(self, no_gridline=True, no_ticks=self.no_ticks)
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
                    marker = self.marker
                else:
                    marker = list(group[self.marker_column])[0]

                if self.marker_size_scaled():
                    size = normalize_marker_size(group[self.markersize['var_scale']], self.markersize['val_max'],
                                                 self.markersize['val_min'], self.markersize['size_max'],
                                                 self.markersize['size_min'])
                else:
                    size = self.markersize

                # Convert points to tuples
                points = [(norm_x.get(i), norm_y.get(i), norm_z.get(i)) for i, sample in
                          group[self.top_var].items()]

                label = list(group[self.label_column])[0] if self.label_defined else name
                zorder = 4
                if self.zorder_column:
                    zorder = list(group[self.zorder_column])[0]

                sample_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_edge_color)
                self.tax.scatter(points, edgecolors=edge_color,
                                 marker=marker, label=label, facecolors=sample_color, s=size,
                                 zorder=zorder)

                if self.annotation:
                    for i, sample in group[self.top_var].items():
                        self.tax.annotate(group[self.annotation].get(i), (norm_x.get(i), norm_y.get(i)),
                                          fontsize='xx-small')

        self.plot_legend()

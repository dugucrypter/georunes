from georunes.base.helpers import ArrowDrawerTernary
from georunes.base.ternary import DiagramTernaryBase
from georunes.tools.language import get_translator
from georunes.tools.plotting import normalize_marker_size


class DiagramAFM(DiagramTernaryBase, ArrowDrawerTernary):
    def __init__(self, datasource, title="AFM diagram (Irvine and Baragar 1971)", **kwargs):
        DiagramTernaryBase.__init__(self, datasource=datasource,
                                    title=title,
                                    top_label='F', left_label='A', right_label='M',
                                    tscale='linear', left_scale='linear', right_scale='linear',
                                    legend_ncol=4,
                                    **kwargs)

    def set_decoration(self, ):
        _ = get_translator(self.lang_cfg)
        # Order for points : right var, top var, left var

        p11 = (4, 36, 60)
        p12 = (15.5, 53, 31.5)
        p13 = (19, 55, 26)
        p14 = (23, 55, 28)
        p15 = (27.5, 53, 19.5)
        p16 = (50, 35, 15)

        limit = [p11, p12, p13, p14, p15, p16]
        self.tax.plot(limit, linewidth=1.0, color=self.decor_line_col)
        self.tax.annotate(_("Tholeiite series"), (5, 70,), fontsize="small")
        self.tax.annotate(_("Calc-alkaline series"), (30, 10,), fontsize="small")

    def plot(self):
        DiagramTernaryBase.plot_config(self, no_ticks=True)
        self.set_decoration()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.is_group_allowed(name):
                top_var = group['Fe2O3t']
                left_var = group['Na2O'] + group['K2O']
                right_var = group['MgO']

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

                points = []
                for i, sample in top_var.iteritems():
                    pos = (norm_x.get(i), norm_y.get(i), norm_z.get(i))
                    points.append(pos)

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

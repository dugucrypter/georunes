import numpy as np
from matplotlib.colors import to_rgba

from georunes.plot.base import DiagramBase
from georunes.plot.helpers import LegendDrawer, ArrowDrawer
from georunes.tools.language import format_chemical_formula as _fml, get_translator


# Cox, K.G., Bell, J.D. and Pankhurst, R.J., 1979. Petrographic aspects of plutonic rocks. In The Interpretation of
# Igneous Rocks (pp. 283-307). Springer, Dordrecht.
# Le Maitre, R.W., Streckeisen, A., Zanettin, B., Le Bas, M.J., Bonin, B. and Bateman, P., 2005. Igneous Rocks: A
# Classification and Glossary of Terms. Igneous Rocks: A Classification and Glossary of Terms, p.252.

class DiagramSiAlkali(DiagramBase, ArrowDrawer, LegendDrawer):

    def __init__(self, datasource, decor_set="Cox", title="Total alkali versus silica diagram",
                 padding={"bottom": 0.20}, annotation=None, classi_line=True,
                 alpha_color=0.4, alpha_edge_color=0.8,
                 **kwargs):

        if decor_set not in ("Cox", "TAS"):
            raise ValueError("Parameter 'decor_set' must be 'TAS' or 'Cox'")

        DiagramBase.__init__(self, datasource, title=title, padding=padding, **kwargs)

        self.classi_line = classi_line
        self.annotation = annotation
        self.xlabel = _fml("SiO2 (wt%)")
        self.ylabel = _fml("Na2O + K2O (wt%)")
        self.alpha_color = alpha_color
        self.alpha_edge_color = alpha_edge_color
        self.decor_set = decor_set

    def set_decorations(self):
        _ = get_translator(self.lang_cfg)
        self.ax.set_xlim(35, 80)
        self.ax.set_ylim(1, 17)

        if not self.no_title:
            self.ax.set_title(self.title, size=self.title_fs)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

        if self.decor_set == "Cox":
            lx1 = np.array([41, 44, 52, 52, 53, 46.4, 44.5, 41])
            ly1 = np.array([3, 2, 1.75, 5.6, 7.2, 7, 5.75, 3])

            lx2 = np.array([52, 55, 54.75, 52, 52])
            ly2 = np.array([1.75, 1.75, 5.5, 5.6, 1.75])

            lx3 = np.array([55, 57, 63, 62.5, 54.75, 55])
            ly3 = np.array([1.75, 2, 3.5, 7, 5.5, 1.75])
            lx4 = np.array([63, 70, 65, 62.5, 63])
            ly4 = np.array([3.5, 5.5, 9, 7, 3.55])
            lx5 = np.array([70, 75, 75, 69.3, 65, 70])
            ly5 = np.array([5.5, 8, 9, 11.9, 9, 5.5])
            lx6 = np.array([52, 54.75, 62.5, 65, 62, 57, 53, 52])
            ly6 = np.array([5.6, 5.5, 7, 9, 10, 9, 7.2, 5.6])
            lx7 = np.array([39.5, 41, 44.5, 46.4, 48, 50.25, 54.5, 51.5, 49, 40.5, 43.5, 39.5])
            ly7 = np.array([4, 3, 5.75, 7, 8.3, 9.25, 11, 13.2, 15, 9.5, 8.33, 4])
            lx8 = np.array([46.4, 53, 57, 54.25, 50.25, 48, 46.4])
            ly8 = np.array([7, 7.2, 9, 9.35, 9.25, 8.3, 7])
            lx9 = np.array([50.25, 54.25, 57, 62, 65, 69.3, 62, 57.75, 54.5, 50.25])
            ly9 = np.array([9.25, 9.35, 9, 10, 9, 11.9, 14, 11.25, 11, 9.25])
            lx10 = np.array([36, 39.5, 43.5, 40.5, 36, 36])
            ly10 = np.array([5.9, 4, 8.33, 9.5, 6.5, 5.9])
            lx11 = np.array([49, 51.5, 54.5, 57.75, 62, 52.2, 51.5, 49])
            ly11 = np.array([15, 13.2, 11, 11.25, 14, 16.25, 16.25, 15])
            lx12 = np.array([57.75, 62])
            ly12 = np.array([11.25, 10])
            lx13 = np.array([43.5, 45.35, 51.5])
            ly13 = np.array([8.33, 9.375, 13.2])
            lx14 = np.array([45.35, 48])
            ly14 = np.array([9.375, 8.3])
            lx15 = np.array([44.5, 52])
            ly15 = np.array([5.75, 5.6])

            self.ax.plot(lx1, ly1, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx2, ly2, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx3, ly3, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx4, ly4, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx5, ly5, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx6, ly6, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx7, ly7, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx8, ly8, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx9, ly9, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx10, ly10, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx11, ly11, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx12, ly12, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx13, ly13, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx14, ly14, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(lx15, ly15, color=self.decor_line_col, linewidth=0.6)

            if self.classi_line:
                lx17 = np.array([44, 52, 65, 80])
                ly17 = np.array([2, 5.6, 8, 8.35])

                p = np.poly1d(np.polyfit(lx17, ly17, 3))
                t17 = np.arange(44, 76, 1)
                u17 = []
                for val in t17:
                    u17.append(p(val))
                self.ax.plot(t17, u17, color=self.decor_line_col, linewidth=1)

            labels = [
                [68, 9.5, _("Granite")],
                [64, 4.9, _("Quartz diorite")],
                [57, 4.5, _("Diorite")],
                [43, 3.5, _("Gabbro")],
                [59.5, 11.5, _("Syenite")],
                [49, 8, _("Syenodiorite")],
                [50.5, 14, _("Nepheline\nsyenite")],
                [46, 6.2, _("Gabbro")],
                [37, 6.5, _("Ijolite")],
                [56.5, 10, _("Syenite")]
            ]
            for elt in labels:
                self.ax.text(*elt, fontsize="x-small", color=self.decor_text_col)

            self.ax.text(70, 14, _("Alkaline"), color=self.decor_text_col)
            self.ax.text(70, 3, _("Subalkaline"), color=self.decor_text_col)

        elif self.decor_set == 'TAS':
            lx0 = np.array([41, 41, 45])
            ly0 = np.array([3, 7, 9.4])
            hx1 = np.array([45, 48.4, 52.5])
            hy1 = np.array([9.4, 11.5, 14])
            hx2 = np.array([45, 45, 49.4, 53, 57.6])
            hy2 = np.array([1, 5, 7.3, 9.3, 11.7])
            hx3 = np.array([45, 52, 57, 63, 69])
            hy3 = np.array([5, 5, 5.9, 7, 8])

            vx4 = np.array([41, 41, 45])
            vy4 = np.array([1, 3, 3])
            vx5 = np.array([52, 52, 49.4, 45])
            vy5 = np.array([1, 5, 7.3, 9.4])
            vx6 = np.array([57, 57, 53, 48.4])
            vy6 = np.array([1, 5.9, 9.3, 11.5])
            vx7 = np.array([63, 63, 57.6, 52.5, 50.28])
            vy7 = np.array([1, 7, 11.7, 14, 15])
            vx8 = np.array([74, 69, 69])
            vy8 = np.array([1, 8, 13])

            self.ax.plot(lx0, ly0, color=self.decor_line_col, linewidth=0.6, linestyle="--", )
            self.ax.plot(hx1, hy1, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(hx2, hy2, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(hx3, hy3, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(vx4, vy4, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(vx5, vy5, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(vx6, vy6, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(vx7, vy7, color=self.decor_line_col, linewidth=0.6)
            self.ax.plot(vx8, vy8, color=self.decor_line_col, linewidth=0.6)

            labels = [
                [43, 2, _("picro-\nbasalt")],
                [48, 3, _("basalt")],
                [54.5, 3.5, _("basaltic\nandesite")],
                [60, 5, _("andesite")],
                [66.5, 4.5, _("dacite")],
                [49, 5.5, _("trachy-\nbasalt")],
                [53, 6.5, _("basaltic\ntrachy-\nandesite")],
                [57.5, 8.2, _("trachy-\nandesite")],
                [64, 10.5, _("trachyte/\ntrachydacite")],
                [45, 7, _("tephrite/\nbasanite")],
                [49, 9.3, _("phonotephrite")],
                [53, 11.5, _("tephriphonolite")],
                [57, 14, _("phonolite")],
                [40, 9.5, _("foidite")],
            ]
            for elt in labels:
                self.ax.text(*elt, fontsize="x-small", ha="center", color=self.decor_text_col)

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decorations()

        # Categorize by group
        groups = self.data.groupby(self.group_name)
        for name, group in groups:

            if self.exclude_groups and name not in self.exclude_groups:
                nak = group["Na2O"] + group["K2O"]

                label = list(group['label'])[0] if self.label_defined else name
                zorder = 4
                if self.drawing_order:
                    zorder = list(group[self.drawing_order])[0]

                sample_color = to_rgba(list(group["color"])[0], alpha=self.alpha_color)
                edge_color = to_rgba(list(group["color"])[0], alpha=self.alpha_edge_color)
                self.ax.scatter(group["SiO2"], nak, edgecolors=edge_color,
                                marker=list(group["marker"])[0], label=label, facecolors=sample_color,
                                s=self.markersize,
                                zorder=zorder)

                if self.annotation:
                    for i, sample in group["SiO2"].items():
                        self.ax.annotate(group[self.annotation].get(i), (group["SiO2"].get(i), nak[i]),
                                         fontsize='xx-small')

        self.plot_arrows()
        self.plot_legend()

import warnings
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import lines
from georunes.plot.base import DiagramBase
from georunes.tools.chemistry import val_ox_to_el_ppm, name_el_to_def_ox
from georunes.tools.data import row_min, row_max
from georunes.tools.preprocessing import check_geochem_res
from georunes.tools.reservoirs import Reservoirs

listing_ree = ["La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]


class DiagramSpider(DiagramBase):
    def __init__(self, datasource,
                 listing=listing_ree,
                 show_reservoirs=["", ],
                 norm="CI",
                 h_ratio=1. / 2,
                 fillmode="marked-lines",
                 ylim=None,
                 legend_fs="small", thick_legend_linewidth=False,
                 enclosed_in_bg=("",),
                 markersize=8,
                 xlabel="", ylabel="",
                 drawing_order = "zorder",
                 **kwargs
                 ):

        if fillmode not in ("lines", "marked-lines", "enclosed", "enclosed-lines", "mixed"):
            raise ValueError("Incorrect parameter 'fillmode'")

        DiagramBase.__init__(self, datasource=datasource, h_ratio=h_ratio, **kwargs)

        self.thick_legend_linewidth = thick_legend_linewidth
        self.listing = listing
        self.show_reservoirs = (*show_reservoirs,)

        res = Reservoirs.get_instance()

        if isinstance(norm, dict) and check_geochem_res(norm):
            self.norm = res.register_model(norm)
        elif norm in res.model_list:
            self.norm = res.compos[norm]
        else:
            if norm is not None:
                msg = "The data of reservoir " + norm + " are not found. Check the figure configuration."
                warnings.warn(msg)
            self.norm = res.compos["CI"]
        self.fillmode = fillmode
        self.enclosed_in_bg = enclosed_in_bg
        self.drawing_order = drawing_order
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ylim = ylim
        self.markersize = markersize
        self.legend_fs = legend_fs
        if enclosed_in_bg is None:
            self.enclosed_in_bg = ("",)
        else:
            self.enclosed_in_bg = enclosed_in_bg

    def init_plot(self):

        if self.h_ratio is None:
            self.fig, self.ax = plt.subplots()
        else:
            if isinstance(self.h_ratio, list):
                self.fig, self.ax = plt.subplots(figsize=self.h_ratio)
            else:
                self.fig, self.ax = plt.subplots(figsize=plt.figaspect(self.h_ratio))

    def set_decoration(self):

        if not self.no_title:
            self.ax.set_title(self.title, size="small")

        if self.ylim:
            self.ax.set_ylim(self.ylim)

        self.ax.tick_params(axis='x', labelsize=self.fontsize)
        self.ax.tick_params(axis='y', labelsize=self.fontsize)

        self.ax.set_xlabel(self.xlabel, fontsize=self.fontsize)
        self.ax.set_ylabel(self.ylabel, fontsize=self.fontsize)

    def is_group_enclosed(self, name):
        if type(name) != str and len(
                name) > 1:  # If multiple parameters are chosen to filter group data,
            # take the first one who must be the group
            name = name[0]

        if (self.enclosed_in_bg is not None) and (str(name) in self.enclosed_in_bg):
            return True
        return False

    def plot(self):
        DiagramBase.plot_config(self)
        self.set_decoration()

        label_defined = True if 'label' in self.data.columns else False

        d_min = dict()
        d_max = dict()

        # Draw spectras
        groups = self.data.groupby(self.group_name)
        legend_cfg = []
        legend_cfg_labels = []
        legend_list = []

        for name, group in groups:
            if self.is_group_allowed(name):
                if self.is_group_enclosed(name):
                    custom_fillmode = 'enclosed'
                else:
                    custom_fillmode = self.fillmode

                last = None
                label = list(group['label'])[0] if label_defined else name
                min_vals = [None] * len(self.listing)  # Trick to deal with missing value
                max_vals = [None] * len(self.listing)
                lw = 0.3  # Linewidth

                for index, row in group.iterrows():
                    vals, calc_val = [], []
                    drow = row.to_dict()
                    for elt in self.listing:
                        if elt in drow.keys():
                            calc_val = drow[elt] / self.norm[elt]
                        elif elt in name_el_to_def_ox.keys():
                            ox = name_el_to_def_ox[elt]
                            calc_val = val_ox_to_el_ppm(drow[ox], ox) / self.norm[elt]

                        vals.append(calc_val)
                        if calc_val:
                            if elt in d_min.keys():
                                d_min[elt] = min(d_min[elt], calc_val)
                            else:
                                d_min[elt] = calc_val

                            if elt in d_max.keys():
                                d_max[elt] = max(d_max[elt], calc_val)
                            else:
                                d_max[elt] = calc_val

                    zorder = None
                    if self.drawing_order:
                        zorder = list(group[self.drawing_order])[0]
                    if custom_fillmode in ("enclosed-lines", "mixed", "enclosed"):
                        min_vals = row_min(min_vals, vals)
                        max_vals = row_max(max_vals, vals)
                    mark = list(group["marker"])[0]
                    marker_edge_w = None
                    if mark in ("+", "x"):
                        marker_edge_w = 3

                    if custom_fillmode in ("enclosed-lines", "lines"):
                        last, = self.ax.semilogy(self.listing, vals, markersize=0,
                                                 c=drow['color'],
                                                 mec=drow['color'],
                                                 linewidth=lw,
                                                 alpha=0.8,
                                                 label=label, zorder=zorder
                                                 )

                    elif custom_fillmode in ('marked-lines', 'mixed'):
                        last, = self.ax.semilogy(self.listing,
                                                 vals,
                                                 c=drow['color'],
                                                 mec=drow['color'],
                                                 marker=mark,
                                                 linewidth=lw,
                                                 markeredgewidth=marker_edge_w,
                                                 alpha=0.8,
                                                 label=label,
                                                 markersize=self.markersize
                                                 , zorder=zorder)

                    elif custom_fillmode == "enclosed":  # Fake draw to deal with figure canvas
                        last, = self.ax.semilogy(self.listing, vals,
                                                 linewidth=0, zorder=zorder
                                                 )

                if custom_fillmode in ("enclosed", "enclosed-lines", "mixed"):
                    self.ax.fill_between(self.listing, min_vals, max_vals, facecolor=list(group["color"])[0], zorder=zorder,
                                         alpha=0.25)

                    # For legend
                    pseudo_square = patches.Rectangle((0, 0), 0, 0, facecolor=list(group["color"])[0], alpha=0.25)
                    pseudo_line = lines.Line2D((0, 0), (0, 0), linewidth=lw * 1.8, c=drow['color'], )

                if name not in legend_list:
                    legend_cfg_labels.append(label)
                    if custom_fillmode == "enclosed":
                        legend_cfg.append(pseudo_square)
                    elif custom_fillmode == "enclosed-lines":
                        legend_cfg.append((pseudo_square, pseudo_line))
                    elif custom_fillmode == "lines":
                        legend_cfg.append(last)
                    elif custom_fillmode == "mixed":
                        legend_cfg.append((pseudo_square, last))
                    elif custom_fillmode == "marked-lines":
                        legend_cfg.append(last)
                    legend_list.append(name)

        self.plot_reservoirs(legend_cfg, legend_list, legend_cfg_labels)
        self.plot_legend(legend_cfg, legend_cfg_labels)

    def plot_reservoirs(self, legend_cfg, legend_list, legend_cfg_labels):
        res = Reservoirs.get_instance()

        for model in self.show_reservoirs:
            if model in res.model_list:
                compo = res.compos[model]

                vals = []
                for val in self.listing:
                    vals.append(compo[val] / self.norm[val])

                last, = self.ax.semilogy(self.listing, vals,
                                         c=res.get_color(model), marker="o", markersize=2,
                                         linewidth=1.5, alpha=0.8,
                                         label=res.get_label(model))
                if model not in legend_list:
                    legend_cfg.append(last)
                    legend_list.append(model)
                    legend_cfg_labels.append(res.get_label(model))

    def plot_legend(self, legend_cfg, legend_cfg_labels):

        if not self.no_legend:

            leg_canvas = self.ax if self.legend_in_axs else self.fig
            leg = leg_canvas.legend(handles=tuple(legend_cfg), labels=tuple(legend_cfg_labels), loc=self.legend_loc,
                                    ncol=self.legend_ncol, edgecolor='k', fontsize=self.legend_fs)
            if self.thick_legend_linewidth:

                for leg_obj in leg.legendHandles:
                    leg_obj.set_linewidth(2.0)

            self.fig.subplots_adjust(bottom=0.2)

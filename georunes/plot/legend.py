from matplotlib import patches
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D
from georunes.plot.base import DiagramBase
from georunes.tools.reservoirs import Reservoirs


class PlotLegend(DiagramBase):
    def __init__(self, datasource,
                 show_reservoirs=None,
                 lines_to_break=None,
                 label_order_column='label_order',
                 decor_set=None,
                 title='Legend',
                 alpha_color=0.4, alpha_edge_color=1,
                 **kwargs
                 ):
        DiagramBase.__init__(self, datasource=datasource,
                             title=title, **kwargs)
        self.lines_to_break = lines_to_break
        if show_reservoirs is None:
            show_reservoirs = ["", ],
        self.show_composition = (*show_reservoirs,)
        self.decor_set = decor_set
        self.alpha_color = alpha_color
        self.alpha_edge_color = alpha_edge_color
        self.label_order_column = label_order_column

    def is_group_allowed(self, name):
        if (self.exclude_groups is not None) and (name not in self.exclude_groups):
            return True
        return False

    def plot(self):
        if hasattr(self, "window_title"):
            self.fig.canvas.manager.set_window_title(self.window_title)

        self.ax.set_axis_off()
        groups = self.data.groupby(self.group_name)
        list_label_legend = {}
        handles_norm = {}
        res = Reservoirs.get_instance()

        label_order_i = 0
        for name, group in groups:
            if self.is_group_allowed(name):
                if self.label_defined and group[self.label_column].iloc[0]:
                    label = group[self.label_column].iloc[0]
                else:
                    label = name

                # Add group to list of order appearance
                if self.label_order_column in group.keys():
                    list_label_legend[list(group[self.label_order_column])[0]] = label
                else:
                    list_label_legend[label_order_i] = label
                    label_order_i += 1

                # Scatter
                if self.decor_set == "spiderlines":
                    self.ax.plot([], [], linewidth=1, label=label, color=list(group[self.color_column])[0], )

                if self.decor_set == "mixed":
                    color = group[self.color_column].iloc[0]
                    marker = group[self.marker_column].iloc[0]
                    sample_color = to_rgba(color, alpha=self.alpha_color)
                    edge_color = to_rgba(color, alpha=self.alpha_edge_color)
                    self.ax.plot([], [], linewidth=1, label=label, color=list(group[self.color_column])[0],
                                 marker=marker, markeredgecolor=edge_color,
                                 markerfacecolor=sample_color, markersize=self.markersize,
                                 )
                else:
                    sample_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_color)
                    edge_color = to_rgba(list(group[self.color_column])[0], alpha=self.alpha_edge_color)
                    self.ax.scatter([], [], edgecolors=edge_color, facecolors=sample_color,
                                    marker=list(group[self.marker_column])[0], label=label,
                                    s=self.markersize,
                                    )
                self.fig.subplots_adjust(left=0.1, right=0.9)

        for reference in self.show_composition:
            if reference in res.get_models_list():
                line = Line2D([], [], c=res.get_color(reference), linewidth=1.5, label=res.get_label(reference), )
                handles_norm[res.get_label(reference)] = line

        handles, labels = self.ax.get_legend_handles_labels()
        max_order = max(*[int(x) for x in list_label_legend.keys()])
        ordered_handles = []
        ordered_labels = []
        line = 0
        for i in range(1, max_order + 1):
            if i in list_label_legend.keys():  # If group is not excluded
                idx = labels.index(list_label_legend[i])
                ordered_handles.append(handles[idx])
                ordered_labels.append(labels[idx])
                line += 1
                if self.lines_to_break and line in self.lines_to_break:
                    r = patches.Rectangle((0, 0), 1, 1, fill=False, edgecolor='none', visible=False)
                    ordered_handles.append(r)
                    ordered_labels.append("")

        for key, val in handles_norm.items():
            ordered_handles.append(val)
            ordered_labels.append(key)

        self.ax.legend(ordered_handles, ordered_labels, ncol=self.legend_ncol, loc=self.legend_loc)

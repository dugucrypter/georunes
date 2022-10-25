import matplotlib.patches as mpatches


class ArrowDrawer:
    def plot_arrows(self, arrowstyle="->"):
        if self.arrows and len(self.arrows) > 0:
            for arr in self.arrows:
                arr_patch = mpatches.FancyArrowPatch(arr[0], arr[1], arrowstyle=arrowstyle, mutation_scale=10)
                self.ax.add_patch(arr_patch)


class ArrowDrawerTernary:
    def plot_arrows(self, arrowstyle="->"):  # Plot arrow with normal x vs y projection
        if self.arrows and len(self.arrows) > 0:

            for arr in self.arrows:
                arr_patch = mpatches.FancyArrowPatch(arr[0], arr[1], arrowstyle=arrowstyle, mutation_scale=10)
                self.ax.add_patch(arr_patch)


class LegendDrawer:
    def plot_legend(self):
        if not self.no_legend:
            leg_canvas = self.ax if self.legend_in_axs else self.fig
            leg = leg_canvas.legend(loc=self.legend_loc, ncol=self.legend_ncol, fontsize=self.legend_fs, edgecolor='k')

            # Set marker size in legend
            for leg_obj in leg.legendHandles:
                leg_obj._sizes = self.legend_ms
        else:
            self.fig.subplots_adjust(bottom=0.11)

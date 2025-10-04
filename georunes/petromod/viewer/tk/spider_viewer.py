import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from georunes.petromod.viewer.tk.fract_viewer import FractViewerTk
from georunes.tools.reservoirs import get_reservoir_norm


class SpiderViewerTk(FractViewerTk):
    def __init__(self, petro_model, data_coeffs, initial_conc, norm="CI", cmap='plasma_r', *args, **kwargs):
        self.norm = get_reservoir_norm(norm)
        self.line = None # For ax.semilogy
        self.cmap = plt.get_cmap(cmap)
        FractViewerTk.__init__(self, petro_model, data_coeffs, initial_conc, *args, **kwargs)

    def set_supplement_status(self):
        self.supplement_status = []
        norm_status = "Norm : " + str(self.norm["reservoir"])
        self.supplement_status.append(norm_status)

    def draw(self, element=None):
        list_elements = [el for el in self.model.list_elements() if el in self.initial_conc_elts]
        concentration_func = self.model.get_phase_concentration_func(self.selected_phase)
        for f in self.liq_fract_values:
            values = [concentration_func(el, f, self.initial_conc) / self.norm[el] for el in list_elements]
            self.ax.semilogy(list_elements, values, label='F={}'.format(f), color=self.cmap(f))
        self.ax.set_ylabel('Normalized concentrations')
        self.ax.grid(axis='y', which='both', linestyle='-', color='#e8e8e8')
        if self.show_legend:
            cbar = plt.colorbar(ScalarMappable(cmap=self.cmap, norm=Normalize(0, 1)), ax=self.ax)
            cbar.set_label('Liquid fraction (F)')
        self.canvas.draw()

    def fill_frame(self):
        FractViewerTk.fill_frame(self)

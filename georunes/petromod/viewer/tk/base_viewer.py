import tkinter as tk
from abc import abstractmethod, ABC
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

_fract_values = [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]


def check_float_list_and_order(lst, order="up"):

    # Validate input type and float range
    if isinstance(lst, list):
        for x in lst:
            if not isinstance(x, float) or not (0 <= x <= 1):
                return False

        # Check ordering function
        def is_sorted(l, ascending=True):
            for i in range(len(l) - 1):
                if ascending and l[i] > l[i + 1]:
                    return False
                if not ascending and l[i] < l[i + 1]:
                    return False
            return True

        ascending = (order == "up")

        if is_sorted(lst, ascending=ascending):
            return lst
        else:
            return sorted(lst, reverse=not ascending)
    else :
        return _fract_values

def total_label_color(total):
    if total == 100:
        total_lbl = "100"
        total_lbl_color = "#080"
    else:
        total_lbl = str(total)
        total_lbl_color = "#f00"
    return total_lbl, total_lbl_color


class BaseViewerTk(ABC):
    def __init__(self, petro_model, suppl_wm_title=None, liq_fract_values=None, verbose=0):
        self.verbose = verbose
        self.model = petro_model
        self.liq_fract_values = check_float_list_and_order(liq_fract_values,)

        # Window
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.root = tk.Tk()
        wm_title = "GeoRunes - PetroMod" + " - " + self.model.modeler_name

        if suppl_wm_title:
            wm_title = wm_title + " - " + suppl_wm_title
        self.root.wm_title(wm_title)
        self.show_legend = True

        # Frame
        self.frame = tk.Toplevel(self.root, )
        self.frame.minsize(300, 100)  # Minimum width
        self.plot_title = None

        # matplotlib canvas
        self.set_mpl_canvas()

    def set_supplement_status(self):
        pass

    def adjust_frame_position(self):
        # Frame position and settings
        self.root.update()
        dx = self.root.winfo_x() + self.root.winfo_width()
        dy = self.root.winfo_y()
        self.frame.geometry("+%d+%d" % (dx, dy))
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing_frame)

    def set_mpl_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def fill_frame(self):
        # Structure
        self.toolbar = tk.Frame(self.frame, height=40)
        self.headerbar = tk.Frame()
        self.content = tk.PanedWindow(self.frame)
        self.bottombar = tk.Frame(self.frame, height=60)
        self.statusbar = tk.Frame(self.frame, height=30)

        self.toolbar.pack(side="top", fill="x")
        self.statusbar.pack(side="bottom", fill="x")
        self.bottombar.pack(side="bottom", fill="x")
        self.content.pack(side="top", fill="both", expand=True)

    @abstractmethod
    def draw(self, element=None):
        pass

    def toggle_legend(self):
        self.show_legend = not self.show_legend
        self.refresh_plotting()

    def loop(self):
        self.root.mainloop()

    def refresh_plotting(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot()
        self.draw()

    def on_closing_frame(self):
        self.canvas.get_tk_widget().destroy()
        self.root.destroy()

    def extra_widgets(self):
        pass

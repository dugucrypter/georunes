import warnings
import matplotlib.pyplot as plt
from georunes.tools.preprocessing import check_data, data_create_graphic_preset, data_set_graphic_preset
from georunes.tools.filemanager import FileManager


class DiagramBase:
    def __init__(self, datasource,
                 sheet=0,
                 no_marker=False,
                 no_title=False, no_legend=False,
                 title="", window_title=None, h_ratio=None,
                 group_name='group', exclude_groups=("",),
                 supp_group=None,  # Second group for classification data
                 ignore_checkings=False, ignore_checking_markers=False,
                 decor_text_col="k", decor_line_col="k",
                 legend_ncol=1, legend_loc="lower center", legend_in_axs=False,
                 drawing_order=None,
                 arrows=None,
                 padding=None,
                 lang_cfg=None,
                 custom_zorder={},
                 fontsize='medium', title_fs='medium', legend_fs='medium',
                 legend_ms=[50], markersize=None,
                 auto_graphic_preset=True, graphic_preset=None,
                 ):

        filemanager = FileManager.get_instance()
        self.data = filemanager.read_file(datasource, sheet_name=sheet)
        self.check_parameters()  # Verify if some required data are present in file. Can be implemented in child classes
        self.title = title
        self.h_ratio = h_ratio
        self.init_plot()
        if exclude_groups is None:
            self.exclude_groups = ("",)
        else:
            self.exclude_groups = exclude_groups

        self.window_title = window_title if window_title else title
        self.no_title = no_title
        self.no_legend = no_legend
        self.group_name = group_name
        self.supp_group = supp_group
        self.datasource = datasource
        self.no_marker = no_marker
        self.custom_zorder = custom_zorder
        self.arrows = arrows
        self.legend_ncol = legend_ncol
        self.legend_loc = legend_loc
        self.legend_in_axs = legend_in_axs
        self.decor_text_col = decor_text_col
        self.decor_line_col = decor_line_col
        self.padding_config = False
        self.init_padding(padding)
        self.lang_cfg = lang_cfg
        self.fontsize = fontsize
        self.title_fs = title_fs
        self.legend_fs = legend_fs
        self.legend_ms = legend_ms
        self.markersize = markersize
        self.label_defined = True if 'label' in self.data.columns else False
        self.drawing_order = drawing_order if drawing_order in self.data.columns else None
        if not ignore_checkings:
            check_data(self.data, group_name=self.group_name, supp_group=self.supp_group,
                       ignore_checking_markers=ignore_checking_markers)

        if auto_graphic_preset and 'color' not in self.data.columns:  # If color is missing, no graphic preset is provided
                if graphic_preset:
                    self.data = data_set_graphic_preset(self.data, graphic_preset, group_name=group_name)
                else:
                    self.data = data_create_graphic_preset(self.data, group_name=group_name)

    def init_padding(self, padding):
        self.padding_left, self.padding_right, self.padding_top, self.padding_bottom = None, None, None, None

        if padding:
            self.padding_config = True
            for side in padding.keys():
                if side == "left":
                    self.padding_left = padding["left"]
                if side == "top":
                    self.padding_top = padding["top"]
                if side == "bottom":
                    self.padding_bottom = padding["bottom"]
                if side == "right":
                    self.padding_right = padding["right"]

    def adjust_padding(self):
        if self.padding_left:
            self.fig.subplots_adjust(left=self.padding_left)
        if self.padding_right:
            self.fig.subplots_adjust(right=self.padding_right)
        if self.padding_top:
            self.fig.subplots_adjust(top=self.padding_top)
        if self.padding_bottom:
            self.fig.subplots_adjust(bottom=self.padding_bottom)

    def init_plot(self):
        if self.h_ratio is None:
            self.fig, self.ax = plt.subplots()
        else:
            if isinstance(self.h_ratio, list):
                self.fig, self.ax = plt.subplots(figsize=self.h_ratio)
            else:
                self.fig, self.ax = plt.subplots(figsize=plt.figaspect(self.h_ratio))

    def is_group_allowed(self, name):
        if type(name) != str and len(
                name) > 1:  # If multiple parameters are chosen to filter group data,
            # take the first one who must be the group
            name = name[0]
        if (self.exclude_groups is not None) and (not str(name) in self.exclude_groups):
            return True
        return False

    def set_xlabel(self, nx):
        self.xlabel = nx

    def set_ylabel(self, ny):
        self.ylabel = ny

    def plot_config(self):
        if hasattr(self, "window_title"):
            self.fig.canvas.manager.set_window_title(self.window_title)

        if self.padding_config:
            self.adjust_padding()

    def marker_size_scaled(self, markersize=None):

        if markersize is None:
            markersize = self.markersize

        if isinstance(markersize, dict):
            chklist = ('var_scale', 'val_max', 'val_min')
            if all(key in markersize.keys() for key in chklist):
                if 'size_max' not in markersize.keys():
                    markersize['size_max'] = None
                if 'size_min' not in markersize.keys():
                    markersize['size_min'] = None
                return True
            else:
                warnings.warn("Key parameters missing for configuration of markersize")
        return False

    def check_parameters(self):
        pass

    def save(self, fname, **kwargs):
        self.fig.savefig(fname, **kwargs)

    def save_svg(self, fname, **kwargs):
        self.fig.savefig(fname, **kwargs)

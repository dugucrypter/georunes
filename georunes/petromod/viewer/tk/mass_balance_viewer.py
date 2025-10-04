import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.collections import LineCollection
from pandas import Series
from georunes.petromod.finders.cumulate_finder import CumulateFinder
from georunes.tools.gui.tkwidets.entry_with_callback import EntryWithCallback
from georunes.tools.gui.tkwidets.editable_treeview import EditableFloatTreeview
from georunes.petromod.viewer.tk.base_viewer import BaseViewerTk, total_label_color
from georunes.tools.colors import merge_colormaps
from georunes.tools.data import float_or_zero


class MassBalanceViewerTk(BaseViewerTk):
    def __init__(self, petro_model, parent_conc, child_conc=None,
                 suppl_wm_title=None, alpha_step=0.1, *args, **kwargs):
        self.minerals = petro_model.get_minerals_list()
        self.oxels = petro_model.get_elements_list()
        self.default_parent_conc = parent_conc.copy()
        for oxel in self.oxels:
            if oxel not in self.default_parent_conc.keys():
                raise Exception(
                    "Non Null value is required for all elements in parental composition. Check the element " + oxel + ".")
        self.parent = self.default_parent_conc.copy()
        self.parent_elements = self.default_parent_conc.index.tolist()
        self.child = child_conc
        self.set_supplement_status()
        self.oxelx = self.oxels[0]
        self.oxely = self.oxels[1]
        self.alpha_step = alpha_step
        self.show_infos = True
        BaseViewerTk.__init__(self, petro_model, suppl_wm_title=suppl_wm_title, *args, **kwargs)
        self.init_cumulate_modal()
        self.cumulate_finder_method = 'BVLS'
        self.cumulate_finder_norm = 'euclidian'
        self.fill_frame()
        self.adjust_frame_position()
        self.found_cumulate_row = None

    def set_supplement_status(self):
        self.supplement_status = []

    # init cumulate modal composition
    def init_cumulate_modal(self):
        value_per_mineral = 100 / len(self.minerals)
        self.default_cumulate = {mineral: value_per_mineral for mineral in self.minerals}
        self.cumulate_modal = self.default_cumulate.copy()
        total = 0
        for mineral, val in self.default_cumulate.items():
            total += float_or_zero(val)
        self.solid_total = total

        self.missing_minerals = []
        for mineral in self.cumulate_modal.keys():
            if mineral not in self.minerals:
                self.missing_minerals.append(mineral)
        self.missing_oxels = []
        for element in self.parent_elements:
            if element not in self.model.oxel_list:
                self.missing_oxels.append(element)

    def update_parent_conc(self):
        new_parent_conc = self.parent.copy()
        for label, entry in self.parental_conc_widget:
            new_parent_conc[label.cget("text")] = float(entry.get())
        self.parent = new_parent_conc

    def update_cumulate_modal(self):
        new_mineral_props = {}
        total = 0
        for label, entry in self.cumulate_modal_widgets:
            new_mineral_props[label.cget("text")] = float_or_zero(entry.get())
            total += float_or_zero(entry.get())
        total_new_label, total_color = total_label_color(total)
        self.label_total.config(text=total_new_label, fg=total_color)
        self.cumulate_modal = new_mineral_props
        self.solid_total = total

    def update_oxelx(self, _event):  # update_selected_phase
        self.oxelx = self.oxelx_selector.get()
        self.oxely = self.oxely_selector.get()
        self.refresh_plotting()

    def update_oxely(self, _event):  # update_selected_phase
        self.oxely = self.oxely_selector.get()
        self.refresh_plotting()

    def refresh_model(self):
        self.update_parent_conc()
        self.update_cumulate_modal()
        self.refresh_cumulate_concentrations()

    def refresh_model_and_plot(self):
        self.refresh_model()
        self.refresh_plotting()

    def update_minerals_data(self, event):
        new_data_minerals = self.minerals_tree.data_tab
        self.model.set_minerals_data(new_data_minerals)
        self.refresh_cumulate_concentrations()

    def _reset_cumulate_modal(self):
        for index, (label, entry) in enumerate(self.cumulate_modal_widgets):
            entry.delete(0, tk.END)  # Clear the current content
            if label.cget("text") in self.default_cumulate.keys():
                entry.insert(0, self.default_cumulate[label.cget("text")])
        self.refresh_plotting()

    def event_reset_cumulate_modal(self):
        self._reset_cumulate_modal()

    def update_cumulate_finder_method(self, _event):
        self.cumulate_finder_method = self.method_selector.get()

    def update_cumulate_finder_norm(self, _event):
        self.cumulate_finder_norm = self.norm_selector.get()

    def _find_cumulate_frame(self):
        self.finder_level = tk.Toplevel(self.root)
        self.finder_level.title("Search for a cumulate")
        content = tk.Frame(self.finder_level)
        content.pack(side="top")
        content_left = tk.Frame(content)
        content_left.pack(side="left")
        content_right = tk.Frame(content)
        content_right.pack(side="right")
        bottom = tk.Frame(self.finder_level)
        bottom.pack(side="top")

        # Cumulate in content_left
        tk.Label(content_left, text="Cumulate modal composition :").grid(row=0, column=0, columnspan=2, sticky="ew")
        self.cumulate_finder_widgets = list()
        for index, (mineral, value) in enumerate(self.cumulate_modal.items()):
            label = tk.Label(content_left, text=mineral)
            entry = tk.Entry(content_left, width=10)
            entry.insert(0, str(value))
            self.cumulate_finder_widgets.append((label, entry))
        for index, (label, entry) in enumerate(self.cumulate_finder_widgets):  # +1 in the grid
            label.grid(row=index + 1, column=0, sticky=tk.W, pady=2)
            entry.grid(row=index + 1, column=1, sticky=tk.W, pady=2)

        # Child concentration in content_right
        tk.Label(content_right, text="Residual composition to get :").grid(row=0, column=0, columnspan=2, sticky="ew")
        if self.child is not None:
            comp_to_show = self.child
        else:
            comp_to_show = self.parent()

        self.finder_widgets_child = list()
        for index, (oxel, value) in enumerate(comp_to_show.items()):
            label = tk.Label(content_right, text=oxel)
            entry = tk.Entry(content_right, width=10)
            entry.insert(0, value)
            self.finder_widgets_child.append((label, entry))

        for index, (label, entry) in enumerate(self.finder_widgets_child):  # +1 in the grid
            label.grid(row=index + 1, column=0, sticky=tk.W, pady=2)
            entry.grid(row=index + 1, column=1, sticky=tk.W, pady=2)

        tk.Label(bottom, text="Research method").grid(row=0, column=0)
        methods = ['NNLS', 'BVLS', 'RS', 'GD']
        self.method_selector = ttk.Combobox(bottom, width=8, values=methods)
        self.method_selector.set(self.cumulate_finder_method)
        self.method_selector.grid(row=1, column=0)
        self.method_selector.bind("<<ComboboxSelected>>", self.update_cumulate_finder_method)

        tk.Label(bottom, text="Norm").grid(row=0, column=1)
        methods = ['euclidian', 'max', 'min', 'MAE', 'MSE', 'RMSE', 'SMAPE']
        self.norm_selector = ttk.Combobox(bottom, width=8, values=methods)
        self.norm_selector.set(self.cumulate_finder_norm)
        self.norm_selector.grid(row=1, column=1)
        self.norm_selector.bind("<<ComboboxSelected>>", self.update_cumulate_finder_norm)

        compute_cumulate_btn = tk.Button(bottom, text="Compute cumulate", command=self.event_search_cumulate)
        compute_cumulate_btn.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=4, pady=4)
        self.use_cumulate_btn = tk.Button(bottom, text="Use cumulate", fg='red', command=self.event_use_cumulate)
        self.use_cumulate_btn.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=4, pady=4)

        self.finder_level.grab_set()
        self.finder_level.lift()
        self.finder_level.focus_force()

    def event_find_cumulate_frame(self):
        self._find_cumulate_frame()

    def event_search_cumulate(self):
        finder = CumulateFinder(self.model.minerals_data.T.reset_index(),
                                verbose=1, optimizer=self.cumulate_finder_method, norm=self.cumulate_finder_norm)
        self.child_test = self.parent.copy()
        for label, entry in self.finder_widgets_child:
            self.child_test[label.cget("text")] = float(entry.get())

        df_props, df_suppl, fracts_list = finder.find_cumulate_to_remove(self.parent, self.child_test)

        # Select a proportion of the cumulate to extract (alpha)
        select_alpha_level = tk.Toplevel(self.finder_level)
        select_alpha_level.grab_set()
        tk.Label(select_alpha_level, text="Choose a cumulate proportion value :").pack(pady=(0, 10))
        combo = ttk.Combobox(select_alpha_level, values=fracts_list, state="readonly")
        combo.pack()
        combo.current(0)  # Select the first item by default

        def on_ok():
            value = combo.get()
            index = fracts_list.index(float(value)) if float(value) in fracts_list else None

            # Get a composition by the index of the alpha value
            row_selected = df_props.iloc[index][:-1]
            row_selected_dict = row_selected.to_dict()
            self.found_cumulate_row = row_selected_dict

            # Update the displayed infos in cumulate finder toplevel
            for index, (label, entry) in enumerate(self.cumulate_finder_widgets):
                entry.delete(0, tk.END)  # Clear the current content
                if label.cget("text") in row_selected_dict.keys():
                    entry.insert(0, row_selected_dict[label.cget("text")])

            select_alpha_level.destroy()
            self.use_cumulate_btn.config(fg= "green")

        tk.Button(select_alpha_level, text="OK", command=on_ok).pack(pady=(10, 0))
        self.finder_level.wait_window(select_alpha_level)

    def event_use_cumulate(self):
        if self.found_cumulate_row:
            for index, (label, entry) in enumerate(self.cumulate_modal_widgets):
                entry.delete(0, tk.END)  # Clear the current content
                if label.cget("text") in self.found_cumulate_row.keys():
                    entry.insert(0, self.found_cumulate_row[label.cget("text")])
        self.child = self.child_test.copy()

        self.finder_level.destroy()
        self.refresh_plotting()

    def _reset_parent_conc(self):
        for index, (label, entry) in enumerate(self.parental_conc_widget):
            entry.delete(0, tk.END)  # Clear the current content
            entry.insert(0, self.default_parent_conc[label.cget("text")])  # Insert the new content

    def reset_parent_conc(self):
        self._reset_parent_conc()
        self.refresh_model()
        self.refresh_plotting()

    def _reset_minerals_data(self):
        self.model.reset_minerals_data()
        self.refresh_minerals_treeview()

    def event_reset_minerals_data(self):
        self._reset_minerals_data()
        self.refresh_plotting()

    def refresh_minerals_treeview(self):
        for row in self.minerals_tree.get_children():
            self.minerals_tree.delete(row)
        for index, row in self.model.minerals_data.iterrows():
            self.minerals_tree.insert("", tk.END, iid=index, values=[index] + row.tolist())

    def refresh_cumulate_concentrations(self):
        for row in self.cumulate_modal_tree.get_children():
            self.cumulate_modal_tree.delete(row)
        self.cumulate_conc = self.model.modal_props_to_concentration(self.cumulate_modal)
        for oxel, val in self.cumulate_conc.items():
            self.cumulate_modal_tree.insert("", tk.END,tags=('inert',), values=(oxel, val))

    def draw(self, **kwargs):
        self.ax.scatter(self.cumulate_conc[self.oxelx], self.cumulate_conc[self.oxely], marker='o', color='k',
                        label="Cumulate")
        self.ax.scatter(self.parent[self.oxelx], self.parent[self.oxely], marker='s', color='g', label="Parent")
        if self.child is not None:
            self.ax.scatter(self.child[self.oxelx], self.child[self.oxely], marker='D', color='m', label="Child")
        self.draw_model()
        self.ax.set_xlabel(self.oxelx)
        self.ax.set_ylabel(self.oxely)
        if self.show_legend:
            self.ax.legend()
        self.canvas.draw()

    def draw_model(self):
        max_extraction = self.model.compute_alpha_limit_removal(self.parent, Series(self.cumulate_conc))
        fracts = np.arange(0, min(max_extraction, 1.01), self.alpha_step)
        fracts = np.append(fracts, min(max_extraction, 1.01))
        valx = self.model.get_residual_liq_concentration(self.oxelx, self.cumulate_modal, self.parent, fracts)
        valy = self.model.get_residual_liq_concentration(self.oxely, self.cumulate_modal, self.parent, fracts)

        if self.show_infos:
            for i in range(1, len(fracts)):
                self.ax.annotate(str(round(fracts[i], 2)), (valx[i], valy[i]))

        if max_extraction < 1 - self.alpha_step:
            s_fracts = np.arange(fracts[-2] + self.alpha_step, 1.0, self.alpha_step)
            s_valx = self.model.get_residual_liq_concentration(self.oxelx, self.cumulate_modal, self.parent, s_fracts)
            s_valy = self.model.get_residual_liq_concentration(self.oxely, self.cumulate_modal, self.parent, s_fracts)

        else:
            s_fracts = np.arange(fracts[-2] + self.alpha_step, 1.0, self.alpha_step)
            s_valx = self.model.get_residual_liq_concentration(self.oxelx, self.cumulate_modal, self.parent, s_fracts)
            s_valy = self.model.get_residual_liq_concentration(self.oxely, self.cumulate_modal, self.parent, s_fracts)

        all_fracts = [*fracts, *s_fracts]
        all_valx = [*valx, *s_valx]
        all_valy = [*valy, *s_valy]
        cmap = merge_colormaps("winter_r", "autumn", max_extraction)
        self.ax.scatter(all_valx[1:], all_valy[1:], marker='x', cmap=cmap, c=all_fracts[1:], vmin=0, vmax=1)
        all_points = np.array([all_valx, all_valy]).T.reshape(-1, 1, 2)
        all_segments = np.concatenate([all_points[:-1], all_points[1:]], axis=1)
        lc = LineCollection(all_segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(all_fracts[:-1])  # Set which values to color by
        line = self.ax.add_collection(lc)  # Add the gradient line
        self.ax.autoscale()  # Auto-rescale to fit data
        cbar = self.fig.colorbar(line, ax=self.ax)
        cbar.set_label('Extracted fraction')

        if max(all_valx) > 100:
            self.ax.set_xlim(right=99.9)
        if min(all_valx) < -5:
            self.ax.set_xlim(left=-10)
        if max(all_valy) > 100:
            self.ax.set_ylim(top=99.9)
        if min(all_valy) < -5:
            self.ax.set_ylim(bottom=-10)

        if self.show_infos:
            for i in range(0, len(s_fracts)):
                self.ax.annotate(str(round(s_fracts[i], 2)), (s_valx[i], s_valy[i]))

    def fill_frame(self):
        BaseViewerTk.fill_frame(self)

        # Sideview
        self.sideview = tk.Frame(self.content)
        self.sideview.pack(side="left")
        pane_high = tk.Frame(self.sideview, )
        pane_high.pack(side='top')
        pane_low = tk.Frame(self.sideview, )
        pane_low.pack(side='bottom')
        pane_one = tk.Frame(self.sideview, width=140, padx=2, pady=2)
        pane_two = tk.Frame(self.sideview, width=140, padx=2, pady=2)
        pane_three = tk.Frame(self.sideview, width=140, padx=2, pady=2)
        pane_one.pack(side="left", anchor="n")
        pane_two.pack(side="left", anchor="n")
        pane_three.pack(side="left", anchor="n")
        pane_tab = tk.Frame(self.content, width=380, padx=2, pady=2)
        pane_tab.pack_propagate(False)
        pane_tab.pack(side="left", fill=tk.BOTH, anchor="n")

        # In sideview

        # Cumulate modal composition
        comp_title = tk.Label(pane_one, text="Cumulate modal composition", anchor=tk.CENTER)
        comp_title.pack(side="top", )
        ttk.Separator(pane_one, orient='horizontal').pack(fill="x")

        proportions_pane = tk.Frame(pane_one)
        proportions_pane.pack(side="top")
        self.cumulate_modal_widgets = []
        total = 0
        for index, (mineral, value) in enumerate(self.cumulate_modal.items()):
            label = tk.Label(proportions_pane, text=mineral)
            entry = EntryWithCallback(proportions_pane, width=10, callback=self.refresh_model)
            entry.insert(0, str(value))
            entry.enable_callback()  # Enabled after initialization
            self.cumulate_modal_widgets.append((label, entry))
            total += value

        for index, (label, entry) in enumerate(self.cumulate_modal_widgets):
            label.grid(row=index, column=0, sticky=tk.W, pady=2)
            entry.grid(row=index, column=1, sticky=tk.W, pady=2)

        # Find cumulate button
        find_cumulate_btn = tk.Button(pane_one, text="Search cumulate", command=self.event_find_cumulate_frame)
        find_cumulate_btn.pack(side='top')

        # Reset modal composition button
        reset_solid_btn = tk.Button(pane_one, text="Reset solid composition", command=self.event_reset_cumulate_modal)
        reset_solid_btn.pack(side='top')

        # Pane two
        cumulate_modal_title = tk.Label(pane_two, text="Cumulate concentrations", anchor=tk.CENTER)
        cumulate_modal_title.pack(side="top", )

        # Create a Treeview widget to display the DataFrame
        self.cumulate_modal_tree = ttk.Treeview(pane_two, columns=("col1", "col2"),
                                                show="headings")
        self.cumulate_modal_tree.heading("col1", text="Element")
        self.cumulate_modal_tree.heading("col2", text="Concentration")
        self.cumulate_modal_tree.column("col1", width=60, anchor="center")
        self.cumulate_modal_tree.column("col2", width=60, anchor="center")

        self.cumulate_conc = self.model.modal_props_to_concentration(self.cumulate_modal)
        for element, coeff in self.cumulate_conc.items():
            self.cumulate_modal_tree.insert("", "end", tags=('inert',), values=(element, coeff))
        self.cumulate_modal_tree.tag_configure(tagname='inert', background='#f0f0f0')
        self.cumulate_modal_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Pane three
        tk.Label(pane_three, text=self.model.init_name, anchor=tk.CENTER).pack(side="top")
        ttk.Separator(pane_three, orient='horizontal').pack(side="top", fill="x")

        concentration_pane = tk.Frame(pane_three)
        concentration_pane.pack(side="top")
        self.parental_conc_widget = []
        for index, (element, value) in enumerate(self.parent.items()):
            label = tk.Label(concentration_pane, text=element)
            entry = tk.Entry(concentration_pane, width=10)
            entry.insert(0, value)
            self.parental_conc_widget.append((label, entry))
        for index, (label, entry) in enumerate(self.parental_conc_widget):
            label.grid(row=index, column=0, sticky=tk.W, pady=2)
            entry.grid(row=index, column=1, sticky=tk.W, pady=2)

        reset_conc_init_btn = tk.Button(pane_three, text="Reset parental concentrations", command=self.reset_parent_conc)
        reset_conc_init_btn.pack()

        # Bottom bar
        ttk.Separator(self.bottombar, orient='horizontal').pack(side="top", fill="x")

        # Oxel selection
        label_oxelx = tk.Label(self.bottombar, text="Oxide/element X", anchor=tk.CENTER)
        label_oxelx.pack(side="left", padx=5)
        self.oxelx_selector = ttk.Combobox(self.bottombar, width=10, values=list(self.oxels))
        self.oxelx_selector.set(self.oxels[0])
        self.oxelx_selector.pack(side="left", padx=5)
        self.oxelx_selector.bind("<<ComboboxSelected>>", self.update_oxelx)
        label_oxely = tk.Label(self.bottombar, text="Oxide/element Y", anchor=tk.CENTER)
        label_oxely.pack(side="left", padx=5)
        self.oxely_selector = ttk.Combobox(self.bottombar, width=10, values=list(self.oxels))
        self.oxely_selector.set(self.oxels[1])
        self.oxely_selector.pack(side="left", padx=5)
        self.oxely_selector.bind("<<ComboboxSelected>>", self.update_oxely)

        ttk.Separator(self.bottombar, orient='vertical').pack(side="left", padx=8, fill="y")
        check_legend = tk.Checkbutton(self.bottombar, text='Show/hide legend', command=self.toggle_legend, )
        check_legend.select()
        check_legend.pack(side="left")

        ttk.Separator(self.bottombar, orient='vertical').pack(side="left", padx=8, fill="y")
        check_infos = tk.Checkbutton(self.bottombar, text='Show/hide information', command=self.toggle_infos)
        check_infos.select()
        check_infos.pack(side="left")

        # Refresh plotting
        ttk.Separator(self.bottombar, orient='vertical').pack(side="left", padx=8, fill="y")
        refresh_plotting_btn = tk.Button(self.bottombar, text="Refresh plotting", command=self.refresh_model_and_plot)
        refresh_plotting_btn.pack(side="left")

        # Status bar
        self.fill_status_bar()

        # Tab view
        # Coefficients Treeview
        label_minerals_tree = tk.Label(pane_tab, text="Minerals compositions", anchor=tk.CENTER)
        label_minerals_tree.pack(side="top")

        # Reset coefficients button in the bottom
        reset_minerals_data_btn = tk.Button(pane_tab, text="Reset mineral compositions",
                                            command=self.event_reset_minerals_data)
        reset_minerals_data_btn.pack(side="bottom", )

        # Treeview
        self.minerals_tree = EditableFloatTreeview(pane_tab, self.model.minerals_data, )
        self.minerals_tree.column('#0', width=0, stretch=tk.NO)  # Hide the first column

        # Define number of columns
        self.minerals_tree['columns'] = ['Element'] + list(self.minerals)

        # Format columns
        for col in self.model.minerals_data.columns:
            self.minerals_tree.column(col, width=60, stretch=False, anchor='w')
            self.minerals_tree.heading(col, text=col)

        # Insert data into the Treeview
        for index, row in self.model.minerals_data.iterrows():
            self.minerals_tree.insert("", tk.END, iid=index, values=[index] + row.tolist())
        self.minerals_tree.column('#1', width=40, stretch=False, anchor='w')

        # Horizontal scrollbar
        hscroll = tk.Scrollbar(pane_tab, orient="horizontal", command=self.minerals_tree.xview)
        hscroll.pack(side="bottom", fill=tk.X)

        self.minerals_tree.configure(xscrollcommand=hscroll.set)
        self.minerals_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.minerals_tree.bind('<<CellUpdated>>', self.update_minerals_data)

        # Extra widgets
        self.extra_widgets()

    def fill_status_bar(self):
        ttk.Separator(self.statusbar, orient='horizontal').pack(side="top", fill="x")

        # Total
        total_label, total_color = total_label_color(self.solid_total)
        tk.Label(self.statusbar, text="Total :").pack(side="left")
        self.label_total = tk.Label(self.statusbar, text=total_label, fg=total_color)
        self.label_total.pack(side="left")

        # About missing minerals or missing oxels
        if len(self.missing_minerals) > 0:
            ttk.Separator(self.statusbar, orient='vertical').pack(side="left", fill="y")
            label_content = "Minerals missing in the dataset: " + str(self.missing_minerals)
            tk.Label(self.statusbar, text=label_content, fg="#f00").pack(side="left")

        if len(self.missing_oxels) > 0:
            ttk.Separator(self.statusbar, orient='vertical').pack(side="left", fill="y")
            label_content2 = "Elements missing in the dataset: " + str(self.missing_oxels)
            tk.Label(self.statusbar, text=label_content2, fg="#f00").pack(side="left")

        for content in self.supplement_status:
            ttk.Separator(self.statusbar, orient='vertical').pack(side="left", fill="y")
            tk.Label(self.statusbar, text=content, ).pack(side="left")

    def toggle_infos(self):
        self.show_infos = not self.show_infos
        self.refresh_plotting()

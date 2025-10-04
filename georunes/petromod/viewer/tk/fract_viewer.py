import tkinter as tk
from tkinter import ttk
from georunes.petromod.modelers.partition import compute_bulk_coeffs
from georunes.tools.gui.tkwidets.entry_with_callback import EntryWithCallback
from georunes.tools.gui.tkwidets.editable_treeview import EditableFloatTreeview
from georunes.petromod.viewer.tk.base_viewer import BaseViewerTk, total_label_color
from georunes.tools.data import get_key, float_or_zero


class FractViewerTk(BaseViewerTk):
    def __init__(self, petro_model, data_coeffs, initial_conc, solid_comp=None, suppl_wm_title=None, *args, **kwargs):
        self.default_solid = solid_comp
        self.default_coeffs = data_coeffs
        self.default_initial_conc = initial_conc.copy()
        self.current_coeffs = self.default_coeffs.copy()
        self.coeffs_minerals = self.default_coeffs.keys()
        self.coeffs_elements = self.default_coeffs.index.tolist()
        self.initial_conc = initial_conc.copy()
        self.initial_conc_elts = initial_conc.index.tolist()
        self.set_supplement_status()
        self.init_solid_comp()

        BaseViewerTk.__init__(self, petro_model, suppl_wm_title=suppl_wm_title, *args, **kwargs)
        self.init_bulk_coeffs()

        # Concentration choice
        self.phases_labels = self.model.get_phases_labels()
        self.selected_phase = list(self.phases_labels.keys())[0]
        self.plot_title = list(self.phases_labels.values())[0]

        self.fill_frame()
        self.adjust_frame_position()

    def set_supplement_status(self):
        self.supplement_status = []

    def update_initial_conc(self):
        new_conc0 = self.initial_conc.copy()

        for label, entry in self.initial_conc_widgets:
            new_conc0[label.cget("text")] = float(entry.get())
        self.initial_conc = new_conc0

    def init_solid_comp(self):
        self.solid_comp = self.default_solid
        total = 0
        for element, val in self.default_solid.items():
            total += float_or_zero(val)
        total = round(total, 6)
        self.solid_total = total

        self.missing_minerals = []
        for mineral in self.solid_comp.keys():
            if mineral not in self.coeffs_minerals:
                self.missing_minerals.append(mineral)
        self.missing_elements = []
        for element in self.initial_conc_elts:
            if element not in self.coeffs_elements:
                self.missing_elements.append(element)

    def update_solid_comp(self):
        new_mineral_props = {}
        total = 0
        for label, entry in self.solid_comp_widgets:
            new_mineral_props[label.cget("text")] = float_or_zero(entry.get())
            total += float_or_zero(entry.get())
        total = round(total, 6)
        total_new_label, total_color = total_label_color(total)
        self.label_total.config(text=total_new_label, fg=total_color)
        self.solid_comp = new_mineral_props
        self.solid_total = total

    def get_selected_phase(self):
        return self.phase_selector.get()

    def update_selected_phase(self, _event):
        selected_label = self.get_selected_phase()
        selected_value = get_key(self.phases_labels, selected_label)
        self.selected_phase = selected_value
        self.plot_title = selected_label
        self.refresh_plotting()

    def refresh_model(self):
        self.update_initial_conc()
        self.update_solid_comp()
        self.update_bulk_coeffs()

    def refresh_model_and_plot(self):
        self.refresh_model()
        self.refresh_plotting()

    def update_coeffs(self, event):
        new_coeffs = self.coeffs_tree.data_tab
        self.current_coeffs = new_coeffs
        self.update_bulk_coeffs()
        self.refresh_bulk_coeffs_treeview()

    def _reset_solid(self):
        for index, (label, entry) in enumerate(self.solid_comp_widgets):
            entry.delete(0, tk.END)  # Clear the current content
            if label.cget("text") in self.default_solid.keys():
                entry.insert(0, self.default_solid[label.cget("text")])

    def event_reset_solid(self):
        self._reset_solid()

    def _reset_init_conc(self):
        for index, (label, entry) in enumerate(self.initial_conc_widgets):
            entry.delete(0, tk.END)  # Clear the current content
            entry.insert(0, self.default_initial_conc[label.cget("text")])  # Insert the new content

    def reset_init_conc(self):
        self._reset_init_conc()
        self.refresh_model()
        self.refresh_plotting()

    def _reset_coeffs(self):
        self.current_coeffs = self.default_coeffs.copy()
        self.update_bulk_coeffs()
        self.refresh_coeffs_treeview()

    def event_reset_coeffs(self):
        self._reset_coeffs()
        self.refresh_plotting()

    def refresh_coeffs_treeview(self):
        for row in self.coeffs_tree.get_children():
            self.coeffs_tree.delete(row)
        for index, row in self.current_coeffs.iterrows():
            self.coeffs_tree.insert("", tk.END, iid=index, values=[index] + row.tolist())

    def refresh_bulk_coeffs_treeview(self):
        for row in self.bulk_coeffs_tree.get_children():
            self.bulk_coeffs_tree.delete(row)
        for element, coeff in self.current_bulk_coeffs.items():
            self.bulk_coeffs_tree.insert("", tk.END, values=(element, coeff))

    def init_bulk_coeffs(self):
        new_bulk_coeffs = compute_bulk_coeffs(self.solid_comp, self.current_coeffs)
        self.model.set_bulk_dist_coeffs(new_bulk_coeffs)
        self.current_bulk_coeffs = new_bulk_coeffs
        if self.verbose > 0:
            print("New bulk partition coefficients")
            print(self.current_bulk_coeffs.to_dict())

    def update_bulk_coeffs(self):
        self.init_bulk_coeffs()
        self.refresh_bulk_coeffs_treeview()

    def draw(self, element=None):
        list_elements = self.model.list_elements()
        concentration_func = self.model.get_phase_concentration_func(self.selected_phase)
        self.ax.set_yscale('log')
        liq_vals = self.liq_fract_values
        liq_vals.sort()

        for element in list_elements:
            values = [concentration_func(element, f, self.initial_conc) for f in liq_vals]
            self.ax.plot(liq_vals, values, label=element, linestyle='-')
        self.ax.set_xlim((0, 1))
        self.ax.set_xlabel('Liquid fraction (F)')
        self.ax.set_ylabel('Concentration')
        self.ax.set_title(self.plot_title)
        self.ax.grid(axis='y', which='both', linestyle='-', color='#e8e8e8')
        if self.model.f_reverse is True:
            self.ax.invert_xaxis()
        if self.show_legend:
            self.ax.legend()
        self.canvas.draw()

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

        # in sideview

        # Compositions
        comp_title = tk.Label(pane_one, text="Modal solid composition", anchor=tk.CENTER)
        comp_title.pack(side="top", )
        ttk.Separator(pane_one, orient='horizontal').pack(fill="x")

        proportions_pane = tk.Frame(pane_one)
        proportions_pane.pack(side="top")
        self.solid_comp_widgets = []
        total = 0
        for index, (oxel, value) in enumerate(self.solid_comp.items()):
            label = tk.Label(proportions_pane, text=oxel)
            entry = EntryWithCallback(proportions_pane, width=10, callback=self.refresh_model)
            entry.insert(0, value)
            entry.enable_callback()  # Enabled after initialization
            self.solid_comp_widgets.append((label, entry))
            total += value

        # Add other minerals existing in dataset
        for mineral in self.coeffs_minerals:
            if mineral not in self.solid_comp.keys():
                label = tk.Label(proportions_pane, text=mineral)
                entry = EntryWithCallback(proportions_pane, width=10, callback=self.refresh_model)
                entry.insert(0, '0')
                entry.enable_callback()  # Enabled after initialization
                self.solid_comp_widgets.append((label, entry))

        for index, (label, entry) in enumerate(self.solid_comp_widgets):
            label.grid(row=index, column=0, sticky=tk.W, pady=2)
            entry.grid(row=index, column=1, sticky=tk.W, pady=2)

        # Reset modal composition
        reset_solid_btn = tk.Button(pane_one, text="Reset solid composition", command=self.event_reset_solid)
        reset_solid_btn.pack()

        # Pane two
        tk.Label(pane_two, text=self.model.init_name, anchor=tk.CENTER).pack(side="top")
        ttk.Separator(pane_two, orient='horizontal').pack(side="top", fill="x")

        concentration_pane = tk.Frame(pane_two)
        concentration_pane.pack(side="top")
        self.initial_conc_widgets = []
        for index, (element, value) in enumerate(self.initial_conc.items()):
            label = tk.Label(concentration_pane, text=element)
            entry = tk.Entry(concentration_pane, width=10)
            entry.insert(0, value)
            self.initial_conc_widgets.append((label, entry))
        for index, (label, entry) in enumerate(self.initial_conc_widgets):
            label.grid(row=index, column=0, sticky=tk.W, pady=2)
            entry.grid(row=index, column=1, sticky=tk.W, pady=2)

        reset_conc_init_btn = tk.Button(pane_two, text="Reset initial composition", command=self.reset_init_conc)
        reset_conc_init_btn.pack()

        # Pane three
        bulk_coeffs_title = tk.Label(pane_three, text="Bulk partition coefficients", anchor=tk.CENTER)
        bulk_coeffs_title.pack(side="top", )

        # Create a Treeview widget to display the DataFrame
        self.bulk_coeffs_tree = ttk.Treeview(pane_three, columns=("col1", "col2"),
                                             show="headings", height=len(self.coeffs_elements))
        self.bulk_coeffs_tree.heading("col1", text="Element")
        self.bulk_coeffs_tree.heading("col2", text="Bulk distribution coeff.")
        self.bulk_coeffs_tree.column("col1", width=60, anchor="center")
        self.bulk_coeffs_tree.column("col2", width=60, anchor="center")
        for element, coeff in self.current_bulk_coeffs.items():
            self.bulk_coeffs_tree.insert("", "end", values=(element, coeff))

        self.bulk_coeffs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.bulk_coeffs_tree.bind('<<CellUpdated>>', self.update_coeffs)

        # Bottom bar
        ttk.Separator(self.bottombar, orient='horizontal').pack(side="top", fill="x")

        # Phase selection
        label_phase = tk.Label(self.bottombar, text="Phase selection", anchor=tk.CENTER)
        label_phase.pack(side="left", padx=5)
        self.phase_selector = ttk.Combobox(self.bottombar, width=30, values=list(self.phases_labels.values()))
        self.phase_selector.set(self.phases_labels[self.selected_phase])
        self.phase_selector.pack(side="left", padx=5)
        self.phase_selector.bind("<<ComboboxSelected>>", self.update_selected_phase)
        ttk.Separator(self.bottombar, orient='vertical').pack(side="left", padx=8, fill="y")

        check_legend = tk.Checkbutton(self.bottombar, text='Show/hide legend', command=self.toggle_legend)
        check_legend.select()
        check_legend.pack(side="left")

        # Refresh plotting
        ttk.Separator(self.bottombar, orient='vertical').pack(side="left", padx=8, fill="y")
        refresh_plotting_btn = tk.Button(self.bottombar, text="Refresh plotting", command=self.refresh_model_and_plot)
        refresh_plotting_btn.pack(side="left")

        # Status bar
        self.fill_status_bar()

        # Tab view
        # Coefficients Treeview

        label_coeffs_tree = tk.Label(pane_tab, text="Coefficients by mineral", anchor=tk.CENTER)
        label_coeffs_tree.pack(side="top")

        # Reset coefficients button in the bottom
        reset_coeffs_btn = tk.Button(pane_tab, text="Reset coefficients", command=self.event_reset_coeffs)
        reset_coeffs_btn.pack(side="bottom", )

        # Treeview
        self.coeffs_tree = EditableFloatTreeview(pane_tab, self.default_coeffs, )
        self.coeffs_tree.column('#0', width=0, stretch=tk.NO)  # Hide the first column

        # Define number of columns
        self.coeffs_tree['columns'] = ['Element'] + list(self.coeffs_minerals)

        # Format columns
        for col in self.current_coeffs.columns:
            self.coeffs_tree.column(col, width=60, stretch=False, anchor='w')  # width=100, minwidth=100
            self.coeffs_tree.heading(col, text=col)

        # Insert data into the Treeview
        for index, row in self.current_coeffs.iterrows():
            self.coeffs_tree.insert("", tk.END, iid=index, values=[index] + row.tolist())
        self.coeffs_tree.column('#1', width=40, stretch=False, anchor='w')

        # Create a horizontal scrollbar
        hscroll = ttk.Scrollbar(pane_tab, orient="horizontal", command=self.coeffs_tree.xview)
        hscroll.pack(side="bottom", fill=tk.X)

        self.coeffs_tree.configure(xscrollcommand=hscroll.set)
        self.coeffs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.coeffs_tree.bind('<<CellUpdated>>', self.update_coeffs)

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

        if len(self.missing_elements) > 0:
            ttk.Separator(self.statusbar, orient='vertical').pack(side="left", fill="y")
            label_content2 = "Elements missing in the dataset: " + str(self.missing_elements)
            tk.Label(self.statusbar, text=label_content2, fg="#f00").pack(side="left")

        for content in self.supplement_status:
            ttk.Separator(self.statusbar, orient='vertical').pack(side="left", fill="y")
            tk.Label(self.statusbar, text=content, ).pack(side="left")

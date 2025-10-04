import tkinter as tk
from tkinter import ttk


class EditableTreeview(ttk.Treeview):
    def __init__(self, master, data_tab, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.data_tab = data_tab.copy()
        self.bind("<Double-1>", self.on_double_click)
        self.editing_item = None
        self.editing_column = None
        self.entry = None

    def on_double_click(self, event):
        item = self.identify_row(event.y)
        column = self.identify_column(event.x)
        if item and column:
            self.start_editing(item, column)

    def start_editing(self, item, column):
        self.editing_item = item
        self.editing_column = column
        col_index = int(column[1:]) - 1

        # Get the current value
        value = self.item(item, "values")[col_index]

        # Create an Entry widget for editing
        bbox = self.bbox(item, column=column)
        if bbox:
            x, y, width, height = bbox
            self.entry = tk.Entry(self)
            self.entry.place(x=x,
                             y=y,
                             width=width)
            self.entry.insert(0, value)
            self.entry.focus_set()

            # Bind the events for saving and cancelling edit
            self.entry.bind('<Return>', lambda e: self.save_edit(col_index))
            self.entry.bind('<Escape>', self.cancel_edit)

    def finish_item_edition(self):
        if self.editing_item and self.entry:
            new_value = self.entry.get()
            col_index = int(self.editing_column[1:]) - 1
            # column = self.heading(col_index)['text']
            values = list(self.item(self.editing_item, "values"))
            values[col_index] = new_value
            self.item(self.editing_item, values=values)

            # Clean up
            self.entry.destroy()
            self.editing_item = None
            self.editing_column = None
            self.entry = None

    def save_edit(self, col_num):
        if self.editing_item and self.entry:
            new_value = self.entry.get()
            col_index = int(self.editing_column[1:]) - 1
            values = list(self.item(self.editing_item, "values"))
            column = self.heading(col_index)['text']
            self.data_tab.loc[self.editing_item, column] = new_value
            values[col_num] = new_value
            self.item(self.editing_item, values=values)

            # Clean up
            self.entry.destroy()
            self.editing_item = None
            self.editing_column = None
            self.entry = None
            self.event_generate('<<CellUpdated>>', when="tail")

    def cancel_edit(self, event):
        self.entry.destroy()

    def on_focus_out(self, event):
        if self.editing_item:
            self.finish_item_edition()

class EditableFloatTreeview(EditableTreeview):
    def save_edit(self, col_num):
        if self.editing_item and self.entry:
            new_value = self.entry.get()
            col_index = int(self.editing_column[1:]) - 1
            values = list(self.item(self.editing_item, "values"))
            column = self.heading(col_index)['text']

            try:
                float_value = float(new_value)
            except ValueError:
                # If conversion fails, do NOT update and just destroy entry
                self.entry.destroy()
                self.editing_item = None
                self.editing_column = None
                self.entry = None
                return  # exit without update

            self.data_tab.loc[self.editing_item, column] = float_value
            values[col_num] = new_value
            self.item(self.editing_item, values=values)

            # Clean up
            self.entry.destroy()
            self.editing_item = None
            self.editing_column = None
            self.entry = None
            self.event_generate('<<CellUpdated>>', when="tail")


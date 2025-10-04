import tkinter as tk


class EntryWithCallback(tk.Entry):
    def __init__(self, parent=None, callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.callback = callback
        self.var = tk.StringVar()
        self.var.trace_add("write", self._on_change)  # Attach the callback
        self.config(textvariable=self.var)
        self.callback_enabled = False

    def _on_change(self, *args):
        if self.callback_enabled and self.callback:
            self.callback()

    def disable_callback(self):
        self.callback_enabled = False

    def enable_callback(self):
        self.callback_enabled = True

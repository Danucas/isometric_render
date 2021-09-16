#!/usr/bin/env python3
from tkinter import *
import uuid
from interface.windows import Window


class OpenDialog(Window):
    """
    Start Dialog, shows an input to open a saved project from file
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'Open saved project'
        self.width = int(self.root.winfo_screenwidth() / 3)
        self.height = int(self.root.winfo_screenheight() / 3)
        self.padding_top = int(self.root.winfo_screenheight() / 3)
        self.display()


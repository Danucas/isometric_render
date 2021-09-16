from tkinter import *
from tkinter.ttk import *
import uuid


class Window():
    width: int
    height: int
    padding_top: 0
    padding_left: 0
    root: Tk
    id: str
    widgets: dict
    title: str

    def __init__(self, root, *args, **kwargs):
        """Defines the root window"""
        self.root = root
        self.id = uuid.uuid4().hex

    def display(self):
        """Attach the dialog to the root"""
        frame = Frame(width=self.width, height=self.height)
        if self.title:
            label = Label(frame, text=self.title)
            label.pack(pady=4, padx=4)
        frame.pack(pady=self.padding_top)

    
    def close(self):
        """Detach the dialog from the root"""


class MainWindow(Window):
    """
    Main UI container
    """
    window = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        print(w, h)
        self.window = self.root.geometry("{}x{}+0+0".format(w, h))
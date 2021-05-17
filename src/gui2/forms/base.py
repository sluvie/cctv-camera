import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox

class BaseWindow:
    win = None

    # initialization
    def __init__(self, title, maximize = False):
        self.win = tk.Tk()
        if len(title) > 0: self.win.title(title)
        self.win.eval('tk::PlaceWindow . center')

        # maximize the window
        if maximize:
            w, h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
            self.win.geometry("%dx%d+0+0" % (w, h))

    # render the form
    def render(self):
        self.win.mainloop()


class BaseDialog:
    def __init__(self, parent, title, window_width=800, window_height=300):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.transient(parent)
        if len(title) > 0: self.top.title(title)

        # position center
        screen_width, screen_height = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.top.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        # can't resize
        self.top.resizable(False, False)
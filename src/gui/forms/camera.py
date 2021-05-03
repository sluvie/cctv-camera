import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox

class CameraWindow:
    win = None

    def __init__(self, win, title):
        self.win = win

        self.win.title(title)
        
        # button
        b1 = tk.Button(self.win, text='Quit', command=self.win.destroy)
        b1.pack(side=tk.BOTTOM, padx=5, pady=5)
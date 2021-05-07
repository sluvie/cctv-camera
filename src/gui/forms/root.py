import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox

import threading

from forms.thumbnail import ThumbnailWindow

class RootWindow:

    win = None

    def __init__(self, title):
        self.win = tk.Tk()
        self.win.title(title)
        self.win.eval('tk::PlaceWindow . center')

        # component
        fields = 'Username', 'Password'
        ents = self.makeform(self.win, fields)
        self.win.bind('<Return>', (lambda event, e=ents: fetch(e)))
        
        # button
        b1 = tk.Button(self.win, text='Show', command=(lambda e=ents: self.signin_callback(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(self.win, text='Quit', command=self.win.quit)
        b2.pack(side=tk.LEFT, padx=5, pady=5)


    def makeform(self, root, fields):
        entries = {}
        for field in fields:
            row = tk.Frame(root)
            lab = tk.Label(row, width=15, text=field, anchor='w')
            ent = tk.Entry(row)
            ent.insert(0, "") # for default value
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            entries[field] = ent
        return (entries)


    def render(self):
        self.win.mainloop()


    def signin_callback(self, entries):
        username = entries['Username'].get()
        password = entries['Password'].get()

        if username == "admin" and password == "215802":
            # show the thumbnail web camera
            thumbnail_window = tk.Toplevel(self.win)
            cameraWindow = ThumbnailWindow(thumbnail_window, "All Camera")
            self.win.withdraw()
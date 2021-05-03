import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox

import threading

from forms.camera import CameraWindow

import ptz.camera as cam

class RootWindow:

    win = None

    def __init__(self, title):
        self.win = tk.Tk()
        self.win.title(title)
        self.win.eval('tk::PlaceWindow . center')

        # component
        fields = 'Ip address', 'Username', 'Password'
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
        ipaddress = entries['Ip address'].get()
        username = entries['Username'].get()
        password = entries['Password'].get()

        ''' new window
        win2 = tk.Toplevel(self.win)
        cameraWindow = CameraWindow(win2, "Camera {}".format(ipaddress))
        '''

        t = threading.Thread(target=cam.capture, args=(ipaddress, username, password))
        t.daemon = True
        t.start()
        t.join()

        self.win.destroy()


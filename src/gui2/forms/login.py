# tkinter
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox

# form
from forms.base import BaseDialog

# models
from models.account import Account_m

class LoginWindow(BaseDialog):

    accountid = -1
    username = ""
    password = ""
    e_username = None
    e_password = None

    def __init__(self, parent, title):
        super().__init__(parent, title, window_width=350, window_height=125)

        # add component
        self.add_component()
        pass

    def add_component(self):
        # username
        f_username = tk.Frame(self.top)
        l_username = tk.Label(f_username, width=15, text="Username", anchor="w")
        self.e_username = tk.Entry(f_username)
        self.e_username.insert(tk.END, 'admin')
        f_username.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        l_username.pack(side=tk.LEFT)
        self.e_username.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        
        # password
        f_password = tk.Frame(self.top)
        l_password = tk.Label(f_password, width=15, text="Password", anchor="w")
        self.e_password = tk.Entry(f_password, show="*")
        self.e_password.insert(tk.END, '') #215802
        f_password.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        l_password.pack(side=tk.LEFT)
        self.e_password.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        
        # button cancel
        b_cancel = tk.Button(self.top, width=10, text='Cancel', command=lambda: self.cancel_callback())
        b_cancel.pack(side=tk.RIGHT, padx=5, pady=5)

        # button ok
        b_ok = tk.Button(self.top, width=10, text='Ok', command=lambda: self.ok_callback())
        b_ok.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # window event
        self.top.protocol("WM_DELETE_WINDOW", self.cancel_callback)


    # login event
    def ok_callback(self):
        # get data entry
        self.username = self.e_username.get()
        self.password = self.e_password.get()

        account = Account_m()
        self.accountid = account.auth(self.username, self.password)

        if self.accountid > 0:
            self.top.destroy()
        else:
            # failed to login
            messagebox.showerror(title=None, message="Account not registered.")
            # reset
            self.accountid = -1
            self.username = ""
            self.password = ""


    # cancel event
    def cancel_callback(self):
        self.accountid = -2
        self.top.destroy()

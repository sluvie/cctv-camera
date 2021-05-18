# tkinter
import tkinter as tk
from tkinter.constants import DISABLED
from tkinter.font import NORMAL
from tkinter.ttk import *
from tkinter import messagebox

# form
from forms.base import BaseDialog

# models
from models.camera import Camera_m


class SettingCameraWindow(BaseDialog):

    camera_list = None

    # component
    tree_camera = None
    e_ipaddress = None
    e_username = None
    e_password = None
    e_idtext = None
    e_ipaddresstext = None
    e_usernametext = None
    e_passwordtext = None
    b_save = None

    
    def __init__(self, parent, title):
        super().__init__(parent, title, window_width=800, window_height=400)

        # models
        self.camera_list = Camera_m()

        # add component
        self.add_component()
        pass


    def add_component(self):

        # tree data camera
        f_tree_camera = Frame(self.top)
        self.tree_camera = Treeview(f_tree_camera, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
        self.tree_camera.pack(side='left')

        vsb = Scrollbar(f_tree_camera, orient="vertical", command=self.tree_camera.yview)
        vsb.pack(side='right', fill='y')
        self.tree_camera.configure(yscrollcommand=vsb.set)

        self.tree_camera.column("#1", width=50, anchor='c')
        self.tree_camera.heading("#1", text="Id")
        self.tree_camera.column("#2", width=150, anchor=tk.CENTER)
        self.tree_camera.heading("#2", text="IP")
        self.tree_camera.column("#3", anchor="w")
        self.tree_camera.heading("#3", text="Username")
        self.tree_camera.column("#4", anchor="w")
        self.tree_camera.heading("#4", text="Password")
        self.tree_camera.column("#5", width=50, anchor='c')
        self.tree_camera.heading("#5", text="Status")

        self.refresh_tree_camera()

        f_tree_camera.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


        # data entry (add / edit)
        f_dataentry = Frame(self.top)

        # id
        self.e_idtext = tk.StringVar()
        l_id = tk.Label(f_dataentry, width=15, text="Id", anchor="w")
        l_idvalue = tk.Label(f_dataentry, width=15, text="", anchor="w", textvariable=self.e_idtext)
        l_id.grid(row=0, column=0)
        l_idvalue.grid(row=0, column=1)

        # ip address
        self.e_ipaddresstext = tk.StringVar()
        l_ipaddress = tk.Label(f_dataentry, width=15, text="Ip address", anchor="w")
        self.e_ipaddress = tk.Entry(f_dataentry, width=50, textvariable=self.e_ipaddresstext)
        self.e_ipaddress.insert(tk.END, '')
        l_ipaddress.grid(row=1, column=0)
        self.e_ipaddress.grid(row=1, column=1)

        # username
        self.e_usernametext = tk.StringVar()
        l_username = tk.Label(f_dataentry, width=15, text="Username", anchor="w")
        self.e_username = tk.Entry(f_dataentry, width=50, textvariable=self.e_usernametext)
        self.e_username.insert(tk.END, '')
        l_username.grid(row=2, column=0)
        self.e_username.grid(row=2, column=1)

        # password
        self.e_passwordtext = tk.StringVar()
        l_password = tk.Label(f_dataentry, width=15, text="Password", anchor="w")
        self.e_password = tk.Entry(f_dataentry, width=50, textvariable=self.e_passwordtext)
        self.e_password.insert(tk.END, '')
        l_password.grid(row=3, column=0)
        self.e_password.grid(row=3, column=1)

        # button save
        f_button = Frame(f_dataentry)
        self.b_save = tk.Button(f_button, width=10, text='Save', command=lambda: self.save_data())
        self.b_save.grid(row=0, column=0)
        self.b_save["state"] = DISABLED
        # button close
        b_close = tk.Button(f_button, width=10, text='Close', command=lambda: self.top.destroy())
        b_close.grid(row=0, column=1)
        f_button.grid(row=4, column=1)

        # event
        self.tree_camera.bind("<<TreeviewSelect>>", self.doubleclick_callback)

        # position pack
        f_dataentry.pack(side=tk.TOP, padx=5, pady=5)

        # reset
        self.reset_data_entry()

    
    # refresh data tree camera
    def refresh_tree_camera(self):
        # delete data tree
        for i in self.tree_camera.get_children():
            self.tree_camera.delete(i)

        # data camera
        # header (id, ip, username, password, status)
        camera_list = self.camera_list.list()
        for row in camera_list:
            self.tree_camera.insert("", tk.END, text=row["id"],
            values=(
                row["id"],
                row["ip"],
                row["username"],
                row["password"],
                "OFF" if row["status"] == -1 else "ON" if row["status"] == 1 else ""
            ))


    # tree camera select
    def doubleclick_callback(self, event):
        try:
            item = self.tree_camera.selection()
            #print('item:', item)
            #print('event:', event)
            item = self.tree_camera.selection()[0]

            # update the data entry
            row = self.tree_camera.item(item, "value")
            self.e_idtext.set(row[0])
            self.e_ipaddresstext.set(row[1])
            self.e_usernametext.set(row[2])
            self.e_passwordtext.set(row[3])

            self.b_save["state"] = NORMAL
        except:
            self.reset_data_entry()


    # reset data entry
    def reset_data_entry(self):
        self.e_idtext.set("-1")
        self.e_ipaddresstext.set("")
        self.e_usernametext.set("")
        self.e_passwordtext.set("")
        self.b_save["state"] = DISABLED

    # save the data (add / edit)
    def save_data(self):
        id = self.e_idtext.get()
        print(id)
        if id == "-1":
            # add
            pass
        else:
            # edit
            row = self.camera_list.get(int(id))
            print(row)
            if row:
                row[0]["ip"] = self.e_ipaddresstext.get()
                row[0]["username"] = self.e_usernametext.get()
                row[0]["password"] = self.e_passwordtext.get()
                if self.camera_list.update(row[0]):
                    # refresh tree
                    self.refresh_tree_camera()
                    self.reset_data_entry()
                    messagebox.showinfo(title=None, message="Saving data successfully.")
                else:
                    messagebox.showerror(title=None, message="Error, data can't be inserted or updated.")
            else:
                messagebox.showerror(title=None, message="Data not found, update failed.")
        pass
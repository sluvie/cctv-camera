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
    e_port = None
    e_username = None
    e_password = None
    e_idtext = None
    e_ipaddresstext = None
    e_porttext = None
    e_usernametext = None
    e_passwordtext = None
    b_add = None
    b_edit = None
    b_delete = None
    b_save = None
    b_cancel = None

    
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
        self.tree_camera.column("#3", width=150, anchor=tk.CENTER)
        self.tree_camera.heading("#3", text="PORT")
        self.tree_camera.column("#4", anchor="w")
        self.tree_camera.heading("#4", text="Username")
        self.tree_camera.column("#5", anchor="w")
        self.tree_camera.heading("#5", text="Password")
        self.tree_camera.column("#6", width=50, anchor='c')
        self.tree_camera.heading("#6", text="Status")

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

        # port
        self.e_porttext = tk.StringVar()
        l_port = tk.Label(f_dataentry, width=15, text="Port", anchor="w")
        self.e_port = tk.Entry(f_dataentry, width=50, textvariable=self.e_ipaddresstext)
        self.e_port.insert(tk.END, '')
        l_port.grid(row=2, column=0)
        self.e_port.grid(row=2, column=1)

        # username
        self.e_usernametext = tk.StringVar()
        l_username = tk.Label(f_dataentry, width=15, text="Username", anchor="w")
        self.e_username = tk.Entry(f_dataentry, width=50, textvariable=self.e_usernametext)
        self.e_username.insert(tk.END, '')
        l_username.grid(row=3, column=0)
        self.e_username.grid(row=3, column=1)

        # password
        self.e_passwordtext = tk.StringVar()
        l_password = tk.Label(f_dataentry, width=15, text="Password", anchor="w")
        self.e_password = tk.Entry(f_dataentry, width=50, textvariable=self.e_passwordtext)
        self.e_password.insert(tk.END, '')
        l_password.grid(row=4, column=0)
        self.e_password.grid(row=4, column=1)

        f_button = Frame(f_dataentry)
        # button add
        self.b_add = tk.Button(f_button, width=10, text='Add', command=lambda: self.add_data())
        self.b_add.grid(row=0, column=0)
        # button edit
        self.b_edit = tk.Button(f_button, width=10, text='Edit', command=lambda: self.edit_data())
        self.b_edit.grid(row=0, column=1)
        # button delete
        self.b_delete = tk.Button(f_button, width=10, text='Delete', command=lambda: self.delete_data())
        self.b_delete.grid(row=0, column=2)
        # button save
        self.b_save = tk.Button(f_button, width=10, text='Save', command=lambda: self.save_data())
        self.b_save.grid(row=0, column=3)
        # button close
        self.b_cancel = tk.Button(f_button, width=10, text='Cancel', command=lambda: self.cancel_addedit())
        self.b_cancel.grid(row=0, column=4)
        f_button.grid(row=5, column=0, columnspan=5)

        # event
        self.tree_camera.bind("<<TreeviewSelect>>", self.doubleclick_callback)

        # position pack
        f_dataentry.pack(side=tk.TOP, padx=5, pady=5)

        # reset
        self.reset_data_entry(1)

    
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
                row["port"],
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
            self.e_porttext.set(row[2])
            self.e_usernametext.set(row[3])
            self.e_passwordtext.set(row[4])
        except:
            self.reset_data_entry(1)


    # reset data entry
    def reset_data_entry(self, status):
        # status 1 : normal
        # status 2 : add
        # status 3 : edit
        if status == 1:
            self.e_idtext.set("-1")
            self.e_ipaddresstext.set("")
            self.e_porttext.set("")
            self.e_usernametext.set("")
            self.e_passwordtext.set("")
            self.e_ipaddress.configure(state=DISABLED)
            self.e_port.configure(state=DISABLED)
            self.e_username.configure(state=DISABLED)
            self.e_password.configure(state=DISABLED)
            self.b_add["state"] = NORMAL
            self.b_edit["state"] = NORMAL
            self.b_delete["state"] = DISABLED
            self.b_save["state"] = DISABLED
            self.b_cancel["state"] = DISABLED
        elif status == 2:
            self.e_idtext.set("-1")
            self.e_ipaddresstext.set("")
            self.e_porttext.set("")
            self.e_usernametext.set("")
            self.e_passwordtext.set("")
            self.e_ipaddress.configure(state=NORMAL)
            self.e_port.configure(state=NORMAL)
            self.e_username.configure(state=NORMAL)
            self.e_password.configure(state=NORMAL)
            self.b_add["state"] = DISABLED
            self.b_edit["state"] = DISABLED
            self.b_delete["state"] = DISABLED
            self.b_save["state"] = NORMAL
            self.b_cancel["state"] = NORMAL
        elif status == 3:
            self.e_ipaddress.configure(state=NORMAL)
            self.e_port.configure(state=NORMAL)
            self.e_username.configure(state=NORMAL)
            self.e_password.configure(state=NORMAL)
            self.b_add["state"] = DISABLED
            self.b_edit["state"] = DISABLED
            self.b_delete["state"] = NORMAL
            self.b_save["state"] = NORMAL
            self.b_cancel["state"] = NORMAL

    # add data
    # edit data
    def add_data(self):
        self.reset_data_entry(2)

    # edit data
    def edit_data(self):
        id = self.e_idtext.get()
        if id == "-1":
            messagebox.showerror(title=None, message="Error, can't edit data.")
        else:
            self.reset_data_entry(3)

    # edit data
    def delete_data(self):
        msgbox = tk.messagebox.askquestion ('Confirmation Delete','Are you sure you want to delete the data',icon = 'warning')
        if msgbox == 'yes':
            id = self.e_idtext.get()
            row = self.camera_list.get(int(id))
            if self.camera_list.delete(row.doc_id, id):
                # refresh tree
                self.refresh_tree_camera()
                self.reset_data_entry(1)
                messagebox.showinfo(title=None, message="Deleting data successfully.")
            else:
                messagebox.showerror(title=None, message="Error, data can't be deleted.")

    # save the data (add / edit)
    def save_data(self):
        id = self.e_idtext.get()
        if id == "-1":
            # add
            newid = self.camera_list.getmaxid()
            row = {
                'id': newid + 1, 
                'ip': self.e_ipaddresstext.get(), 
                'port': self.e_porttext.get(), 
                'username': self.e_usernametext.get(), 
                'password': self.e_passwordtext.get(), 
                'status': -1
            }
            if self.camera_list.insert(row):
                self.refresh_tree_camera()
                self.reset_data_entry(1)
                messagebox.showinfo(title=None, message="Saving data successfully.")
            else:
                messagebox.showerror(title=None, message="Error, data can't be inserted.")
        else:
            # edit
            row = self.camera_list.get(int(id))
            if row:
                row["ip"] = self.e_ipaddresstext.get()
                row["port"] = self.e_porttext.get()
                row["username"] = self.e_usernametext.get()
                row["password"] = self.e_passwordtext.get()
                if self.camera_list.update(row):
                    # refresh tree
                    self.refresh_tree_camera()
                    self.reset_data_entry(1)
                    messagebox.showinfo(title=None, message="Saving data successfully.")
                else:
                    messagebox.showerror(title=None, message="Error, data can't be updated.")
            else:
                messagebox.showerror(title=None, message="Data not found, update failed.")

    # cancel
    def cancel_addedit(self):
        self.reset_data_entry(1)
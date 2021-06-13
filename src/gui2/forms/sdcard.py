# tkinter
import tkinter as tk
from tkinter.constants import DISABLED, NONE
from tkinter.font import NORMAL
from tkinter.ttk import *
from tkinter import messagebox

# form
from forms.base import BaseDialog

# http
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

# models


class SDCardWindow(BaseDialog):


    camera_data = None
    tree = None
    tree_data = None

    
    def __init__(self, parent, title, camera):
        super().__init__(parent, title, window_width=800, window_height=450)

        # add component
        self.camera_data = camera
        self.add_component()
        pass


    def get_url_paths(self, url, username, password, ext='', params={}):
        response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)
        if response.ok:
            response_text = response.text
        else:
            return response.raise_for_status()
        soup = BeautifulSoup(response_text, 'html.parser')
        parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
        return parent


    def add_component(self):
        # tree data
        f_tree = Frame(self.top)
        self.tree = Treeview(f_tree, column=("c1"), show='headings')
        self.tree.pack(side='left')

        vsb = Scrollbar(f_tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.column("#1", width=500, anchor='w')
        self.tree.heading("#1", text="Name")

        f_tree.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        # event
        self.tree.bind("<<TreeviewSelect>>", self.doubleclick_callback)

        # tree data inside folder
        f_tree_data = Frame(self.top)
        self.tree_data = Treeview(f_tree_data, column=("c1"), show='headings')
        self.tree_data.pack(side='left')

        vsb = Scrollbar(f_tree_data, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree_data.configure(yscrollcommand=vsb.set)

        self.tree_data.column("#1", width=500, anchor='w')
        self.tree_data.heading("#1", text="Name")

        f_tree_data.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)


        url = "http://{}:{}/sd/".format(self.camera_data["ip"], self.camera_data["port"])
        ext = ''
        result = self.get_url_paths(url, self.camera_data["username"], self.camera_data["password"], ext)
        
        for row in result:
            f = row.replace(url, '')
            f = f.replace('/sd/', '')
            if f.endswith('/'):
                self.tree.insert("", tk.END, text=f,
                values=(
                    f
                ))


    def doubleclick_callback(self, event):
        try:
            item = self.tree.selection()
            item = self.tree.selection()[0]
            row = self.tree.item(item, "value")
            
            url = "http://{}:{}/sd/{}".format(self.camera_data["ip"], self.camera_data["port"], row[0])
            ext = '.db'
            result = self.get_url_paths(url, self.camera_data["username"], self.camera_data["password"], ext)

            for i in self.tree_data.get_children():
                self.tree_data.delete(i)
            
            for x in result:
                f = x.replace(url, '')
                # example: http://192.168.13.100:12345/sd/20210419//sd/20210419/recdata.db
                f = f.replace("/sd/{}".format(row[0]), '')
                self.tree_data.insert("", tk.END, text=f,
                values=(
                    f
                ))


        except:
            pass
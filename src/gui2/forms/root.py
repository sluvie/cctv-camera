import tkinter as tk
from tkinter.ttk import *
from tkinter import Menu, messagebox
from PIL import Image, ImageTk

# system
import sys
import threading
import time
from collections import deque

# form
from forms.base import BaseWindow
from forms.login import LoginWindow
from forms.settingcamera import SettingCameraWindow
from forms.control_ptz import ControlPTZWindow

# models
from models.account import Account_m
from models.camera import Camera_m

# camera libraries
from ptz.camera import Camera_PTZ

class RootWindow(BaseWindow):

    camera_ptz = None
    camera_list = None
    camera_pause = False

    accountid = -1
    accounttarget = 0
    username = ""
    password = ""

    def __init__(self, title, maximize):
        super().__init__(title, maximize)

        # can't resize
        # self.win.resizable(False, False)
        self.win.attributes('-fullscreen', True)

        self.camera_list = Camera_m()

        # show form login
        do_login = True
        while do_login:
            win_login = LoginWindow(self.win, "Login")
            self.win.wait_window(win_login.top)

            if win_login.accountid:
                if win_login.accountid > 0:
                    self.accountid = win_login.accountid
                    self.username = win_login.username
                    self.password = win_login.password

                    do_login = False

                    self.initialize_component()
                elif win_login.accountid == -2:
                    sys.exit()

    
    # Deleting (Calling destructor)
    def __del__(self):
        camera_ptz = None


    def initialize_component(self):

        # menu bar
        # main menu
        menubar = Menu(self.win)
        appmenu = Menu(menubar, tearoff=0)
        preferencesmenu = Menu(self.win, tearoff=0)
        preferencesmenu.add_command(label="Settings Camera", command=self.show_setting_camera_window)
        appmenu.add_cascade(label="Preferences", menu=preferencesmenu)
        appmenu.add_separator()
        appmenu.add_command(label="Close", command=self.win.quit)
        menubar.add_cascade(label="App Camera", menu=appmenu)
        self.win.config(menu=menubar)
        

        # get data camera
        camera_list = self.camera_list.list()

        # loop all camera (sampling with 1 camera)
        image_camera = []
        button_onoff_camera = []
        columns = 5
        rows = int(abs(len(camera_list) / columns))
        number_camera = 0
        pos_row = 0
        f_camera = tk.Frame(self.win)
        for i in range(0, rows):
            for j in range(0, columns):
                # image
                l_ipcamera = tk.Label(f_camera, text="")
                l_ipcamera.grid(row=pos_row, column=j, padx=5, pady=2)
                #l_ipcamera.bind("<Button>", self.open_url)
                
                # information camera
                f_information_camera = tk.Frame(f_camera)

                # text
                l_camera_text = tk.Label(f_information_camera, text="Camera {}".format(camera_list[number_camera]["ip"]), anchor="e")# label for the video frame
                l_camera_text.grid(row=0, column=0, padx=5, pady=2)

                # button on / off
                color_onoff = "red"
                text_onoff = "OFF"
                if camera_list[number_camera]["status"] == 1:
                    color_onoff = "green"
                    text_onoff = "ON"
                b_onoff = tk.Button(f_information_camera, width=10, text=text_onoff, bg=color_onoff, command=lambda k=camera_list[number_camera]["id"]: self.onoff_callback(k))
                b_onoff.grid(row=0, column=1, padx=5, pady=2)

                # button show
                b_show = tk.Button(f_information_camera, width=10, text='Show', bg="blue", fg="white", command=lambda k=camera_list[number_camera]: self.show_callback(k))
                b_show.grid(row=0, column=2, padx=5, pady=2)

                f_information_camera.grid(row=pos_row+1, column=j, padx=2, pady=2)

                number_camera = number_camera + 1
                image_camera.append(l_ipcamera)
                button_onoff_camera.append(b_onoff)

            pos_row = pos_row + 2

        # 
        f_camera.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=2)




        # TODO
        # must can maintan multiple camera
        # initialization camera
        # self.camera_ptz = Camera_PTZ("192.168.13.100", self.username, self.password)
        
        # setup the update callback
        # self.win.after(0, func=lambda: self.update_all(image_camera, button_onoff_camera))
    

    # setting camera window
    def show_setting_camera_window(self):
        win_setting = SettingCameraWindow(self.win, "Setting Camera")
        self.win.wait_window(win_setting.top)


    # 
    def open_url(self, event):
        camera_label = event.widget
        ipcamera = camera_label.cget("text")
        # open frame camera
        self.camera_ptz.render(ipcamera, self.username, self.password)


    # turn on / off camera
    def onoff_callback(self, id):
        row = self.camera_list.get(id)
        if not row:
            messagebox.showerror(title=None, message="Failed to get data camera.")
        else:
            row[0]["status"] = row[0]["status"] * -1
            result = self.camera_list.update(row[0])
            if not result:
                messagebox.showerror(title=None, message="Failed to update data camera.")


    # show window control camera
    def show_callback(self, camera):
        # temporary, must build with single window
        self.camera_ptz.render(camera["ip"], camera["username"], camera["password"])

        '''
        self.camera_pause = True
        win_control_ptz = ControlPTZWindow(self.win, "Control PTZ")
        self.win.wait_window(win_control_ptz.top)
        self.camera_pause = False
        '''

    # update all component
    def update_all(self, image_camera, button_onoff_camera):
        # get data camera
        camera_list = self.camera_list.list()

        for x in range(len(camera_list)):
            # update button on / off
            color_onoff = "red"
            text_onoff = "OFF"
            if camera_list[x]["status"] == 1:
                color_onoff = "green"
                text_onoff = "ON"
            button_onoff_camera[x].configure(text=text_onoff, bg=color_onoff)
            
            # update image
            self.update_image(image_camera[x], camera_list[x]['status'])
        
        self.win.after(1000, func=lambda: self.update_all(image_camera, button_onoff_camera))


    # update image camera
    def update_image(self, image_label, status):
        if self.camera_pause == False:
            if status == 1:
                try:
                    w, h = self.win.winfo_screenwidth() - 250, self.win.winfo_screenheight() - 250
                    wi = int(abs(w / 5))
                    hi = int(abs(h / 4))
                    a = self.camera_ptz.capture_image(True, wi, hi)
                    print(a)
                    try:
                        b = ImageTk.PhotoImage(image=a)
                        image_label.configure(image=b)
                        image_label.configure(text="")
                        image_label._image_cache = b  # avoid garbage collection        
                        
                        self.win.update()
                    except Exception as e:
                        print(e)
                except:
                    pass
            else:
                image_label.configure(image=None)
                image_label._image_cache = None
                self.win.update()

        else:
            image_label.configure(image=None)
            image_label._image_cache = None
            self.win.update()
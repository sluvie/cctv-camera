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

    # component
    f_camera = None

    camera_pause = False

    accountid = -1
    accounttarget = 0
    username = ""
    password = ""

    # data camera
    camera = None
    camera_list = []
    camera_list_component = []

    def __init__(self, title, maximize):
        super().__init__(title, maximize)

        # can't resize
        # self.win.resizable(False, False)
        self.win.attributes('-fullscreen', True)

        self.camera = Camera_m()

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
        self.camera = None


    def initialize_component(self):

        # menu bar
        # main menu
        menubar = Menu(self.win)
        appmenu = Menu(menubar, tearoff=0)
        preferencesmenu = Menu(self.win, tearoff=0)
        preferencesmenu.add_command(label="Settings Camera", command=self.show_setting_camera_window)
        appmenu.add_cascade(label="Preferences", menu=preferencesmenu)
        appmenu.add_separator()
        appmenu.add_command(label="Refresh", command=self.initialize_list_camera)
        appmenu.add_separator()
        appmenu.add_command(label="Close", command=self.win.quit)
        menubar.add_cascade(label="App Camera", menu=appmenu)
        self.win.config(menu=menubar)

        # show list camera
        self.initialize_list_camera()
    

    # initialize / refresh list camera
    def initialize_list_camera(self):
        # get data camera
        self.camera_list = self.camera.list()

        # loop all camera (sampling with 1 camera)
        self.camera_list_component = []

        columns = 5
        rows = int(abs(len(self.camera_list) / columns) + 0.5)
        
        if not (self.f_camera == None):
            self.f_camera.destroy()
        self.f_camera = tk.Frame(self.win)
        number_camera = 0
        pos_row = 0
        row = 0
        column = 0
        while number_camera < len(self.camera_list):
            # add component
            # image
            l_ipcamera = tk.Label(self.f_camera, text="")
            l_ipcamera.grid(row=row, column=column, padx=5, pady=2)
            
            # information camera
            f_information_camera = tk.Frame(self.f_camera)

            # text
            l_camera_text = tk.Label(f_information_camera, text="Camera {}".format(self.camera_list[number_camera]["ip"]))# label for the video frame
            l_camera_text.grid(row=0, column=0, columnspan=2, padx=5, pady=2)

            # button on / off
            text_onoff = "OFF"
            if self.camera_list[number_camera]["status"] == 1:
                text_onoff = "ON"
            b_onoff = tk.Button(f_information_camera, width=10, text=text_onoff, command=lambda k=self.camera_list[number_camera]["id"]: self.onoff_callback(k))
            b_onoff.grid(row=1, column=0, padx=5, pady=2)

            # button show
            b_show = tk.Button(f_information_camera, width=10, text='Show', command=lambda k=self.camera_list[number_camera]: self.show_callback(k))
            b_show.grid(row=1, column=1, padx=5, pady=2)

            f_information_camera.grid(row=row+1, column=column, padx=2, pady=2)

            # list of component
            cam_function = Camera_PTZ(self.camera_list[number_camera]["ip"], self.username, self.password)
            thread_x = threading.Thread(target=cam_function.connect)
            cam_component = {
                "image": l_ipcamera,
                "button": b_onoff,
                "camera": cam_function,
                "thread": thread_x
            }
            self.camera_list_component.append(cam_component)
            thread_x.start()

            
            # column
            column = column + 1 if column < columns - 1 else 0
            # row
            row = row + 2 if column == 0 else row
            # camera
            number_camera = number_camera + 1
            pos_row = pos_row + 2

        # show on window 
        self.f_camera.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=2)
        
        # setup the update callback
        self.win.after(0, func=lambda: self.update_all())



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
        row = self.camera.get(id)
        if not row:
            messagebox.showerror(title=None, message="Failed to get data camera.")
        else:
            print(row)
            row["status"] = row["status"] * -1
            result = self.camera.update(row)
            if not result:
                messagebox.showerror(title=None, message="Failed to update data camera.")


    # show window control camera
    def show_callback(self, camera):

        for x in range(len(self.camera_list)):
            if self.camera_list[x]["ip"] == camera["ip"]:
                self.camera_list_component[x]["camera"].render()
                break

        


        # temporary, must build with single window
        #camera.render(camera["ip"], camera["username"], camera["password"])

        '''
        self.camera_pause = True
        win_control_ptz = ControlPTZWindow(self.win, "Control PTZ")
        self.win.wait_window(win_control_ptz.top)
        self.camera_pause = False
        '''

    # update all component
    def update_all(self):
        
        for x in range(len(self.camera_list)):
            # update button on / off
            text_onoff = "OFF"
            if self.camera_list[x]["status"] == 1:
                text_onoff = "ON"

            # refresh button
            self.camera_list_component[x]["button"].config(text=text_onoff)
            self.camera_list_component[x]["button"].update()
            
            # update image
            self.update_image(self.camera_list_component[x], self.camera_list[x]['status'])
        
        self.win.after(1000, func=lambda: self.update_all())


    # update image camera
    def update_image(self, camera_component, status):
        if self.camera_pause == False:
            if status == 1:
                try:
                    w, h = self.win.winfo_screenwidth() - 250, self.win.winfo_screenheight() - 250
                    wi = int(abs(w / 5))
                    hi = int(abs(h / 4))
                    a = camera_component["camera"].capture_image(True, wi, hi)
                    try:
                        b = ImageTk.PhotoImage(image=a)
                        camera_component["image"].configure(image=b)
                        camera_component["image"].configure(text="")
                        camera_component["image"]._image_cache = b  # avoid garbage collection        
                        
                        self.win.update()
                    except Exception as e:
                        print(e)
                except:
                    pass
            else:
                camera_component["image"].configure(image=None)
                camera_component["image"]._image_cache = None
                self.win.update()

        else:
            camera_component["image"].configure(image=None)
            camera_component["image"]._image_cache = None
            self.win.update()
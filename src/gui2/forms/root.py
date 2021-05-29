import tkinter as tk
from tkinter.ttk import *
from tkinter import Menu, messagebox
from PIL import Image, ImageTk

# camera
import cv2

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

    # thread
    exit_thumb_thread = False

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
    

    def initialize_component(self):

        # menu bar
        # main menu
        menubar = Menu(self.win)
        appmenu = Menu(menubar, tearoff=0)
        preferencesmenu = Menu(self.win, tearoff=0)
        preferencesmenu.add_command(label="Settings Camera", command=self.show_setting_camera_window)
        appmenu.add_cascade(label="Preferences", menu=preferencesmenu)
        appmenu.add_separator()
        appmenu.add_command(label="Refresh", command=self.refresh)
        appmenu.add_separator()
        appmenu.add_command(label="Close", command=self.close_window)
        menubar.add_cascade(label="App Camera", menu=appmenu)
        self.win.config(menu=menubar)

        # show list camera
        self.initialize_list_camera()
    

    def close_window(self):
        self.win.destroy()
        sys.exit()


    def refresh(self):
        # stop threading
        self.exit_thumb_thread = True
        for x in  range(len(self.camera_list_component)):
            self.camera_list_component[x]["image"] = None
            self.camera_list_component[x]["button"] = None
            self.camera_list_component[x]["camera"] = None
            #self.camera_list_component[x]["thread"] = None
            self.camera_list_component[x]["thread_thumb"] = None

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
            color_onoff = "red"
            if self.camera_list[number_camera]["status"] == 1:
                text_onoff = "ON"
                color_onoff = "green"
            b_onoff = tk.Button(f_information_camera, width=10, text=text_onoff, bg=color_onoff, command=lambda k=self.camera_list[number_camera]["id"]: self.onoff_callback(k))
            b_onoff.grid(row=1, column=0, padx=5, pady=2)

            # list of component
            cam_function = Camera_PTZ(self.camera_list[number_camera]["ip"], self.username, self.password, self.camera_list[number_camera]["status"])
            #thread_connect = threading.Thread(target=cam_function.connect, daemon = True)
            #thread_thumb = threading.Thread(target=self.show_thumbnail, args=(cam_function, number_camera, l_ipcamera), daemon = True)
            cam_component = {
                "image": l_ipcamera,
                "button": b_onoff,
                "camera": cam_function,
                #"thread": threading.Thread(target=cam_function.connect, daemon = True),
                "thread_thumb": threading.Thread(target=self.show_thumbnail, args=(cam_function, number_camera, l_ipcamera), daemon = True)
            }
            self.camera_list_component.append(cam_component)
            
            # button show
            b_show = tk.Button(f_information_camera, width=10, text='Show', command=lambda k=self.camera_list[number_camera]: self.show_callback(k))
            b_show.grid(row=1, column=1, padx=5, pady=2)

            f_information_camera.grid(row=row+1, column=column, padx=2, pady=2)

            
            # column
            column = column + 1 if column < columns - 1 else 0
            # row
            row = row + 2 if column == 0 else row
            # camera
            number_camera = number_camera + 1
            pos_row = pos_row + 2


        # start threading
        self.exit_thumb_thread = False
        for x in  range(len(self.camera_list_component)):
            #self.camera_list_component[x]["thread"].start()
            self.camera_list_component[x]["thread_thumb"].start()


        # show on window 
        self.f_camera.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=2)


    # show thumbnail (loop)
    def show_thumbnail(self, camera, index_camera, camera_image):
        try:
            while True:
                
                if self.exit_thumb_thread == True:
                    break

                if not self.camera_pause:

                    camera.status = self.camera_list[index_camera]["status"]
                
                    # load default image
                    load = Image.open("images/no-camera.png")

                    # check active or not
                    if camera.cam == None:
                        print("camera not ready")
                        camera.connect()
                    elif camera.status == 1:
                        success, frame = camera.cam.read()

                        if not success:
                            camera.connect()
                        else:
                            frame = cv2.resize(frame, (250, 200))
                            load = Image.fromarray(frame)
                    else:
                        pass

                    # refresh the image
                    b = ImageTk.PhotoImage(image=load)
                    camera_image.configure(image=b)
                    camera_image.configure(text="")
                    camera_image._image_cache = b  # avoid garbage collection

                time.sleep(1)
        except:
            pass


    # setting camera window
    def show_setting_camera_window(self):
        win_setting = SettingCameraWindow(self.win, "Setting Camera")
        self.win.wait_window(win_setting.top)


    # turn on / off camera
    def onoff_callback(self, id):
        row = self.camera.get(id)
        if not row:
            messagebox.showerror(title=None, message="Failed to get data camera.")
        else:
            row["status"] = row["status"] * -1
            result = self.camera.update(row)
            if not result:
                messagebox.showerror(title=None, message="Failed to update data camera.")

            text_onoff = "OFF"
            color_onoff = "red"
            if row["status"] == 1:
                text_onoff = "ON"
                color_onoff = "green"

            for x in range(len(self.camera_list)):
                if self.camera_list[x]["ip"] == row["ip"]:
                    self.camera_list[x]["status"] = row["status"]
                    self.camera_list_component[x]["button"].configure(text=text_onoff, bg=color_onoff)


    # show window control camera
    def show_callback(self, camera_list):

        self.camera_pause = True

        # creatte custom form
        #win_ptz = ControlPTZWindow(self.win, camera_list["ip"], camera_list["ip"], camera_list["username"], camera_list["password"])
        #self.win.wait_window(win_ptz.top)


        # render with default form
        for x in range(len(self.camera_list)):
            if self.camera_list[x]["ip"] == camera_list["ip"]:
                self.camera_list_component[x]["camera"].render()
                break

        self.camera_pause = False

# tkinter
import tkinter
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
'''
import tkinter as tk
from tkinter.ttk import *
from tkinter import Menu, messagebox
from PIL import Image, ImageTk
'''

# camera
import cv2

# system
import sys
import threading
import time
from collections import deque
from datetime import datetime

# form
from forms.base import BaseWindow
from forms.login import LoginWindow
from forms.settingcamera import SettingCameraWindow
from forms.sdcard import SDCardWindow
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

        # database camera
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
        menubar = tkinter.Menu(self.win)
        appmenu = tkinter.Menu(menubar, tearoff=0)
        preferencesmenu = tkinter.Menu(self.win, tearoff=0)
        preferencesmenu.add_command(label="Settings Camera", command=self.show_setting_camera_window)
        appmenu.add_cascade(label="Preferences", menu=preferencesmenu)
        # appmenu.add_separator()
        # appmenu.add_command(label="Refresh", command=self.refresh)
        appmenu.add_separator()
        appmenu.add_command(label="Close", command=self.close_window)
        menubar.add_cascade(label="App Camera", menu=appmenu)
        self.win.config(menu=menubar)


        # button pause
        self.btn_pause = tkinter.Button(self.win, text="Pause", bg="yellow", width=20, command=self.on_pause)
        self.btn_pause.pack()
        


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

        # array of camera
        self.camera_list_component = []

        columns = 5
        rows = int(abs(len(self.camera_list) / columns) + 0.5)
        
        if not (self.f_camera == None):
            self.f_camera.destroy()
        
        self.f_camera = tkinter.Frame(self.win)
        number_camera = 0
        pos_row = 0
        row = 0
        column = 0
        while number_camera < len(self.camera_list):
            # add component
            self.addcomponent(self.f_camera, number_camera)

            # thumbnail settings
            # column
            column = column + 1 if column < columns - 1 else 0
            # row
            row = row + 2 if column == 0 else row
            # camera
            number_camera = number_camera + 1
            pos_row = pos_row + 2

        # show on window 
        self.f_camera.pack(side=tkinter.TOP, fill=tkinter.BOTH, padx=5, pady=2)


        self.delay = 0.15

        # start threading
        for x in  range(len(self.camera_list_component)):
            self.camera_list_component[x]["thread_update"].start()


    # add component
    def addcomponent(self, mainframe, number_camera):

        # customization
        text_onoff = "ON" if self.camera_list[number_camera]["status"] == 1 else "OFF"
        color_onoff = "green" if self.camera_list[number_camera]["status"] == 1 else "red"

        f_camera = tkinter.Frame(mainframe)

        # camera canvas
        canvas = tkinter.Canvas(f_camera, width=300, height=200)
        canvas.pack()
        # name camera
        self.l_camera_text = tkinter.Label(f_camera, text="Camera {}".format(self.camera_list[number_camera]["ip"]))
        self.l_camera_text.pack()
        # on / off camera
        self.btn_onoff = tkinter.Button(f_camera, text=text_onoff, bg=color_onoff, width=20, command=lambda k=number_camera: self.onoff(k))
        self.btn_onoff.pack()
        # show ptz form
        self.btn_show_ptz = tkinter.Button(f_camera, text="PTZ", width=20, command=lambda k=number_camera: self.show_ptz_form(k))
        self.btn_show_ptz.pack()
        # show sd card form
        self.btn_show_sdcard = tkinter.Button(f_camera, text="SDCARD", width=20, command=lambda k=number_camera: self.show_sdcard_form(k))
        self.btn_show_sdcard.pack()
        
        f_camera.pack()

        # initialize camera
        vid = Camera_PTZ(
            self.camera_list[number_camera]["ip"], 
            self.camera_list[number_camera]["port"], 
            self.username, self.password, 
            self.camera_list[number_camera]["status"])
        camera_component = {
            "video": vid,
            "canvas": canvas,
            "thread_update": threading.Thread(target=self.update, args=(vid, canvas, number_camera), daemon = True),
        }
        self.camera_list_component.append(camera_component)

    
    # pause
    def on_pause(self):
        self.camera_pause = not self.camera_pause
        text_pause = "Play" if self.camera_pause else "Pause"
        self.btn_pause.configure(text=text_pause)


    # onoff
    def onoff(self, number_camera):
        id = self.camera_list[number_camera]["id"]
        row = self.camera.get(id)

        if not row:
            tkinter.messagebox.showerror(title=None, message="Failed to get data camera.")
        else:
            row["status"] = row["status"] * -1
            result = self.camera.update(row)
            if not result:
                tkinter.messagebox.showerror(title=None, message="Failed to update data camera.")

            # customization
            text_onoff = "ON" if row["status"] == 1 else "OFF"
            color_onoff = "green" if row["status"] == 1 else "red"

            for x in range(len(self.camera_list)):
                if self.camera_list[x]["ip"] == row["ip"]:
                    self.camera_list[x]["status"] = row["status"]
                    self.camera_list_component[x]["button"].configure(text=text_onoff, bg=color_onoff)


    # show window control camera
    def show_ptz_form(self, index):
        # create custom form
        ip = self.camera_list[index]["ip"]
        port = self.camera_list[index]["port"]
        username = self.camera_list[index]["username"]
        password = self.camera_list[index]["password"]
        video = self.camera_list_component[index]["video"]

        self.camera_pause = True
        text_pause = "Play" if self.camera_pause else "Pause"
        self.btn_pause.configure(text=text_pause)

        messagebox.showinfo(title="Info", message="After close PTZ Control, don't forget to click the button Play to start real time camera (Because it's still buggy after close not actually start the camera)")

        win_ptz = ControlPTZWindow(self.win, ip, ip, port, username, password, video)
        self.win.wait_window(win_ptz.top)


    # show sdcard access
    def show_sdcard_form(self, number_camera):
        win_sdcard = SDCardWindow(self.win, "SD CARD", self.camera_list[number_camera])
        self.win.wait_window(win_sdcard.top)


    # setting camera window
    def show_setting_camera_window(self):
        win_setting = SettingCameraWindow(self.win, "Setting Camera")
        self.win.wait_window(win_setting.top)


    # update camera real time
    def update(self, vid, canvas, index):
        try:
            while True:
                if not self.camera_pause:
                    status = self.camera_list[index]["status"]

                    if status == 1:
                        # camera not ready
                        if vid.vid == None:
                            print("camera not ready")

                            # try to connect again
                            vid.connect()
                        # ready
                        else:
                            # Get a frame from the video source
                            ret, frame = vid.get_frame()

                            if ret:
                                frame = cv2.resize(frame, (300, 200)) 
                                photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                                canvas.create_image(0, 0, image = photo, anchor = tkinter.NW)
                
                time.sleep(self.delay)
        except:
            pass
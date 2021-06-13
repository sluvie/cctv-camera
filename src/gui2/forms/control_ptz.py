# tkinter
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk

# camera
import cv2

# system
import time
import threading

# form
from forms.base import BaseWindow
from forms.base import BaseDialog

# camera libraries
from ptz.camera import Camera_PTZ


class ControlPTZWindow(BaseDialog):

    image_camera = None

    ip = ""
    port = 0
    username = ""
    password = ""
    camera = None

    def __init__(self, parent, title, ip, port, username, password):
        super().__init__(parent, title, window_width=800, window_height=600)

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        # add component
        self.add_component()
        
        pass

    def add_component(self):

        f_main = tk.Frame(self.top)

        # frame left
        f_left = tk.Frame(f_main)
        # image label
        self.image_camera = tk.Label(f_left, text="")
        self.image_camera.grid(row=0, column=0, padx=5, pady=2)        
        f_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

        # frame right
        f_right = tk.Frame(f_main)
        # control (left, right, up, down, stop)
        b_up = tk.Button(f_right, width=5, text="UP", command=lambda: self.up_callback())
        b_up.grid(row=0, column=1, padx=5, pady=2)
        b_left = tk.Button(f_right, width=5, text="LEFT", command=lambda: self.left_callback())
        b_left.grid(row=1, column=0, padx=5, pady=2)
        b_right = tk.Button(f_right, width=5, text="RIGHT", command=lambda: self.right_callback())
        b_right.grid(row=1, column=2, padx=5, pady=2)
        b_down = tk.Button(f_right, width=5, text="DOWN", command=lambda: self.down_callback())
        b_down.grid(row=2, column=1, padx=5, pady=2)
        b_stop = tk.Button(f_right, width=5, text="STOP", command=lambda: self.stop_callback())
        b_stop.grid(row=1, column=1, padx=5, pady=2)
        # control (zoom in, zoom out)
        b_zoomin = tk.Button(f_right, width=10, text="ZOOM IN", command=lambda: self.zoomin_callback())
        b_zoomin.grid(row=4, column=0, columnspan=3, padx=5, pady=2)
        b_zoomout = tk.Button(f_right, width=10, text="ZOOM OUT", command=lambda: self.zoomout_callback())
        b_zoomout.grid(row=5, column=0, columnspan=3, padx=5, pady=2)
        f_right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)

        f_main.pack()

        # initialization camera
        self.camera = Camera_PTZ(self.ip, self.port, self.username, self.password, 1)
        thread_connect = threading.Thread(target=self.camera.connect, daemon = True)    
        thread_thumb = threading.Thread(target=self.show_thumbnail, daemon = True)
        thread_connect.start()
        thread_thumb.start()


    # show thumbnail (loop)
    def show_thumbnail(self):
        try:
            while True:

                # load default image
                load = Image.open("images/no-camera.png")

                # check active or not
                if self.camera.cam == None:
                    print("camera ptz not ready")
                else:
                    success, frame = self.camera.cam.read()

                    if not success:
                        self.camera.connect()
                    else:
                        frame = cv2.resize(frame, (500, 500))
                        load = Image.fromarray(frame)

                # refresh the image
                b = ImageTk.PhotoImage(image=load)
                self.image_camera.configure(image=b)
                self.image_camera.configure(text="")
                self.image_camera._image_cache = b  # avoid garbage collection
                #time.sleep(1)
        except:
            pass


    def up_callback(self):
        self.camera.up()


    def down_callback(self):
        self.camera.down()


    def left_callback(self):
        self.camera.left()


    def right_callback(self):
        self.camera.right()


    def stop_callback(self):
        self.camera.stop()


    def zoomin_callback(self):
        self.camera.zoomin()


    def zoomout_callback(self):
        self.camera.zoomout()
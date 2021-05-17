# tkinter
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk

# form
from forms.base import BaseWindow
from forms.base import BaseDialog

# camera libraries
from ptz.camera import Camera_PTZ


class ControlPTZWindow(BaseDialog):

    def __init__(self, parent, title):
        super().__init__(parent, title, window_width=800, window_height=450)

        # add component
        self.add_component()
        
        pass

    def add_component(self):

        f_main = tk.Frame(self.top)

        # frame left
        f_left = tk.Frame(f_main)
        # image label
        l_ipcamera = tk.Label(f_left, text="camera")
        l_ipcamera.grid(row=0, column=0, padx=5, pady=2)        
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
        self.camera_ptz = Camera_PTZ("192.168.13.100", "admin", "215802")
        
        # setup the update callback
        self.top.after(0, func=lambda: self.update_all(l_ipcamera))


    def up_callback(self):
        self.camera_ptz.up()


    def down_callback(self):
        self.camera_ptz.down()


    def left_callback(self):
        self.camera_ptz.left()


    def right_callback(self):
        self.camera_ptz.right()


    def stop_callback(self):
        self.camera_ptz.stop()


    def zoomin_callback(self):
        self.camera_ptz.zoomin()


    def zoomout_callback(self):
        self.camera_ptz.zoomout()


    # update all component
    def update_all(self, image_camera):
        # update image
        self.update_image(image_camera)
        self.top.after(5, func=lambda: self.update_all(image_camera))

    
    # update image camera
    def update_image(self, image_label):
        try:
            wi = 500
            hi = 300
            a = self.camera_ptz.capture_image(True, wi, hi)
            b = ImageTk.PhotoImage(image=a)

            image_label.configure(image=b)
            image_label.configure(text="")
            image_label._image_cache = b  # avoid garbage collection        
            
            self.top.update()
        except Exception as e:
            print(e)
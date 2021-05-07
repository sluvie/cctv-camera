# tkinter
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk

# others
from collections import deque
import time

# camera libraries
from ptz.camera import Camera_PTZ

class ThumbnailWindow:
    win = None
    camera_ptz = None

    def __init__(self, win, title):
        
        self.win = win
        self.win.title(title)
        
        # maximize the window
        w, h = self.win.winfo_screenwidth(), self.win.winfo_screenheight()
        self.win.geometry("%dx%d+0+0" % (w, h))


        # main frame
        frame_main = tk.Frame(self.win)
        frame_main.grid(sticky='news')

        # fps
        fps_label = tk.Label(master=frame_main)# label for fps
        fps_label._frame_times = deque([0]*5)  # arbitrary 5 frame average FPS
        fps_label.grid(row=0, column=0)


        # Create a frame for the canvas with non-zero row&column weights
        frame_canvas = tk.Frame(frame_main)
        frame_canvas.grid(row=1, column=0, pady=(5, 0), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        #frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=2, column=0, sticky="news")

        # camera frame
        frame_camera = tk.Frame(canvas)
        frame_camera.grid(sticky='news')

        # loop all camera (sampling with 1 camera)
        image_camera = []
        rows = 4
        columns = 5
        number_camera = 1
        pos_row = 0
        for i in range(0, rows):
            for j in range(0, columns):
                # image
                image_label = tk.Label(master=frame_camera, text="192.168.13.100")# label for the video frame
                image_label.grid(row=pos_row, column=j)
                image_label.bind("<Button>", self.open_url)


                # text
                text_label = tk.Label(master=frame_camera, text="Camera {}".format(number_camera))# label for the video frame
                text_label.grid(row=pos_row+1, column=j)

                number_camera = number_camera + 1
                image_camera.append(image_label)
            
            pos_row = pos_row + 2

        # Update cameras frames idle tasks to let tkinter calculate buttons sizes
        frame_camera.update_idletasks()

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))

        # initialization camera
        self.camera_ptz = Camera_PTZ("192.168.13.100", "admin", "215802")

        # setup the update callback
        self.win.after(0, func=lambda: self.update_all(image_camera, fps_label))

        # window event
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)


    def close_window(self):
        import sys;sys.exit()


    def open_url(self, event):
        camera_label = event.widget
        ipcamera = camera_label.cget("text")
        # open frame camera
        self.camera_ptz.render(ipcamera, "admin", "215802")


    # update all component
    def update_all(self, image_camera, fps_label):
        self.update_fps(fps_label)
        for x in image_camera:
            self.update_image(x)
        self.win.after(5, func=lambda: self.update_all(image_camera, fps_label))


    # update fps
    def update_fps(self, fps_label):
        frame_times = fps_label._frame_times
        frame_times.rotate()
        frame_times[0] = time.time()
        sum_of_deltas = frame_times[0] - frame_times[-1]
        count_of_deltas = len(frame_times) - 1
        try:
            fps = int(float(count_of_deltas) / sum_of_deltas)
        except ZeroDivisionError:
            fps = 0
        fps_label.configure(text='FPS: {}'.format(fps))


    # update image camera
    def update_image(self, image_label):
        w, h = self.win.winfo_screenwidth() - 250, self.win.winfo_screenheight() - 250
        wi = int(abs(w / 5))
        hi = int(abs(h / 4))
        a = self.camera_ptz.capture_image(True, wi, hi)
        b = ImageTk.PhotoImage(image=a)

        image_label.configure(image=b)
        image_label._image_cache = b  # avoid garbage collection        
        
        self.win.update()
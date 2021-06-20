# tkinter
import tkinter
import PIL.Image
import PIL.ImageTk

# camera
import cv2

# system
import time

# form
from forms.base import BaseDialog

# camera libraries
from ptz.camera import Camera_PTZ


class ControlPTZWindow(BaseDialog):

    def __init__(self, parent, title, ip, port, username, password, video):
        super().__init__(parent, title, window_width=640, window_height=400)
        
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.vid = video

        self.capture_movie = False

        # add component
        self.add_component()
        
        pass

    def add_component(self):

        # open video source (by default this will try to open the computer webcam)
        #self.vid = Camera_PTZ(self.ip, self.port, self.username, self.password)
        if self.vid.vid == None:
            try:
                self.vid.connect()
            except:
                tkinter.messagebox.showinfo(title="Error", message="Unable to open video source")
        

        # main layout
        f_main = tkinter.Frame(self.top)
        
        # frame left
        # Create a canvas that can fit the above video source size
        f_left = tkinter.Frame(f_main)
        self.canvas = tkinter.Canvas(
            f_left, width=500, height=400)
        self.canvas.pack()
        f_left.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=5, pady=5)

        # frame right
        f_right = tkinter.Frame(f_main)
        # snapshot
        self.btn_snapshot = tkinter.Button(
            f_right, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        # movie
        self.btn_movie = tkinter.Button(
            f_right, text="Save MP4", width=50, command=self.movie)
        self.btn_movie.pack(anchor=tkinter.CENTER, expand=True)
        # control
        self.btn_up = tkinter.Button(f_right, text="Up", width=50, command=lambda: self.up_callback())
        self.btn_up.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_down = tkinter.Button(f_right, text="Down", width=50, command=lambda: self.down_callback())
        self.btn_down.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_left = tkinter.Button(f_right, text="Left", width=50, command=lambda: self.left_callback())
        self.btn_left.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_right = tkinter.Button(f_right, text="Right", width=50, command=lambda: self.right_callback())
        self.btn_right.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_stop = tkinter.Button(f_right, text="Stop", width=50, command=lambda: self.stop_callback())
        self.btn_stop.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_zoomin = tkinter.Button(f_right, text="Zoom In", width=50, command=lambda: self.zoomin_callback())
        self.btn_zoomin.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_zoomout = tkinter.Button(f_right, text="Zoom Out", width=50, command=lambda: self.zoomout_callback())
        self.btn_zoomout.pack(anchor=tkinter.CENTER, expand=True)
        f_right.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, padx=5, pady=5)

        f_main.pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.top.mainloop()


    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:                 
            filename = "data/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            tkinter.messagebox.showinfo(title="Capture Success", message="Capture success, data will be stored at {}".format(filename))


    def movie(self):
        if self.capture_movie == False:
            tkinter.messagebox.showinfo(title="Info", message="MP4 capture i'ts still bug (after saving the movie, must close all aplication so the movie can play at video player")


            self.filename = "data/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".mp4"

            # initialize the result of movie
            # We need to set resolutions.
            # so, convert them from float to integer.
            frame_width = int(self.vid.vid.get(3))
            frame_height = int(self.vid.vid.get(4))
            size = (frame_width, frame_height)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.result_movie = cv2.VideoWriter(self.filename, fourcc, 20, size)

            self.btn_movie.configure(text="Click to stop")

            self.capture_movie = True
        else:
            self.capture_movie = False

            self.btn_movie.configure(text="Save MP4")
            tkinter.messagebox.showinfo(title="Capture Success", message="Capture success, data will be stored at {}".format(self.filename))


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            frame2 = cv2.resize(frame, (500, 400)) 
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame2))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

            # toggle for save movie
            if self.capture_movie == True:
                self.result_movie.write(frame)

        self.top.after(self.delay, self.update)


    def up_callback(self):
        self.vid.up()


    def down_callback(self):
        self.vid.down()


    def left_callback(self):
        self.vid.left()


    def right_callback(self):
        self.vid.right()


    def stop_callback(self):
        self.vid.stop()


    def zoomin_callback(self):
        self.vid.zoomin()


    def zoomout_callback(self):
        self.vid.zoomout()
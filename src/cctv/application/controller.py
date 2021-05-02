from datetime import datetime
import json
import numpy as np

import cherrypy
import functools


# CAMERA
import cv2
import base64
import threading
import time

camera_url = 'rtsp://192.168.13.100/1'


class VideoCamera(object):

    frames = {}

    def __init__(self):
        self.cap = cv2.VideoCapture(camera_url)

    def get_frame(self):
        try:
            success, frame = self.cap.read()
            time.sleep(0.5)
            if success:
                frame = cv2.resize(frame, (640, 480))
                ret, data = cv2.imencode('.jpg', frame)
                jpeg_base64 = base64.b64encode(data.tostring()).decode('utf-8')
                return jpeg_base64
            else:
                pass
        except:
            print("An exception occurred")
            self.cap = cv2.VideoCapture(camera_url)
            pass

class Index:

    video_camera = None

    def __init__(self):
        self.video_camera = VideoCamera()
        pass

    @cherrypy.expose
    @cherrypy.tools.template
    def index(self):
        pass


    @cherrypy.tools.template
    def get_data_camera(self):
        if self.video_camera == None:
            self.video_camera = VideoCamera()

        while True:
            with lock:
                data = self.video_camera.get_frame()
                if data != None:
                    return data
        pass


    @cherrypy.expose
    @cherrypy.tools.template
    def camera(self):
        pass


    @cherrypy.expose
    @cherrypy.tools.template
    def login(self):
        pass
    
    @cherrypy.expose
    def broken(self):
        raise RuntimeError('Pretend something has broken')

def errorPage(status, message, **kwargs):
    return cherrypy.tools.template._engine.get_template('page/error.html').render()
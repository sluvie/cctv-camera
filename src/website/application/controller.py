import base64
from datetime import datetime
import json

import cherrypy

#import application.libraries.camera as camera

import cv2

video_source = "rtsp://{}/1".format("192.168.13.100")
camera = cv2.VideoCapture(video_source)



class Index:

    def __init__(self):
        pass
        #self.camera_ip = "192.168.13.100"
        #self.camera = camera.Camera_PTZ(self.camera_ip, "12345", "admin", "215802")
        #self.camera.connect()


    def gen_frames(self):  
        while True:
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


    @cherrypy.expose
    @cherrypy.tools.template
    def index(self):
        pass
        #return {
        #    "camera_ip": self.camera_ip
        #}

    @cherrypy.expose
    @cherrypy.tools.template
    def refresh_camera(self):
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
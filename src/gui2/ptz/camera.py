import cv2
cv2.ocl.setUseOpenCL(False)

import numpy as np
import time
import requests
from requests.auth import HTTPBasicAuth

from PIL import Image, ImageTk

camera_url = 'rtsp://192.168.13.100/1'
username = 'admin'
password = '215802'
exit_program = 0
screen_width = 800
screen_height = 600


screen_width_thumb = 320
screen_height_thumb = 240

URL = "http://192.168.13.100/web/cgi-bin/hi3510/ptzctrl.cgi"


def home_event():
    PARAMS = {'-step': "0", "-act": "home", "-speed": "1"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))

def stop_event():
    PARAMS = {'-step': "0", "-act": "stop", "-speed": "1"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))


def event_keyboard(k):
    global exit_program
    global username
    global password


    if k == 27:
        exit_program = 1

    elif k == ord('w') or k == ord('W'):
        PARAMS = {'-step': "0", "-act": "up", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        
    elif k == ord('a') or k == ord('A'):
        PARAMS = {'-step': "0", "-act": "left", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        
    elif k == ord('s') or k == ord('S'):
        PARAMS = {'-step': "0", "-act": "down", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        
    elif k == ord('d') or k == ord('D'):
        PARAMS = {'-step': "0", "-act": "right", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        
    elif k == ord('z') or k == ord('Z'):
        PARAMS = {'-step': "0", "-act": "zoomin", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.01)
        stop_event()
    
    elif k == ord('x') or k == ord('X'):
        PARAMS = {'-step': "0", "-act": "zoomout", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.01)
        stop_event()

    elif k == ord('h') or k == ord('H'):
        stop_event()    



def capture(p_ipaddress, p_user, p_password):
    global exit_program
    global username
    global password

    # connect to camera
    camera_url = "rtsp://{}/1".format(p_ipaddress)
    username = p_user
    password = p_password


    try:
        cap = cv2.VideoCapture(camera_url)
        exit_program = 0

        while True:
            if exit_program == 1:
                break

            # capture the frames
            success, frame = cap.read()

            if not success:
                time.sleep(0.02)
                break

            frame = cv2.resize(frame, (screen_width, screen_height)) 
            cv2.imshow('frame', frame)

            # grab event keyboard
            event_keyboard(cv2.waitKey(1) & 0xff)

        
        # destroy all camera
        cap.release()
        cv2.destroyAllWindows()
    except:
        pass


# MAIN CLASS FOR CAMERA HANDLE
class Camera_PTZ:

    ipaddress = None
    username = None
    password = None
    status = -1
    cam = None

    # window
    exit_window_frame = False

    def __init__(self, p_ipaddress, p_username, p_password, p_status):
        self.ipaddress = p_ipaddress
        self.username = p_username
        self.password = p_password
        self.status = p_status
        self.exit_window_frame = False

    def connect(self):
        # init the camera
        cam_url = "rtsp://{}/1".format(self.ipaddress)
        try:
            self.cam = cv2.VideoCapture(cam_url)
            print(self.cam)
        except cv2.error as e:
            print(e)

    def disconnect(self):
        self.cam = None

    def capture_image(self, is_thumbnail, width, height):
        try:
            success, frame = self.cam.read()
            if not success:
                return None
            
            if (is_thumbnail):
                frame = cv2.resize(frame, (width, height)) 

            #gray_im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            a = Image.fromarray(frame)
            return (a)
        except:
            return None

    def render(self):
        try:
            self.exit_window_frame = False

            while True:
                if self.exit_window_frame == True:
                    break

                # capture the frames
                success, frame = self.cam.read()

                if not success:
                    #time.sleep(0.01)
                    break

                frame = cv2.resize(frame, (screen_width, screen_height)) 
                cv2.imshow(self.ipaddress, frame)

                # grab event keyboard
                self.event_keyboard(cv2.waitKey(1) & 0xff)

            # destroy all camera
            #cap.release()
            cv2.destroyAllWindows()
        except:
            cv2.destroyAllWindows()
            

    def event_keyboard(self, key):
        if key == 27:
            self.exit_window_frame = True

        elif key == ord('w') or key == ord('W'):
            self.up()
            
        elif key == ord('a') or key == ord('A'):
            self.left()

        elif key == ord('s') or key == ord('S'):
            self.down()

        elif key == ord('d') or key == ord('D'):
            self.right()

        elif key == ord('z') or key == ord('Z'):
            self.zoomin()
        
        elif key == ord('x') or key == ord('X'):
            self.zoomout()

        elif key == ord('h') or key == ord('H'):
            stop_event()


    def left(self):
        global URL
        PARAMS = {'-step': "0", "-act": "left", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))

    def right(self):
        global URL
        PARAMS = {'-step': "0", "-act": "right", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        
    def up(self):
        global URL
        PARAMS = {'-step': "0", "-act": "up", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
    
    def down(self):
        global URL
        PARAMS = {'-step': "0", "-act": "down", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
    
    def stop(self):
        global URL
        PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
    
    def zoomin(self):
        global URL
        PARAMS = {'-step': "0", "-act": "zoomin", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(0.02)
        self.stop()

    def zoomout(self):
        global URL
        PARAMS = {'-step': "0", "-act": "zoomout", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(0.02)
        self.stop()
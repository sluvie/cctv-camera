import cv2
import numpy as np
import sys
import threading
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
        PARAMS = {'-step': "0", "-act": "up", "-speed": "20"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(1)
        stop_event()

    elif k == ord('a') or k == ord('A'):
        PARAMS = {'-step': "0", "-act": "left", "-speed": "20"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(1)
        stop_event()

    elif k == ord('s') or k == ord('S'):
        PARAMS = {'-step': "0", "-act": "down", "-speed": "20"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(1)
        stop_event()

    elif k == ord('d') or k == ord('D'):
        PARAMS = {'-step': "0", "-act": "right", "-speed": "20"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(1)
        stop_event()

    elif k == ord('z') or k == ord('Z'):
        PARAMS = {'-step': "0", "-act": "zoomin", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.02)
        stop_event()
    
    elif k == ord('x') or k == ord('X'):
        PARAMS = {'-step': "0", "-act": "zoomout", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.02)
        stop_event()

    elif k == ord('h') or k == ord('H'):
        home_event()    



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



class Camera_PTZ:

    ipaddress = None
    username = None
    password = None
    cam = None

    def __init__(self, p_ipaddress, p_username, p_password):
        self.ipaddress = p_ipaddress
        self.username = p_username
        self.password = p_password

        # init the camera
        cam_url = "rtsp://{}/1".format(p_ipaddress)
        try:
            self.cam = cv2.VideoCapture(cam_url)
        except:
            pass

    def capture_image(self, is_thumbnail, width, height):
        success, frame = self.cam.read()
        if not success:
            return None
        
        if (is_thumbnail):
            frame = cv2.resize(frame, (width, height)) 

        gray_im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        a = Image.fromarray(gray_im)
        return (a)

    def render(self, p_ipaddress, p_user, p_password):
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
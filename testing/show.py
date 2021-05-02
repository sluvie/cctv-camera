import cv2
import numpy as np
import sys
import threading
import time
import requests
from requests.auth import HTTPBasicAuth

camera_url = 'rtsp://192.168.13.100/1'
username = 'admin'
password = '215802'
exit_program = 0
screen_width = 800
screen_height = 600

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
        time.sleep(0.02)
        stop_event()

    elif k == ord('a') or k == ord('A'):
        PARAMS = {'-step': "0", "-act": "left", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.02)
        stop_event()

    elif k == ord('s') or k == ord('S'):
        PARAMS = {'-step': "0", "-act": "down", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.02)
        stop_event()

    elif k == ord('d') or k == ord('D'):
        PARAMS = {'-step': "0", "-act": "right", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
        time.sleep(0.02)
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



def capture():
    global exit_program

    # connect to camera
    cap = cv2.VideoCapture(camera_url)

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


t = threading.Thread(target=capture)
t.start()


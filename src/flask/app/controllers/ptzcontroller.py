from flask import render_template, Response
from app import app
#from app.models.user import User ## import kelas User dari model

import cv2
import time
import requests
from requests.auth import HTTPBasicAuth
import json
import threading

# database
from app.models.position import PositionDB


ipaddress = "192.168.13.100"
port = "12345"
username = "admin"
password = "215802"
video_source = "rtsp://{}/1".format("192.168.13.100")
camera = cv2.VideoCapture(video_source)
#camera = cv2.VideoCapture(0)

# tools camera
outputFrame = None
lock = threading.Lock()


# CAMERA FUNCTION
def gen_frames(width=800, height=600):
    global outputFrame, lock, camera

    while True:
        # wait until the lock is required
        with lock:
            success, outputFrame = camera.read()  # read the camera frame
        
            if not success:
                camera = cv2.VideoCapture(video_source)
                break
                
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            dim = (width, height)
            resized = cv2.resize(outputFrame, dim) 
            (flag, encodedImage) = cv2.imencode('.jpg', resized)
            #(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
# END OF CAMERA FUNCTION


@app.route('/ptz/video_feed')
def ptz_video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ptz/control', methods = ['GET'])
def ptz_control():
    return render_template(
        'ptz/control.html', 
        title=ipaddress,
        description="")

# send ptz turn left
@app.route('/ptz/left')
def ptz_left():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "left", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz turn right
@app.route('/ptz/right')
def ptz_right():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "right", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz turn up
@app.route('/ptz/up')
def ptz_up():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "up", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz turn down
@app.route('/ptz/down')
def ptz_down():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "down", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz stop
@app.route('/ptz/stop')
def ptz_stop():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz preset
@app.route('/ptz/preset')
def ptz_preset():
    URL = "http://{}:{}/web/cgi-bin/hi3510/param.cgi".format(ipaddress, port)
    PARAMS = {'cmd': "preset", "-act": "goto", "-status":1, "-number": "0"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz zoomin
@app.route('/ptz/zoomin')
def ptz_zoomin():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "zoomin", "-speed": "1"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    time.sleep(0.05)
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz zoomout
@app.route('/ptz/zoomout')
def ptz_zoomout():
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "zoomout", "-speed": "1"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    time.sleep(0.05)
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# capture image
@app.route('/ptz/captureimage')
def ptz_capture_image():
    return {
        "data": None
    }


# save position
@app.route('/ptz/saveposition/{name}')
def save_position(name: str):
    position_db = PositionDB()
    # add
    newid = position_db.getmaxid()
    row = {
        'id': newid + 1, 
        'name': name
    }
    position_db.insert(row)
    return {
        "success": 1
    }
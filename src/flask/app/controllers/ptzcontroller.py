from flask import (
    render_template, 
    g,
    request,
    Response,
    redirect,
    url_for)
from app import app

import cv2
import base64
import time
import requests
from requests.auth import HTTPBasicAuth
import json
import threading
import configparser

# database
from app.models.cameraposition import CameraPosition_m
from app.models.camerasnapshot import CameraSnapshot_m

# config
config = configparser.ConfigParser()
config.readfp(open(r'app/config.ini'))

ipaddress = config.get('CAMERA', 'ipaddress')
port = config.get('CAMERA', 'port')
username = config.get('CAMERA', 'username')
password = config.get('CAMERA', 'password')
cameraid = config.get('CAMERA', 'cameraid')

video_source = "rtsp://{}/1".format(ipaddress)
camera = cv2.VideoCapture(video_source)

# trial camera laptop
#camera = cv2.VideoCapture(0)

# tools camera
outputFrame = None
lock = threading.Lock()
# tools snapshot
dosnapshot = False
snapshot_m = CameraSnapshot_m()


# CAMERA FUNCTION
def gen_frames(width=800, height=600):
    global outputFrame, lock, camera, dosnapshot, cameraid

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

            # do snapshot
            if dosnapshot:
                print("=========================================> SNAPSHOT")
                # save to 
                (flag, encodedImage) = cv2.imencode('.jpg', outputFrame)
                jpg_as_text = base64.b64encode(encodedImage)
                result, message = snapshot_m.insert(jpg_as_text, cameraid, "suli")
                print(message)
                dosnapshot = False

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
    global ipaddress, port, username, password
    
    return render_template(
        'ptz/control.html', 
        title=ipaddress,
        ip=ipaddress,
        port=port,
        description="")

# send ptz turn left
@app.route('/ptz/left/<speed>')
def ptz_left(speed: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "left", "-speed": speed}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz turn right
@app.route('/ptz/right/<speed>')
def ptz_right(speed: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "right", "-speed": speed}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz turn up
@app.route('/ptz/up')
def ptz_up(speed: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "up", "-speed": speed}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz turn down
@app.route('/ptz/down/<speed>')
def ptz_down(speed: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "down", "-speed": speed}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz stop
@app.route('/ptz/stop')
def ptz_stop():
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }

# send ptz zoomin
@app.route('/ptz/zoomin')
def ptz_zoomin():
    global ipaddress, port, username, password
    
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
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "zoomout", "-speed": "1"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    time.sleep(0.05)
    URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(ipaddress, port)
    PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }




# send ptz goto preset
@app.route('/ptz/gotopreset/<number>')
def ptz_gotopreset(number: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/param.cgi".format(ipaddress, port)
    PARAMS = {'cmd': "preset", "-act": "goto", "-status":1, "-number": number}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }


# send ptz set preset
@app.route('/ptz/setpreset/<number>')
def ptz_setpreset(number: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/param.cgi".format(ipaddress, port)
    PARAMS = {'cmd': "preset", "-act": "set", "-status":1, "-number": number}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }


# send ptz remove preset
@app.route('/ptz/removepreset/<number>')
def ptz_removepreset(number: str):
    global ipaddress, port, username, password
    
    URL = "http://{}:{}/web/cgi-bin/hi3510/param.cgi".format(ipaddress, port)
    PARAMS = {'cmd': "preset", "-act": "set", "-status":0, "-number": number}
    r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(username, password))
    return { "success": 1 }




# save position
@app.route('/ptz/saveposition', methods = ['POST'])
def save_position():
    global cameraid
    
    data = request.json
    cameraposition_m = CameraPosition_m()
    result, positionnumber, message = cameraposition_m.insert(data["positionname"], cameraid, "suli")
    return {
        "success": "1" if result else "0",
        "message": message,
        "positionnumber": positionnumber
    }


# delete position
@app.route('/ptz/deleteposition', methods = ['POST'])
def delete_position():
    data = request.json
    cameraposition_m = CameraPosition_m()
    result, message = cameraposition_m.delete(data["camerapositionid"])
    return {
        "success": "1" if result else "0",
        "message": message
    }


# list position
@app.route('/ptz/listposition')
def list_position():
    global cameraid

    cameraposition_m = CameraPosition_m()
    result, message = cameraposition_m.list(cameraid)
    return {
        "success": "1" if result else "0",
        "message": message,
        "data": result
    }







# capture image
@app.route('/ptz/captureimage')
def ptz_capture_image():
    global dosnapshot

    dosnapshot = True
    return {
        "data": None
    }
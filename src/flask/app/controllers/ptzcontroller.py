from flask import (
    render_template, 
    send_file,
    g,
    request,
    Response,
    redirect,
    url_for)
from app import app

import cv2
import base64
import time
import json
import threading
import configparser

# http
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup


# setting
from app.settings import UPLOADS_IMAGES_PATH
from app.settings import UPLOADS_VIDEOS_PATH
from app.settings import DOWNLOADS_PATH

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
def gen_frames(width=320, height=240):
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
                filepath = UPLOADS_IMAGES_PATH
                # save full frame
                filename = "frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"
                cv2.imwrite(filepath + "/" + filename, cv2.cvtColor(outputFrame, cv2.COLOR_RGB2BGR))
                # save thumb frame
                dim = (200, 150)
                resized = cv2.resize(outputFrame, dim) 
                cv2.imwrite(filepath + "/thumb/" + filename, cv2.cvtColor(resized, cv2.COLOR_RGB2BGR))
                
                result, message = snapshot_m.insert(filename, 1, cameraid, "suli")
                dosnapshot = False

            # encode the frame in JPEG format
            dim = (width, height)
            resized = cv2.resize(outputFrame, dim) 
            (flag, encodedImage) = cv2.imencode('.jpg', resized)

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
@app.route('/ptz/up/<speed>')
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


# GALLERY / CAPTURE

# capture image
@app.route('/ptz/captureimage')
def ptz_capture_image():
    global dosnapshot

    dosnapshot = True
    return {
        "data": None
    }


# gallery
@app.route('/ptz/gallery')
def ptz_gallery():
    global ipaddress, cameraid

    galleries, message = snapshot_m.list(cameraid)

    return render_template(
        'ptz/gallery.html', 
        title=ipaddress,
        description="",
        galleries=galleries)


# sdcard
def get_url_paths(url, username, password, ext='', params={}):
    response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)
    if response.ok:
        response_text = response.text
    else:
        return response.raise_for_status()
    soup = BeautifulSoup(response_text, 'html.parser')
    parent = [url + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    return parent


@app.route('/ptz/sdcard/<path>/<isfile>')
def ptz_sdcard(path=None,isfile=0):
    global ipaddress, port, username, password


    # absolutely download file
    if isfile == "1":
        # get name file, take the last array
        f_split = path.split("-")
        filename = f_split[-1]
        
        url_download = path.replace("-", "/")
        url_download = "http://{}:{}/sd/{}".format(ipaddress, port, url_download)
        params = {}
        response = requests.get(url_download, auth=HTTPBasicAuth(username, password), params=params)
        print(response)
        if response.ok:
            with open(DOWNLOADS_PATH + filename, 'wb') as f:
                f.write(response.content)
            return send_file(DOWNLOADS_PATH + filename, attachment_filename=filename)
        else:
            return response.raise_for_status()

    else:
        # result data
        sdcard = []

        # prepare the url
        url = "http://{}:{}/sd/".format(ipaddress, port)
        if not path == "root":
            url_path = path.replace("-", "/")
            url = "http://{}:{}/sd/{}/".format(ipaddress, port, url_path)

        # get folder
        result = get_url_paths(url, username, password, '')
        for row in result:
            f = row.replace(url, '')
            
            # only get name of folder / file
            if not path == "root":
                f = f.replace('/sd/{}/'.format(url_path), '')
            else:
                f = f.replace('/sd/', '')

            # pick only folder not file
            if f.endswith('/'):
                data = {
                    "name": f.rstrip(f[-1]),
                    "path": f.rstrip(f[-1]) if path == "root" else path + "-" + f.rstrip(f[-1]),
                    "isfile": 0
                }
                sdcard.append(data)

        # get db file
        result = get_url_paths(url, username, password, '.265')
        for row in result:
            f = row.replace(url, '')
            
            # only get name of folder / file
            if not path == "root":
                f = f.replace('/sd/{}/'.format(url_path), '')
            else:
                f = f.replace('/sd/', '')

            # pick files
            data = {
                "name": f,
                "path": f if path == "root" else path + "-" + f,
                "isfile": 1
            }
            sdcard.append(data)

        return render_template(
            'ptz/sdcard.html', 
            title=ipaddress,
            description="",
            sdcard=sdcard)
import cv2

import time
import requests
from requests.auth import HTTPBasicAuth

from PIL import Image, ImageTk
import base64

exit_program = 0
screen_width = 800
screen_height = 600

screen_width_thumb = 320
screen_height_thumb = 240

# MAIN CLASS FOR CAMERA HANDLE
class Camera_PTZ:

    ipaddress = None
    port = None
    username = None
    password = None
    status = -1

    # camera
    vid = None
    width = 0
    height = 0

    # window
    exit_window_frame = False


    def __init__(self, p_ipaddress, p_port, p_username, p_password, p_status = 1):
        # initialize
        self.ipaddress = p_ipaddress
        self.port = p_port
        self.username = p_username
        self.password = p_password
        self.status = p_status
        self.exit_window_frame = False


    # connect to camera
    def connect(self):
        # init the camera
        video_source = "rtsp://{}/1".format(self.ipaddress)
        try:
            # Open the video source
            self.vid = cv2.VideoCapture(video_source)
            if not self.vid.isOpened():
                print("Unable to open video source {}".format(video_source))
                raise ValueError("Unable to open video source", video_source)
            else:
                print(self.vid)

            # Get video source width and height
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        except cv2.error as e:
            print(e)


    
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (None, None)


    def get_frame_base64(self, width=640, height=480):
        if not self.vid.isOpened():
            self.connect()
            
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                dim = (width, height)
                resized = cv2.resize(frame, dim) 
                ret, buffer = cv2.imencode('.jpg', resized)
                jpg_as_text = base64.b64encode(buffer).decode()
                return (ret, jpg_as_text)
            else:
                return (ret, None)
        else:
            return (None)

    
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid == None:
            pass
        else:
            if self.vid.isOpened():
                self.vid.release()

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
            self.stop()


    def left(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "left", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))

    def right(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "right", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        
    def up(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "up", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
    
    def down(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "down", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
    
    def stop(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "stop", "-speed": "2"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
    
    def zoomin(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "zoomin", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(0.05)
        self.stop()

    def zoomout(self):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "zoomout", "-speed": "1"}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(0.05)
        self.stop()

    def left_degree(self, degree):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "left", "-speed": str(degree)}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(5)
        self.stop()

    def right_degree(self, degree):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "right", "-speed": str(degree)}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(5)
        self.stop()


    def up_degree(self, degree):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "up", "-speed": str(degree)}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(5)
        self.stop()
    
    def down_degree(self, degree):
        URL = "http://{}:{}/web/cgi-bin/hi3510/ptzctrl.cgi".format(self.ipaddress, self.port)

        PARAMS = {'-step': "0", "-act": "down", "-speed": str(degree)}
        r = requests.get(url = URL, params = PARAMS, auth = HTTPBasicAuth(self.username, self.password))
        time.sleep(5)
        self.stop()

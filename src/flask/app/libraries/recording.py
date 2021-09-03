import cv2
import threading
import time

# config
import configparser
config = configparser.ConfigParser()
config.readfp(open(r'app/config.ini'))

# tools camera
lock = threading.Lock()

# database
from app.settings import UPLOADS_IMAGES_PATH
from app.settings import UPLOADS_VIDEOS_PATH

class VideoCamera(object):

    def __init__(self):
        # Open a camera
        self.ipaddress = config.get('CAMERA', 'ipaddress')
        self.port = config.get('CAMERA', 'port')
        self.username = config.get('CAMERA', 'username')
        self.password = config.get('CAMERA', 'password')
        self.cameraid = config.get('CAMERA', 'cameraid')

        video_source = "rtsp://{}/1".format(self.ipaddress)
        #video_source = 0
        self.cap = cv2.VideoCapture(video_source)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            # show the frame camera
            resized = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            ret, jpeg = cv2.imencode('.jpg', resized)

            # save / record
            if self.is_record:
                self.out.write(frame)

            return ret, jpeg.tobytes()
        else:
            return None, None

    def start_record(self):
        self.is_record = True

        filepath = UPLOADS_VIDEOS_PATH
        self.filename_video = "video-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".mp4"

        frame_width  = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        size = (frame_width, frame_height)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(filepath + self.filename_video,fourcc, 20.0, size)

    def stop_record(self):
        self.is_record = False
        self.out.release()
        return self.filename_video
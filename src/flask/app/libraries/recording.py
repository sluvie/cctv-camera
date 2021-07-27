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

class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        filepath = UPLOADS_VIDEOS_PATH
        filename_video = "video-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".avi"
        
        '''
        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(filepath + filename_video,fourcc, 20.0, (800,600))
        '''
        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter(filepath + filename_video,fourcc, 20.0, (640,480))


    def run(self):
        while self.isRunning:
            with lock:
                ret, frame = self.cap.read()
                if ret:
                    self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()



class VideoCamera(object):

    def __init__(self):
        # Open a camera
        self.ipaddress = config.get('CAMERA', 'ipaddress')
        self.port = config.get('CAMERA', 'port')
        self.username = config.get('CAMERA', 'username')
        self.password = config.get('CAMERA', 'password')
        self.cameraid = config.get('CAMERA', 'cameraid')

        video_source = "rtsp://{}/1".format(self.ipaddress)
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
            ret, jpeg = cv2.imencode('.jpg', frame)
            return ret, jpeg.tobytes()
        else:
            return None, None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()
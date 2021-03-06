import cv2
import sys
import threading
from sensecam_control import vapix_control


ip = '192.168.13.100'
login = 'admin'
password = '215802'

exit_program = 0


def event_keyboard(k):
    global exit_program

    if k == 27:  # esc
        exit_program = 1

    elif k == ord('e') or k == ord('E'):
        X.absolute_move(0.02, 0.60, 0.0)

    elif k == ord('w') or k == ord('W'):
        X.relative_move(None, 1, None)

    elif k == ord('a') or k == ord('A'):
        X.relative_move(-1, None, None)

    elif k == ord('s') or k == ord('S'):
        X.relative_move(None, -1, None)

    elif k == ord('d') or k == ord('D'):
        X.relative_move(1, None, None)

    elif k == ord('h') or k == ord('H'):
        X.go_home_position()


def capture(ip_camera):
    global exit_program

    #url http login axis camera
    #ip2 = 'http://' + login + ':' + password + '@' + ip_camera + '/mjpg/1/video.mjpg?'

    #url rtsp axis camera
    ip2 = 'rtsp://' + ip_camera + '/1'

    cap = cv2.VideoCapture(ip2)

    while True:
        ret, frame = cap.read()
        if ret is not False:
            break

    while True:
        ret, frame = cap.read()

        if exit_program == 1:
            sys.exit()

        #cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        frame = cv2.resize(frame, (640, 480)) 
        cv2.imshow('Camera', frame)
        event_keyboard(cv2.waitKey(1) & 0xff)


X = vapix_control.CameraControl(ip + ':8080', login, password)
t = threading.Thread(target=capture, args=(ip,))
t.start()
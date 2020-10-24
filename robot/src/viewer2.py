#import robotmsg as msg
import io
import numpy as np
import socket

import cv2

import time
import functools
import imutils



class Viewer():


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.1.26', 1884))
            
            bytes=b''

            print("Connected", flush=True)

            last_frame=None

            while True:
                #try:
                bytes+=s.recv(1024)
                start = bytes.find(b'\xff\xd8')
                end = bytes.find(b'\xff\xd9')

                if start != -1 and end != -1:
                    img=bytes[start:end+2]
                    bytes=bytes[end+2:]
                    frame = cv2.imdecode(np.fromstring(img, dtype=np.uint8),cv2.IMREAD_COLOR)

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (21, 21), 0)

                    if last_frame is None:
                        last_frame=gray
                        continue

                    frameDelta = cv2.absdiff(last_frame, gray)
                    thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]

                    thresh = cv2.dilate(thresh, None, iterations=2)

                    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51,51)))

                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    for c in cnts:
                        if cv2.contourArea(c) < 500:
                            cv2.fillPoly(thresh, pts=[c], color=0)
                            continue

                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


                    cv2.imshow('robot', frame)
                    key = cv2.waitKey(1) & 0xFF

                    last_frame=gray.copy()


                #except:
                #    pass


if __name__ == '__main__':
    viewer = Viewer()
    viewer.run()

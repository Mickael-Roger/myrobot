#import robotmsg as msg
import io
import numpy as np
import socket

import cv2

import time
import functools



class Viewer():


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.1.26', 1884))
            
            bytes=b''

            print("Connected", flush=True)

            while True:
                try:
                    bytes+=s.recv(1024)
                    print (bytes)
                    print("---")
                    start = bytes.find('\xff\xd8')
                    end = bytes.find('\xff\xd9')

                    if start != -1 and end != -1:
                        frame=bytes[start:end+2]
                        bytes=bytes[end+2:]
                        img = cv2.imdecode(np.fromstring(frame, dtype=np.uint8),cv2.IMREAD_COLOR)
                        cv2.imshow('robot', img)
                except:
                    pass


if __name__ == '__main__':
    viewer = Viewer()
    viewer.run()

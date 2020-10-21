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
            
            while True:
                data = b''.join(iter(functools.partial(s.recv, 1000), b'---ENDFRAME---'))

                frame = np.load(io.BytesIO(data), allow_pickle=True)
                print("Reicv" + str(type(frame)))



if __name__ == '__main__':
    viewer = Viewer()
    viewer.run()

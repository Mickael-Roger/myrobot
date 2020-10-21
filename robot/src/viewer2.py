#import robotmsg as msg
import io
import numpy as np
import socket

import cv2

import time



class Viewer():


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.1.26', 1884))
            
            while True:
                data = s.recv(500000)
                print("Type: " + str(type(data)) + " " + str(len(data)))
                frame = np.load(io.BytesIO(data), allow_pickle=True)
                print("Reicv" + str(type(frame)))



if __name__ == '__main__':
    viewer = Viewer()
    viewer.run()

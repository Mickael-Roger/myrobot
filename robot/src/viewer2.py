#import robotmsg as msg
import io
import numpy as np
import socket

import cv2

import time



class Viewer():

    def __init__(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.s:
            self.s.connect(('192.168.1.26', 1884))




    def run(self):
        while True:
            data = self.s.recv(1024)
            print("Reicv" + str(data))



if __name__ == '__main__':
    viewer = Viewer()
    viewer.run()

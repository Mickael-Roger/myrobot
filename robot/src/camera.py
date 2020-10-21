import robotmsg as msg
from threading import Thread
import json
import io
import numpy as np
import time

import cv2 as cv

import socket

class Stream(Thread):

    def __init__(self):
        Thread.__init__(self)
        #self.stream = msg.msg(msgName='stream')
        self.stop = 0




    def run(self):
        self.stop = 1
        self.cap = cv.VideoCapture(0)

        while self.stop != 0:
            try:
                if self.cap.isOpened():
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('', 1884))
                        s.listen()
                        conn, addr = s.accept()

                        with conn:      
                            ret, myframe = self.cap.read()
                            if ret:
                                np_bytes = io.BytesIO()
                                np.save(np_bytes, myframe, allow_pickle=True)
                                np_bytes = np_bytes.getvalue()
                                #self.stream.send(msg=np_bytes)
                                conn.sendall(b'Image\n')
            except:
                time.sleep(1)
                pass

     

            
    def stopStream(self):
        self.stop = 0
    




class Camera():

    def __init__(self):
        self.queue = msg.msg(msgName='camera')
        self.stream = None
                    


    def dispatch(self, client, userdata, message):

        print("camera received: " + str(message.payload) + " - " + str(type(message.payload)))
        
        try:
            msg = json.loads(message.payload.decode('utf8'))

            if msg['action'] == 'startstream':
                if self.stream == None :
                    self.stream = Stream()
                    self.stream.start()
            
            elif msg['action'] == 'stopstream':
                if self.stream != None :
                    self.stream.stopStream()
                    self.stream.join()
                    self.stream = None

        except:
            pass



    def start(self):
        self.queue.listen(callback=self.dispatch)



if __name__ == '__main__':
    camera = Camera()
    camera.start()

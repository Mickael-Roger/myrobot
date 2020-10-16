import robotmsg as msg
from threading import Thread
import json

import cv2 as cv


class Stream(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stream = msg.msg(msgName='stream')
        self.stop = 0


    def run(self):
        self.stop = 1
        self.cap = cv.VideoCapture(0)
        if self.cap.isOpened():
            while self.stop != 0:
                ret, myframe = self.cap.read()
                if ret:
                    self.stream.send(msg=myframe)

            
    def stopStream(self):
        self.stop = 0
    




class Camera():

    def __init__(self):
        self.queue = msg.msg(msgName='camera')
        self.stream = None
                    


    def dispatch(self, client, userdata, message):
        
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

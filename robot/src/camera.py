import robotmsg as msg
from threading import Thread, Condition
import json


import socket
import cv2



class Stream(Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = 1

    def start(self):
        self.stop = 0
        self.cap = cv2.VideoCapture(0)

        
        if self.cap.isOpened():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', 1884))
                s.listen()
                conn, addr = s.accept()

                with conn:
                    while self.stop == 0:
                        try:
                            ret, frame = self.cap.read()
                            if ret:
                                _, jpgframe=cv2.imencode('.jpg', frame)
                                conn.sendall(jpgframe)
                        except:
                            pass


    def stopStream(self):
        self.stop = 1

    

    # Later: For each connection start a thread


class Camera():

    def __init__(self):
        self.queue = msg.msg(msgName='camera')
        self.stream = None
        self.server = None
                    


    def dispatch(self, client, userdata, message):

        print("camera received: " + str(message.payload) + " - " + str(type(message.payload)))
        
        try:
            msg = json.loads(message.payload.decode('utf8'))

            if msg['action'] == 'startstream':
                if self.stream == None :
                    self.stream = Stream()
                    print('start')
                    self.stream.start()
                    print('end start')
            
            elif msg['action'] == 'stopstream':
                if self.stream != None :
                    print("stop 1")
                    self.stream.stopStream()
                    print("stop 2")
                    self.stream.join()
                    print("stop 3")
                    self.stream = None
                    print("stop 4")

        except:
            pass



    def start(self):
        self.queue.listen(callback=self.dispatch)



if __name__ == '__main__':
    camera = Camera()
    camera.start()

import robotmsg as msg
from threading import Thread, Condition
import json


import socket
import cv2
import time



class Stream(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = 1

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 1884))

        self.conn = None

    def run(self):
        print("Run")
        self.stop = 0
        self.cap = cv2.VideoCapture(0)
        
        if self.cap.isOpened():
            self.socket.listen()
            self.conn, addr = self.socket.accept()

            while self.stop == 0:
                #self.conn.append(conn)
                #self.socket.setblocking(False)
                
                #if len(self.conn) > 0:
                #for conn in self.conn:
                try:
                    ret, frame = self.cap.read()
                    if ret:
                        _, jpgframe=cv2.imencode('.jpg', frame)
                        self.conn.sendall(jpgframe)
                except:
                    pass
                #else:
                #    time.sleep(0.05)


    def stopStream(self):
        #for conn in self.conn:
        self.stop = 1
        self.conn.close()
        self.socket.close()
        self.cap.release()



class Camera():

    def __init__(self):
        self.queue = msg.msg(msgName='camera')
            

    def dispatch(self, client, userdata, message):

        print("camera received: " + str(message.payload) + " - " + str(type(message.payload)))
        
        try:
            msg = json.loads(message.payload.decode('utf8'))

            if msg['action'] == 'startstream':
                self.stream = Stream()
                self.stream.start()
            
            elif msg['action'] == 'stopstream':
                self.stream.stopStream()
                del self.stream

        except:
            pass



    def start(self):
        self.queue.listen(callback=self.dispatch)



if __name__ == '__main__':
    camera = Camera()
    camera.start()

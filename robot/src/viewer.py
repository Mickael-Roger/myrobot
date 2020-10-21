#import robotmsg as msg
import io
import numpy as np
import paho.mqtt.client as mqtt
import threading

import cv2

import time

frame = None
frameLock = threading.Lock()

class Display(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global frame
        while True:
            frameLock.acquire()
            if frame is not None:
                print("toto")
                cv2.imshow('frame',frame)
                time.sleep(10)
            frameLock.release()
            time.sleep(0.03)
            print(type(frame))


class Viewer():

    def __init__(self):

        #self.queue = msg.msg(msgName='stream')
        self.client = mqtt.Client()
        self.client.connect('192.168.1.26')
        self.client.max_queued_messages_set(24)
        self.time = time.time()




    def dispatch(self, client, userdata, message):
        global frame
        print("Reicv")
        frameLock.acquire()
        frame = np.load(io.BytesIO(message.payload), allow_pickle=True)
        frameLock.release()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #self.time = time.time()
        
        #cv2.waitKey()



    def start(self):
        print("start")
        self.client.subscribe('robot/stream')
        self.client.on_message=self.dispatch
        self.client.loop_forever()
        #self.queue.listen(callback=self.dispatch)


if __name__ == '__main__':
    viewer = Viewer()
    display = Display()
    display.start()
    viewer.start()
    display.join()

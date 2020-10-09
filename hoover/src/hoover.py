import time
import hoovermsg as msg

class Hoover():

    def __init__(self):

        self.services={}
        
        for srv in ('camera',):
            self.services[srv] = msg.msg(msgName=srv)
            
        

    def start(self):
        while True:
            if 'camera' in self.services:
                self.services['camera'].send('{"action": "takePicture"}')
            time.sleep(1)



if __name__ == '__main__':
    hoover = Hoover()
    hoover.start()

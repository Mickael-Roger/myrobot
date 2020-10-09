import robotmsg as msg
import json

class Robot():

    def __init__(self):

        self.services={}
        
        for srv in ('camera', 'motors',):
            self.services[srv] = msg.msg(msgName=srv)

        self.queue = msg.msg(msgName='external')

        self.actions = { "takePicture": self.takePicture,
                         "move": self.move,
                         "videoStream": self.videoStream,
                         "moveCamera": self.moveCamera
                        }



            
    def takePicture(self, params):
        if 'camera' in self.services:
            self.services['camera'].send('{"action": "takePicture"}')


    def move(self, params):
        # If no obstacles
        print("move")
        try:
            if 'motors' in self.services:
                print("move motors " + type(params))
                values = json.loads(params)
                print("move values " + str(values))
                message = { "speed": values['speed'],
                            "left": values['left'],
                            "right": values['right']
                        }
                print("move json " + str(json.dumps(message)))
                self.services['motors'].send(msg=json.dumps(message))

        except:
            print("move error")
            pass



    def videoStream(self, params):
        pass

    def moveCamera(self, params):
        pass


    def dispatch(self, client, userdata, message):

        print("Reicv : " + str(message.payload))
        # Orchestrate actions
        try:
            msg = json.loads(message.payload.decode('utf8'))
            print("loaded")

            if msg['action'] in self.actions:
                print("actions")
                if 'params' not in msg:
                    msg['params'] = ""
                
                print("send")
                self.actions[msg['action']](params=msg['params'])
                print("done")
        except:
            print("error")
            pass



    def start(self):
        # Listen to obstacle in another thread, then update self.thread in consequences

        # Listen to external orders
        self.queue.listen(callback=self.dispatch)


if __name__ == '__main__':
    robot = Robot()
    robot.start()

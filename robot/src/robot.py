import robotmsg as msg
import json

class Robot():

    def __init__(self):

        self.services={}
        
        for srv in ('camera', 'motors',):
            self.services[srv] = msg.msg(msgName=srv)

        self.queue = msg.msg(msgName='external')

        self.actions = { "move": self.move,
                         "video": self.videoStream,
                         "moveCamera": self.moveCamera
                        }



    def move(self, params):
        # If no obstacles
        try:
            if 'motors' in self.services:

                message = { "speed": params['speed'],
                            "left": params['left'],
                            "right": params['right']
                        }
                
                self.services['motors'].send(msg=json.dumps(message))

        except:
            print("move error")
            pass



    def videoStream(self, params):
        if 'camera' in self.services:
            self.services['camera'].send(msg=json.dumps(params))



    def moveCamera(self, params):
        pass


    def dispatch(self, client, userdata, message):
        # Orchestrate actions
        try:
            msg = json.loads(message.payload.decode('utf8'))

            if msg['action'] in self.actions:
                if 'params' not in msg:
                    msg['params'] = {}
                
                self.actions[msg['action']](params=msg['params'])
        except:
            pass



    def start(self):
        # Listen to obstacle in another thread, then update self.thread in consequences

        # Listen to external orders
        self.queue.listen(callback=self.dispatch)


if __name__ == '__main__':
    robot = Robot()
    robot.start()

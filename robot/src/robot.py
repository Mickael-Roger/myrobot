import robotmsg as msg
import json

class Robot():

    def __init__(self):

        self.services={}
        
        for srv in ('camera', 'motors',):
            self.services[srv] = msg.msg(msgName=srv)

        self.queue = msg.msg(msgName='camera')

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

        try:
            if 'motors' in self.services:
                values = json.loads(params.decode('utf8'))
                message = { "speed": values['speed'],
                            "left": values['left'],
                            "right": values['right']
                        }
                
                self.services['motors'].send(json.dumps(message))

        except:
            pass



    def videoStream(self, params):
        pass

    def moveCamera(self, params):
        pass


    def dispatch(self, ch, method, properties, body):

        # Orchestrate actions
        try:
            message = json.loads(body.decode('utf8'))

            if message['action'] in self.actions:
                if 'params' not in message:
                    message['params'] = ""
                
                self.actions['action'](params=message['params'])
        except:
            pass



    def start(self):
        # Listen to obstacle in another thread, then update self.thread in consequences

        # Listen to external orders
        self.queue.listen(callback=self.dispatch)


if __name__ == '__main__':
    robot = Robot()
    robot.start()

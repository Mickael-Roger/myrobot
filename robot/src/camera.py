import robotmsg as msg

class Camera():

    def __init__(self):
        self.queue = msg.msg(msgName='camera')
            
    #def dispatch(self, ch, method, properties, body):
    def dispatch(self, client, userdata, message):
        print('Reicv : ' + str(message))

    def start(self):
        self.queue.listen(callback=self.dispatch)



if __name__ == '__main__':
    camera = Camera()
    camera.start()

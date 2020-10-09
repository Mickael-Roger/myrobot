#import pika
import paho.mqtt.client as mqtt
import time
import os

class msg():
  
    def __init__(self, msgName):
        self.msgName = 'robot/' + msgName
        
        connect=0
        while connect == 0:
            try:
                self.client = mqtt.Client(os.uname()[1])
                self.client.connect('mosquitto')
                connect=1
            except:
                print('Could not connect to MQTT ... Retrying')
                time.sleep(1)
                pass
    
        
    def listen(self, callback):
        self.client.subscribe(self.msgName)
        self.client.on_message=callback
        self.client.loop_forever()

           
          
    def send(self, msg):
        self.client.publish(topic=self.msgName, payload=msg)

        
        
  

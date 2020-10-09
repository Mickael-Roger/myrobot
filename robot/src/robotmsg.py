#import pika
import paho.mqtt.client as mqtt
import time
import os

class msg():
  
    def __init__(self, msgName):
        #rabbitmqUser = os.environ['RABBITMQ_DEFAULT_USER']
        #rabbitmqPasswd = os.environ['RABBITMQ_DEFAULT_PASS']
        self.msgName = 'robot/' + msgName
        
        connect=0
        while connect == 0:
            try:
                self.client = mqtt.Client(os.uname()[1])
                self.client.connect('mosquitto')
                #credentials = pika.PlainCredentials(rabbitmqUser, rabbitmqPasswd)
                #connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
                #self.channel = connection.channel()
                connect=1
            except:
                print('Could not connect to MQTT ... Retrying')
                time.sleep(1)
                pass
        
        #self.channel.queue_declare(queue=self.msgName)
    
        
    def listen(self, callback):
        self.client.subscribe(self.msgName)
        self.client.on_message=callback
        self.client.loop_forever()

        #self.channel.basic_consume(queue=self.msgName,
        #              auto_ack=True,
        #              on_message_callback=callback)
        #self.channel.start_consuming()
           
          
    def send(self, msg):
        self.client.publish(topic=self.msgName, payload=msg)
        #self.channel.basic_publish(exchange='',
        #              routing_key=self.msgName,
        #              body=msg)
        
        
  

import pika
import time
import os

class msg():
  
    def __init__(self, msgName):
        rabbitmqUser = os.environ['RABBITMQ_DEFAULT_USER']
        rabbitmqPasswd = os.environ['RABBITMQ_DEFAULT_PASS']
        self.msgName = msgName
        
        connect=0
        while connect == 0:
            try:
                credentials = pika.PlainCredentials(rabbitmqUser, rabbitmqPasswd)
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
                self.channel = connection.channel()
                connect=1
            except:
                print('Could not connect to RabbitMQ ... Retrying')
                time.sleep(1)
                pass
        
        self.channel.queue_declare(queue=self.msgName)
        
        
    def listen(self, callback):
        self.channel.basic_consume(queue=self.msgName,
                      auto_ack=True,
                      on_message_callback=callback)
        self.channel.start_consuming()
           
          
    def send(self, msg):
        self.channel.basic_publish(exchange='',
                      routing_key=self.msgName,
                      body=msg)
        
        
  

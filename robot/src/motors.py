import robotmsg as msg
import RPi.GPIO as GPIO  
import json

class Motors():

    def __init__(self):
        self.queue = msg.msg(msgName='motors')

        # Define ports
        self.inLeft1 = 36
        self.inLeft2 = 38
        self.inRight1 = 35
        self.inRight2 = 33

        self.enLeft = 40
        self.enRight = 37


        # Setup board pins
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.inLeft1,GPIO.OUT)
        GPIO.setup(self.inLeft2,GPIO.OUT)
        GPIO.setup(self.enLeft,GPIO.OUT)
        GPIO.output(self.inLeft1,GPIO.LOW)
        GPIO.output(self.inLeft2,GPIO.LOW)

        GPIO.setup(self.inRight1,GPIO.OUT)
        GPIO.setup(self.inRight2,GPIO.OUT)
        GPIO.setup(self.enRight,GPIO.OUT)
        GPIO.output(self.inRight1,GPIO.LOW)
        GPIO.output(self.inRight2,GPIO.LOW)


        self.pLeft = GPIO.PWM(self.enLeft,1000)
        self.pRight = GPIO.PWM(self.enRight,1000)

        self.pLeft.star(100)
        self.pRight.star(100)

            
    
    def stop(self):

        GPIO.output(self.inLeft1,GPIO.LOW)
        GPIO.output(self.inLeft2,GPIO.LOW)
        GPIO.output(self.inRight1,GPIO.LOW)
        GPIO.output(self.inRight2,GPIO.LOW)

        self.pLeft.ChangeDutyCycle(0)
        self.pRight.ChangeDutyCycle(0)




    def rotate(self, left, right):
        self.pLeft.ChangeDutyCycle(0)
        self.pRight.ChangeDutyCycle(0)

        if left < 0:
            left = abs(left)
            GPIO.output(self.inLeft1,GPIO.LOW)
            GPIO.output(self.inLeft2,GPIO.HIGH)
            GPIO.output(self.inRight1,GPIO.HIGH)
            GPIO.output(self.inRight2,GPIO.LOW)

        else:
            right = abs(right)
            GPIO.output(self.inLeft1,GPIO.HIGH)
            GPIO.output(self.inLeft2,GPIO.LOW)
            GPIO.output(self.inRight1,GPIO.LOW)
            GPIO.output(self.inRight2,GPIO.HIGH)


        self.pLeft.ChangeDutyCycle(left)
        self.pRight.ChangeDutyCycle(right)



    def move(self, ch, method, properties, body):
        try:
            val = json.loads(body.decode('utf8'))
            
            if (val['left'] + val['right'] > 100) or val['speed'] < -100 or val['speed'] > 100:
                val['left'] = val['right'] = val['speed'] = 0


            # Just want to turn or stop
            if val['speed'] > -15 and val['speed'] < 15:

                # Turn
                if val['left'] > 55 or val['right'] > 55:
                    left = 2 * (val['left'] - 50)
                    right = 2 * (val['right'] - 50)

                    self.rotate(left=left, right=right)

                # Stop
                else:
                    self.stop()

            print('Reicv : ' + str(val))

        except:
            pass

    def start(self):
        self.queue.listen(callback=self.move)



if __name__ == '__main__':
    motors = Motors()
    motors.start()
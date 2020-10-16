#include <ESP8266WiFi.h>
#include <PubSubClient.h> // To be installed
#include "I2Cdev.h"
#include "MPU6050.h" // To be installed
#include "math.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

 
const char* ssid     = "X";
const char* password = "X";
const char* mqttServer = "192.168.1.26";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
 
WiFiClient espClient;
PubSubClient client(espClient);



///////////////////
// MPU6050 vars
///////////////////

MPU6050 accelgyro;
 
int16_t ax, ay, az;
int16_t gx, gy, gz;
uint8_t Accel_range;
uint8_t Gyro_range;
float angleFront=0;
float angleSide=0;
int gyroStatus = 0;

 
void startGyro(){

  // join I2C bus (I2Cdev library doesn't do this automatically)
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
      Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
#endif

  Serial.println("Start initializing Gyro");
  // Wait for the MPU6050 initialization
  for( int j = 0; j<60; j++){
    accelgyro.initialize();
    delay(100);
    if(accelgyro.getDeviceID() == 57){      // testconneciton() doesn't work because it's supposed to find a 52 getDeviceID !
      delay(1000);
      gyroStatus = 1;
      break;
    }
    Serial.print("Could not initialize Gyro : ");
    Serial.println(accelgyro.testConnection());
    if(accelgyro.testConnection()){      // testconneciton() doesn't work because it's supposed to find a 52 getDeviceID !
      delay(1000);
      gyroStatus = 1;
      break;
    }
    Serial.println("Could not initialize Gyro 2");
    delay(900);
  }  
}


void updatePosition(){
   
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  angleFront=0.20*(angleFront+float(gy)*0.01/131) + 0.80*atan2((double)ax,(double)az)*180/PI;
  angleSide=0.20*(angleSide+float(gx)*0.01/131) + 0.80*atan2((double)ay,(double)az)*180/PI;
  
}


void setup() {
 
  Serial.begin(115200);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);

 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }

  // Start Gyro
  startGyro();

  delay(1000);
 

}

int i=0;
float front, left, avgAngleFront=0, avgAngleSide=0;
char buf[80];
String message;

void loop() {
  updatePosition();
  avgAngleFront=(avgAngleFront*i + angleFront)/(i+1);
  avgAngleSide=(avgAngleSide*i + angleSide)/(i+1);
  
  
  if( i>3 ){

      if(avgAngleFront < -90){
        avgAngleFront=-90.0;
      }
      if(avgAngleFront > 90){
        avgAngleFront=90.0;
      }
      
      front=-0.11111*avgAngleFront;


      if(angleSide < -90){
        angleSide=-90.0;
      }
      if(angleSide > 90){
        angleSide=90.0;
      }
      left=5+angleSide*-0.05556;


    message="{\"action\": \"move\", \"params\": {\"left\": " + String(round(left)*10) + ", \"right\": " + String(100 - round(left)*10) + ", \"speed\": " + String(round(front)*10) + "}}";
    message.toCharArray(buf, 80);
    client.publish("robot/external", buf);
    //Serial.println(message);

    i=0;
    avgAngleFront=0;
    avgAngleSide=0;
  }

  i++;
  delay(50);
}
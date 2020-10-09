#include <ESP8266WiFi.h>
#include <PubSubClient.h>
 
const char* ssid     = "XX";
const char* password = "XX";
const char* mqttServer = "192.168.1.26";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
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
 

}
 
 
void loop() {
  client.publish("robot/external", '{"action": "move, "params": {"left": 100, "right": 0, "speed": 0}');
  delay(1000);
}
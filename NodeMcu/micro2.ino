#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Servo.h>

#define NPK_SENSOR_PIN A0
#define WATER_LEVEL_SENSOR_PIN D3
#define AIR_QUALITY_SENSOR_PIN A1
#define MOTOR_PIN D4
#define TRIG_PIN D5
#define ECHO_PIN D6

Servo myservo;

const char* ssid = "Iphone12";
const char* password = "@Guest$567";
const char* serverAddress = "192.168.9.78";
const int serverPort = 5600;

WiFiClient client;

void setup() {
  myservo.attach(D2);
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }

  Serial.println("Connected to WiFi");

  pinMode(NPK_SENSOR_PIN, INPUT);
  pinMode(WATER_LEVEL_SENSOR_PIN, INPUT);
  pinMode(AIR_QUALITY_SENSOR_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  int npkSensorValue = analogRead(NPK_SENSOR_PIN);
  int waterLevel = digitalRead(WATER_LEVEL_SENSOR_PIN);
  int airQualityValue = analogRead(AIR_QUALITY_SENSOR_PIN);
  
  long duration, distance;
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  duration = pulseIn(ECHO_PIN, HIGH);
  distance = duration * 0.0343 / 2;
  float wind_speed = (10 * distance) / 100;

  if (waterLevel == LOW) {
    digitalWrite(MOTOR_PIN, HIGH);
  } else {
    digitalWrite(MOTOR_PIN, LOW);
  }

  String device_id = "ab010";
 
  if (client.connect(serverAddress, serverPort)) {
    String payload = "{\"device_id\":\"" + device_id + "\",\"npk_sensor_value\":" + String(npkSensorValue) +
                     ",\"water_level\":" + String(waterLevel) +
                     ",\"air_quality\":" + String(airQualityValue) +
                     ",\"wind_speed\":" + String(wind_speed) + "}";

    client.print("POST /api/data HTTP/1.1\r\n");
    client.print("Host: ");
    client.print(serverAddress);
    client.print("\r\n");
    client.print("Content-Type: application/json\r\n");
    client.print("Content-Length: ");
    client.print(payload.length());
    client.print("\r\n\r\n");
    client.print(payload);
    
    Serial.println("Data sent to server");
    Serial.print("NPK Sensor Value: ");
    Serial.println(npkSensorValue);
    Serial.print("Water Level: ");
    Serial.println(waterLevel);
    Serial.print("Air Quality Value: ");
    Serial.println(airQualityValue);
    Serial.print("Wind Speed: ");
    Serial.print(wind_speed);
    Serial.println(" m/s");
   
    client.stop();
  } else {
    Serial.println("Failed to connect to server");
  }

  delay(20000);
}

#include <WiFi.h>
#include <esp_camera.h>

const char* ssid = "Iphon12";
const char* password = "@Guest$567";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL;
  config.ledc_timer = LEDC_TIMER;
  config.pin_d7 = 13;
  config.pin_d6 = 12;
  config.pin_d5 = 14;
  config.pin_d4 = 27;
  config.pin_d3 = 26;
  config.pin_d2 = 25;
  config.pin_d1 = 33;
  config.pin_d0 = 32;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sccb_sda = 21;
  config.pin_sccb_scl = 22;
  config.frame_size = FRAMESIZE_SVGA;
  config.pixel_format = PIXFORMAT_JPEG;

  esp_camera_init(&config);

  WiFiServer server(80);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    client.flush();
    
    if (request.indexOf("GET /stream") != -1) {
 
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: multipart/x-mixed-replace; boundary=frame");
      client.println();
      
      while (client.connected()) {
        camera_fb_t *fb = esp_camera_fb_get();
        if (!fb) {
          Serial.println("Camera capture failed");
          client.stop();
          break;
        }
        client.println("--frame");
        client.println("Content-Type: image/jpeg");
        client.println("Content-Length: " + String(fb->len));
        client.println();
        client.write(fb->buf, fb->len);
        client.println();
        esp_camera_fb_return(fb);
      }
    } else {
      client.stop();
    }
  }
}

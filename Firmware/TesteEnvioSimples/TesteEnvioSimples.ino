#include <Arduino.h>
#include "AudioGeneratorWAV.h"
#include "AudioOutputI2S.h"
#include "AudioFileSourcePROGMEM.h"
#include <WiFi.h>

AudioFileSourcePROGMEM *in;
AudioGeneratorWAV *aac;
AudioOutputI2S *out;


// Replace with your network credentials
const char* ssid     = "Vipper-Access-Point";
const char* password = "123456789vipper";

// Set server port number to SERVER_PORT
WiFiServer server(1775);


typedef struct DesktopAppData{
  uint8_t audioFile[50000];
  uint32_t audioFileLen;
  uint8_t messageAvailable;
} DesktopAppData;

typedef struct Vipper{
  uint16_t timeoutTimer;
  WiFiClient desktopApp;
  DesktopAppData appData;
} Vipper;

Vipper vipper;

void setup()
{
  Serial.begin(115200);


#ifdef ACCESS_POINT
  /* PONTO DE ACESSO */
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Setting AP (Access Point)…");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("IP address: ");
  Serial.println(IP);
#endif
  Serial.print("MAC address: ");
  Serial.println(WiFi.macAddress());
  
  server.begin();
  
  audioLogger = &Serial;
  aac = new AudioGeneratorWAV();
  out = new AudioOutputI2S();
  out->SetPinout( 27, 26, 25);
}


void loop()
{
  while(!vipper.desktopApp){
    vipper.desktopApp = server.available();   // Listen for incoming clients
    vipper.timeoutTimer = 30000; // 30 segundos timeout
  }


  uint8_t header_info[4];
  uint32_t pckt_size = 0;
  byte byte_read;
  uint8_t num_read = 0;


  while(vipper.appData.audioFileLen < 48044)
  {
    byte_read = vipper.desktopApp.read(vipper.appData.audioFile + vipper.appData.audioFileLen, 500);

    if(vipper.appData.audioFileLen > 48044){
      Serial.println("Overflow audio");
      vipper.appData.audioFileLen = 0;
    }
    
    vipper.appData.audioFileLen += byte_read;
    if(vipper.appData.audioFile[0] == 'R' && num_read == 0)
      header_info[0] = vipper.appData.audioFile[0];
    if(vipper.appData.audioFile[1] == 'I' && num_read == 1)
      header_info[1] = vipper.appData.audioFile[1];
    if(vipper.appData.audioFile[2] == 'F' && num_read == 2)
      header_info[2] = vipper.appData.audioFile[2];
    if(vipper.appData.audioFile[3] == 'F' && num_read == 3)
      header_info[3] = vipper.appData.audioFile[3];

    if((vipper.appData.audioFile[0] == 'R') && (vipper.appData.audioFile[1] == 'I') && (vipper.appData.audioFile[2] == 'F') && (vipper.appData.audioFile[3] == 'F'))
    { 
      if(vipper.appData.audioFileLen < 48044)
      {
        Serial.print("Bytes recebidos: ");
        Serial.println(vipper.appData.audioFileLen);
        return;
      }
      vipper.appData.messageAvailable = true;
      Serial.println("Mensagem recebida com sucesso");
      Serial.print("Tamanho do arquivo: "); Serial.println(*((uint32_t*)(&vipper.appData.audioFile[4])));
      //while(vipper.appData.audioFileLen > 16044)

      
    }
    else
    {
      Serial.println("Failed reading RIFF");
      Serial.print(header_info[0]);  Serial.print(header_info[1]); Serial.print(header_info[2]); Serial.print(header_info[3]); 
      vipper.appData.audioFileLen = 0;
      return;

    }
  }
  
  in = new AudioFileSourcePROGMEM(vipper.appData.audioFile, 48044);
  aac->begin(in, out);
  
  
  if (aac->isRunning()) {
    aac->loop();
  } else {
    Serial.printf("AAC done\n");
    delay(1000);
    delete (in);
    in = new AudioFileSourcePROGMEM(vipper.appData.audioFile, 48044);
    aac->begin(in,out);
  }
}

// Load Wi-Fi library
#include <WiFi.h>
#include "AudioFileSourcePROGMEM.h"
#include "AudioGeneratorWAV.h"
#include "AudioOutputI2S.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#define SERVER_PORT 1775
//#define ACCESS_POINT

#define SENSOR
//#define CONTROLE

#define GAS_GPIO 14
#define SOUND_LRC 26
#define SOUND_BCLK 27
#define SOUND_DIN 25
#define MPU_SCL 22
#define MPU_SDA 21


#define PINO_FRENTE 27
#define PINO_TRAS 26

// Replace with your network credentials
const char* ssid     = "Vipper-Access-Point";
const char* password = "123456789vipper";

//const char* ssid     = "Copel20";
//const char* password = "93002000";

#ifdef ACCESS_POINT
  IPAddress local_IP(192,168,4,1);
#else
  IPAddress local_IP(192,168,4,2);
#endif

// Set your Gateway IP address
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

// Set server port number to SERVER_PORT
WiFiServer server(SERVER_PORT);

typedef enum VipperState{
  ESTABLISHING_CONNECTION = 0,
  CONNECTED
} VipperState;

typedef enum VipperConnectedSubstate{
  WAITING_FOR_DATA = 0,
  PROCESSING_DATA,
  PLAYING_MESSAGE
} VipperConnectedSubstate;

typedef enum VipperConnectingSubstate{
  NOT_CONNECTING_WIFI = 0,
  CONNECTING_WIFI,
  CONNECTING_APP
} VipperConnectingSubstate;

typedef struct DesktopAppData{
#ifdef SENSOR
  uint8_t* audioFile;//[100000];
  uint32_t audioFileLen;
  uint8_t messageAvailable;
#endif
#ifdef CONTROLE
  uint8_t command;
#endif
} DesktopAppData;

#ifdef CONTROLE
typedef enum DesktopAppCommand{
  BACK = 0,
  FORWARD = 1,
  NO_COMMAND = 2
} DesktopAppCommand;
#endif

typedef struct Vipper{
  VipperState state;
  uint16_t substate;
  uint16_t timeoutTimer;
  WiFiClient desktopApp;
  DesktopAppData appData;
} Vipper;

Vipper vipper;

void goToState(VipperState state);
void trataConectando();

// SOUND //
AudioGeneratorWAV* wav;
AudioFileSourcePROGMEM* file;
AudioOutputI2S* out;

// MPU //
Adafruit_MPU6050 mpu;

// SYSTICK //
volatile int interruptCounter = 0;
volatile uint32_t timerComando = 0;
hw_timer_t * timer = NULL;
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;

void IRAM_ATTR onTimer() {
  portENTER_CRITICAL_ISR(&timerMux);
  interruptCounter++;
  if(timerComando)
    timerComando--;
  portEXIT_CRITICAL_ISR(&timerMux);
 
}

void setup() {
  
  Serial.begin(115200);
  while (!Serial)
    delay(10);

  if (!WiFi.config(local_IP, gateway, subnet))
  {
    Serial.println("Falha na configuracao do wifi");
  }

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
  

  vipper.state = ESTABLISHING_CONNECTION;

#ifdef SENSOR

  vipper.appData.audioFile =  (uint8_t*) malloc(sizeof(uint8_t) * 100000);
  // SOUND_SETUP //
  audioLogger = &Serial;
  wav = new AudioGeneratorWAV();
  out = new AudioOutputI2S();
  file = new AudioFileSourcePROGMEM();
  out->SetPinout( SOUND_BCLK, SOUND_LRC, SOUND_DIN);
  out->SetChannels(1);
  out->SetBitsPerSample(16);
  out->SetOutputModeMono(true);
  out->SetRate(8000);

  // MPU_SETUP //
  if (!mpu.begin()) 
    Serial.println("Failed to find MPU6050 chip");
  else
    Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }
    
  // GAS_SETUP //
  pinMode(GAS_GPIO, INPUT);

  vipper.appData.messageAvailable = false;
  vipper.appData.audioFileLen = 0;
#endif

#ifdef CONTROLE
  pinMode(PINO_FRENTE, OUTPUT);
  pinMode(PINO_TRAS, OUTPUT);
    digitalWrite(PINO_FRENTE, 0);
    digitalWrite(PINO_TRAS, 0); 
#endif

  // SYSTICK SETUP // 
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &onTimer, true);
  // 100000 -> 0.1s
  timerAlarmWrite(timer, 10000, true);
  timerAlarmEnable(timer);


  vipper.desktopApp.setTimeout(2);
}

#ifdef SENSOR
void enviaMsgPlacaSensor(uint8_t gas, uint8_t movimento, float x_gyro, float y_gyro, float z_gyro, float temp);

void trataConectadoSensor__stub()
{
  static uint32_t x = 0;
  if(!x)
  {
    Serial.println("Enviando");
    enviaMsgPlacaSensor(1, 0, 3000, 2000, 1000, 1920);
    x = 3000;
  }
  x--;

}


void trataConectadoSensor()
{
  sensors_event_t a, g, temp;
  static uint8_t tocando = 0;
  
  switch(vipper.substate)
  {
    case WAITING_FOR_DATA:
      if(interruptCounter > 20 && !vipper.appData.messageAvailable)
      {
        interruptCounter = 0;
        vipper.substate = PROCESSING_DATA;
      }
      else if(vipper.appData.messageAvailable)
      {
        vipper.substate = PLAYING_MESSAGE;
      }
      break;
      
    case PROCESSING_DATA:/* Get new sensor events with the readings */
      mpu.getEvent(&a, &g, &temp);
    
      /* Print out the values */
      /*
      Serial.print("Acceleration X: ");
      Serial.print(a.acceleration.x);
      Serial.print(", Y: ");
      Serial.print(a.acceleration.y);
      Serial.print(", Z: ");
      Serial.print(a.acceleration.z);
      Serial.println(" m/s^2");
    
      Serial.print("Rotation X: ");
      Serial.print(g.gyro.x);
      Serial.print(", Y: ");
      Serial.print(g.gyro.y);
      Serial.print(", Z: ");
      Serial.print(g.gyro.z);
      Serial.println(" rad/s");
    
      Serial.print("Temperature: ");
      Serial.print(temp.temperature);
      Serial.println(" degC");
      */
      enviaMsgPlacaSensor(digitalRead(GAS_GPIO), 1, g.gyro.x, g.gyro.y, g.gyro.z, temp.temperature);
      
      vipper.substate = WAITING_FOR_DATA;
      break;
      
    case PLAYING_MESSAGE:
      if(!tocando){
        Serial.println("PLAYING_MESSAGE - Reading data");
        file->open((const void*)vipper.appData.audioFile, 16100);
  
        wav->begin(file, out);
        Serial.println("PLAYING_MESSAGE - Playing data");
        tocando = 1;
      }
      if (tocando && !wav->loop()) 
      {
        Serial.println("PLAYING_MESSAGE - Stop playing data");
        wav->stop();
        file->close();
        vipper.substate = WAITING_FOR_DATA;
        vipper.appData.messageAvailable = false;
        vipper.appData.audioFileLen = 0;
        tocando = 0;
        break;
      }
  }

  if(!vipper.desktopApp.connected())
  {
    vipper.desktopApp.stop();
    vipper.desktopApp = 0;
    goToState(ESTABLISHING_CONNECTION);
    Serial.println("Conexao perdida");
  }

}
#endif

#ifdef ACCESS_POINT
/* SERVIDOR COM PONTO DE ACESSO */
void trataConectandoAP()
{
  if(!vipper.desktopApp){
    vipper.desktopApp = server.available();   // Listen for incoming clients
    vipper.timeoutTimer = 30000; // 30 segundos timeout
  }

  if (vipper.desktopApp) {                             
    if (vipper.desktopApp.connected()) {            
      /* A partir daqui o cliente estah conectado */
      goToState(CONNECTED);
      Serial.println("Conectado");
    }
    // Se estourou o timer limite de conexao, reinicia a conexao.
    else if (!vipper.timeoutTimer){
      vipper.desktopApp.stop();
      vipper.desktopApp = 0;
    }
  }
}
#endif

#ifndef ACCESS_POINT
/* SERVER SEM PONTO DE ACESSO */
void trataConectandoServer()
{
  //Conectamos Access Point criado
  //pelo outro ESP
  if (vipper.substate == NOT_CONNECTING_WIFI){
    WiFi.begin(ssid, password);
    vipper.timeoutTimer = 30000;
    vipper.substate = CONNECTING_WIFI;
    Serial.println("Conectando wifi");
  }

  //Esperamos conectar
  if (vipper.substate == CONNECTING_WIFI){
    if (WiFi.status() == WL_CONNECTED){
      vipper.substate = CONNECTING_APP;
      Serial.println("Conectando app");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());

    }
    else if (!vipper.timeoutTimer)
    {
      //Timeout?
    }
  }

  if(vipper.substate == CONNECTING_APP)
  {
    if(!vipper.desktopApp){
      vipper.desktopApp = server.available();   // Listen for incoming clients
      vipper.timeoutTimer = 30000; // 30 segundos timeout
    }

    if (vipper.desktopApp) {                             
      if (vipper.desktopApp.connected()) {            
        /* A partir daqui o cliente estah conectado */
        goToState(CONNECTED);
        Serial.println("Conectado");
      }
      // Se estourou o timer limite de conexao, reinicia a conexao.
      else if (!vipper.timeoutTimer){
        vipper.desktopApp.stop();
        vipper.desktopApp = 0;
      }
    }
  }

}
#endif

void goToState(VipperState state)
{
  vipper.state = state;
  vipper.substate = 0;
}


#ifdef CONTROLE
// Coloca o comando recebido na variavel vipper.appData.command
void trataMsgPlacaComando()
{
  vipper.appData.command = NO_COMMAND;
  
  while(vipper.desktopApp && vipper.desktopApp.available())
  {
    if(vipper.desktopApp.read())
      vipper.appData.command = BACK;
    else
      vipper.appData.command = FORWARD;  
    Serial.print("Comando: "); Serial.println(vipper.appData.command);
  } 
}

void trataConectadoControle()
{
  if(vipper.appData.command == FORWARD)
  {
    digitalWrite(PINO_FRENTE, 1);
    digitalWrite(PINO_TRAS, 0);
    timerComando = 30000;
  }
  else if(vipper.appData.command == BACK)
  {
    digitalWrite(PINO_FRENTE, 0);
    digitalWrite(PINO_TRAS, 1);
    timerComando = 30000;
  }
  else if(timerComando <= 0)
  {
    digitalWrite(PINO_FRENTE, 0);
    digitalWrite(PINO_TRAS, 0); 
  }

}

#endif

#ifdef SENSOR
// Coloca a mensagem recebida no ringbuffer
void trataMsgPlacaSensor()
{
  uint8_t header_info[4];
  uint32_t pckt_size = 0;
  byte byte_read;
  uint8_t num_read = 0;


  if(vipper.desktopApp && vipper.desktopApp.available() && vipper.appData.messageAvailable == false)
  {
    while(vipper.appData.audioFileLen < 16100)
    {
      if(vipper.desktopApp.available() >= 100){
        byte_read = vipper.desktopApp.read(vipper.appData.audioFile + vipper.appData.audioFileLen, 100);
  
        if(vipper.appData.audioFileLen > 16100){
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
          if(vipper.appData.audioFileLen < 16100)
          {
            //Serial.print("Bytes recebidos: ");
            //Serial.println(vipper.appData.audioFileLen);
            //return;
          }
          else{
            vipper.appData.messageAvailable = true;
            Serial.println("Mensagem recebida com sucesso");
            Serial.print("Tamanho do arquivo: "); Serial.println(*((uint32_t*)(&vipper.appData.audioFile[4])));
            //while(vipper.appData.audioFileLen > )
          }
          
        }
        else
        {
          Serial.println("Failed reading RIFF");
          Serial.print(header_info[0]);  Serial.print(header_info[1]); Serial.print(header_info[2]); Serial.print(header_info[3]); 
          vipper.appData.audioFileLen = 0;
          return;
    
        }
      }
    }
  }
  
}

void enviaMsgPlacaSensor(uint8_t gas, uint8_t movimento, float x_gyro, float y_gyro, float z_gyro, float temp)
{
  uint8_t message[9];
  message[0] = (((1 && gas) << 2) | (movimento & 3)) << 5;
  message[1] = ((((int16_t)(x_gyro*1000.)) & 0xFF00) >> 8);
  message[2] = (((int16_t)(x_gyro*1000.)) & 0xFF);
  message[3] = ((((int16_t)(y_gyro*1000.)) & 0xFF00) >> 8);
  message[4] = ((((int16_t)(y_gyro*1000.)) & 0xFF));
  message[5] = ((((int16_t)(z_gyro*1000.)) & 0xFF00) >> 8);
  message[6] = ((((int16_t)(z_gyro*1000.)) & 0xFF));
  message[7] = ((((int16_t)(temp*100.)) & 0xFF00) >> 8);
  message[8] = ((((int16_t)(temp*100.)) & 0xFF));


  if(vipper.desktopApp.connected())
    vipper.desktopApp.write(message, 9);
}
#endif

void loop(){
  switch(vipper.state)
  {
    case ESTABLISHING_CONNECTION:
#ifdef ACCESS_POINT
      trataConectandoAP();
#else
      trataConectandoServer();
#endif
      break;

    case CONNECTED:
      //stub
      #ifdef SENSOR
        trataConectadoSensor();
      #endif
      #ifdef CONTROLE
        trataConectadoControle();
      #endif
      
      if(!vipper.desktopApp.connected())
      {
        vipper.desktopApp.stop();
        vipper.desktopApp = 0;
        goToState(ESTABLISHING_CONNECTION);
      }
      break;

    default:
      Serial.println("Erro - maquina de estados principal");
      break;
  }

#ifdef SENSOR
  trataMsgPlacaSensor();
#endif

#ifdef CONTROLE
  trataMsgPlacaComando();
#endif
}
      

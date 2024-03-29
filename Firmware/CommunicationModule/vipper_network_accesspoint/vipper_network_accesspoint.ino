// Load Wi-Fi library
#include <WiFi.h>
#include <RingBuf.h>

#define SERVER_PORT 1775
#define ACCESS_POINT

#define SENSOR
//#define CONTROLE

// Replace with your network credentials
const char* ssid     = "Vipper-Access-Point";
const char* password = "123456789vipper";

//const char* ssid     = "Copel20";
//const char* password = "93002000";

#ifdef ACCESS_POINT
  IPAddress local_IP(192,168,4,1);
#else
  IPAddress local_IP(192,168,100,200);
#endif

// Set your Gateway IP address
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);

// Set server port number to SERVER_PORT
WiFiServer server(SERVER_PORT);

typedef enum VipperState{
  ESTABLISHING_CONNECTION = 0,
  CONNECTED
} VipperState;

typedef enum VipperConnectedSubstate{
  WAITING_FOR_DATA = 0,
  PROCESSING_SENSOR_DATA,
  PLAYING_MESSAGE
} VipperConnectedSubstate;

typedef enum VipperConnectingSubstate{
  NOT_CONNECTING_WIFI = 0,
  CONNECTING_WIFI,
  CONNECTING_APP
} VipperConnectingSubstate;

typedef struct DesktopAppData{
#ifdef SENSOR
  RingBuf<uint8_t, 8000> message;
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


void setup() {
  Serial.begin(115200);

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

  Serial.print("IP address: ");
  Serial.println(local_IP);
  
  Serial.print("MAC address: ");
  Serial.println(WiFi.macAddress());
  
  server.begin();

  vipper.state = ESTABLISHING_CONNECTION;
}

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
        trataConectadoSensor__stub();
      #endif
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
    }
    // Se estourou o timer limite de conexao, reinicia a conexao.
    else if (!vipper.timeoutTimer){
      vipper.desktopApp.stop();
      vipper.desktopApp = 0;
    }
  }
}

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
    vipper.appData.command = vipper.desktopApp.read();
    Serial.print("Comando: "); Serial.println(vipper.appData.command);
  } 
}
#endif

#ifdef SENSOR
// Coloca a mensagem recebida no ringbuffer
void trataMsgPlacaSensor()
{
  while(vipper.desktopApp && vipper.desktopApp.available() && !vipper.appData.message.isFull())
  {
      vipper.appData.message.push(vipper.desktopApp.read());
  }

  #warning TESTE
  while(!vipper.appData.message.isEmpty())
  {
    unsigned char a;
    vipper.appData.message.pop(a);
    Serial.print(a);
    Serial.print("\n");
  }

}

void enviaMsgPlacaSensor(uint8_t gas, uint8_t movimento, float x_gyro, float y_gyro, float z_gyro, float temp)
{
  uint8_t message[9];
  message[0] = (((1 && gas) << 1) | (1 && movimento)) << 6;
  message[1] = ((*((uint16_t*)&x_gyro) & 0xFF00) >> 8);
  message[2] = ((*((uint16_t*)&x_gyro) & 0xFF));
  message[3] = ((*((uint16_t*)&y_gyro) & 0xFF00) >> 8);
  message[4] = ((*((uint16_t*)&y_gyro) & 0xFF));
  message[5] = ((*((uint16_t*)&z_gyro) & 0xFF00) >> 8);
  message[6] = ((*((uint16_t*)&z_gyro) & 0xFF));
  message[7] = ((*((uint16_t*)&temp) & 0xFF00) >> 8);
  message[8] = ((*((uint16_t*)&temp) & 0xFF));

  vipper.desktopApp.write(message, 9);
}
#endif

      

// Load Wi-Fi library
#include <WiFi.h>
#include <RingBuf.h>

#define SERVER_PORT 1775
#define ACCESS_POINT

//#define SENSOR
#define CONTROLE

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

#define PINO_FRENTE 27
#define PINO_TRAS 26

// Set your Gateway IP address
IPAddress gateway(192, 168, 4, 1);
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

  pinMode(PINO_FRENTE, OUTPUT);
  pinMode(PINO_TRAS, OUTPUT);
    digitalWrite(PINO_FRENTE, 0);
    digitalWrite(PINO_TRAS, 0); 
}

void trataConectadoControle()
{
  static uint32_t timerComando = 0;
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

  if(timerComando > 0)
    timerComando--;
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
      trataConectadoControle();

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
      Serial.println("Conectado");
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
    Serial.println("Conectando wifi");
    WiFi.begin(ssid, password);
    vipper.timeoutTimer = 30000;
    vipper.substate = CONNECTING_WIFI;
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
    if(vipper.desktopApp.read())
      vipper.appData.command = BACK;
    else
      vipper.appData.command = FORWARD;  
    Serial.print("Comando: "); Serial.println(vipper.appData.command);
  } 
}
#endif
      

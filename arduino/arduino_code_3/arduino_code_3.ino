
//Este arduino eh responsavel por:
// Vaso 9: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Tanque: Sensor TDS (pino A2) e Sensor de pH (pino A3)
// Temperatura dos vasos (pino D12)
// Temperatura do tanque (pin A4)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_9': { 'tds': [0-1023], 'umidade': [0-1023]}, 'tanque': { 'tds': [0-1023], 'pH': [0-1023]} }

#include <EEPROM.h>

#define TdsSensorPin0 A0
#define TdsSensorPin1 A2

#define MoistSensorPin0 A1

#define pHSensorPin0 A3
#define pHTempSensorPin0 A4


int sensorValue = 0;
unsigned long int avgValue;
float b;
int buf[10], temp;

void setup()
{
    Serial.begin(115200);
    pinMode(TdsSensorPin0,INPUT);
    pinMode(TdsSensorPin1,INPUT);
    pinMode(MoistSensorPin0,INPUT);
    pinMode(pHSensorPin0,INPUT);
    pinMode(pHTempSensorPin0,INPUT);

}

void loop()
{
    int MoistSensorValue0;
    int tdsEcCoef = 280;
    //temperature = readTemperature();  //add your temperature sensor and read it
    float temperature = 25;
    float aref = 5.0;
    float ecCalibration = 1;
    float temperatureCoefficient = 1.0 + 0.02 * (25.0 - 25.0); // temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
    
    float rawEc0 = analogRead(TdsSensorPin0) * aref / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
    float ec0 = (rawEc0 / temperatureCoefficient) * ecCalibration; // temperature and calibration compensation
    float tdsValue0 = ec0*tdsEcCoef;

    float rawEc1 = analogRead(TdsSensorPin1) * aref / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
    float ec1 = (rawEc1 / temperatureCoefficient) * ecCalibration; // temperature and calibration compensation
    float tdsValue1 = ec1*tdsEcCoef;
  
    MoistSensorValue0 = analogRead(MoistSensorPin0);


       for(int i = 0; i<10; i++)
    {
      buf[i]=analogRead(pHSensorPin0);
      delay(10);
    }
    for(int i=0;i<9;i++)
    {
      for(int j=i+1;j<10;j++)
      {
        if (buf[i]>buf[j])
        {
          temp = buf[i];
          buf[i]=buf[j];
          buf[j]=temp;
        }
       }
     }
   avgValue =0;
   for(int i=2;i<8;i++)
   {
    avgValue+=buf[i];
   }
   
 
    
    float pHVol=(float)avgValue*5.0/1024*0.135;
    //float pHSensorValue0 = -9.9454 * pHVol + 29.1936;
    float  pHSensorValue0 = pHVol;

    
    int pHTempSensorValue0 = analogRead(pHTempSensorPin0);   
   

    Serial.print("3-\"vaso_9\":{\"tds\":\"");
    Serial.print(tdsValue0);
    Serial.print("\",\"umidade\":\"");
    Serial.print(MoistSensorValue0);
    Serial.print("\"},\"tanque\":{\"tds\":\"");
    Serial.print(tdsValue1);
    Serial.print("\",\"pH\":\"");
    Serial.print(pHSensorValue0);
    Serial.print("\",\"temp\":\"");
    Serial.print(pHTempSensorValue0);
    Serial.print("\"}}");
    Serial.print("fim");
    delay(400);

}

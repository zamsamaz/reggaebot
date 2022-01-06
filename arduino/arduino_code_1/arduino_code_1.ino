//Este arduino eh responsavel por:
// Vaso 1: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Vaso 2: Sensor TDS (pino A2) e Sensor de umidade (pino A3)
// Vaso 3: Sensor TDS (pino A4) e Sensor de umidade (pino A5)
// Vaso 4: Sensor TDS (pino A6) e Sensor de umidade (pino A7)
// Sensor de temperatura de agua (pino D12)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_1': { 'tds': [0-1023], 'umidade': [0-1023]}, 'vaso_2': { 'tds': [0-1023], 'umidade': [0-1023]}, ... }


#include <EEPROM.h>

#include <OneWire.h>

#include <DallasTemperature.h>


#define TdsSensorPin0 19//a0
#define TdsSensorPin1 21//a2
#define TdsSensorPin2 23//A4
#define TdsSensorPin3 25//A6
#define VREF 5.0      // analog reference voltage(Volt) of the ADC
#define SCOUNT  30           // sum of sample point
int analogBuffer[SCOUNT];    // store the analog value in the array, read from ADC
int analogBufferTemp[SCOUNT];
int analogBufferIndex = 0,copyIndex = 0;
float averageVoltage = 0,temperature = 25;
float tdsValue0 = 0, tdsValue1 = 0,tdsValue2 = 0,tdsValue3 = 0;

#define MoistSensorPin0 20//A1
#define MoistSensorPin1 22//A3
#define MoistSensorPin2 24//A5
#define MoistSensorPin3 26//A7

#define ONE_WIRE_BUS 15//D12

// Setup a oneWire instance to communicate with any OneWire device
OneWire oneWire(ONE_WIRE_BUS);

// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);

int MoistSensorValue0;
int MoistSensorValue1;
int MoistSensorValue2;
int MoistSensorValue3;

void setup()
{
    Serial.begin(115200);
    sensors.begin();	// Start up the library
    pinMode(TdsSensorPin0,INPUT);
    pinMode(TdsSensorPin1,INPUT);
    pinMode(TdsSensorPin2,INPUT);
    pinMode(TdsSensorPin3,INPUT);

}

void loop()
{

    //temperature = readTemperature();  //add your temperature sensor and read it
    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);

  static unsigned long analogSampleTimepoint = millis();
   if(millis()-analogSampleTimepoint > 40U)     //every 40 milliseconds,read the analog value from the ADC
   {
     analogSampleTimepoint = millis();
     analogBuffer[analogBufferIndex] = analogRead(TdsSensorPin);    //read the analog value and store into the buffer
     analogBufferIndex++;
     if(analogBufferIndex == SCOUNT) 
         analogBufferIndex = 0;
   }   
   static unsigned long printTimepoint = millis();
   if(millis()-printTimepoint > 800U)
   {
      printTimepoint = millis();
      for(copyIndex=0;copyIndex<SCOUNT;copyIndex++)
        analogBufferTemp[copyIndex]= analogBuffer[copyIndex];
      averageVoltage = getMedianNum(analogBufferTemp,SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
      float compensationCoefficient=1.0+0.02*(temperature-25.0);    //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
      float compensationVolatge=averageVoltage/compensationCoefficient;  //temperature compensation
      tdsValue=(133.42*compensationVolatge*compensationVolatge*compensationVolatge - 255.86*compensationVolatge*compensationVolatge + 857.39*compensationVolatge)*0.5; //convert voltage value to tds value
 


    MoistSensorValue0 = analogRead(MoistSensorPin0);
    MoistSensorValue1 = analogRead(MoistSensorPin1);
    MoistSensorValue2 = analogRead(MoistSensorPin2);
    MoistSensorValue3 = analogRead(MoistSensorPin3);


    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      if (data == "sendit"){;
        
          Serial.print("{\"vaso_1\": { \"tds\": \"");
          Serial.print(tdsValue0);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue0);
          Serial.println("\"}, {\"vaso_2\": { \"tds\": \"");
          Serial.print(tdsValue1);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue1);
          Serial.println("\"}, {\"vaso_3\": { '\"tds\": \"");
          Serial.print(tdsValue2);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue2);
          Serial.println("\"}, {\"vaso_4\": { \"tds\": \"");
          Serial.print(tdsValue3);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue3);
          Serial.println("\"} }");
          }
      delay(1000);
    }

}


int getMedianNum(int bArray[], int iFilterLen) 
{
      int bTab[iFilterLen];
      for (byte i = 0; i<iFilterLen; i++)
      bTab[i] = bArray[i];
      int i, j, bTemp;
      for (j = 0; j < iFilterLen - 1; j++) 
      {
      for (i = 0; i < iFilterLen - j - 1; i++) 
          {
        if (bTab[i] > bTab[i + 1]) 
            {
        bTemp = bTab[i];
            bTab[i] = bTab[i + 1];
        bTab[i + 1] = bTemp;
         }
      }
      }
      if ((iFilterLen & 1) > 0)
    bTemp = bTab[(iFilterLen - 1) / 2];
      else
    bTemp = (bTab[iFilterLen / 2] + bTab[iFilterLen / 2 - 1]) / 2;
      return bTemp;
}

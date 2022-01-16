
//Este arduino eh responsavel por:
// Vaso 9: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Tanque: Sensor TDS (pino A2) e Sensor de pH (pino A3)
// Temperatura dos vasos (pino D12)
// Temperatura do tanque (pin A4)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_9': { 'tds': [0-1023], 'umidade': [0-1023]}, 'tanque': { 'tds': [0-1023], 'pH': [0-1023]} }

#include <EEPROM.h>

#include "GravityTDS.h"

#define TdsSensorPin0 A0
#define TdsSensorPin1 A2

#define MoistSensorPin0 A1

#define pHSensorPin0 A3

#define pHTempSensorPin0 A4

GravityTDS gravityTds0;
GravityTDS gravityTds1;

int MoistSensorValue0;


void setup()
{
    Serial.begin(115200);

        pinMode(pHSensorPin0,INPUT);
        pinMode(pHTempSensorPin0,INPUT);


    gravityTds0.setPin(TdsSensorPin0);
    gravityTds1.setPin(TdsSensorPin1);

    gravityTds0.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds1.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO

    gravityTds0.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds1.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC

    gravityTds0.begin();  //initialization
    gravityTds1.begin();  //initialization

}

void loop()
{
    float temperature = 26;

    gravityTds0.setTemperature(temperature);  // set the temperature and execute temperature compensation
    gravityTds1.setTemperature(temperature);  // set the temperature and execute

    gravityTds0.update();  //sample and calculate
    gravityTds1.update();  //sample and calculate

    float tdsValue0 = gravityTds0.getTdsValue();  // then get the value
    float tdsValue1 = gravityTds1.getTdsValue();  // then get the value

    MoistSensorValue0 = analogRead(MoistSensorPin0);

    int pHSensorValue0 = analogRead(pHSensorPin0);
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
    delay(1000);

}

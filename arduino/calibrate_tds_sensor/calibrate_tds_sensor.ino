
//Este arduino eh responsavel por:
// Vaso 9: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Tanque: Sensor TDS (pino A2) e Sensor de pH (pino A3)
// Temperatura dos vasos (pino D12)
// Temperatura do tanque (pin A4)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_9': { 'tds': [0-1023], 'umidade': [0-1023]}, 'tanque': { 'tds': [0-1023], 'pH': [0-1023]} }

#include <EEPROM.h>

#include "GravityTDS.h"

#define TdsSensorPin A2


GravityTDS gravityTds;



void setup()
{
    Serial.begin(115200);
    pinMode(TdsSensorPin,INPUT);

    gravityTds.setPin(TdsSensorPin);

    gravityTds.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO

    gravityTds.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC

    gravityTds.begin();  //initialization

}

void loop()
{
    float temperature = 24;

    gravityTds.setTemperature(temperature);  // set the temperature and execute temperature compensation

    gravityTds.update();  //sample and calculate

    float tdsValue = gravityTds.getTdsValue();  // then get the value

    Serial.println(tdsValue);
    delay(500);

}

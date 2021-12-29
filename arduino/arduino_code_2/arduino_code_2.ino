//Este arduino eh responsavel por:
// Vaso 5: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Vaso 6: Sensor TDS (pino A2) e Sensor de umidade (pino A3)
// Vaso 7: Sensor TDS (pino A4) e Sensor de umidade (pino A5)
// Vaso 8: Sensor TDS (pino A6) e Sensor de umidade (pino A7)
// Sensor de temperatura de agua (pino D12)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_1': { 'tds': [0-1023], 'umidade': [0-1023]}, 'vaso_2': { 'tds': [0-1023], 'umidade': [0-1023]}, ... }

#include <EEPROM.h>

#include <OneWire.h>

#include <DallasTemperature.h>

#include "GravityTDS.h" 


#define TdsSensorPin0 19//a0
#define TdsSensorPin1 21//a2
#define TdsSensorPin2 23//A4
#define TdsSensorPin3 25//A6

#define MoistSensorPin0 20//A1
#define MoistSensorPin1 22//A3
#define MoistSensorPin2 24//A5
#define MoistSensorPin3 26//A7

#define ONE_WIRE_BUS 15//D12

GravityTDS gravityTds0;
GravityTDS gravityTds1;
GravityTDS gravityTds2;
GravityTDS gravityTds3;

int MoistSensorValue0;
int MoistSensorValue1;
int MoistSensorValue2;
int MoistSensorValue3;

// Setup a oneWire instance to communicate with any OneWire device
OneWire oneWire(ONE_WIRE_BUS);

// Pass oneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);


void setup()
{
    Serial.begin(115200);
    sensors.begin();	// Start up the library


    gravityTds0.setPin(TdsSensorPin0);
    gravityTds1.setPin(TdsSensorPin1);
    gravityTds2.setPin(TdsSensorPin2);
    gravityTds3.setPin(TdsSensorPin3);

    gravityTds0.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds1.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds2.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO
    gravityTds3.setAref(5.0);  //reference voltage on ADC, default 5.0V on Arduino UNO

    gravityTds0.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds1.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds2.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC
    gravityTds3.setAdcRange(1024);  //1024 for 10bit ADC;4096 for 12bit ADC


    gravityTds0.begin();  //initialization
    gravityTds1.begin();  //initialization
    gravityTds2.begin();  //initialization
    gravityTds3.begin();  //initialization

}

void loop()
{
    //temperature = readTemperature();  //add your temperature sensor and read it
    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);


    gravityTds0.setTemperature(temperature);  // set the temperature and execute temperature compensation
    gravityTds1.setTemperature(temperature);  // set the temperature and execute
    gravityTds2.setTemperature(temperature);  // set the temperature and execute
    gravityTds3.setTemperature(temperature);  // set the temperature and execute

    gravityTds0.update();  //sample and calculate
    gravityTds1.update();  //sample and calculate
    gravityTds2.update();  //sample and calculate
    gravityTds3.update();  //sample and calculate

    float tdsValue0 = gravityTds0.getTdsValue();  // then get the value
    float tdsValue1 = gravityTds1.getTdsValue();  // then get the value
    float tdsValue2 = gravityTds2.getTdsValue();  // then get the value
    float tdsValue3 = gravityTds3.getTdsValue();  // then get the value

    MoistSensorValue0 = analogRead(MoistSensorPin0);
    MoistSensorValue1 = analogRead(MoistSensorPin1);
    MoistSensorValue2 = analogRead(MoistSensorPin2);
    MoistSensorValue3 = analogRead(MoistSensorPin3);


    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      if (data == "sendit"){;
          Serial.print("{\"vaso_5\": { \"tds\": \"");
          Serial.print(tdsValue0);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue0);
          Serial.println("\"}, {\"vaso_6\": { \"tds\": \"");
          Serial.print(tdsValue1);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue1);
          Serial.println("\"}, {\"vaso_7\": { '\"tds\": \"");
          Serial.print(tdsValue2);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue2);
          Serial.println("\"}, {\"vaso_8\": { \"tds\": \"");
          Serial.print(tdsValue3);
          Serial.print("\", \"umidade\": \"");
          Serial.print(MoistSensorValue3);
          Serial.println("\"} }");
        }
    delay(1000);
    }

}
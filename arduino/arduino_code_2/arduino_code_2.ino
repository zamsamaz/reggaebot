//Este arduino eh responsavel por:
// Vaso 5: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Vaso 6: Sensor TDS (pino A2) e Sensor de umidade (pino A3)
// Vaso 7: Sensor TDS (pino A4) e Sensor de umidade (pino A5)
// Vaso 8: Sensor TDS (pino A6) e Sensor de umidade (pino A7)
// Sensor de temperatura de agua (pino D12)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_1': { 'tds': [0-1023], 'umidade': [0-1023]}, 'vaso_2': { 'tds': [0-1023], 'umidade': [0-1023]}, ... }
#include <EEPROM.h>


#define TdsSensorPin0 A0
#define TdsSensorPin1 A2
#define TdsSensorPin2 A4
#define TdsSensorPin3 A6

#define MoistSensorPin0 A1
#define MoistSensorPin1 A3
#define MoistSensorPin2 A5
#define MoistSensorPin3 A7


void setup()
{
    Serial.begin(115200);
    pinMode(TdsSensorPin0,INPUT);
    pinMode(TdsSensorPin1,INPUT);
    pinMode(TdsSensorPin2,INPUT);
    pinMode(TdsSensorPin3,INPUT);
    pinMode(MoistSensorPin0,INPUT);
    pinMode(MoistSensorPin1,INPUT);
    pinMode(MoistSensorPin2,INPUT);
    pinMode(MoistSensorPin3,INPUT);

}

void loop()
{
    int MoistSensorValue0;
    int MoistSensorValue1;
    int MoistSensorValue2;
    int MoistSensorValue3;
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
    
    float rawEc2 = analogRead(TdsSensorPin2) * aref / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
    float ec2 = (rawEc2 / temperatureCoefficient) * ecCalibration; // temperature and calibration compensation
    float tdsValue2 = ec2*tdsEcCoef;
    
    float rawEc3 = analogRead(TdsSensorPin3) * aref / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
    float ec3 = (rawEc3 / temperatureCoefficient) * ecCalibration; // temperature and calibration compensation
    float tdsValue3 = ec3*tdsEcCoef;

    MoistSensorValue0 = analogRead(MoistSensorPin0);

    MoistSensorValue1 = analogRead(MoistSensorPin1);

    MoistSensorValue2 = analogRead(MoistSensorPin2);

    MoistSensorValue3 = analogRead(MoistSensorPin3);
    

    Serial.print("2-\"vaso_5\":{\"tds\":\"");
    Serial.print(tdsValue0);
    Serial.print("\",\"umidade\":\"");
    Serial.print(MoistSensorValue0);
    Serial.print("\"},\"vaso_6\":{\"tds\":\"");
    Serial.print(tdsValue1);
    Serial.print("\",\"umidade\":\"");
    Serial.print(MoistSensorValue1);
    Serial.print("\"},\"vaso_7\":{\"tds\":\"");
    Serial.print(tdsValue2);
    Serial.print("\",\"umidade\":\"");
    Serial.print(MoistSensorValue2);
    Serial.print("\"},\"vaso_8\":{\"tds\":\"");
    Serial.print(tdsValue3);
    Serial.print("\",\"umidade\":\"");
    Serial.print(MoistSensorValue3);
    Serial.print("\"},");
    Serial.print("fim");
    delay(700);

}

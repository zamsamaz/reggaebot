
//Este arduino eh responsavel por:
// Vaso 9: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Tanque: Sensor TDS (pino A2) e Sensor de pH (pino A3)
// Temperatura dos vasos (pino D12)
// Temperatura do tanque (pin A4)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_9': { 'tds': [0-1023], 'umidade': [0-1023]}, 'tanque': { 'tds': [0-1023]} }

#include <EEPROM.h>

#define TdsSensorPin0 A0
#define TdsSensorPin1 A2

#define MoistSensorPin0 A1


void setup()
{

    Serial.begin(115200);
    pinMode(TdsSensorPin0,INPUT);
    pinMode(TdsSensorPin1,INPUT);
    pinMode(MoistSensorPin0,INPUT);

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


    Serial.print("3-\"vaso_9\":{\"tds\":\"");
    Serial.print(tdsValue0);
    Serial.print("\",\"umidade\":\"");
    Serial.print(MoistSensorValue0);
    Serial.print("\"},\"tanque\":{\"tds\":\"");
    Serial.print(tdsValue1);
    Serial.print("\"}}");
    Serial.print("fim");
    delay(700);

}

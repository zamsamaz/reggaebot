//Este arduino eh responsavel por:
// Vaso 1: Sensor TDS (pino A0) e Sensor de umidade (pino A1)
// Vaso 2: Sensor TDS (pino A2) e Sensor de umidade (pino A3)
// Vaso 3: Sensor TDS (pino A4) e Sensor de umidade (pino A5)
// Vaso 4: Sensor TDS (pino A6) e Sensor de umidade (pino A7)
// Sensor de temperatura de agua (pino D12)
// as infos sao mandadas via serial no formato de um python dict (JSON)
// exemplo: { 'vaso_1': { 'tds': [0-1023], 'umidade': [0-1023]}, 'vaso_2': { 'tds': [0-1023], 'umidade': [0-1023]}, ... }


#include <EEPROM.h>

#define TdsSensorPin0 A0
#define TdsSensorPin1 A2
#define TdsSensorPin2 A4
#define TdsSensorPin3 A6
#define VREF 5.0      // analog reference voltage(Volt) of the ADC
#define SCOUNT  30           // sum of sample point
int analogBuffer0[SCOUNT], analogBuffer1[SCOUNT], analogBuffer2[SCOUNT], analogBuffer3[SCOUNT];    // store the analog value in the array, read from ADC
int analogBufferTemp0[SCOUNT], analogBufferTemp1[SCOUNT], analogBufferTemp2[SCOUNT], analogBufferTemp3[SCOUNT];
int analogBufferIndex0 = 0, analogBufferIndex1 = 0, analogBufferIndex2 = 0, analogBufferIndex3 = 0;
int copyIndex0 = 0, copyIndex1 = 0, copyIndex2 = 0, copyIndex3 = 0;
float averageVoltage0 = 0, averageVoltage1 = 0, averageVoltage2 = 0, averageVoltage3 = 0;
float temperature = 25;
float tdsValue0 = 0, tdsValue1 = 0,tdsValue2 = 0,tdsValue3 = 0;

#define MoistSensorPin0 A1
#define MoistSensorPin1 A3
#define MoistSensorPin2 A5
#define MoistSensorPin3 A7

int MoistSensorValue0;
int MoistSensorValue1;
int MoistSensorValue2;
int MoistSensorValue3;

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

    //TDS SENSOR 0

    static unsigned long analogSampleTimepoint = millis();
    if(millis()-analogSampleTimepoint > 40U)     //every 40 milliseconds,read the analog value from the ADC
    {
    analogSampleTimepoint = millis();
    analogBuffer0[analogBufferIndex0] = analogRead(TdsSensorPin0);    //read the analog value and store into the buffer
    analogBufferIndex0++;
    if(analogBufferIndex0 == SCOUNT)
        analogBufferIndex0 = 0;
    }
    static unsigned long printTimepoint = millis();
    if(millis()-printTimepoint > 800U)
    {
     printTimepoint = millis();
     for(copyIndex0=0;copyIndex0<SCOUNT;copyIndex0++)
       analogBufferTemp0[copyIndex0]= analogBuffer0[copyIndex0];
     averageVoltage = getMedianNum(analogBufferTemp0,SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
     float compensationCoefficient=1.0+0.02*(temperature-25.0);    //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
     float compensationVoltage=averageVoltage/compensationCoefficient;  //temperature compensation
     tdsValue0=(133.42*compensationVoltage*compensationVoltage*compensationVoltage - 255.86*compensationVoltage*compensationVoltage + 857.39*compensationVoltage)*0.5; //convert voltage value to tds value
    }

    //TDS SENSOR 1

    static unsigned long analogSampleTimepoint = millis();
    if(millis()-analogSampleTimepoint > 40U)     //every 40 milliseconds,read the analog value from the ADC
    {
    analogSampleTimepoint = millis();
    analogBuffer1[analogBufferIndex1] = analogRead(TdsSensorPin1);    //read the analog value and store into the buffer
    analogBufferIndex1++;
    if(analogBufferIndex1 == SCOUNT)
        analogBufferIndex1 = 0;
    }
    static unsigned long printTimepoint = millis();
    if(millis()-printTimepoint > 800U)
    {
     printTimepoint = millis();
     for(copyIndex1=0;copyIndex1<SCOUNT;copyIndex1++)
       analogBufferTemp1[copyIndex1]= analogBuffer1[copyIndex1];
     averageVoltage = getMedianNum(analogBufferTemp1,SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
     float compensationCoefficient=1.0+0.02*(temperature-25.0);    //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
     float compensationVoltage=averageVoltage/compensationCoefficient;  //temperature compensation
     tdsValue1=(133.42*compensationVoltage*compensationVoltage*compensationVoltage - 255.86*compensationVoltage*compensationVoltage + 857.39*compensationVoltage)*0.5; //convert voltage value to tds value
    }

    //TDS SENSOR 2

    static unsigned long analogSampleTimepoint = millis();
    if(millis()-analogSampleTimepoint > 40U)     //every 40 milliseconds,read the analog value from the ADC
    {
    analogSampleTimepoint = millis();
    analogBuffer2[analogBufferIndex2] = analogRead(TdsSensorPin2);    //read the analog value and store into the buffer
    analogBufferIndex2++;
    if(analogBufferIndex2 == SCOUNT)
        analogBufferIndex2 = 0;
    }
    static unsigned long printTimepoint = millis();
    if(millis()-printTimepoint > 800U)
    {
     printTimepoint = millis();
     for(copyIndex2=0;copyIndex2<SCOUNT;copyIndex2++)
       analogBufferTemp2[copyIndex2]= analogBuffer2[copyIndex2];
     averageVoltage = getMedianNum(analogBufferTemp2,SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
     float compensationCoefficient=1.0+0.02*(temperature-25.0);    //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
     float compensationVoltage=averageVoltage/compensationCoefficient;  //temperature compensation
     tdsValue2=(133.42*compensationVoltage*compensationVoltage*compensationVoltage - 255.86*compensationVoltage*compensationVoltage + 857.39*compensationVoltage)*0.5; //convert voltage value to tds value
    }

    //TDS SENSOR 3

    static unsigned long analogSampleTimepoint = millis();
    if(millis()-analogSampleTimepoint > 40U)     //every 40 milliseconds,read the analog value from the ADC
    {
    analogSampleTimepoint = millis();
    analogBuffer3[analogBufferIndex3] = analogRead(TdsSensorPin3);    //read the analog value and store into the buffer
    analogBufferIndex3++;
    if(analogBufferIndex3 == SCOUNT)
        analogBufferIndex3 = 0;
    }
    static unsigned long printTimepoint = millis();
    if(millis()-printTimepoint > 800U)
    {
     printTimepoint = millis();
     for(copyIndex3=0;copyIndex3<SCOUNT;copyIndex3++)
       analogBufferTemp3[copyIndex3]= analogBuffer3[copyIndex3];
     averageVoltage = getMedianNum(analogBufferTemp3,SCOUNT) * (float)VREF / 1024.0; // read the analog value more stable by the median filtering algorithm, and convert to voltage value
     float compensationCoefficient=1.0+0.02*(temperature-25.0);    //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0));
     float compensationVoltage=averageVoltage/compensationCoefficient;  //temperature compensation
     tdsValue3=(133.42*compensationVoltage*compensationVoltage*compensationVoltage - 255.86*compensationVoltage*compensationVoltage + 857.39*compensationVoltage)*0.5; //convert voltage value to tds value
    }


    MoistSensorValue0 = analogRead(MoistSensorPin0);
    MoistSensorValue1 = analogRead(MoistSensorPin1);
    MoistSensorValue2 = analogRead(MoistSensorPin2);
    MoistSensorValue3 = analogRead(MoistSensorPin3);


    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      if (data == "sendit"){

          Serial.print("1-{\"vaso_1\": { \"tds\": \"");
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
    delay(1000);
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

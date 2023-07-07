#define button 8  
#include "Arduino_SensorKit.h"
#include <stdio.h>
#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

//load cells pins:
const int HX711_dout_1 = 3; //mcu > HX711 dout pin
const int HX711_sck_1 = 2; //mcu > HX711 sck pin

const int HX711_dout_2 = 5; //mcu > HX711 dout pin
const int HX711_sck_2 = 4; //mcu > HX711 sck pin

const int HX711_dout_3 = 7; //mcu > HX711 dout pin
const int HX711_sck_3 = 6; //mcu > HX711 sck pin

//HX711 constructors:
HX711_ADC LoadCell_1(HX711_dout_1, HX711_sck_1);
HX711_ADC LoadCell_2(HX711_dout_2, HX711_sck_2);
HX711_ADC LoadCell_3(HX711_dout_3, HX711_sck_3);

const int calVal_eepromAdress = 0;
unsigned long t = 0;

bool post_status_arduino =true;
int button_state = 0;

void setup() {
  
  pinMode(button, INPUT);

  Serial.begin(9600);
  LoadCell_1.begin();
  LoadCell_2.begin();
  LoadCell_3.begin();
  Pressure.begin();
   
  float calibrationValue_1 = 465.00;
  float calibrationValue_2 = 291.36;
  float calibrationValue_3 = 513.18; 
  
  #if defined(ESP8266)|| defined(ESP32)
  //EEPROM.begin(512); // uncomment this if you use ESP8266/ESP32 and want to fetch the calibration value from eeprom
  #endif
  //EEPROM.get(calVal_eepromAdress, calibrationValue); // uncomment this if you want to fetch the calibration value from eeprom

  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step
  LoadCell_1.start(stabilizingtime, _tare);
  LoadCell_2.start(stabilizingtime, _tare);
  LoadCell_3.start(stabilizingtime, _tare);

  if (LoadCell_1.getTareTimeoutFlag()) {
    //Serial.println("Timeout1, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell_1.setCalFactor(calibrationValue_1); // set calibration value (float)
    //Serial.println("Startup 1 is complete");
  }

  if (LoadCell_2.getTareTimeoutFlag()) {
    //Serial.println("Timeout2, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell_2.setCalFactor(calibrationValue_2); // set calibration value (float)
    //Serial.println("Startup 2 is complete");
  }

  if (LoadCell_3.getTareTimeoutFlag()) {
    //Serial.println("Timeout3, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell_3.setCalFactor(calibrationValue_3); // set calibration value (float)
    //Serial.println("Startup 3 is complete");
  }
}

void loop(){

  static boolean newDataReady = false;
  const int serialPrintInterval = 5000; //increase value to slow down serial print activity
  float weight_1=0, weight_2=0, weight_3=0, pressure=0, temperature=0;


  button_state = digitalRead(button);
  
  temperature = Pressure.readTemperature(); 
  
  pressure = Pressure.readPressure(); //misura in Pascal
  pressure = pressure/100000; //per ottenere la misura in Bar

  // check for new data/start next conversion:
  if (LoadCell_1.update() || LoadCell_2.update() || LoadCell_3.update()) newDataReady = true;

  // get smoothed value from the dataset:
  if (newDataReady) {

    if (button_state == HIGH) {
      if (millis() > t + 250) {
        post_status_arduino = !post_status_arduino; 
        //Serial.println("bottone premuto");
        t = millis();
      }
    }

    if (millis() > t + serialPrintInterval) {
      //float i = LoadCell.getData();
      //Serial.print("Load_cell output val: ");
      //Serial.println(i);
       weight_1 = LoadCell_1.getData();
       weight_2 = LoadCell_2.getData();
       weight_3 = LoadCell_3.getData();

       if (weight_1<0.2) weight_1=0.0;
       if (weight_2<0.2) weight_2=0.0;
       if (weight_3<0.2) weight_3=0.0;

       
       Serial.write(0xff);
       Serial.print(String(temperature)+ "," + String(pressure) + "," + String(weight_1)+ "," + String(weight_2)+ "," + String(weight_3)+ "," + String(post_status_arduino));
       Serial.write(0xfe);

      newDataReady = false;
      t = millis();
    }
  }

  /*// receive command from serial terminal, send 't' to initiate tare operation:
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't'){
      LoadCell_1.tareNoDelay();
      LoadCell_2.tareNoDelay();
      LoadCell_3.tareNoDelay();
    } 
  }

  // check if last tare operation is complete:
  if ((LoadCell_1.getTareStatus() == true) && (LoadCell_2.getTareStatus() == true) && (LoadCell_3.getTareStatus() == true)) {
    Serial.println("Tare complete");
  }*/

}

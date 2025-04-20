#include <Arduino.h>
#include <LiquidCrystal.h>
#include <string.h>
#include <Servo.h>

#define X_POS  A1 // Arduino pin connected to VRX pin
#define Y_POS  A0
#define POT A2
 
int xValue=0;
int yValue=0;

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

String cities[11] = {
  "Tokyo",
  "Paris",
  "New York",
  "Sydney",
  "Cairo",
  "Rio de Janeiro",
  "Moscow",
  "Cape Town",
  "Toronto",
  "Bangkok",
  "Berlin"
};

Servo wateringCan;


void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(8, OUTPUT);
  wateringCan.attach(6);

  Serial.begin(9600);
  lcd.begin(16, 2);
}

int canPos;
int crop;

int cityPos;
int prev=0;
int x=0;
bool tracking=false;
String incoming;
String cityArray[11];
int cityCounter=0;
String cityNameArray[11];
String forecastArray[11];
String temperatureArray[11];
String aqiArray[11];

bool orangeDetected=false;

boolean doneLoading=false;

int health=1;

struct crop{
  bool warm;
  bool sun;
  bool smogResistant;
};

bool potChanged=false;
bool goodSpinachTemp=false;
bool goodOrangeTemp=false;

enum plant_type{orange,spinach,none};
bool waterPoured=true;

void scroll(){
  int index=map(analogRead(POT),0,1023,0,10);
  potChanged=true;

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(cityNameArray[index]);
  lcd.setCursor(0,1);

  //assuming for socal, most plants like sun and clouds 
  if (potChanged){
    waterPoured=true;
    if(forecastArray[index].indexOf("Cloudy") != -1){
      goodSpinachTemp=true;

    }if(forecastArray[index].indexOf("Clear") != -1 || forecastArray[index].indexOf("Sunny") != -1 ){
      goodOrangeTemp=true;
    }

    if(temperatureArray[index].toInt()<55){
      goodSpinachTemp=true;
    }

    bool airBad=false;
    if(aqiArray[index].toInt()>50){
      lcd.print("bad air");
      digitalWrite(8,HIGH);
      airBad=true;
    }
    if(!goodOrangeTemp ||!goodSpinachTemp){
      lcd.print(" bad temp");
      digitalWrite(8,HIGH);

    }
    else if(crop==spinach &&goodSpinachTemp && !airBad){
      lcd.print("great spinach");
    }
    else if(crop==orange &&goodOrangeTemp && !airBad && orangeDetected){
      lcd.print("great orange");
      
      if(waterPoured){
        wateringCan.write(0);
        delay(250);
        wateringCan.write(100);
        waterPoured=false;
      }
      digitalWrite(8,LOW);

    }
    potChanged=false;
  }

}

void loop() {



  if (Serial.available()) {

    if(cityCounter<=11){
      incoming = Serial.readStringUntil('\n');
      cityArray[cityCounter]=incoming;
      int commaIndex = incoming.indexOf(',');
      int dashIndex = incoming.indexOf('-');
      int tildeIndex = incoming.indexOf('+');

      
      if (commaIndex != -1) {
        cityNameArray[cityCounter] = incoming.substring(0, commaIndex);
        forecastArray[cityCounter] = incoming.substring(commaIndex+1, dashIndex);
        temperatureArray[cityCounter] = incoming.substring(dashIndex+1,tildeIndex);
        aqiArray[cityCounter] = incoming.substring(tildeIndex+1);

      } 

      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print(aqiArray[cityCounter]);
      lcd.setCursor(0,1);
      lcd.print(cityNameArray[cityCounter]);
      delay(125); 

      cityCounter++;
      if(cityCounter>=11){
        doneLoading=true;
      }
    }

    lcd.clear();

    if(doneLoading){
      while (true){
        scroll();
        delay(100);
        lcd.clear();
        if (Serial.available()) {
          String incoming = Serial.readStringUntil('\n');
          int val = incoming.toInt();
  
          if (val == 1) {
            crop = orange;
            digitalWrite(9, HIGH);
            digitalWrite(10, LOW);
            orangeDetected=true;
          } else if (val == 2) {
            crop = spinach;
            digitalWrite(10, HIGH);
            digitalWrite(9, LOW);
          } else if (val == 0) {
            orangeDetected=false;
            digitalWrite(10, LOW);
            digitalWrite(9, LOW);
          }
        }
      }
    }
  }
}


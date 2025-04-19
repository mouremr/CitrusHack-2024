#include <Arduino.h>
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  while(!Serial);  // Wait for serial port on Leonardo/32u4 boards
}

void loop() {
  if(Serial.available()) {
    String incoming = Serial.readStringUntil('\n');
    incoming.trim();  // Remove any whitespace
    
    // Enhanced feedback
    Serial.println(incoming);  // Critical \n addition
    
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    digitalWrite(LED_BUILTIN, LOW);
    delay(100);

  }
}

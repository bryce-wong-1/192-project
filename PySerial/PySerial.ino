#include <LiquidCrystal.h>
int x;
LiquidCrystal lcd(11,10,5,4,3,2);
int counter = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(8, INPUT);
  lcd.begin(16,2);
  lcd.clear();
}

void loop() {
  // put your main code here, to run repeatedly:
  while (!Serial.available())
  {
    if(digitalRead(8) == HIGH || Serial.readString() == "y"){
      counter++;
      lcd.setCursor(3,1);
      lcd.print(counter);
      delay(200);
      x = Serial.readString().toInt();
      Serial.print(counter);
    }
  }
}

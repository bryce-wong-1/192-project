#include <LiquidCrystal.h>
using namespace std;
// Creates an LCD object. Parameters: (rs, enable, d4, d5, d6, d7)
LiquidCrystal lcd(11, 10, 5, 4, 3, 2);
int counter = 0;
void setup() 
{
  pinMode(8,INPUT);
	// set up the LCD's number of columns and rows:
	lcd.begin(16, 2);

	// Clears the LCD screen
	lcd.clear();
}

void loop() 
{
	// Print a message to the LCD
  lcd.setCursor(3,1);
  lcd.print(counter);
  if(digitalRead(8) == HIGH){
    counter += 1;
    lcd.setCursor(3,1);
    lcd.print(counter);
    delay(200);
    }
  else{
    lcd.print("");
  }
	

	// set the cursor to column 0, line 1
	// (note: line 1 is the second row, since counting begins with 0):
	// Print a message to the LCD.
	
}
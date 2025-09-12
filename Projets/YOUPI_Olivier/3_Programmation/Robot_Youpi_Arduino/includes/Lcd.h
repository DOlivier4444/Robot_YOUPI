#include <LiquidCrystal_I2C.h>

//// LCD screen
constexpr int SCREEN_ADRESS = 0x27; // chip : PCF8574T
constexpr int NBR_CHAR = 20;
constexpr int NBR_LINES = 4;
LiquidCrystal_I2C lcd(SCREEN_ADRESS, NBR_CHAR, NBR_LINES);  // Setup the LCD display to NBR_CHAR chars and NBR_LINES lines


void init_lcd(){  // Initialisation of the lcd screen
  lcd.init();
  delay(50);
  lcd.backlight();
  delay(50);
  lcd.clear();
}

void lcd_clear_line(int noLine){  // clear a dedicated line
  for(int i = 0; i < NBR_CHAR; i++){
    lcd.setCursor(i, noLine);
    lcd.print(" ");
  }
}
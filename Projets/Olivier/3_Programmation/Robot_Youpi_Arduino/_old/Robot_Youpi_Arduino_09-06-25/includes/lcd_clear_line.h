//#include <LiquidCrystal_I2C.h>

void lcd_clear_line(int noLine, LiquidCrystal_I2C &lcd, int nbrChar){
  for(int i = 0; i < nbrChar; i++){
    lcd.setCursor(i, noLine);
    lcd.print(" ");
  }
}

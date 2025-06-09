#include <LiquidCrystal_I2C.h>
#include "lcd_clear_line.h"
#include "receive_from_rpi.h"
#include "send_to_rpi.h"

//// Robot Data
// Lengths of the Robot's arm
#define L1 0.28
#define L2 0.162
#define L3 0.162
#define L4 0.15


const int MOTOR_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};  // ports where cables are plugged in

const int SCREEN_ADRESS = 0x27; // chip : PCF8574T
const int NBR_CHAR = 20;
const int NBR_LINES = 4;
LiquidCrystal_I2C lcd(SCREEN_ADRESS, NBR_CHAR, NBR_LINES);  // Setup the LCD display to 20 chars and 4 line

typedef enum {
    ARDUINO_READY,
    RASPBERRY_READY,
    MOVEMENT_FINISHED,
    PROGRAM_FINISHED,
    ERROR_MOVEMENT,
    MESSAGE_COUNT
} Message;

const char* messageStrings[MESSAGE_COUNT] = {
    "Arduino ready!",
    "Raspberry ready!",
    "Movement finished",
    "Program finished"
    "Error movement !"
};

void initialisation() {

  // Reset signal
  const int RESET_SIGNAL = 0X47; // 2#01000111 -- 16#47
  int resetByte[8];

  for (int i = 0; i < 8; i++) {
    pinMode(MOTOR_PINS[i], OUTPUT);

    resetByte[i] = (RESET_SIGNAL & (1 << i )) >> i;
    digitalWrite(MOTOR_PINS[i], resetByte[i]);
  }
  delay(125);

  for (int i = 0; i < 8; i++){
    digitalWrite(MOTOR_PINS[i], LOW);
  }


  // initialize the lcd
  lcd.init();
  lcd.backlight();
  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("Allumage de YOUPI...");


  // Serial connexion
  const int BAUD_RATE = 9600;

  Serial.begin(BAUD_RATE); 
  while (!Serial) {
    lcd.setCursor(0,2);
    lcd.print("Ouverture port serie");
  }

  lcd.setCursor(4,2);
  lcd.print("Com RPI 3B+ :");

  int nbrOfTry = 0;
  String receivedData = "";
  do {
    if (Serial.available() > 0){
      
      nbrOfTry ++;
      lcd_clear_line(3, lcd, NBR_CHAR);
      lcd.setCursor(3,3);
      lcd.print("Tentative no ");
      lcd.print(nbrOfTry);

      receivedData = receive_from_rpi();

    } else {
      
      lcd.setCursor(1,3);
      lcd.print("Attente de donnees");

    }    
  } while (receivedData != "Raspberry ready !");

  lcd_clear_line(3, lcd, NBR_CHAR);
  lcd.setCursor(2,3);
  lcd.print(receivedData);

  send_to_rpi("Arduino ready !");

}


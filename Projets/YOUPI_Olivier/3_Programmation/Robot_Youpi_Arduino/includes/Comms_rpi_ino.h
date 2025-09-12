#include "api/Common.h"
//// Communication
constexpr int DIRECT = true;  // If true, the data is sent directly without markers

// Messages from Raspberry to Arduino
enum From_RPI : uint8_t {
  FROM_RPI_RASPBERRY_READY = 0xA1,
  FROM_RPI_START_MOVEMENT = 0xA2,
  FROM_RPI_ABORT_PROGRAM = 0xA3,
  FROM_RPI_PROGRAM_EXECUTION = 0xA4,
  FROM_RPI_PROGRAM_FINISHED = 0xA5,
  FROM_RPI_ROBOT_RESET_SIGNAL = 0xAA,
  FROM_RPI_RESET_ARDUINO = 0xA
};

// Messages from Arduino to Raspberry
enum To_RPI : uint8_t {
  TO_RPI_ARDUINO_READY = 0xB1,
  TO_RPI_READY_TO_RECEIVE = 0xB2,
  TO_RPI_MOVEMENT_FINISHED = 0xB3
};

void send_to_rpi(uint8_t cmd) {
  Serial.write('<');  // start marker
  Serial.write(cmd);  // binary command code
  Serial.write('>');  // end marker
}

bool receive_from_rpi(uint8_t &cmd, String &payload) {
  if (Serial.available() <= 0) return false;

  // attendre start marker
  if (Serial.read() != '<') return false;

  // attendre commande
  while (!Serial.available());
  cmd = (uint8_t)Serial.read();

  payload = "";

  // Lire jusqu'au '>'
  String temp = "";
  while (true) {
    while (!Serial.available());
    char c = Serial.read();
    if (c == '>') break;
    temp += c;
  }

  // Si il y a un séparateur '|', séparer payload
  int sepIndex = temp.indexOf('|');
  if (sepIndex != -1) {
    payload = temp.substring(sepIndex + 1);
  }

  return true;
}




//String receive_from_rpi(bool direct) {
//  const char startMarker  = '<';
//  const char endMarker    = '>';
//
//  char    incomingChar;  // one character (ex : L )
//  String  receivedData = "";  // exemple of data : <L-1500-1-2-3-4-5-6-7-8>
//
//
//  if (direct){
//    incomingChar = Serial.read();
//    receivedData += incomingChar;
//
//  } else {
//
//    do {
//      if (Serial.available() > 0) {
//        incomingChar = Serial.read();
//      }
//    } while (incomingChar != startMarker);
//
//    while (true) {
//      if (Serial.available()) {
//        incomingChar = Serial.read();
//
//        if (incomingChar == endMarker) {
//          receivedData += '\0';
//          break;
//        } else {
//          receivedData += incomingChar;
//        }
//      } // timeout ?
//    }
//
//  }
//  return receivedData;
//}

void init_serial_connexion() {  // Initialise the serial connexion --> synchronysing the raspberry and the arduino
  // this function needs the lcd screen to be initialized

  // Opens serial ports
  lcd.setCursor(0, 2);
  lcd.print("Ouverture port serie");
  const int BAUD_RATE = 9600;
  Serial.begin(BAUD_RATE);
  while(!Serial){}
  lcd_clear_line(2);

  // Wait for the ready message
  lcd.setCursor(4, 2);
  lcd.print("Com RPI 3B+ :");
  lcd.setCursor(1, 3);
  lcd.print("Attente de donnees");
  uint8_t cmd;
  String payload;
  do {
  } while (!receive_from_rpi(cmd, payload) && cmd != FROM_RPI_RASPBERRY_READY);
  lcd_clear_line(3);
  lcd.setCursor(2, 3);
  lcd.print("raspberry ready !");


  // Send the ready message back
  send_to_rpi(TO_RPI_ARDUINO_READY);
}

  //uint8_t cmd = 0x00;
  //String payload = "";
  //do {
  //  lcd.setCursor(1, 3);
  //  lcd.print("Attente de donnees");
  //} while (!receive_from_rpi(cmd, payload) && cmd != FROM_RPI_RASPBERRY_READY);
//
  //lcd_clear_line(3);
  //lcd.setCursor(2, 3);
  //lcd.print("raspberry ready !");
//
  //send_to_rpi(TO_RPI_ARDUINO_READY);
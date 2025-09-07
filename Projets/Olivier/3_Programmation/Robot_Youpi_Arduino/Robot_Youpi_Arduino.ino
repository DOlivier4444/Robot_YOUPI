#include "includes\Arduino_tools.h"

#include "includes\Led_matrix.h"
#include "includes\Lcd.h"
#include "includes\Comms_rpi_ino.h"
#include "includes\Robot_interface.h"

#include "includes\Robots_program.h"

// Initialisation of the robot's data
int codersMotors[6] = { 0, 0, 0, 0, 0, 0 };

void setup(){
  init_lcd();
  lcd.setCursor(0,0);
  lcd.print("Allumage de YOUPI...");
  matrix_robot_pick_place();
  matrix_youpi_blinking();

  robot_pinout_init();
  robot_reset_signal();

  init_serial_connexion();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Attente de commande.");
}

void loop() {  
  uint8_t cmd;
  String payload;

  if (receive_from_rpi(cmd, payload)) {
    switch (cmd) {
      case FROM_RPI_PROGRAM_EXECUTION:
        lcd.setCursor(0,0);
        lcd.print("Demarrage programme ");
        robots_program(codersMotors);
        lcd.setCursor(0,0);
        lcd.print("Fin programme");
        break;

      case FROM_RPI_ROBOT_RESET_SIGNAL:
        robot_reset_signal();
        break;

      case FROM_RPI_RESET_ARDUINO:
        reboot();
        break;
    }
  }
}


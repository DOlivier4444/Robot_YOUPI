#include <stdio.h>

#include "includes\initialisation.h"
#include "includes\robots_program.h"

void setup() {

  initialisation();  //Initialisation of the motors --> //void Initialisation(const int MotorPins[]); ??

  // Initialisation of the robot's data
  int   codersMotors[6] = { 0 };  
  float motorAngles[6] = { 0 };
  float cartesianPositions[6] = { 0 };

  lcd.clear();
  delay(125);

  int etat;



  do{
    etat = robots_program(codersMotors, motorAngles);
    delay(125);
  } while (etat == 0x00);
  lcd.print("Mouvement invalide");

  lcd.setCursor(0,1);
  lcd.print("code erreur : ");
  lcd.print(etat);

  lcd.setCursor(0,2);
  for (int i; i<6; i++) {
    lcd.print(motorAngles[i]);
  }
}

void loop() {

}


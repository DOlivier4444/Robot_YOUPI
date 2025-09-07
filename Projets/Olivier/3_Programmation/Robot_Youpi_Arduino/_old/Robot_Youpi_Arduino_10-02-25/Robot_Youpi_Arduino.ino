// Device signature = 0x1e9406 // Arduino NANO (ATmega 168)

/* Note for myself:
 be sure to select ATmega 168 in tools --> Processor --> ATmega 168 !
*/

#include ".\Includes\Initialisation.h"
#include ".\Programs\Robots_dance_v1.h"


void Initialisation();


void setup() {

  Serial.begin(9600);  //Opening the serial connexion

  Initialisation();  //Initialisation of the motors

  int coders_motors[6] = { 0, 0, 0, 0, 0, 0 };  // Initialisation of the coders
  float thetas[6] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };
  float cartesian_position[6] = { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

  Robots_dance_v1(coders_motors, thetas, cartesian_position);

}

void loop() {

  //Test communication série
  //if (Serial.available() > 0) {
  //  String data = Serial.readStringUntil('\n');
  //  Serial.print("You sent me: ");
  //  Serial.println(data);
  //}
}
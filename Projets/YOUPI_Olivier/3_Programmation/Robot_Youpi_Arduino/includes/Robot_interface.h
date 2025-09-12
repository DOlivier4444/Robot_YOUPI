#include "api/Common.h"

//// Robot Data
// Pinout arduino
constexpr int MOTOR_PINS[8] = {2, 3, 4, 5, 6, 7, 8, 9};
// Lengths of the Robot's arm
constexpr float L1 = 0.28;
constexpr float L2 = 0.162;
constexpr float L3 = 0.162;
constexpr float L4 = 0.15;


void robot_pinout_init(){ // Initialisation of the arduino pinouts used by the robot
  for (int i = 0; i < 8; i++) {
    pinMode(MOTOR_PINS[i], OUTPUT);
  }
}

void robot_reset_signal(){  // the robot needs to receive a "reset signal" before any movements -- see documentations
  const int RESET_SIGNAL = 0X47; // 2#01000111 -- 16#47
  int resetBit;

  for (int i = 0; i < 8; i++){
    digitalWrite(MOTOR_PINS[i], LOW);
  }
  delay(10);

  for (int i = 0; i < 8; i++) {
    resetBit = (RESET_SIGNAL >> i) & 1;
    digitalWrite(MOTOR_PINS[i], resetBit);
  }
  delay(10);

  for (int i = 0; i < 8; i++){
    digitalWrite(MOTOR_PINS[i], LOW);
  }
}

void motor_stepper_prep() { // preparation of the motor pins before the first step
  // Increase the movement speed by limiting function calls or conditionnal testing in the motor stepper function
  digitalWrite(MOTOR_PINS[7], LOW);
}

void motor_stepper(int motorID) { // Function to move 1 step of the motorID motor of the robot
  int Delay = 5;  // Delay between the preparation of the rotation, and the rotation command
  int motorIDBit;
  // Prevent the rotation of motor4 when motor3 moves
  //if (motor_id == 3) {
  //  for (int i = 0; i < 3; i++) {
  //    Motor_bin[i] = ((motor_id + 1) & (1 << i)) >> i;
  //    digitalWrite(MOTOR_PINS[i], Motor_bin[i]);
  //  }
  //  // Validation pin off : byte sent
  //  digitalWrite(MOTOR_PINS[6], HIGH);
  //  delayMicroseconds(Delay);
  //  digitalWrite(MOTOR_PINS[6], LOW);
  //}

  digitalWrite(MOTOR_PINS[6], HIGH); // validation pin

  for (int i = 0; i < 3; i++) {
    motorIDBit = (motorID >> i) & 1;
    digitalWrite(MOTOR_PINS[i], motorIDBit);
  }
  digitalWrite(MOTOR_PINS[6], LOW);  // Validation pin off : byte sent

  /*
  Note to explain the code below :
  //-------------------------------------------------------
    for (int i = 0; i < 3; i++) {
      digitalWrite(MOTOR_PINS[i], (motorID >> i) & 1));
    }
  
  familly friendly version :

  MOTOR_PINS[0] = (motorID >> 0) & 1); // test and write this bit 00000001
  MOTOR_PINS[1] = (motorID >> 1) & 1); // test and write this bit 00000010
  MOTOR_PINS[2] = (motorID >> 2) & 1); // test and write this bit 00000100

  It's as shrimple as that
  //-------------------------------------------------------
  */
}


void rotation_direction(int rotations[], int mvtToDo[]) {
  const int FORWARD = 1;
  const int BACKWARDS = 0;
  const int delay = 0; // In microseconds
  
  digitalWrite(MOTOR_PINS[6], LOW); // turn off the 2 validation pin
  digitalWrite(MOTOR_PINS[7], LOW);

  for (int i = 0; i < 6; i++) {
    rotations[i] = (mvtToDo[i] >= 0) ? FORWARD : BACKWARDS;
    digitalWrite(MOTOR_PINS[i], rotations[i]);
  }

  // Validation pin off : byte sent
  digitalWrite(MOTOR_PINS[7], HIGH);
  delayMicroseconds(delay);
  digitalWrite(MOTOR_PINS[7], LOW);
}



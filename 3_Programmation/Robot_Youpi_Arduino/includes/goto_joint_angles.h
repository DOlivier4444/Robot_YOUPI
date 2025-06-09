#include <stdio.h>
#include <time.h>


#include "coder_motor_target.h"
#include "rotation_direction.h"
#include "movement_to_do.h"
#include "max_array_int.h"

#include "motor_stepper.h"
#include "encoders.h"


int goto_joint_angles(int speed, float motorAngles[], int codersMotors[]) {

  const int MOTOR_IDS[6] = { 0, 1, 2, 3, 4, 5 };

  int codersMotorsTarget[6] = { 0 };
  int rotations[6] = { 0 };
  int mvtToDo[6] = { 0 };
  int maxMovement;

  unsigned long t, timeTaken = 0;


  coder_motor_target(motorAngles, codersMotorsTarget);
  movement_to_do(mvtToDo, codersMotorsTarget, codersMotors);
  maxMovement = max_array_int(mvtToDo, 6);  
  rotation_direction(rotations, mvtToDo, MOTOR_PINS); 

  // ---------- Movement of the robot ----------

  for (int i = 0; i < maxMovement; i++) {
    t = micros();
    for (int m = 0; m < 6; m++) {  // switch between the 6 motors
      if ( abs(mvtToDo[m]) > 0) {
        motor_stepper(MOTOR_IDS[m], MOTOR_PINS);
        codersMotors[m] = encoders(rotations[m], codersMotors[m]);
        mvtToDo[m] = codersMotorsTarget[m] - codersMotors[m];
      }
    }
    timeTaken = micros() - t;  // in miliseconds
    delayMicroseconds(speed - timeTaken);
  }
}

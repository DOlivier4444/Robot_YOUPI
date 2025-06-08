#include <stdio.h>
#include <time.h>


#include "coder_motor_target.h"
#include "rotation_direction.h"
#include "movement_to_do.h"
#include "max_array_int.h"

#include "validate_move.h"
#include "motor_stepper.h"
#include "encoders.h"


int goto_joint_angles(int speed, float motorAngles[], int codersMotors[]) {

  const int MOTOR_IDS[6] = { 0, 1, 2, 3, 4, 5 };

  int codersMotorsTarget[6] = { 0 };
  int rotations[6] = { 0 };
  int mvtToDo[6] = { 0 };
  int maxMovement;

  unsigned long t, timeTaken = 0;

  int movement_validation = validate_move(motorAngles);

  if ( movement_validation == 0x00 )
  {
    coder_motor_target(motorAngles, codersMotorsTarget);
    movement_to_do(mvtToDo, codersMotorsTarget, codersMotors);
    maxMovement = max_array_int(mvtToDo, 6);

    rotation_direction(rotations, mvtToDo, MOTOR_PINS);

    /*----------------------------------------------------------------------------------------------------
     ------------------------------------ Movement of the robot -------------------------------------------
    //----------------------------------------------------------------------------------------------------*/

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
    send_to_rpi(messageStrings[MOVEMENT_FINISHED]);
  } else {
    send_to_rpi(messageStrings[ERROR_MOVEMENT]);
  };
  return movement_validation;


/*
  for (int i = 0; i < Max_movement; i++) { //
    t = micros();
    for (int m = 0; m < 6; m++) {  // switch between the 6 motors
      if (mvt_to_do[m] > 0) {
        if (validate_move(motor_IDs[m], rotations[m], coders_motors)) {
          motor_stepper(motor_IDs[m]);
          coders_motors[m] = encoders(rotations[m], coders_motors[m]);    // --> logique pas bonne ici -- codeur du moteur 5 ne doit pas s'incrémenter
        } else if (! MovementDone(motor_IDs[m], rotations[m], coders_motors)) {  // Prevent the robot to "wait"
          Max_movement++;
        }
        mvt_to_do[m] = fabs(coders_motors[m] - coders_motors_target[m]);
      }
    }
    delayMicroseconds(Speed);
    time_taken = micros() - t;  // in miliseconds
    if (Speed > time_taken) { // Delay to have between two "step_motor" signal (minimum of 1500us)
      delayMicroseconds(Speed - time_taken);
    }
  }
*/


}

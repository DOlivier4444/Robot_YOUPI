//#include "HardwareSerial.h"
#include <stdio.h>
#include <time.h>


//------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------
#include "Coder_motor_target.h"
#include "Sens_rotation.h"
#include "Movement_to_do.h"
#include "Maximum_Value_Of_Int_Array.h"

#include "Validate_move.h"
#include "Step_motor.h"
#include "Coders.h"

#include "Forward_kinematic_solver.h"

void  Coder_motor_target(float thetas[], int coders_motors_target[]);
void  Sens_rotation(int rotations[], int movement_to_do[]);
void  Movement_to_do(int movement_to_do[], int coders_motors_target[], int coders_motors[]);
int   Maximum_Value_Of_Int_Array(int Array[], int SizeOfArray);

bool  Validate_Move(int motor_id, int rotation, int coders_motors[]);
void  Step_motor(int motor_id);
int   Coders(int rotations, int coders_motors);

void  Forward_kinematic_solver(float coders_motors[], float cartesian_position[]);
//------------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------


void GoToJointAngles(float thetas[], int Speed, int coders_motors[], float cartesian_position[]) {
 
  const int motor_IDs[6] = { 0, 1, 2, 3, 4, 5 };

  int simu_coders_motors[6] = { 0 }, coders_motors_target[6] = { 0 };
  int rotations[6] = { 0 };
  int movement_to_do[6] = { 0 }, Max_movement;

  unsigned long t, time_taken = 0;


  Coder_motor_target(thetas, coders_motors_target);
  Movement_to_do(movement_to_do, coders_motors_target, coders_motors);
  Max_movement = Maximum_Value_Of_Int_Array(movement_to_do, 6);

  Sens_rotation(rotations, movement_to_do);


//-------------------------------------------------------
  Serial.println("-----------------------------");
  Serial.println("-----------------------------");
  Serial.println("Coder motor target before");
  for (int i = 0; i<6; i++){
    Serial.println(coders_motors_target[i]);
  }
//----
  Serial.println("movement to do before simulation");
  for (int i = 0; i<6; i++){
    Serial.println(movement_to_do[i]);
  }
  Serial.print("Max_movement : ");
  Serial.println(Max_movement);
//-------------------------------------------------------



/*----------------------------------------------------------------------------------------------------
 ------------------------------------ Simulation of the movement ---------------------------------------
//----------------------------------------------------------------------------------------------------*/

  for (int i = 0; i < 6; i++ ){
    simu_coders_motors[i] = coders_motors[i];
    //movement_to_do[i] = abs(movement_to_do[i]);
  }

  for (int i = 0; i < Max_movement; i++) {
    for (int m = 0; m < 6; m++) {  // switch between the 6 motors
      if (abs(movement_to_do[m]) > 0) {
        if (Validate_Move(motor_IDs[m], rotations[m], simu_coders_motors)) {
          simu_coders_motors[m] = Coders(rotations[m], simu_coders_motors[m]);
        } /*else {
          Max_movement++;
        }*/
        movement_to_do[m] = coders_motors_target[m] - simu_coders_motors[m];
      }
    }
  }


 //-------------------------------------------------------
  Serial.println("simu_coders_motors after simulation");
  for (int i = 0; i<6; i++){
    Serial.println(simu_coders_motors[i]);
  }
//-------------------------------------------------------


  for (int i = 0; i < 6; i++ ){
    coders_motors_target[i] = simu_coders_motors[i];
    //movement_to_do[i] = abs(movement_to_do[i]);
  }
  Movement_to_do(movement_to_do, coders_motors_target, coders_motors);
  Max_movement = Maximum_Value_Of_Int_Array(movement_to_do, 6);


//-------------------------------------------------------
//-------------------------------------------------------
  Serial.println("Coder motor target after");
  for (int i = 0; i<6; i++){
    Serial.println(coders_motors_target[i]);
  }
//--
  Serial.println("movement to do after simulation");
  for (int i = 0; i<6; i++){
    Serial.println(movement_to_do[i]);
  }
//-------------------------------------------------------


/*----------------------------------------------------------------------------------------------------
 ------------------------------------ Movement of the robot -------------------------------------------
//----------------------------------------------------------------------------------------------------*/

  for (int i = 0; i < Max_movement; i++) {
    t = micros();
    for (int m = 0; m < 6; m++) {  // switch between the 6 motors
      if ( abs(movement_to_do[m]) > 0) {
        Step_motor(motor_IDs[m]);
        coders_motors[m] = Coders(rotations[m], coders_motors[m]);
        movement_to_do[m] = coders_motors_target[m] - coders_motors[m];
      }
    }
    //delayMicroseconds(Speed);
    time_taken = micros() - t;  // in miliseconds
    if (Speed > time_taken) { // Delay to have between two "step_motor" signal (minimum of 1500us)
      delayMicroseconds(Speed - time_taken);
    }
  }


//-------------------------------------------------------
  Serial.println("Coder motor after");
  for (int i = 0; i<6; i++){
    Serial.println(coders_motors[i]);
  }
//--
  Serial.println("movement to do after simulation");
  for (int i = 0; i<6; i++){
    Serial.println(movement_to_do[i]);
  }
//-------------------------------------------------------






/*----------------------------------------------------------------------------------------------------
 ----------------------- old program, before the movement was simulated ----------------------------
//----------------------------------------------------------------------------------------------------*/

/*
  for (int i = 0; i < Max_movement; i++) { //
    t = micros();
    for (int m = 0; m < 6; m++) {  // switch between the 6 motors
      if (movement_to_do[m] > 0) {
        if (Validate_Move(motor_IDs[m], rotations[m], coders_motors)) {
          Step_motor(motor_IDs[m]);
          coders_motors[m] = Coders(rotations[m], coders_motors[m]);    // --> logique pas bonne ici -- codeur du moteur 5 ne doit pas s'incrémenter
        } else if (! MovementDone(motor_IDs[m], rotations[m], coders_motors)) {  // Prevent the robot to "wait"
          Max_movement++;
        }
        movement_to_do[m] = fabs(coders_motors[m] - coders_motors_target[m]);
      }
    }
    delayMicroseconds(time_taken);   //Delay to have between two "step_motor" signal
    time_taken = micros() - t;  // in miliseconds
  }
  coders_motors[4] = coders_motors[4] - coders_motors[3];
*/


}

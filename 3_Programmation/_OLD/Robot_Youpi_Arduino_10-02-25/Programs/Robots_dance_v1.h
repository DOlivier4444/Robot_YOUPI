#include "Arduino.h"
#include <stdio.h>

#include "..\Includes\GotoJointAngles.h"


void GoToJointAngles(float thetas[], int Speed, int coders_motors[], float cartesian_position[]);


void Robots_dance_v1(int coders_motors[], float thetas[], float cartesian_position[]) {

  enum SPEED {  // In us, Delay betweed two moving signal sent to the motor
    SPEED_LOW = 5000,
    SPEED_MEDIUM = 3000,
    SPEED_HIGH = 1500,          // Delay needs to be 0.0015s = 1500 microseconds at least to protect the motors
    SPEED_MAX = SPEED_HIGH / 2  // Danger for the motors if less than 1500 us, using this speed is not recommanded
  };

  //--------------------
  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 180.0;
  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = -180.0;
  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 0.0;
  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  //--------------------
  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 0.0;
  thetas[4] = 0.0;
  thetas[5] = 180.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 0.0;
  thetas[4] = 0.0;
  thetas[5] = -100.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 0.0;
  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

//----------------------------
/*
  thetas[0] = 90.0;
  thetas[1] = 90.0;
  thetas[2] = 90.0;
  thetas[3] = 90.0;
  thetas[4] = 90.0;
  thetas[5] = 100.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 0.0;
  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);
*/

/*
//-------------------------------------------------------------------------
  thetas[3] = 90.0;
  thetas[4] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);
      delay(2000);


  thetas[3] = -90.0;
  thetas[4] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);
    delay(2000);


  thetas[3] = 0.0;
  thetas[4] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);
    delay(2000);
//-------------------------------------------------------------------------

//----------------------------------------------------------------------------------------------------------------
  // thetas[5] : 100.0% == opened == -6000pts // 0.0% == Closed == 0pts
*/


/*
  thetas[0] = -180.0;
  thetas[1] = 0.0;
  thetas[2] = 110.0;
  thetas[3] = 180.0;
  thetas[4] = 0.0;
  thetas[5] = 75.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);
  //Forward_kinematic_solver(coders_motors, cartesian_position);  // Take a lot of processing power !
  //Serial_sending(array); // Fonction � cr�er...

  delay(3000);

  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = -90.0;
  thetas[1] = 90.0;
  thetas[2] = 90.0;
  thetas[3] = 0.0;
  thetas[4] = 180.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  delay(2000);

  thetas[5] = 75.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);

  thetas[0] = 0.0;
  thetas[1] = 0.0;
  thetas[2] = 0.0;
  thetas[3] = 0.0;
  thetas[4] = 0.0;
  thetas[5] = 0.0;
  GoToJointAngles(thetas, SPEED_HIGH, coders_motors, cartesian_position);
*/
}

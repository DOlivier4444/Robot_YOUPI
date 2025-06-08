#include <stdint.h>


void Coder_motor_target(float thetas[], int coders_motors_target[]) {

  const float ratio = 0.028125;
  const float ratio_0 = 0.033; // calculs says 0.036 but 0.033 works best so... )

  // calculate all the coder targets (taking physical constrain into account for the motor 1, 2 and Gripper)
  for (int i = 0; i < 6; i++) {
    switch (i) {

      case 0: // Motor 1 is different
        coders_motors_target[i] = thetas[i] / ratio_0;  // angle� to step. 0.028125� = 1 motor step
        if (coders_motors_target[i] > 160 / ratio_0){  // Modify angle depending on physical constain
          coders_motors_target[i] = 160 / ratio_0;
        } else if (coders_motors_target[i] < -180 / ratio_0){
          coders_motors_target[i] = -180 / ratio_0;
        }
      break;


      case 1:  // Motor 2
        coders_motors_target[i] = thetas[i] / ratio;
        if ( coders_motors_target[i] > 135 / ratio){
          coders_motors_target[i] = 135 / ratio;
        } else if (coders_motors_target[i] < -75 / ratio){
          coders_motors_target[i] = -75 / ratio;
        }
      break;


      case 2:  // Motor 3 direction is reversed
        coders_motors_target[i] = thetas[i] / (-ratio);
      break;


      case 5:  // percentage to step. for the gripper : 100.0% == opened == -6000pts // 0.0% == Closed == 0pts
        coders_motors_target[i] = thetas[i] * -60;
        if (coders_motors_target[i] < 100.0 * -60){
          coders_motors_target[i] = 100.0 * -60;
        } else if (coders_motors_target[i] > 0.0 * -60){
          coders_motors_target[i] = 0.0 * -60;
        }
      break;


      default:
        coders_motors_target[i] = thetas[i] / ratio;
      break;

    }
  }


//--------------------------------------------------------------------------------

/*
considering the robot straight up :
theta1 : +180 / -160
theta2 : +135 / -75
theta3 : -90 / +135
theta4 : -90 / +90
theta5 : illimited
*/

//-------------------------------------------------------

//----------------------------------------------------------------------------

  /*
//for (int i = 5; i >= 0; i--) {
    switch (i) {
      
      case 0:
      // prevent rotation if the arm is too low ?
      break;


      case 1: // motor 2 / theta2 -- DONE
        if ( coders_motors_target[i] < -3200 - coders_motors_target[i + 1] ){
          coders_motors_target[i] = 3200 - coders_motors_target[i + 1]; 
          // 3200 - ( coders_motors_target[i + 1] / 2) if theta3 is adjusted the same way, to test later
        } else if (coders_motors_target[i] < -4800 - coders_motors_target[i + 1]) {
          coders_motors_target[i] = -4800 - coders_motors_target[i + 1];
        }
      break;


      case 2: // motor 3 / theta3 -- depending on arm n-1 to do...
      // depending on arm n+1
        if ( coders_motors_target[i] < -3200 - coders_motors_target[i + 1] ){
          coders_motors_target[i] = -3200 - coders_motors_target[i + 1]; 
        } else if (coders_motors_target[i] < -4800 - coders_motors_target[i + 1]) {
          coders_motors_target[i] = -4800 - coders_motors_target[i + 1];
        }
      // 
      break;


      case 3: // motor 4 -- depends on arm n-1
      /*
        if ( coders_motors_target[i] < -3200 - coders_motors_target[i + 1] ){
          coders_motors_target[i] = 3200 - coders_motors_target[i + 1]; 
          // 3200 - ( coders_motors_target[i + 1] / 2) if theta3 is adjusted the same way, to test later
        } else if (coders_motors_target[i] < -4800 - coders_motors_target[i + 1]) {
          coders_motors_target[i] = -4800 - coders_motors_target[i + 1];
        }
      
      break;
      
      
      default:
      
      break;
    }
  }
  */
}

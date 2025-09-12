
void coder_motor_target(float motorAngles[], int codersMotorsTarget[]) {

  const float RATIO_MOTORS = 0.028125;
  const float RATIO_MOTOR_0 = 0.033; // calculs says 0.036 but 0.033 works best so...


  // calculate all the coder targets (taking physical constrain into account for the motor 1, 2 and Gripper)
  for (int i = 0; i < 6; i++) {
    switch (i) {

      case 0: // Motor 1 is different
        codersMotorsTarget[i] = motorAngles[i] / RATIO_MOTOR_0;  // angle� to step. 0.028125� = 1 motor step
        if (codersMotorsTarget[i] > 160 / RATIO_MOTOR_0){  // Modify angle depending on physical constain
          codersMotorsTarget[i] = 160 / RATIO_MOTOR_0;
        } else if (codersMotorsTarget[i] < -180 / RATIO_MOTOR_0){
          codersMotorsTarget[i] = -180 / RATIO_MOTOR_0;
        }
      break;


      case 1:  // Motor 2
        codersMotorsTarget[i] = motorAngles[i] / RATIO_MOTORS;
        if ( codersMotorsTarget[i] > 135 / RATIO_MOTORS){
          codersMotorsTarget[i] = 135 / RATIO_MOTORS;
        } else if (codersMotorsTarget[i] < -75 / RATIO_MOTORS){
          codersMotorsTarget[i] = -75 / RATIO_MOTORS;
        }
      break;


      case 2:  // Motor 3 direction is reversed
        codersMotorsTarget[i] = motorAngles[i] / (-RATIO_MOTORS);
      break;


      case 5:  // percentage to step. for the gripper : 100.0% == opened == -6000pts // 0.0% == Closed == 0pts
        codersMotorsTarget[i] = motorAngles[i] * -60;
        if (codersMotorsTarget[i] < 100.0 * -60){
          codersMotorsTarget[i] = 100.0 * -60;
        } else if (codersMotorsTarget[i] > 0.0 * -60){
          codersMotorsTarget[i] = 0.0 * -60;
        }
      break;


      default:
        codersMotorsTarget[i] = motorAngles[i] / RATIO_MOTORS;
      break;
    }
  }


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

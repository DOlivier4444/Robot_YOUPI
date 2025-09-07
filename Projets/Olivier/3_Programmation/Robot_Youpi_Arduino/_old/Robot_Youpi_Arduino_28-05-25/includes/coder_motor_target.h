
void coder_motor_target(float motorAngles[], int codersMotorsTarget[]) {

  const float RATIO_MOTORS = 0.028125;
  const float RATIO_MOTOR_0 = 0.033; // calculs says 0.036 but 0.033 works best so...

  const int MOTOR_0 = 0;  // motor0 - base
  const int MOTOR_1 = 1;  // motor1 - shoulder
  const int MOTOR_2 = 2;  // motor2 - elbow
  const int MOTOR_3 = 3;  // motor3 - wrist
  const int MOTOR_4 = 4;  // motor4 - rotation_hand
  const int MOTOR_5 = 5;  // motor5 - gripper

  for (int motor_no = 0; motor_no < 6; motor_no++) {

    switch (motor_no) {
      case MOTOR_0: // different ratio
        codersMotorsTarget[motor_no] = motorAngles[motor_no] / RATIO_MOTOR_0;  // angle� to step. 0.028125� = 1 motor step
        break;

      case MOTOR_2:  // direction is reversed
        codersMotorsTarget[motor_no] = motorAngles[motor_no] / (-RATIO_MOTORS);
        break;

      case MOTOR_5:  // percentage to step. for the gripper : 100.0% is opened and == -6000pts // 0.0% is closed and == 0pts
        codersMotorsTarget[motor_no] = motorAngles[motor_no] * -60;
        break;

      default: // Motors 1-3-4
        codersMotorsTarget[motor_no] = motorAngles[motor_no] / RATIO_MOTORS;
        break;
    }
  }
}

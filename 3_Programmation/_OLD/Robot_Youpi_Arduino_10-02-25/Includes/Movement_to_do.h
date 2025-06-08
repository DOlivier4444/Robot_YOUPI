
void Movement_to_do(int movement_to_do[], int coders_motors_target[], int coders_motors[]) {

  for (int m = 0; m < 6; m++) {  // movements lengh in coder points
    movement_to_do[m] = coders_motors_target[m] - coders_motors[m];
  }
  // prevent the movement of the motor5 when motor4 is moving
  //movement_to_do[4] = ( - movement_to_do[4]) - movement_to_do[3];
}
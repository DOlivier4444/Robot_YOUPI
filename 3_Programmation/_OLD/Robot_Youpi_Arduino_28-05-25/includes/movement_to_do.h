
void movement_to_do(int mvtToDo[], int codersMotorsTargets[], int codersMotors[]) {
  for (int m = 0; m < 6; m++) {  // movements lengh in coder points
    mvtToDo[m] = codersMotorsTargets[m] - codersMotors[m];
  }
  // prevent the movement of the motor5 when motor4 is moving
  //movement_to_do[4] = ( - movement_to_do[4]) - movement_to_do[3];
}

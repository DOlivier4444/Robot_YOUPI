#include <stdio.h>
#include <time.h>


void movement_to_do(int mvtToDo[], int codersMotorsTargets[], int codersMotors[]) {
  for (int m = 0; m < 6; m++) {  // movements lengh in coder points
    mvtToDo[m] = codersMotorsTargets[m] - codersMotors[m];
  }
  // prevent the movement of the motor5 when motor4 is moving
  //movement_to_do[4] = ( - movement_to_do[4]) - movement_to_do[3];
}

int max_array_int(int array[], int sizeOfArray) {
  int maxValue = abs(array[0]);

  for (int i = 1; i < sizeOfArray; i++) {  // store the maximum value of movements[] in max_value
    if ( abs(array[i]) > maxValue ) {
      maxValue = abs(array[i]);
    }
  }
  return maxValue;
}


int encoders(int rotation, int coderMotor) {  // increase the encoder value depending on the rotation direction

  const int FORWARD = 1;
  const int BACKWARDS = 0;

  switch (rotation) {
    case FORWARD:
      coderMotor++;
      break;
    case BACKWARDS:
      coderMotor--;
      break;
  }
  return coderMotor;
}

void encoder_motor_target(float motorAngles[], int codersMotorsTarget[]) {  // process the targer of the motor in encoder value
  const float RATIO_MOTORS = 0.028125;
  const float RATIO_MOTOR_0 = 0.0325; // calculs says 0.036 but 0.0325 works best so...
  
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
        codersMotorsTarget[motor_no] = motorAngles[motor_no]; //* -60; // commented because the process is done on the RPI
        break;
      
      default: // Motors 1-3-4
        codersMotorsTarget[motor_no] = motorAngles[motor_no] / RATIO_MOTORS;
        break;
    }
  }
}

int goto_joint_angles(int speed, float motorAngles[], int codersMotors[]) {
  const int MOTOR_IDS[6] = { 0, 1, 2, 3, 4, 5 };

  int codersMotorsTarget[6] = { 0 };
  int rotations[6] = { 0 };
  int mvtToDo[6] = { 0 };
  int maxMovement;

  unsigned long t, timeTaken = 0;


  encoder_motor_target(motorAngles, codersMotorsTarget);
  movement_to_do(mvtToDo, codersMotorsTarget, codersMotors);
  maxMovement = max_array_int(mvtToDo, 6);
  
  rotation_direction(rotations, mvtToDo); 

  // ---------- Movement of the robot ----------
  motor_stepper_prep();

  for (int i = 0; i < maxMovement; i++) {
    t = micros();
    for (int m = 0; m < 6; m++) {  // switch between the 6 motors
      if ( abs(mvtToDo[m]) > 0) {
        motor_stepper(MOTOR_IDS[m]);
        codersMotors[m] = encoders(rotations[m], codersMotors[m]);
        mvtToDo[m] = codersMotorsTarget[m] - codersMotors[m];
      }
    }
    timeTaken = micros() - t;  // in miliseconds
    delayMicroseconds(speed - timeTaken);
  }
}

void StrMvt_To_FloatMvt(String StrMvtdata, float FloatMvtDatas[]) {
  const char separator    = '_';
  const char endString = '\0';
  
  char    incomingChar;
  char    dataChar[64];          // data of one movement (ex : 1500 )
  int     nbrOfDataReceived = 0;

  int j = 0;
  int i = 0;

  //exemple of StrMvtdata : 1500_90_45_30_25_90_100\0
  do {
    incomingChar = StrMvtdata[i]; // one character (ex : 1 )  
    if (incomingChar == separator || incomingChar == endString ){
      dataChar[j] = endString;  // Mark the end of the string
      FloatMvtDatas[nbrOfDataReceived] = atof(dataChar);  
      nbrOfDataReceived ++;
      j = 0;  
    } else {
      if (j < sizeof(dataChar) - 1) { // avoid memory overflow
        dataChar[j] = incomingChar;
        j++;
      }
    }
    i += 1;
  } while (incomingChar != endString);
}

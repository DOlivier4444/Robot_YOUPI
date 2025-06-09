int validate_move(float motorAngles[]) { // 1 == valid // 0 == invalid
  const int FORWARD   = 1;
  const int BACKWARDS = 0;

  const int MOTOR_0 = 0;  // motor0 - base
  const int MOTOR_1 = 1;  // motor1 - shoulder
  const int MOTOR_2 = 2;  // motor2 - elbow
  const int MOTOR_3 = 3;  // motor3 - wrist
  const int MOTOR_4 = 4;  // motor4 - rotation_hand
  const int MOTOR_5 = 5;  // motor5 - gripper

/*
  Motor coders limits in angles
  considering the robot straight up :
            Backward  /    Forward
  theta1 :   -180     /     +160
  theta2 :   -75      /     +135
  theta3 :   +90      /     -135
  theta4 :   -90      /     +90
  theta5 :        illimited
  theta6 :   -6000  / 0
*/
  const int ANGLES_LIMITS[6][2] = { // considering the robot straight up
    //BW     FW
    {180,  160 },   // MOTOR_0
    {75,   135 },   // MOTOR_1
    {90,   135 },   // MOTOR_2
    {90,   90  },   // MOTOR_3
    {0,    0   },   // MOTOR_4 (illimited)
    {6000, 0   }    // MOTOR_5 /*closed  opened*/
  };

  for (int motor_no = 0; motor_no < 6; motor_no++) {
    float theta1;
    float theta2;
    float angles;

    //motorAngles[motor_no] = abs(motorAngles[motor_no]);

    switch (motor_no) {

      case MOTOR_0:  // base
        if( motorAngles[MOTOR_0] > ANGLES_LIMITS[MOTOR_0][FORWARD]
            ||
            motorAngles[MOTOR_0] < -ANGLES_LIMITS[MOTOR_0][BACKWARDS])
          {
            return 0xA + MOTOR_0;
          };
        break;


      case MOTOR_1:  // shoulder
        if( motorAngles[MOTOR_1] > ANGLES_LIMITS[MOTOR_1][FORWARD]
            ||
            motorAngles[MOTOR_1] < -ANGLES_LIMITS[MOTOR_1][BACKWARDS])
          {
            return 0xA + MOTOR_1;
          };
        break;

      case MOTOR_2: // elbow
        theta1 = (180 - 90 - motorAngles[MOTOR_1]);
        theta2 = (motorAngles[MOTOR_2] - 90);
        angles = 180 - theta2 - theta1;
        
        if( angles < 180 - ANGLES_LIMITS[MOTOR_2][FORWARD]
            ||
            360 - angles < ANGLES_LIMITS[MOTOR_2][BACKWARDS]) 
          {
            return 0xA + MOTOR_2;
          };
        break;


      case MOTOR_3: // wrist pitch
        theta1 = (180 - 90 - motorAngles[MOTOR_2]);
        theta2 = (motorAngles[MOTOR_3] - 90);
        angles = 180 - theta2 - theta1;
        
        if( angles < 180 - ANGLES_LIMITS[MOTOR_3][FORWARD]
            ||
            360 - angles < ANGLES_LIMITS[MOTOR_3][BACKWARDS])
          {
            return 0xA + MOTOR_3;
          };
        break;


      case MOTOR_4:
        // illimited
        break;


      case MOTOR_5:
        if( motorAngles[MOTOR_5] > ANGLES_LIMITS[MOTOR_5][FORWARD]
            ||
            motorAngles[MOTOR_5] < -ANGLES_LIMITS[MOTOR_5][BACKWARDS]) 
          {
            return 0xA + MOTOR_5;
          };
        break;


      default:
        return 0xFF;
    }
  }

  return 0x00;
}

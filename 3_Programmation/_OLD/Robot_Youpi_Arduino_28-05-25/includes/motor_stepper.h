
void motor_stepper(int motorID, const int motorPins[]) {
  const int Delay = 0;  // Delay between the preparation of the rotation, and the rotation command
  int motorBin[3] = {0};

  digitalWrite(motorPins[6], LOW); // turn off the 2 validation pin
  digitalWrite(motorPins[7], LOW);


  // Prevent the rotation of motor4 when motor3 moves
  //if (motor_id == 3) {
  //  for (int i = 0; i < 3; i++) {
  //    Motor_bin[i] = ((motor_id + 1) & (1 << i)) >> i;
  //    digitalWrite(MotorPins[i], Motor_bin[i]);
  //  }
  //  // Validation pin off : byte sent
  //  digitalWrite(MotorPins[6], HIGH);
  //  delayMicroseconds(Delay);
  //  digitalWrite(MotorPins[6], LOW);
  //}

  for (int i = 0; i < 3; i++) {
    motorBin[i] = (motorID & (1 << i)) >> i;
    digitalWrite(motorPins[i], motorBin[i]);
  }

  // Validation pin off : byte sent
  digitalWrite(motorPins[6], HIGH);
  delayMicroseconds(Delay);
  digitalWrite(motorPins[6], LOW);


  /*
  Note to myself :
  //-------------------------------------------------------
    for (int i = 0; i < 3; i++) {
      Motor_bin[i] = (motor_id & (1 << i)) >> i;
      digitalWrite(MotorPins[i], Motor_bin[i]);
    }
  
  Friendly version :

  bit0 = (motor_id & (1 << 0)) >> 0; // test this bit : 00000001
  bit1 = (motor_id & (1 << 1)) >> 1; // test this bit : 00000010
  bit2 = (motor_id & (1 << 2)) >> 2; // test this bit : 00000100
  Motor_bin[0] = bit0
  Motor_bin[1] = bit1
  Motor_bin[2] = bit2

  It's as shrimple as that
  //-------------------------------------------------------
  */
}



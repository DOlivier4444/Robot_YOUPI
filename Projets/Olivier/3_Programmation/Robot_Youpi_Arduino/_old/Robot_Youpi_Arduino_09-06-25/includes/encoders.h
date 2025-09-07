
int encoders(int rotation, int coderMotor) {

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

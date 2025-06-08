int Coders(int rotations, int coders_motors) {

  const int FORWARD = 1;
  const int BACKWARDS = 0;

  switch (rotations) {
    case FORWARD:
      coders_motors++;
      break;
    case BACKWARDS:
      coders_motors--;
      break;
  }
  return coders_motors;
}


void rotation_direction(int rotations[], int mvtToDo[], const int motorPins[]) {
  const int FORWARD = 1;
  const int BACKWARDS = 0;
  const int delay = 0; // In microseconds
  
  digitalWrite(motorPins[6], LOW); // turn off the 2 validation pin
  digitalWrite(motorPins[7], LOW);

  for (int i = 0; i < 6; i++) {
    rotations[i] = (mvtToDo[i] >= 0) ? FORWARD : BACKWARDS;
    digitalWrite(motorPins[i], rotations[i]);
  }

  // Validation pin off : byte sent
  digitalWrite(motorPins[7], HIGH);
  delayMicroseconds(delay);
  digitalWrite(motorPins[7], LOW);
}

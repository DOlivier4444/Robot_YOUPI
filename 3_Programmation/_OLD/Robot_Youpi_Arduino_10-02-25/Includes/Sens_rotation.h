
#include <stdint.h>

void Sens_rotation(int rotations[], int movement_to_do[]) {

  const int BACKWARDS = 0;
  const int FORWARD = 1;

  const int Delay = 2;       // In microsecond
  uint8_t bin_rotation = 0;

  for (int i = 0; i < 6; i++) {
    rotations[i] = (movement_to_do[i] > 0) ? FORWARD : BACKWARDS;
    //rotations[i] = (coders_motors[i] <= coders_motors_target[i]) ? FORWARD : BACKWARDS;
    if (rotations[i]) {
      bin_rotation |= (1 << i);
    }
  }

  // Sending the rotation direction byte
  PORTD = ((bin_rotation << 2) & B11111100);  // set the directions
  PORTB = B00000010;
  delayMicroseconds(Delay);
  PORTB = B00000000;  // send the directions

  /*
  PORTD = B10000000 | (bin_rotation & B00111111);  // set the direction of rotations
  delayMicroseconds(Delay);
  PORTD = PORTD & B00111111;  // send the direction of rotations
  delayMicroseconds(Delay);
*/ 
}
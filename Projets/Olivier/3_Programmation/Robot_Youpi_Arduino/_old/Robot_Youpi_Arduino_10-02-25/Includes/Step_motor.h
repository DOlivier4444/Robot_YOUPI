
void Step_motor(int motor_id) {
  const int Delay = 2;  // Delay between the preparation of the rotation, and the rotation command

  //https://roboticsbackend.com/arduino-fast-digitalwrite/

  // Prevent the rotation of motor4 when motor3 moves
  if (motor_id == 3) {
    delayMicroseconds(Delay);
    PORTD = ((motor_id + 1 << 2) & B00011100);
    PORTB = B00000001;
    delayMicroseconds(Delay);
    PORTB = B00000000;
    delayMicroseconds(5);
  }

  // Byte sending : rotation of the chosen motor
  PORTD = ((motor_id << 2) & B00011100);  // Creation of the Byte
  PORTB = B00000001;
  delayMicroseconds(Delay);
  PORTB = B00000000;  // Byte sending

  /*
  PORTD = B01000000 | (motor_id & B01000111);  // Send the byte to prepare for the rotation of the chosen motor
  delayMicroseconds(Delay);
  PORTD = PORTD & B00000111;    // Send the byte to order the rotation
*/
}

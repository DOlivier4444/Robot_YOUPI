void Initialisation() {
  // Byte used to set up D2 to D9
  uint8_t Byte[8] = { 2, 3, 4, 5, 6, 7, 8, 9 };

  for (int i = 0; i < 8; i++) {
    pinMode(Byte[i], OUTPUT);  //Set the D0-->D7 pins to OUTPUT
  }
  DDRB = B11111111;
  DDRD = B11111111;

  

  // RESET Signal - initialisation of the motors : 16#47 (2#01000111) --> 16#00 (2#00000000) - see Documentation_general.pdf
  // Using direct port manipulation, see arduino documentation

  PORTD = B00011100;
  PORTB = B00000001;
  delay(50);
  PORTD = B00000000;
  PORTB = B00000000;
  delay(50);

  /*
  PORTD = B01000111;
  delay(125);
  PORTD = B00000000;
  delay(125);
*/
}

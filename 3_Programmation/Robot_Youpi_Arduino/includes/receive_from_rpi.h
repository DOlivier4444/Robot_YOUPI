
String receive_from_rpi(bool direct) {
  const char startMarker  = '<';
  const char endMarker    = '>';

  char    incomingChar;  // one character (ex : L )
  String  receivedData = "";  // exemple of data : <L-1500-1-2-3-4-5-6-7-8>


  if (direct){
    incomingChar = Serial.read();
    receivedData += incomingChar;

  } else {

    do {
      if (Serial.available() > 0) {
        incomingChar = Serial.read();
      }
    } while (incomingChar != startMarker);

    while (true) {
      if (Serial.available()) {
        incomingChar = Serial.read();

        if (incomingChar == endMarker) {
          receivedData += '\0';
          break;
        } else {
          receivedData += incomingChar;
        }
      } // timeout ?
    }

  }

  return receivedData;
}


void send_to_rpi(String data, bool direct) {
  String dataToSend = "";

  if (direct) {
    dataToSend += data;

  } else {
    const char startMarker  = '<';
    const char endMarker    = '>';

    dataToSend += startMarker;
    dataToSend += data;
    dataToSend += endMarker;
  }

  dataToSend += '\0';
  Serial.print( String(dataToSend) );

}

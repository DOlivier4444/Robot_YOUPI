
void send_to_rpi(String data) {
  const char startMarker  = '<';
  const char endMarker    = '>';

  String dataToSend = "";

  dataToSend += startMarker;
  dataToSend += data;
  dataToSend += endMarker;
  dataToSend += '\0';

  Serial.print( String(dataToSend) );

}

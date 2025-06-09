
void StrMvt_To_FloatMvt(String StrMvtdata, float FloatMvtDatas[]) {

  const char separator    = '_';
  const char endString = '\0';
  
  char    incomingChar;
  char    dataChar[64];          // data of one movement (ex : 1500 )
  int     nbrOfDataReceived = 0;

  int j = 0;
  int i = 0;

  //exemple of StrMvtdata : 1500_90_45_30_25_90_100\0
  do {
    incomingChar = StrMvtdata[i]; // one character (ex : 1 )  
    if (incomingChar == separator || incomingChar == endString ){
      dataChar[j] = endString;  // Mark the end of the string
      FloatMvtDatas[nbrOfDataReceived] = atof(dataChar);  
      nbrOfDataReceived ++;
      j = 0;  
    } else {
      if (j < sizeof(dataChar) - 1) { // avoid memory overflow
        dataChar[j] = incomingChar;
        j++;
      }
    }
    i += 1;
  } while (incomingChar != endString);
}

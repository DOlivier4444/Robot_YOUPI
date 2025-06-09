
#include "goto_xyz.h"


int robots_program(int coders_motors[], float motorAngles[]) {

  String receivedData = receive_from_rpi();  //exemple of data : <L-1500-1-2-3-4-5-6-7-8>
  const char separator    = '_';
  const char endString = '\0';

  char    dataChar[64];          // data of one movement (ex : 1500 )
  float   dataFloat[64];          // all the data of one movement (ex : {1500; 1; 2; ... })
  int     nbrOfDataReceived = 0;

  char incomingChar;
  int j = 0;
  int i = 2;
  do {
    incomingChar = receivedData[i]; // one character (ex : L )
    
    if (incomingChar == separator || incomingChar == endString ){
      dataChar[j] = endString;  // Mark the end of the string
      dataFloat[nbrOfDataReceived] = atof(dataChar);

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


  char movementType = receivedData[0];
  const char LINEAR  = 'L';
  const char JOINT   = 'J';

  switch (movementType) {
    case LINEAR : {
      int speed               = int(dataFloat[0]);
      float x                 = dataFloat[1];
      float y                 = dataFloat[2];
      float z                 = dataFloat[3];
      float pitch             = dataFloat[4];
      float roll              = dataFloat[5];
      float gripperPercentage = dataFloat[6];
      float penOffsetV        = dataFloat[7];
      float penOffsetH        = dataFloat[8];

      return goto_xyz(speed, x, y, z, pitch, roll, gripperPercentage, penOffsetV, penOffsetH, motorAngles, coders_motors);
    }

    case JOINT : {
      for (int i = 0; i < 6; i++) {
        motorAngles[i] = dataFloat[i+1];
      }

      int speed = int(dataFloat[0]);

      return goto_joint_angles(speed, motorAngles, coders_motors);
    }
  }

/*
  x                 = -0.20;
  y                 = 0.25;
  z                 = 0.40;
  pitch             = 45 * PI/180;
  roll              = 90;
  gripperPercentage = 100,
  penOffsetV        = 0;
  penOffsetH        = 0;

  SPEED_HIGH
  goto_xyz(x, y, z, pitch, roll, gripperPercentage, penOffsetV, penOffsetH, SPEED_HIGH, thetas, coders_motors);


  penOffsetV        = 0;
  penOffsetH        = 0;
  x                 = 0;
  y                 = 0.0;
  z                 = 0.754;
  pitch            = 0 * PI/180;
  roll             = -180;
  gripperPercentage = 0, 
  goto_xyz(penOffsetV, penOffsetH, x, y, z, pitch, roll, gripperPercentage,  SPEED_HIGH, thetas, coders_motors);
*/

}

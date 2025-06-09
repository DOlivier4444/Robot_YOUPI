#include "goto_joint_angles.h"
#include "StrMvt_To_FloatMvt.h"

int robots_program(int coders_motors[], float motorAngles[]) {

  String receivedData = "";
  float   MvtDatas[64];

  bool stop_program = false;
  do {
    send_to_rpi(toRaspberryMessages[TO_RPI_READY_TO_RECEIVE], !DIRECT);
    receivedData = receive_from_rpi(!DIRECT);

    if (receivedData == fromRaspberryMessages[FROM_RPI_ABORT_PROGRAM] ||
        receivedData == fromRaspberryMessages[FROM_RPI_PROGRAM_FINISHED]){
      stop_program = true;
    } else {
      
      StrMvt_To_FloatMvt(receivedData, MvtDatas);  //exemple of Mvtdata : 1500_90_45_30_25_90_100\0

      int speed = int(MvtDatas[0]);
      for (int i = 0; i < 6; i++) {
        motorAngles[i] = MvtDatas[i+1];
      }
      goto_joint_angles(speed, motorAngles, coders_motors);

      send_to_rpi(toRaspberryMessages[TO_RPI_MOVEMENT_FINISHED], !DIRECT);

    }

  } while (stop_program == false);

}

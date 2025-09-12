#include "Movements.h"

int robots_program(int coders_motors[]) {

  String payload = "";
  uint8_t cmd;
  float MvtDatas[16];
  float motorAngles[6];

  bool stop_program = false;
  do {
    send_to_rpi(TO_RPI_READY_TO_RECEIVE);
    
    if( receive_from_rpi(cmd, payload) ){
      switch (cmd) {
        case FROM_RPI_START_MOVEMENT: {

          StrMvt_To_FloatMvt(payload, MvtDatas);  //exemple of Mvtdata : 1500_90_45_30_25_90_100\0
          
          int speed = MvtDatas[0];
          lcd.setCursor(0, 1);
          lcd.print(speed);
          for (int i = 0; i < 6; i++) {
            motorAngles[i] = MvtDatas[i+1];
            lcd.print("_");
            lcd.print(motorAngles[i]);
          }
          goto_joint_angles(speed, motorAngles, coders_motors);

          send_to_rpi(TO_RPI_MOVEMENT_FINISHED);
          break;
        }

        case FROM_RPI_PROGRAM_FINISHED:
          stop_program = true;
          break;
      }
    }
  } while (stop_program == false);
}

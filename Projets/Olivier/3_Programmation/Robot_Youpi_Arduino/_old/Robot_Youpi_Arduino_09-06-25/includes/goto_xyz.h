#include "inverse_kinematics.h"
#include "goto_joint_angles.h"

int goto_xyz(int speed, double x, double y, double z, double pitch, double roll, float gripperPercentage, double penOffsetV, double penOffsetH, float motorAngles[], int codersMotors[]){

  inverse_kinematics(penOffsetV, penOffsetH, x, y, z, pitch, roll, motorAngles);

  motorAngles[5] = gripperPercentage;
  return goto_joint_angles(speed, motorAngles, codersMotors);
}

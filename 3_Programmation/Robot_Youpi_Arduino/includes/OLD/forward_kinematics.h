#include <math.h>


//  --> Remake it all over again ?


// MotorAngles[θ1, θ2, θ3, θ4, θ5, 100.0%] (the actuator is 0 - 100%)
void forward_kinematics(int codersMotors[], float cartesianPositions[]) {

  // Constant of the DH Parameters, defining the robot
  const float A1 = 0.0;
  const float A2 = L2 / 100;
  const float A3 = L3 / 100;
  const float A4 = 0.0;
  const float A5 = 0.0;

  const float D1 = L1 / 100;
  const float D2 = 0.0;
  const float D3 = 0.0;
  const float D4 = 0.0;
  const float D5 = L4 / 100;

  float R1;

  float motorAngles[6] = {
    // conversion from step (0.028125°/step) to angle° - (from step to percentage for the motor 6)
    codersMotors[0] * 0.036,
    codersMotors[1] * 0.028125,
    codersMotors[2] * 0.028125,  //Note : The sens in reversed for this one
    codersMotors[3] * 0.028125,
    codersMotors[4] * 0.028125,
    codersMotors[5] / -60  // Note : 100% = -6000 || 0% = 0 -- (100 *coders_motors / -6000)
  };

  R1 = sin(motorAngles[1]) * A2 + sin(motorAngles[2]) * A3 + sin(motorAngles[3]) * D5;

  // x, y, z, ry, rz, ActuatorPercentage
  cartesianPositions[0] = cos(motorAngles[1]) * R1;                                                   // = x
  cartesianPositions[1] = sin(motorAngles[1]) * R1;                                                   // = y
  cartesianPositions[2] = D1 + cos(motorAngles[1]) * A2 + cos(motorAngles[2]) * A3 + cos(motorAngles[3]) * D5;  // = z
  cartesianPositions[3] = motorAngles[3];                                                             // = ry
  cartesianPositions[4] = motorAngles[0] + motorAngles[3] + motorAngles[4];                                     // = rz

  if (motorAngles[5] > 100.0) {  // = ActuatorPercentage (Avoid going more than 100% or 0%)
    cartesianPositions[5] = 100.0;
  } else if (motorAngles[5] < 0.0) {
    cartesianPositions[5] = 0.0;
  } else cartesianPositions[5] = motorAngles[5];
}

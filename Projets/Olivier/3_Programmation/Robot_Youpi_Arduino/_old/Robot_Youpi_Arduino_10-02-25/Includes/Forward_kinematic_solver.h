#include <math.h>


// thetas[θ1, θ2, θ3, θ4, θ5, 100.0%] (the actuator is 0 - 100%)
void Forward_kinematic_solver(int coders_motors[], float cartesian_position[]) {

  // Constant of the DH Parameters, defining the robot
  const float a1 = 0.0;
  const float a2 = 16.2;
  const float a3 = 16.2;
  const float a4 = 0.0;
  const float a5 = 0.0;

  const float d1 = 28.0;
  const float d2 = 0.0;
  const float d3 = 0.0;
  const float d4 = 0.0;
  const float d5 = 15.0;

  float r1;

  float thetas[6] = {
    // conversion from step (0.028125°/step) to angle° - (from step to percentage for the motor 6)
    coders_motors[0] * 0.036,
    coders_motors[1] * 0.028125,
    coders_motors[2] * 0.028125,  //Note : The sens in reversed for this one
    coders_motors[3] * 0.028125,
    coders_motors[4] * 0.028125,
    coders_motors[5] / -60  // Note : 100% = -6000 || 0% = 0 -- (100 *coders_motors / -6000)
  };

  r1 = sin(thetas[1]) * a2 + sin(thetas[2]) * a3 + sin(thetas[3]) * d5;

  // x, y, z, ry, rz, ActuatorPercentage
  cartesian_position[0] = cos(thetas[1]) * r1;                                                   // = x
  cartesian_position[1] = sin(thetas[1]) * r1;                                                   // = y
  cartesian_position[2] = d1 + cos(thetas[1]) * a2 + cos(thetas[2]) * a3 + cos(thetas[3]) * d5;  // = z
  cartesian_position[3] = thetas[3];                                                             // = ry
  cartesian_position[4] = thetas[0] + thetas[3] + thetas[4];                                     // = rz

  if (thetas[5] > 100.0) {  // = ActuatorPercentage (Avoid going more than 100% or 0%)
    cartesian_position[5] = 100.0;
  } else if (thetas[5] < 0.0) {
    cartesian_position[5] = 0.0;
  } else cartesian_position[5] = thetas[5];
}

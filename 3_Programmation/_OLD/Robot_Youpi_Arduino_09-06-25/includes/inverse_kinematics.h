#include <math.h>

#define PI 3.14159265358979323846
#define SIGN(x) ((x > 0) - (x < 0))

void inverse_kinematics(float penOffsetV, float penOffsetH, float x, float y, float z, float pitch, float roll, float motorAngles[]){

  // Defining the Dh Parameters of the Robot
    // Need to #define L1-4
  const float D1 = L1             ; const float A1 = 0.0            ; const float ALPHA1 = 90.0 ;
  const float D2 = 0.0            ; const float A2 = L2             ; const float ALPHA2 = 0.0  ;
  const float D3 = 0.0            ; const float A3 = L3             ; const float ALPHA3 = 0.0  ;
  const float D4 = 0.0            ; const float A4 = 0.0            ; const float ALPHA4 = 90.0 ;
  const float D5 = L4             ; const float A5 = 0.0            ; const float ALPHA5 = 0.0  ;
  const float D6 = penOffsetV     ; const float A6 = penOffsetH     ; const float ALPHA6 = 0.0  ;

  double PD[3] = {x, y, z};

  double RotY[3][3] = {
    {cos(pitch), 0, sin(pitch)},
    {0, 1, 0},
    {-sin(pitch), 0, cos(pitch)}
  };

  double Pn[3] = {
    RotY[0][0] * 0 + RotY[0][2] * D6,
    0,
    RotY[2][0] * 0 + RotY[2][2] * D6
  };
  
  double t = atan2(y, x);

  Pn[0] = PD[0] - Pn[0] * cos(t);
  Pn[1] = PD[1] - Pn[1] * sin(t);
  Pn[2] = PD[2] - Pn[2];
  
  x = Pn[0];
  y = Pn[1];
  z = Pn[2];

  // Inverse Kinematics
  double t1 = (fabs(y) < 1e-5 && fabs(x) < 1e-5) ? 0 : atan2(y, x);

  // This will make the robot to follow actual rotation configuration
  // If removed, then positive means robot end-effector always pointing outside
  // Negative means robot end-effector always pointing inside
  if (fabs(x) > 1e-5){
    //pitch = SIGN(X) * pitch;
  }

  double Rn = sqrt(x * x + y * y) - L4 * sin(pitch);
  double Zn = z - L4 * cos(pitch) - L1;

  double C3 = (Rn * Rn + Zn * Zn - L2 * L2 - L3 * L3) / (2 * L2 * L3);
  C3 = fmin(1, fmax(C3, -1));

  double t3 = -acos(C3);
  if (pitch < 0) t3 = -t3;

  double t2 = atan2(Zn, Rn) - atan2(L3 * sin(t3), L2 + L3 * cos(t3));
  double t4 = -pitch - t2 - t3 + PI;
  double t5 = roll;


  /* Motor Compatable Angles */
  double t1_Motor = t1;
  double t2_Motor = t2 - PI/2;
  double t3_Motor = t2_Motor + t3;
  double t4_Motor = t3_Motor + t4 - PI/2;
  double t5_Motor = t5 - t4_Motor;
  
  //t1_Motor = -t1_Motor; 
  t2_Motor = -t2_Motor;
  t3_Motor = -t3_Motor;
  t4_Motor = -t4_Motor;
  t5_Motor = -t5_Motor;

  /* Final Angles */
  motorAngles[0] = t1_Motor * 180 / PI;
  motorAngles[1] = t2_Motor * 180 / PI;
  motorAngles[2] = t3_Motor * 180 / PI;
  motorAngles[3] = t4_Motor * 180 / PI;
  motorAngles[4] = t5_Motor * 180 / PI;
}
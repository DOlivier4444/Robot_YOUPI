from math import *
from enum import Enum


## Robot's parameters
# Constants
L1 = 0.28
L2 = 0.162
L3 = 0.162
L4 = 0.15

class Youpi:
  class Motors(Enum) :
    M0_BASE     = 0  # motor0 - base
    M1_SHOULDER = 1  # motor1 - shoulder
    M2_ELBOW    = 2  # motor2 - elbow
    M3_PITCH    = 3  # motor3 - wrist pitch
    M4_ROLL     = 4  # motor4 - wrist roll
    M5_GRIPPER  = 5  # motor5 - gripper

  class Robot_arms(Enum) :
    # Lengths of the Robot's arm
    L1 = L1
    L2 = L2
    L3 = L3
    L4 = L4

  DH_params = {
    # DH parameters
    #
    # const float D1 = L1             ; const float A1 = 0.0            ; const float ALPHA1 = 90.0 ;
    # const float D2 = 0.0            ; const float A2 = L2             ; const float ALPHA2 = 0.0  ;
    # const float D3 = 0.0            ; const float A3 = L3             ; const float ALPHA3 = 0.0  ;
    # const float D4 = 0.0            ; const float A4 = 0.0            ; const float ALPHA4 = 90.0 ;
    # const float D5 = L4             ; const float A5 = 0.0            ; const float ALPHA5 = 0.0  ;
    # const float D6 = penOffsetV     ; const float A6 = penOffsetH     ; const float ALPHA6 = 0.0  ;
    "D"     : [L1   , 0.0 , 0.0 , 0.0  , L4  , 0.0], #[5] = penOffsetV
    "A"     : [0.0  , L2  , L3  , 0.0  , 0.0 , 0.0], #[5] = penOffsetH
    "ALPHA" : [90.0 , 0.0 , 0.0 , 90.0 , 0.0 , 0.0]
  }


def Inverse_Kinematic(DH_params:list, penOffsetV:float, penOffsetH:float, X:float, Y:float, Z:float, pitch:float, roll:float) : 

  # the DH_params parameters needs to be declared like so :
  # DH_params = {
  #   "D"     : [L1   , 0.0 , 0.0 , 0.0  , L4  , 0.0], #[5] = penOffsetV
  #   "A"     : [0.0  , L2  , L3  , 0.0  , 0.0 , 0.0], #[5] = penOffsetH
  #   "ALPHA" : [90.0 , 0.0 , 0.0 , 90.0 , 0.0 , 0.0]
  # }
  d1 = DH_params["D"][0]
  d2 = DH_params["D"][1] 
  d3 = DH_params["D"][2] 
  d4 = DH_params["D"][3] 
  d5 = DH_params["D"][4]
  d6 = DH_params["D"][5] + penOffsetV

  a1 = DH_params["A"][0]
  a2 = DH_params["A"][1] 
  a3 = DH_params["A"][2]
  a4 = DH_params["A"][3]
  a5 = DH_params["A"][4]
  a6 = DH_params["A"][5] + penOffsetH 

  alpha1 = DH_params["ALPHA"][0]
  alpha2 = DH_params["ALPHA"][1]
  alpha3 = DH_params["ALPHA"][2]
  alpha4 = DH_params["ALPHA"][3]
  alpha5 = DH_params["ALPHA"][4]
  alpha6 = DH_params["ALPHA"][5]

  PD = [X, Y, Z]

  RotY = [
    [cos(pitch), 0, sin(pitch)],
    [0, 1, 0],
    [-sin(pitch), 0, cos(pitch)] 
  ]

  Pn = [
    RotY[0][0] * 0 + RotY[0][2] * d6,
    0,
    RotY[2][0] * 0 + RotY[2][2] * d6 
  ]
  
  t = atan2(Y, X)

  Pn[0] = PD[0] - Pn[0] * cos(t)
  Pn[1] = PD[1] - Pn[1] * sin(t)
  Pn[2] = PD[2] - Pn[2]
  
  X = Pn[0]
  Y = Pn[1]
  Z = Pn[2]

  # Inverse Kinematics
  #t1 = (fabs(y) < 1e-5 && fabs(x) < 1e-5) ? 0 : atan2(y, x);
  if (abs(Y) < 1e-5 and abs(X) < 1e-5) :
    t1 = 0
  else :
    t1 = atan2(Y, X)
  
  # This will make the robot to follow actual rotation configuration
  # If removed, then positive means robot end-effector always pointing outside
  # Negative means robot end-effector always pointing inside
  if (fabs(X) > 1e-5) :
    #pitch = SIGN(X) * pitch
    pass

  Rn = sqrt(X * X + Y * Y) - L4 * sin(pitch)
  Zn = Z - L4 * cos(pitch) - L1

  C3 = (Rn * Rn + Zn * Zn - L2 * L2 - L3 * L3) / (2 * L2 * L3)
  C3 = min(1, max(C3, -1))

  t3 = -acos(C3)
  if (pitch < 0) :
    t3 = -t3

  t2 = atan2(Zn, Rn) - atan2(L3 * sin(t3), L2 + L3 * cos(t3))
  t4 = -pitch - t2 - t3 + pi
  t5 = roll


  # Motor Compatable Angles */
  t1_Motor = t1
  t2_Motor = t2 - pi/2
  t3_Motor = t2_Motor + t3
  t4_Motor = t3_Motor + t4 - pi/2
  t5_Motor = t5 - t4_Motor
    
  #t1_Motor = -t1_Motor 
  t2_Motor = -t2_Motor
  t3_Motor = -t3_Motor
  t4_Motor = -t4_Motor
  t5_Motor = -t5_Motor

  # Final Angles */
  motorAngles = [0] * 5

  motorAngles[0] = t1_Motor * 180 / pi
  motorAngles[1] = t2_Motor * 180 / pi
  motorAngles[2] = t3_Motor * 180 / pi
  motorAngles[3] = t4_Motor * 180 / pi
  motorAngles[4] = t5_Motor * 180 / pi

  return motorAngles

#void GoToXYZ(float P_OffsetV, float P_OffsetH, float X, float Y, float Z, float pitch, float roll, float thetas[])
def main() :

  # Inputs */ 

  penOffsetV = 0.0
  penOffsetH = 0.0

  x = 0.0
  y = 0
  z = 0.754
  
  pitch =  0 * pi/180
  roll  =  pi


  # Function for Inverse Kinematics */
  motorAngles = Inverse_Kinematic(Youpi.DH_params, penOffsetV, penOffsetH, x, y, z, pitch, roll)

  for i in range(0, 5) :
    print(round(motorAngles[i], 4))

if __name__ == "__main__":
  main()
#include <stdio.h>
#include <stdlib.h>


//// Robot Data
// Lengths of the Robot's arm
#define L1 0.28
#define L2 0.162
#define L3 0.162
#define L4 0.15


// Defining the Dh Parameters of the Robot
const float d1 = L1             ; const float a1 = 0.0            ;  const float alpha1 = 90.0   ;
const float d2 = 0.0            ; const float a2 = L2             ;  const float alpha2 = 0.0    ;
const float d3 = 0.0            ; const float a3 = L3             ;  const float alpha3 = 0.0    ;
const float d4 = 0.0            ; const float a4 = 0.0            ;  const float alpha4 = 90.0   ;
const float d5 = L4             ; const float a5 = 0.0            ;  const float alpha5 = 0.0    ;
const float d6 = P_OffsetV      ; const float a6 = P_OffsetH      ;  const float alpha6 = 0.0    ;


//void GoToJointAngles(float thetas[], int Speed, int coders_motors[], float cartesian_position[]);

void GoToXYZ(float P_OffsetV, float P_OffsetH, float X, float Y, float Z, float pitch, float roll, float thetas[]){

// Pencil length :
//  P_OffsetV = Vertical
//  P_OffsetH = Horizontal


//// Desired Pose
//X     = 0;
//Y     = -0.400;
//Z     = 0; // L1 + L2 + L3 + L4 = 0.754.

float PD = [X; Y; Z];

Pitch = 180 * pi/180;
Roll  = pi;

RotY  = [cos(Pitch) 0 sin(Pitch); 0 1 0; -sin(Pitch) 0 cos(Pitch)];

Pn     = RotY * [0; 0; d6]; // Currently only extending pencil conifiguration

t      = atan2(Y, X);

Pn     = PD - [Pn(1)*cos(t); Pn(1)*sin(t); Pn(3)];

X      = Pn(1);
Y      = Pn(2);
Z      = Pn(3);


//// Inverse Kinematics
// Theta1
t1 = atan2(Y, X);

if abs(Y) < 1e-5 && abs(X) < 1e-5

    t1 = 0;

end

// New Configuration for Joint 2 3 4
//if abs(X) > 1e-5
//    Pitch = sign(X) * Pitch
//end

Rn = sqrt(X^2 + Y^2) - L4 * sin(Pitch);
Zn = Z - L4 * cos(Pitch) - L1;

// Theta3
C3 = (Rn^2 + Zn^2 - L2^2 - L3^2)/(2 * L2 * L3);
C3 = min(1,max(C3,-1));

t3 = -acos(C3);

if Pitch < 0

    t3 = -t3;

end

// Theta2
t2 = atan2(Zn, Rn) - atan2(L3 * sin(t3), L2 + L3 * cos(t3));

// Theta4
t4 = -Pitch - t2 - t3 + pi;


// Theta5
t5 = 0;

Thetas = [t1 t2 t3 t4 t5] * 180/pi;

disp('Joint Angles in Degree');

disp(Thetas);

//// Forward Kinematics
// Transformation
A1 =  [cos(t1) -sin(t1)*cosd(alpha1) sin(t1)*sind(alpha1) a1*cos(t1);
       sin(t1) cos(t1)*cosd(alpha1)  -cos(t1)*sind(alpha1) a1*sin(t1);
       0            sind(alpha1)            cosd(alpha1)         d1;
       0                0                 0                1];

A2 =  [cos(t2) -sin(t2)*cosd(alpha2) sin(t2)*sind(alpha2) a2*cos(t2);
       sin(t2) cos(t2)*cosd(alpha2)  -cos(t2)*sind(alpha2) a2*sin(t2);
       0            sind(alpha2)            cosd(alpha2)         d2;
       0                0                 0                1];

A3 =  [cos(t3) -sin(t3)*cosd(alpha3) sin(t3)*sind(alpha3) a3*cos(t3);
       sin(t3) cos(t3)*cosd(alpha3)  -cos(t3)*sind(alpha3) a3*sin(t3);
       0            sind(alpha3)            cosd(alpha3)         d3;
       0                0                 0                1];

A4 =  [cos(t4) -sin(t4)*cosd(alpha4) sin(t4)*sind(alpha4) a4*cos(t4);
       sin(t4) cos(t4)*cosd(alpha4)  -cos(t4)*sind(alpha4) a4*sin(t4);
       0            sind(alpha4)            cosd(alpha4)         d4;
       0                0                 0                1] ;

A5 =  [cos(t5) -sin(t5)*cosd(alpha5) sin(t5)*sind(alpha5) a5*cos(t5);
       sin(t5) cos(t5)*cosd(alpha5)  -cos(t5)*sind(alpha5) a5*sin(t5);
       0            sind(alpha5)            cosd(alpha5)         d5;
       0                0                 0                1];

t6 = 0;

A6 =  [cos(t6) -sin(t6)*cosd(alpha6) sin(t6)*sind(alpha6) a6*cos(t6);
       sin(t6) cos(t6)*cosd(alpha6)  -cos(t6)*sind(alpha6) a6*sin(t6);
       0            sind(alpha6)            cosd(alpha6)         d6;
       0                0                 0                1];

T05 = A1 * A2 * A3 * A4 * A5 * A6;

}
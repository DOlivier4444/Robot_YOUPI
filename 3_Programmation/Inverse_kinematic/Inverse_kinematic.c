#include <stdio.h>
#include <math.h>

#define PI 3.14159265358979323846

#define SIGN(x) ((x > 0) - (x < 0))

void GoToXYZ(double P_OffsetV, double P_OffsetH, double X, double Y, double Z, double pitch, double roll, double thetas[]) {
    // Robot Data
    double L1 = 0.28, L2 = 0.162, L3 = 0.162, L4 = 0.15;

    // DH Parameters
    double d1 = L1, a1 = 0, alpha1 = 90;
    double d2 = 0, a2 = L2, alpha2 = 0;
    double d3 = 0, a3 = L3, alpha3 = 0;
    double d4 = 0, a4 = 0, alpha4 = 90;
    double d5 = L4, a5 = 0, alpha5 = 0;
    double d6 = P_OffsetV, a6 = P_OffsetH, alpha6 = 0;

    double PD[3] = {X, Y, Z};

    double RotY[3][3] = {
        {cos(pitch), 0, sin(pitch)},
        {0, 1, 0},
        {-sin(pitch), 0, cos(pitch)}
    };

    double Pn[3] = {
        RotY[0][0] * 0 + RotY[0][2] * d6,
        0,
        RotY[2][0] * 0 + RotY[2][2] * d6
    };

    double t = atan2(Y, X);

    Pn[0] = PD[0] - Pn[0] * cos(t);
    Pn[1] = PD[1] - Pn[1] * sin(t);
    Pn[2] = PD[2] - Pn[2];

    X = Pn[0];
    Y = Pn[1];
    Z = Pn[2];

    // Inverse Kinematics
    double t1 = (fabs(Y) < 1e-5 && fabs(X) < 1e-5) ? 0 : atan2(Y, X);

    // This will make the robot to follow actual rotation configuration
    // If removed, then positive means robot end-effector always pointing outside
    // Negative means robot end-effector always pointing inside
    if (fabs(X) > 1e-5){

        //pitch = SIGN(X) * pitch;

    }

    double Rn = sqrt(X * X + Y * Y) - L4 * sin(pitch);
    double Zn = Z - L4 * cos(pitch) - L1;

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
    thetas[0] = t1_Motor * 180 / PI;
    thetas[1] = t2_Motor * 180 / PI;
    thetas[2] = t3_Motor * 180 / PI;
    thetas[3] = t4_Motor * 180 / PI;
    thetas[4] = t5_Motor * 180 / PI;

}


//void GoToXYZ(float P_OffsetV, float P_OffsetH, float X, float Y, float Z, float pitch, float roll, float thetas[]);
int main() {
    double thetas[5];

    /* Inputs */

    double Xd    = 0.0;;
    double Yd    = 0;
    double Zd    = 0.754;

    double Pitchd = 0 * PI/180;
    double Rolld  = PI;

    /* Function for Inverse Kinematics */
    GoToXYZ(0, 0, Xd, Yd, Zd, Pitchd, Rolld, thetas);

    printf("Joint Angles in Degree:\n");
    for (int i = 0; i < 5; i++) {
        printf("%f\n", thetas[i]);
    }

    return 0;

}

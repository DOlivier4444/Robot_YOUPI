#!/usr/bin/env python3

from visual_kinematics.RobotSerial import *
import numpy as np
from math import pi


def main():
    np.set_printoptions(precision=3, suppress=True)

    dh_params = np.array([[-90, 90.0, 0.0, 2.8],
                          [90, 180.0, 1.62, 0.0],
                          [0.0, 180.0, 1.62, 0.0],
                          [90.0, 90.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0, 1.50],
                          [0.0, 0.0, 0.0, 0.0]])
    
    robot = RobotSerial(dh_params)

    # =====================================
    # forward
    # =====================================

    theta = np.array([180, 180, 90, 90.0, 90.0, 90.0])
    f = robot.forward(theta)

    print("-------forward-------")
    print("end frame t_4_4:")
    print(f.t_4_4)
    print("end frame xyz:")
    print(f.t_3_1.reshape([3, ]))
    print("end frame abc:")
    print(f.euler_3)
    print("end frame rotational matrix:")
    print(f.r_3_3)
    print("end frame quaternion:")
    print(f.q_4)
    print("end frame angle-axis:")
    print(f.r_3)

    robot.show()


if __name__ == "__main__":
    main()

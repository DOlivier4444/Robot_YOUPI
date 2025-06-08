#!/usr/bin/env python3

from visual_kinematics.RobotSerial import *
import numpy as np
from math import pi


def main():
    np.set_printoptions(precision=3, suppress=True)

    dh_params = np.array([[28.0, 0.0, 90.0, -90.0],
                          [0.0, 16.2, 180.0, 90.0],
                          [0.0, 16.2, 180.0, 0.0],
                          [0.0, 0.0, 90.0, 90.0],
                          [15.0, 0.0, 0.0, 0.0]])

    robot = RobotSerial(dh_params)

    # =====================================
    # inverse
    # =====================================

    xyz = np.array([[15.0], [10.], [60.4]])
    abc = np.array([0., 0., 0.])
    end = Frame.from_euler_3(abc, xyz)
    robot.inverse(end)

    print("inverse is successful: {0}".format(robot.is_reachable_inverse))
    print("axis values: \n{0}".format(robot.axis_values))
    robot.show()

    # example of unsuccessful inverse kinematics
    xyz = np.array([[2.2], [0.], [1.9]])
    end = Frame.from_euler_3(abc, xyz)
    robot.inverse(end)

    print("inverse is successful: {0}".format(robot.is_reachable_inverse))


if __name__ == "__main__":
    main()

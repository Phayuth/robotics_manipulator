"""Generate dataset for forward dynamic model training for Planar Robot
- X dataset (nx2) : (theta1, theta2)
- Y dataset (nx2) : (x, y)
"""

import os
import sys

sys.path.append(str(os.path.abspath(os.getcwd())))

import numpy as np
from robot.planar_rr import PlanarRR


def planar_rr_generate_dataset(robot):

    # start sample
    sample_size = 360
    theta_candidate = np.linspace(-np.pi, np.pi, sample_size)

    sample_theta = [] # X
    sample_endeffector_pose = []  #

    for i in range(sample_size):
        for j in range(sample_size):
            endeffector_pose = robot.forward_kinematic(np.array([[theta_candidate[i]], [theta_candidate[j]]]))  # this is where a machine learning for forward dynamic will replace

            sample_theta_row = [theta_candidate[i], theta_candidate[j]]
            sample_theta.append(sample_theta_row)

            sample_endeffector_row = [endeffector_pose[0, 0], endeffector_pose[1, 0]]
            sample_endeffector_pose.append(sample_endeffector_row)

    return np.array(sample_theta), np.array(sample_endeffector_pose)


if __name__ == "__main__":

    robot = PlanarRR()

    X, y = planar_rr_generate_dataset(robot)

    print("==>> sample_theta.shape: \n", X.shape)
    print("==>> sample_endeffector_pose.shape: \n", y.shape)
import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from robot.ur5e import ur5e

theta = np.array([[0],
                  [0],
                  [0],
                  [0],
                  [0],
                  [0]])
r = ur5e()
x_current = r.forward_kinematic(theta)
print("==>> x_current: ", x_current)

roll = 0
pitch = 0
yaw = 0
x_desired = np.array([[0.2],
                      [0.2],
                      [0.2],
                      [roll],
                      [pitch],
                      [yaw]])

e = x_desired - x_current
max_iter = 100
i = 0

while np.linalg.norm(e) > 0.001 and i < max_iter:
    x_current = r.forward_kinematic(theta)

    e = x_desired - x_current
    Jac = r.jacobian(theta)
    del_theta = np.linalg.pinv(Jac) @ e
    print("==>> del_theta: ", del_theta)
    theta = theta + del_theta
    i += 1

print(theta)
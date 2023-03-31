import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import matplotlib.pyplot as plt
import numpy as np
from util.coord_transform import polar2cats
from robot.planar_rrr import planar_rrr

robot = planar_rrr()

x_targ = 0.5  # user pick
y_targ = 0.5  # user pick
alpha_candidate = 2  # given from grapse pose candidate

theta_coord = np.linspace(0, 2*np.pi, 90)
radius = 0.1
x_coord, y_coord = polar2cats(radius, theta_coord, x_targ, y_targ)

# target
phi_target = alpha_candidate - np.pi
target = np.array([[x_targ],
                   [y_targ],
                   [phi_target]])
theta_ik_tag = robot.inverse_kinematic_geometry(target, elbow_option=0)


# approach point
d_app = 0.1
app_point = np.array([[d_app*np.cos(target[2, 0]+np.pi) + target[0, 0]],
                      [d_app*np.sin(target[2, 0]+np.pi) + target[1, 0]],
                      [target[2, 0]]])
theta_ik_app = robot.inverse_kinematic_geometry(app_point, elbow_option=0)

robot.plot_arm(theta_ik_tag, plt_basis=True)
robot.plot_arm(theta_ik_app)
plt.plot(x_coord, y_coord)
plt.show()
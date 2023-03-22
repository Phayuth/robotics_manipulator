import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
import matplotlib.pyplot as plt
from robot.planar_rr import planar_rr
from config_space_2d.generate_config_planar_rr import configuration_generate_plannar_rr
from map.taskmap_geo_format import task_rectangle_obs_1
from map.map_value_range import map_val

robot = planar_rr()

def polar2cats(r,theta):
    x = r*np.cos(theta) + 1.6
    y = r*np.sin(theta) + 2.15
    return x,y

theta = np.linspace(np.pi/2,3*np.pi/2,10)
radius = 0.1
x_coord, y_coord = polar2cats(radius,theta)

# target
target = np.array([[1.6],
                   [2.15]])
theta_ik_tag = robot.inverse_kinematic_geometry(target, elbow_option=0)

# approach point
d_app = 0.1
alpha = np.pi + np.sum(theta_ik_tag)
app_point = np.array([[d_app*np.cos(alpha)],
                      [d_app*np.sin(alpha)]]) + target
theta_ik_app = robot.inverse_kinematic_geometry(app_point, elbow_option=0)

# import obs list
obs_list = task_rectangle_obs_1()

# setup plot look
plt.axes().set_aspect('equal')
plt.axvline(x=0, c="black")
plt.axhline(y=0, c="black")

for obs in obs_list:
    obs.plot()

plt.plot(x_coord, y_coord)
robot.plot_arm(theta_ik_app)
robot.plot_arm(theta_ik_tag)
plt.show()

# create config space
grid_np = configuration_generate_plannar_rr(robot, obs_list)

theta1_app_index = int(map_val(theta_ik_app[0].item(), -np.pi, np.pi, 0, 360)) 
theta2_app_index = int(map_val(theta_ik_app[1].item(), -np.pi, np.pi, 0, 360))
theta1_goal_index = int(map_val(theta_ik_tag[0].item(), -np.pi, np.pi, 0, 360)) 
theta2_goal_index = int(map_val(theta_ik_tag[1].item(), -np.pi, np.pi, 0, 360))

grid_np[theta1_app_index, theta2_app_index] = 2
grid_np[theta1_goal_index, theta2_goal_index] = 3

plt.imshow(grid_np)
plt.show()

import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
import math
import matplotlib.pyplot as plt
from skimage.measure import profile_line
from planner.research_rrtstar.rrtstar_costmap_biassampling import node , rrt_star
from robot_used.ur5e.ur5e2d import Robot, pmap

# load task space map
map = pmap()

# create start and goal node
x_init = node(180,180)
x_goal = node(95, 95)

# load robot
base_position = [90, 0]
robot = Robot(base_position)

# create config space, but to save time we already create and save into numpy save
c_map = np.load("./map/mapdata/config_space_data_2d/config2D_leaf-x_map1img.npy")

# create planner
iteration = 2000
m = c_map.shape[0] * c_map.shape[1] / 2
r = (2 * (1 + 1/2)**(1/2)) * (m/math.pi)**(1/2)
eta =  r * (math.log(iteration) / iteration)**(1/2)
distance_weight = 0.5
obstacle_weight = 0.5
rrt = rrt_star(c_map, x_init, x_goal, eta, distance_weight, obstacle_weight, iteration)

# start planner
rrt.start_planning()

# get path result
path = rrt.Get_Path()
path = np.flip(path, axis=0)

goal_path = np.array([x_init.arr])
if len(path) >= 2:
    for node in path:
        goal_path = np.append(goal_path, [node.arr], axis=0)

# np.save("path", goal_path)

# plot rrt star in config space
plt.figure(figsize=(12,10))
plt.axes().set_aspect('equal')
plt.imshow(np.transpose(c_map), cmap = "gray", interpolation = 'nearest')
rrt.Draw_Tree()
rrt.Draw_path(path)
plt.gca().invert_yaxis()

plt.scatter(x_init.x, x_init.y, s=10, c="w")
plt.scatter(x_goal.x, x_goal.y, s=10, c="g")
plt.show()

plt.figure(figsize=(10,5))
plt.axes().set_aspect('equal')
plt.imshow(np.transpose(map),cmap = "gray", interpolation = 'nearest')

# plot path and arm in task space
w_path = []
for i in path:

    position = robot.robot_position(i.arr[0]-180, i.arr[1]-180)
    w_path.append(position)

for i in range(len(w_path)):
    plt.plot([base_position[0], w_path[i][0][0]], [base_position[1], w_path[i][0][1]], "k", linewidth=10)
    plt.plot([w_path[i][0][0], w_path[i][1][0]], [w_path[i][0][1], w_path[i][1][1]], "k", linewidth=8)
    plt.plot([w_path[i][1][0], w_path[i][2][0]], [w_path[i][1][1], w_path[i][2][1]], "k", linewidth=7)
for i in range(len(w_path) - 1):
    plt.plot([w_path[i][1][0], w_path[i+1][1][0]], [w_path[i][1][1], w_path[i+1][1][1]], "b", linewidth=2.5)
    plt.plot([w_path[i][2][0], w_path[i+1][2][0]], [w_path[i][2][1], w_path[i+1][2][1]], "r", linewidth=2.5)

plt.plot([base_position[0], w_path[0][0][0]], [base_position[1], w_path[0][0][1]], "y", linewidth=10)
plt.plot([w_path[0][0][0], w_path[0][1][0]], [w_path[0][0][1], w_path[0][1][1]], "b", linewidth=8)
plt.plot([w_path[0][1][0], w_path[0][2][0]], [w_path[0][1][1], w_path[0][2][1]], "r", linewidth=7)

plt.plot([base_position[0], w_path[-1][0][0]], [base_position[1], w_path[-1][0][1]], "y", linewidth=10)
plt.plot([w_path[-1][0][0], w_path[-1][1][0]], [w_path[-1][0][1], w_path[-1][1][1]], "b", linewidth=8)
plt.plot([w_path[-1][1][0], w_path[-1][2][0]], [w_path[-1][1][1], w_path[-1][2][1]], "r", linewidth=7)

plt.gca().invert_yaxis()
plt.show()

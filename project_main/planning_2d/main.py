import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
import math
import matplotlib.pyplot as plt

from map.generate_map import grid_map_probability
from planner.rrtstar_probabilty_2d import node, rrt_star

# Load Map
map_index = 2
filter_size = 3 # 1 = 3x3, 2 = 5x5, 3 = 7x7
classify = True
map = grid_map_probability(map_index, filter_size, classify)

# Creat start and end pose
x_init = node(15, 110)
x_goal = node(110, 17)

# Create planner class
iteration = 1000
distance_weight = 0.5
obstacle_weight = 0.5
m = map.shape[0] * map.shape[1]
r = (2 * (1 + 1/2)**(1/2)) * (m/math.pi)**(1/2)
eta =  r * (math.log(iteration) / iteration)**(1/2)
rrt = rrt_star(x_init, x_goal, map, eta, distance_weight, obstacle_weight, iteration)

# Seed random
np.random.seed(1)

# Call to start planning
rrt.start_planning()

# Get path from planner
path = rrt.Get_Path()

# Print time
rrt.print_time()

# Plot result
plt.figure(figsize=(10,10))
plt.axes().set_aspect('equal')
rrt.Draw_Tree()
rrt.Draw_path(path)
plt.imshow(np.transpose(1-map),cmap = "jet", interpolation = 'nearest')
plt.title("Probability map(same type)")
plt.show()
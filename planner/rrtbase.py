""" Path Planning for Planar RR with RRT based
- Map : Continuous configuration space 2D create from image to geometry with MapLoader and MapClass
- Collsion : Geometry based
- Path Searcher : Naive Seach. the nodes near to x_goal -> add x_goal to tree and find path. we can do better, but for simplication just use this.
                  trace back to the start node using the parent node information. we are able to use this beacause we exploit the fact that a node
                  can only have 1 parent but have many child.

"""

import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
import matplotlib.pyplot as plt
from collision_check_geometry.collision_class import ObjLine2D, ObjPoint2D, intersect_point_v_rectangle, intersect_line_v_rectangle


class node:

    def __init__(self, x, y, parent=None) -> None:
        self.x = x
        self.y = y
        self.parent = parent


class RRTBase():

    def __init__(self, mapclass, x_start, x_goal, eta=0.3, maxiteration=1000) -> None:
        # map properties
        self.mapclass = mapclass
        self.x_min = self.mapclass.xmin
        self.x_max = self.mapclass.xmax
        self.y_min = self.mapclass.ymin
        self.y_max = self.mapclass.ymax
        self.x_start = node(x_start[0, 0], x_start[1, 0])
        self.x_goal = node(x_goal[0, 0], x_goal[1, 0])

        if mapclass.__class__.__name__ == "CostMapClass":
            self.obs = self.mapclass.costmap2geo()
        else:
            self.obs = self.mapclass.obj

        # properties of planner
        self.maxiteration = maxiteration
        self.eta = eta
        self.tree_vertex = [self.x_start]

    def planing(self):
        for itera in range(self.maxiteration):
            print(itera)
            x_rand = self.sampling()
            x_nearest = self.nearest_node(x_rand)
            x_new = self.steer(x_nearest, x_rand)
            x_new.parent = x_nearest
            if self.collision_check_node(x_new) or self.collision_check_line(x_nearest, x_new):
                continue
            else:
                self.tree_vertex.append(x_new)

    def search_path(self):
        x_near_to_goal = self.nearest_node(self.x_goal)
        self.x_goal.parent = x_near_to_goal
        path = [self.x_goal]
        curr_node = self.x_goal

        while curr_node != self.x_start:
            curr_node = curr_node.parent
            path.append(curr_node)

        path.reverse()

        return path

    def sampling(self):
        x = np.random.uniform(low=self.x_min, high=self.x_max)
        y = np.random.uniform(low=self.y_min, high=self.y_max)
        x_rand = node(x, y)

        return x_rand

    def nearest_node(self, x_rand):
        vertex_list = []

        for each_vertex in self.tree_vertex:
            dist_x = x_rand.x - each_vertex.x
            dist_y = x_rand.y - each_vertex.y
            dist = np.linalg.norm([dist_x, dist_y])
            vertex_list.append(dist)

        min_index = np.argmin(vertex_list)
        x_near = self.tree_vertex[min_index]
        
        return x_near

    def steer(self, x_nearest, x_rand):
        dist_x = x_rand.x - x_nearest.x
        dist_y = x_rand.y - x_nearest.y
        dist = np.linalg.norm([dist_x, dist_y])

        if dist <= self.eta:
            x_new = x_rand
        else:
            direction = np.arctan2(dist_y, dist_x)
            new_x = self.eta * np.cos(direction) + x_nearest.x
            new_y = self.eta * np.sin(direction) + x_nearest.y
            x_new = node(new_x, new_y)
        return x_new

    def collision_check_node(self, x_new):
        nodepoint = ObjPoint2D(x_new.x, x_new.y)

        col = []
        for obs in self.obs:
            colide = intersect_point_v_rectangle(nodepoint, obs)
            col.append(colide)

        if True in col:
            return True
        else:
            return False

    def collision_check_line(self, x_nearest, x_new):
        line = ObjLine2D(x_nearest.x, x_nearest.y, x_new.x, x_new.y)

        col = []
        for obs in self.obs:
            colide = intersect_line_v_rectangle(line, obs)
            col.append(colide)

        if True in col:
            return True
        else:
            return False

    def plot_env(self, after_plan=False):
        # plot obstacle
        for obs in self.obs:
            obs.plot()

        if after_plan:
            # plot tree vertex and branches
            for j in self.tree_vertex:
                plt.scatter(j.x, j.y, color="red")  # vertex
                if j is not self.x_start:
                    plt.plot([j.x, j.parent.x], [j.y, j.parent.y], color="green")  # branch

        # plot start and goal node
        plt.scatter([self.x_start.x, self.x_goal.x], [self.x_start.y, self.x_goal.y], color='cyan')


if __name__ == "__main__":
    from map.taskmap_geo_format import task_rectangle_obs_3
    from map.taskmap_img_format import bmap
    from map.mapclass import CostMapLoader, CostMapClass, GeoMapClass
    np.random.seed(9)


    # SECTION - Experiment 1
    # maploader = CostMapLoader.loadarray(bmap())
    # mapclass = CostMapClass(maploader=maploader, maprange=[[-np.pi, np.pi], [-np.pi, np.pi]])
    # start = np.array([0, 0]).reshape(2, 1)
    # goal = np.array([1, 1]).reshape(2, 1)


    # SECTION - Experiment 2
    # mapclass = GeoMapClass(geomap=task_rectangle_obs_3(), maprange=[[-np.pi, np.pi], [-np.pi, np.pi]])
    # start = np.array([0, 0]).reshape(2, 1)
    # goal = np.array([1, 1]).reshape(2, 1)


    # SECTION - Experiment 3
    start = np.array([4, 4]).reshape(2, 1)
    goal = np.array([8.5, 1]).reshape(2, 1)
    maploader = CostMapLoader.loadarray(bmap())
    mapclass = CostMapClass(maploader, maprange=[[0, 10], [0, 10]])


    # SECTION - Planning Section
    planner = RRTBase(mapclass, start, goal, eta=0.1, maxiteration=2000)
    planner.plot_env()
    plt.show()
    planner.planing()
    path = planner.search_path()


    # SECTION - plot planning result
    planner.plot_env(after_plan=True)
    plt.plot([node.x for node in path], [node.y for node in path], color='blue')
    plt.show()
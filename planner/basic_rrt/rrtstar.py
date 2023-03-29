import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
import matplotlib.pyplot as plt
from collision_check_geometry.collision_class import line_obj, point2d_obj, intersect_point_v_rectangle, intersect_line_v_rectangle
from map.taskmap_geo_format import task_rectangle_obs_7

class node:
    def __init__(self, x, y, parent=None, cost=0.0) -> None:
        self.x = x
        self.y = y
        self.parent = parent
        self.cost = 0.0

class rrtstar:
    def __init__(self) -> None:
        # properties of planner
        self.maxiteration = 1000
        self.startnode = node(4, 4)
        self.startnode.cost = 0.0
        self.goalnode = node(7, 8)

        # map
        self.map = np.ones((10, 10))
        self.obs = task_rectangle_obs_7()

        # distance step update per iteration
        m = self.map.shape[0] * self.map.shape[1]
        self.radius = (2 * (1 + 1/2)**(1/2)) * (m/np.pi)**(1/2)
        self.eta = self.radius * (np.log(self.maxiteration) / self.maxiteration)**(1/2)

        # start with a tree vertex have start node and empty branch
        self.tree_vertex = [self.startnode]

    def planning(self):
        for _ in range(self.maxiteration):
            x_rand = self.sampling()
            x_nearest = self.nearest_node(x_rand)
            x_new = self.steer(x_nearest, x_rand)
            if self.collision_check_node(x_new) or self.collision_check_line(x_nearest, x_new):
                continue
            else:
                x_new.cost = x_nearest.cost + self.cost_line(x_new, x_nearest) # add the vertex new, which we have to calculate the cost and add parent as well
                x_new.parent = x_nearest

                # connect along minimum cost path
                X_near = self.near(x_new, self.eta)
                for x_near in X_near:
                    if self.collision_check_line(x_near, x_new):
                        continue
                    c_new = x_near.cost + self.cost_line(x_new, x_near)
                    c_min = x_nearest.cost + self.cost_line(x_new, x_nearest)
                    if c_new < c_min:
                            x_nearest = x_near
                            x_new.cost = x_nearest.cost + self.cost_line(x_new, x_nearest)
                            x_new.parent = x_nearest

                self.tree_vertex.append(x_new)

                # rewire
                for x_near in X_near:
                    if self.collision_check_line(x_near, x_new):
                        continue
                    c_new = x_new.cost + self.cost_line(x_new, x_near)
                    if c_new < x_near.cost:
                        x_near.parent = x_new
                        x_near.cost = x_new.cost + self.cost_line(x_new, x_near)

    def search_path(self):
        X_near = self.near(self.goalnode, self.eta)
        for x_near in X_near:
            if self.collision_check_line(x_near, self.goalnode):
                continue
            self.goalnode.parent = x_near

            path = [self.goalnode]
            curr_node = self.goalnode

            while curr_node != self.startnode:
                curr_node = curr_node.parent
                path.append(curr_node)

            path.reverse()

            best_path = path

            cost = sum(i.cost for i in path)

            if cost < sum(j.cost for j in best_path):
                best_path = path
        
        return best_path

    def sampling(self):
        x = np.random.uniform(low=0, high=self.map.shape[0])
        y = np.random.uniform(low=0, high=self.map.shape[1])
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
            new_x = self.eta*np.cos(direction) + x_nearest.x
            new_y = self.eta*np.sin(direction) + x_nearest.y
            x_new = node(new_x, new_y)
        return x_new

    def near(self, x_new, min_step):
        neighbor = []
        for index, vertex in enumerate(self.tree_vertex):
            dist = np.linalg.norm([(x_new.x - vertex.x), (x_new.y - vertex.y)])
            if dist <= min_step:
                neighbor.append(index)
        return [self.tree_vertex[i] for i in neighbor]

    def cost_line(self, xstart, xend):
        return np.linalg.norm([(xstart.x - xend.x), (xstart.y - xend.y)]) # simple euclidean distance as cost

    def collision_check_node(self, x_new):
        nodepoint = point2d_obj(x_new.x, x_new.y)

        col = []
        for obs in self.obs:
            colide = intersect_point_v_rectangle(nodepoint, obs)
            col.append(colide)

        if True in col:
            return True
        else:
            return False

    def collision_check_line(self, x_nearest, x_new):
        line = line_obj(x_nearest.x, x_nearest.y, x_new.x, x_new.y)

        col = []
        for obs in self.obs:
            colide = intersect_line_v_rectangle(line, obs)
            col.append(colide)

        if True in col:
            return True
        else:
            return False

    def plot_env(self):
        # plot obstacle
        for obs in self.obs:
            obs.plot()

        # plot tree vertex and start and goal node
        for j in self.tree_vertex:
            plt.scatter(j.x, j.y, color="red")

        # plot tree branh
        for k in self.tree_vertex:
            if k is not self.startnode:
                plt.plot([k.x, k.parent.x], [k.y, k.parent.y], color="green")

        # plot start and goal node
        plt.scatter([self.startnode.x, self.goalnode.x], [self.startnode.y, self.goalnode.y], color='cyan')

if __name__ == "__main__":
    np.random.seed(9)
    planner = rrtstar()
    planner.planning()
    planner.plot_env()

    path = planner.search_path()
    plt.plot([node.x for node in path], [node.y for node in path], color='blue')

    plt.show()
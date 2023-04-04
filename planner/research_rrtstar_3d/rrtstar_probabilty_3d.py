import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
import matplotlib.pyplot as plt
import time
ax = plt.axes(projection='3d')


class node(object):
    def __init__(self, x:float, y:float, z:float, cost:float = 0, parent = None):
        """node class

        Args:
            x (float): configuration x
            y (float): configuration y
            z (float): configuration z
            cost (float, optional): cost value. Defaults to 0.
            parent (numpy array, optional): parent node. Defaults to None.
        """
        self.x = x
        self.y = y
        self.z = z
        self.arr = np.array([self.x, self.y, self.z])
        self.cost = cost
        self.parent = parent

class rrt_star():
    def __init__(self, map:np.ndarray, x_init:node, x_goal:node, w1:float, w2:float, eta:float=None, maxiteration:int=1000):
        """YeongMin proposed method of planning using RRT*, Bias sampling, Probability Costmap

        Args:
            map (np.ndarray): occupancy grid map with probability value instead pure 0(obs) and 1(free)
            x_init (node): start configuraton node
            x_goal (node): end configuratoin node
            eta (float): RRT* constants
            w1 (float): distance weight
            w2 (float): obstacle weight
            max_interation (int): maximum of iteration
        """
        # map properties
        self.map = map
        self.x_init = node(x_init[0,0], x_init[1,0], x_init[2,0])
        self.x_goal = node(x_goal[0,0], x_goal[1,0], x_goal[2,0])
        self.nodes = [self.x_init]

        # planner properties
        self.maxiteration = maxiteration
        self.m = map.shape[0] * map.shape[1] * map.shape[2]
        self.r = (2 * (1 + 1/2)**(1/2)) * (self.m/np.pi)**(1/2)
        self.eta = self.r * (np.log(self.maxiteration) / self.maxiteration)**(1/2)
        self.w1 = w1
        self.w2 = w2

        self.sample_taken = 0
        self.total_iter = 0
        self.Graph_sample_num = 0
        self.Graph_data = np.array([[0,0]])

        # timing
        self.s = time.time()
        self.e = None
        self.sampling_elapsed = 0
        self.addparent_elapsed = 0
        self.rewire_elapsed = 0

    def Sampling(self)-> node:
        """bias sampling method

        Returns:
            node: random bias sampling node
        """
        height = self.map.shape[0]
        width = self.map.shape[1]
        depth = self.map.shape[2]

        p = np.ravel(self.map) / np.sum(self.map)

        x_sample = np.random.choice(len(p), p=p)

        z = x_sample // (width * height)
        x = (x_sample - z*(width * height)) % width
        y = (x_sample - z*(width * height)) // width

        x = np.random.uniform(low=x - 0.5, high=x + 0.5)
        y = np.random.uniform(low=y - 0.5, high=y + 0.5)
        z = np.random.uniform(low=z - 0.5, high=z + 0.5)

        x_rand = node(x, y, z)

        return x_rand

    def Distance_Cost(self, start:node, end:node)-> float:
        """calculate distance from one node to other node based on euclidean distance norm
        [note] = yeongmin name this incorrectly. to get distance cost, it must divide by eta which done in function line cost
        
        Args:
            start (node): start pose with node class
            end (node): end pose with node class

        Returns:
            float: norm value between 2 point
        """

        distance_cost = np.linalg.norm(start.arr - end.arr)

        return distance_cost

    def Obstacle_Cost(self, start:node, end:node)-> float:
        """calculate cost for obstacle node

        Args:
            start (node): start pose with node class
            end (node): end pose with node class

        Returns:
            float: cost of obstacle
        """
        seg_length = 1
        seg_point = int(np.ceil(np.linalg.norm(start.arr - end.arr) / seg_length))

        value = 0
        if seg_point > 1:
            v = (end.arr - start.arr) / (seg_point)

            for i in range(seg_point+1):
                seg = start.arr + i * v
                seg = np.around(seg)
                if 1 - self.map[int(seg[0]), int(seg[1]), int(seg[2])] == 1:
                    cost = 1e10  # edge pass through the hard obstacle 

                    return cost
                else:
                    value += 1 - self.map[int(seg[0]), int(seg[1]), int(seg[2])]

            cost = value / (seg_point+1)

            return cost

        else:

            value = self.map[int(start.arr[0]), int(start.arr[1]), int(start.arr[2])] + self.map[int(end.arr[0]), int(end.arr[1]), int(end.arr[2])]
            cost = value / 2

            return cost

    def Line_Cost(self, start:node, end:node)-> float:
        """calculate line cost. if the path crosses an obstacle, it has a high cost

        Args:
            start (node): start pose with node class
            end (node): end pose with node class

        Returns:
            float: line cost = (distance weight * cost distance) + (obstacle weight * obstacle distance) 
        """

        cost = self.w1*(self.Distance_Cost(start, end)/(self.eta)) + self.w2*(self.Obstacle_Cost(start, end))

        return cost

    def Nearest(self, x_rand:node)-> node:
        """Find the nearest node in the tree that is the nearest to the random node

        Args:
            x_rand (node): a random node from bias sampling

        Returns:
            node: the nearest node in tree nearest to the random node x_rand
        """
        vertex = []
        i = 0
        for x_near in self.nodes:

            dist = self.Distance_Cost(x_near, x_rand)
            vertex.append([dist, i, x_near])
            i+=1

        vertex.sort()
        x_nearest = vertex[0][2]

        return x_nearest

    def Steer(self, x_rand:node, x_nearest:node)-> node:
        """steer function to create a new node that is in the direction of x_rand node and near to x_nearest node

        Args:
            x_rand (node): a random node from bias sampling
            x_nearest (node): the nearest node that already in the tree to the random node x_rand

        Returns:
            node: a new node that is near the x_nearest in the direction of x_rand
        """

        d = self.Distance_Cost(x_rand, x_nearest)

        if d < self.eta :
            x_new = node(x_rand.x, x_rand.y, x_rand.z)
        else:
            new_x = x_nearest.x + self.eta * ((x_rand.x - x_nearest.x)/d)
            new_y = x_nearest.y + self.eta * ((x_rand.y - x_nearest.y)/d)
            new_z = x_nearest.z + self.eta * ((x_rand.z - x_nearest.z)/d)

            x_new  = node(new_x, new_y, new_z)

        return x_new

    def Exist_Check(self, x_new:node)-> bool:
        """check if the new node is already exist in the tree

        Args:
            x_new (node): new created node from Steer function

        Returns:
            bool: True if already in the tree, False if not
        """
        for x_near in self.nodes:
            if x_new.x == x_near.x and x_new.y == x_near.y and x_new.z == x_near.z:
                return False
            else :
                return True

    def New_Check(self, x_new:node)-> bool:
        """new yeongmin proposed to Check whether or not to add to the tree.
        check probability cost of node a long with exist node check

        Args:
            x_new (node): new created node from Steer function

        Returns:
            bool: True if already in the tree and the probability is low (i guess ?), False if not
        """

        x_pob = np.array([x_new.x, x_new.y, x_new.z])
        x_pob = np.around(x_pob)

        if x_pob[0] >= self.map.shape[0]:
            x_pob[0] = self.map.shape[0] - 1
        if x_pob[1] >= self.map.shape[1]:
            x_pob[1] = self.map.shape[1] - 1
        if x_pob[2] >= self.map.shape[2]:
            x_pob[2] = self.map.shape[2] - 1

        x_pob = self.map[int(x_pob[0]), int(x_pob[1]), int(x_pob[2])]
        p = np.random.uniform(0, 1)

        if x_pob >= p and self.Exist_Check(x_new):
            return True
        else:
            return False

    def Add_Parent(self, x_new:node, x_nearest:node)-> node:
        """function for adding parent node to x_new node

        Args:
            x_new (node): new created node from Steer function
            x_nearest (node): nearest node in the tree nearest to the x_new

        Returns:
            node: x_new node that has x_nearest as its parent and cost  
        """

        x_min = x_nearest
        c_min = x_min.cost + self.Line_Cost(x_min, x_new)

        for x_near in self.nodes:
            if self.Distance_Cost(x_near, x_new) <= self.eta:
                if x_near.cost + self.Line_Cost(x_near, x_new) < c_min:
                    x_min = x_near
                    c_min = x_near.cost + self.Line_Cost(x_near, x_new)
            x_new.parent = x_min
            x_new.cost = c_min

        return x_new

    def Rewire(self, x_new:node):
        """recontruct rrt tree

        Args:
            x_new (node): new node
        """

        for x_near in self.nodes:
            if x_near is not x_new.parent:
                if self.Distance_Cost(x_near, x_new) <= self.eta :
                    if x_new.cost + self.Line_Cost(x_new, x_near) < x_near.cost:

                        x_near.parent = x_new
                        x_near.cost = x_new.cost + self.Line_Cost(x_new, x_near)

    def Get_Path(self)-> list:
        """get a list of path from start to end if path is found, else None

        Returns:
            list: list of path
        """
        temp_path = []
        path = []
        n = 0
        for i in self.nodes:
            if self.Distance_Cost(i, self.x_goal) < self.eta:
                cost = i.cost + self.Line_Cost(self.x_goal, i)
                temp_path.append([cost, n, i])
                n += 1
        temp_path.sort()

        if temp_path == []:
            print("cannot find path")
            return None

        else:
            closest_node = temp_path[0][2]
            i = closest_node
            self.x_goal.cost = temp_path[0][0]

            while i is not self.x_init:
                path.append(i)
                i = i.parent
            path.append(self.x_init)

            self.x_goal.parent = path[0]
            path.insert(0, self.x_goal)

            return path

    def Cost_Graph(self):

        temp_path = []
        n = 0
        for i in self.nodes:
            if self.Distance_Cost(i, self.x_goal) < self.eta:
                cost = i.cost + self.Line_Cost(self.x_goal, i)
                temp_path.append([cost, n, i])
                n += 1
        temp_path.sort()

        if temp_path == []:
            return 0
        else:
            closest_node = temp_path[0][2]
            i = closest_node

            self.x_goal.cost = temp_path[0][0]

            return self.x_goal.cost
        
    def Draw_tree(self):
        """draw rrt tree on plot
        """

        for i in self.nodes:
            if i is not self.x_init:
                ax.plot3D([i.x, i.parent.x], [i.y, i.parent.y], [i.z, i.parent.z], "blue")

    def Draw_path(self, path:list):
        """draw result path on plot

        Args:
            path (list): list of node obtain from result Get Path function
        """

        for i in path:
            if i is not self.x_init:
                ax.plot3D([i.x, i.parent.x], [i.y, i.parent.y], [i.z, i.parent.z], "r", linewidth=2.5)

    def start_planning(self):
        """start planning loop
        """
        while True:
            # start record sampling time
            time_sampling_start = time.time()
            while True:
                # create random node by start bias sampling
                x_rand = self.Sampling()
                # update number of iteration
                self.total_iter += 1
                # find the nearest node to sampling
                x_nearest = self.Nearest(x_rand)
                # create new node in the direction of random and nearest to nearest node
                x_new = self.Steer(x_rand, x_nearest)
                # check whether to add new node to tree or not, if yes then add and breeak out of sampling loop, if not then continue sampling loop
                b = self.New_Check(x_new)
                if b == True :
                    break
                # stop if the sampling iteration reach maximum
                if self.total_iter == self.maxiteration:
                    break
            # stop record sampling time
            time_sampling_end = time.time()
            # determine sampling time elapsed
            self.sampling_elapsed += time_sampling_end - time_sampling_start
            # stop the entire planner if iteration reach maximum
            if self.total_iter == self.maxiteration:
                break
            # update sample taken number
            self.sample_taken += 1
            print("==>> self.sample_taken: ", self.sample_taken)

            # start record addparent time
            time_addparent_start = time.time()
            # create xnew node with xnearest as its parent
            x_new = self.Add_Parent(x_new, x_nearest)
            time_addparent_end = time.time()
            # determine addparent time elapsed
            self.addparent_elapsed += (time_addparent_end - time_addparent_start)
            # add xnew to rrt tree nodes
            self.nodes.append(x_new)

            # start record rewire time
            time_rewire_start = time.time()
            # start rewire tree
            self.Rewire(x_new)
            # stop record rewire time
            time_rewire_end = time.time()
            # determine rewire time elapsed
            self.rewire_elapsed += (time_rewire_end - time_rewire_start)

            # record graph cost data
            self.Graph_sample_num += 1
            if self.Graph_sample_num%100 == 0:
                Graph_cost = self.Cost_Graph()
                self.Graph_data = np.append(self.Graph_data,np.array([[self.Graph_sample_num, Graph_cost]]), axis = 0)
    
        # record end of planner loop
        self.e = time.time()

    def print_time(self):
        print("Total time : ", self.e - self.s,"second")
        print("Sampling time : ", self.sampling_elapsed,"second", (self.sampling_elapsed*100)/(self.e-self.s),"%")
        print("Add_Parent time : ", self.addparent_elapsed,"second", (self.addparent_elapsed*100)/(self.e-self.s),"%")
        print("Rewire time : ", self.rewire_elapsed,"second", (self.rewire_elapsed*100)/(self.e-self.s),"%")
        print("Total_iteration = ", self.total_iter)
        print("Cost : ", self.x_goal.cost)

 
if __name__=="__main__":
    from map.taskmap_img_format import map_3d_empty
    from util.extract_path_class import extract_path_class_3d
    np.random.seed(0)


    # SECTION - Experiment 1
    filter_size = 0  # 1 = 3x3, 2 = 5x5, 3 = 7x7
    classify = False
    map = map_3d_empty()
    x_init = np.array([0, 0, 0]).reshape(3,1)
    x_goal = np.array([40, 10, 30]).reshape(3,1)


    # SECTION - Experiment 2
    # filter_size = 0  # 1 = 3x3, 2 = 5x5, 3 = 7x7
    # classify = False
    # map = np.load('./map/mapdata/config_space_data_3d/config3D.npy')
    # x_init = np.array([0, 0, 0]).reshape(3,1)
    # x_goal = np.array([40, 10, 30]).reshape(3,1)


    # SECTION - planner 
    distance_weight = 0.5
    obstacle_weight = 0.5
    rrt = rrt_star(map, x_init, x_goal, distance_weight, obstacle_weight, maxiteration=1000)
    rrt.start_planning()


    # SECTION - result
    path = rrt.Get_Path()
    pathx, pathy, pathz = extract_path_class_3d(path)
    rrt.print_time()
    rrt.Draw_tree()
    rrt.Draw_path(path)
    plt.show()
""" Path Planning for Planar RR with RRT at runtime
"""

import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import matplotlib.pyplot as plt
import numpy as np

from collision_check_geometry.collision_class import ObjLine2D, intersect_line_v_rectangle


class Node:

    def __init__(self, x, y, parent=None) -> None:
        self.x = x
        self.y = y
        self.parent = parent


class RuntimeRRTBase():

    def __init__(self, robot, taskMapObs, xStart, xGoal, eta=0.3, maxIteration=1000) -> None:
        # robot and workspace
        self.robot = robot
        self.taskMapObs = taskMapObs
        self.xMinRange = -np.pi
        self.xMaxRange = np.pi
        self.yMinRange = -np.pi
        self.yMaxRange = np.pi
        self.probabilityGoalBias = 0.2
        self.xStart = Node(xStart[0, 0], xStart[1, 0])
        self.xGoal = Node(xGoal[0, 0], xGoal[1, 0])

        # properties of planner
        self.maxIteration = maxIteration
        self.eta = eta
        self.treeVertex = [self.xStart]
        self.inGoal = False

    def planning(self):
        for itera in range(self.maxIteration):
            print(itera)
            if self.inGoal:
                xRand = self.cir_sampling()
            else:
                xRand = self.bias_sampling()

            xNearest = self.nearest_node(xRand)
            xNew = self.steer(xNearest, xRand)
            xNew.parent = xNearest
            if self.is_config_in_collision(xNew) or self.is_connect_config_possible(xNearest, xNew):
                continue
            else:
                self.treeVertex.append(xNew)
                if self.ingoal_region(xNew):
                    self.inGoal = True

    def search_path(self):
        xNearToGoal = self.nearest_node(self.xGoal)
        self.xGoal.parent = xNearToGoal
        path = [self.xGoal]
        currentNode = self.xGoal

        while currentNode != self.xStart:
            currentNode = currentNode.parent
            path.append(currentNode)

        path.reverse()

        return path

    def uni_sampling(self):
        x = np.random.uniform(low=self.xMinRange, high=self.xMaxRange)
        y = np.random.uniform(low=self.yMinRange, high=self.yMaxRange)
        xRand = Node(x, y)

        return xRand
    
    def bias_sampling(self):
        if np.random.uniform(low=0, high=1.0) < self.probabilityGoalBias:
            xRand = Node(self.xGoal.x, self.xGoal.y)
        else:
            x = np.random.uniform(low=self.xMinRange, high=self.xMaxRange)
            y = np.random.uniform(low=self.yMinRange, high=self.yMaxRange)
            xRand = Node(x, y)
        return xRand

    def cir_sampling(self):
        r = self.eta
        theta = np.random.uniform(low=-np.pi, high=np.pi)
        x = r*np.cos(theta) + self.xGoal.x
        y = r*np.sin(theta) + self.xGoal.y
        xRand = Node(x, y)
        return xRand
    
    def nearest_node(self, xRand):
        vertexList = []

        for eachVertex in self.treeVertex:
            distX = xRand.x - eachVertex.x
            distY = xRand.y - eachVertex.y
            dist = np.linalg.norm([distX, distY])
            vertexList.append(dist)

        minIndex = np.argmin(vertexList)
        xNear = self.treeVertex[minIndex]

        return xNear

    def ingoal_region(self, xNew):
        if np.linalg.norm([self.xGoal.x - xNew.x, self.xGoal.y - xNew.y]) <= self.eta:
            return True
        else:
            return False
        
    def steer(self, xNearest, xRand):
        distX = xRand.x - xNearest.x
        distY = xRand.y - xNearest.y
        dist = np.linalg.norm([distX, distY])

        if dist <= self.eta:
            xNew = xRand
        else:
            direction = np.arctan2(distY, distX)
            newX = self.eta * np.cos(direction) + xNearest.x
            newY = self.eta * np.sin(direction) + xNearest.y
            xNew = Node(newX, newY)
        return xNew

    def is_config_in_collision(self, xNew):
        theta = np.array([xNew.x, xNew.y]).reshape(2, 1)
        linkPose = self.robot.forward_kinematic(theta, return_link_pos=True)
        linearm1 = ObjLine2D(linkPose[0][0], linkPose[0][1], linkPose[1][0], linkPose[1][1])
        linearm2 = ObjLine2D(linkPose[1][0], linkPose[1][1], linkPose[2][0], linkPose[2][1])
        for obs in self.taskMapObs:
            if intersect_line_v_rectangle(linearm1, obs):
                return True
            else:
                if intersect_line_v_rectangle(linearm2, obs):
                    return True
        return False

    def is_connect_config_possible(self, xNearest, xNew):  # check if connection between 2 node is possible
        distX = xNew.x - xNearest.x
        distY = xNew.y - xNearest.y
        desiredStep = 10
        rateX = distX / desiredStep
        rateY = distY / desiredStep
        for i in range(1, desiredStep - 1):
            newX = xNearest.x + (rateX * i)
            newY = xNearest.y + (rateY * i)
            xNew = Node(newX, newY)
            if self.is_config_in_collision(xNew):
                return True
        return False


if __name__ == "__main__":
    np.random.seed(9)
    from robot.planar_rr import PlanarRR
    from map.taskmap_geo_format import task_rectangle_obs_1
    from util.extract_path_class import extract_path_class_2d
    from planner.planner_util.tree import plot_tree

    robot = PlanarRR()
    taskMapObs = task_rectangle_obs_1()

    xStart = np.array([0, 0]).reshape(2, 1)
    xGoal = np.array([np.pi/2, 0]).reshape(2, 1)

    robot.plot_arm(xStart, plt_basis=True)
    robot.plot_arm(xGoal)
    for obs in taskMapObs:
        obs.plot()
    plt.show()

    planner = RuntimeRRTBase(robot, taskMapObs, xStart, xGoal, eta=0.3, maxIteration=500)
    planner.planning()
    path = planner.search_path()

    pathx, pathy = extract_path_class_2d(path)
    print("==>> pathx: \n", pathx)
    print("==>> pathy: \n", pathy)

    plt.axes().set_aspect('equal')
    plt.axvline(x=0, c="green")
    plt.axhline(y=0, c="green")
    obs_list = task_rectangle_obs_1()
    for obs in obs_list:
        obs.plot()
    for i in range(len(path)):
        robot.plot_arm(np.array([[pathx[i]], [pathy[i]]]))
        plt.pause(0.1)
    plt.show()

    plot_tree(planner.treeVertex, path)
    plt.show()
""" Path Planning for Planar RRR with Informed RRT star at runtime
"""

import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import matplotlib.pyplot as plt
import numpy as np

from collision_check_geometry.collision_class import ObjLine2D, intersect_line_v_rectangle


class Node:

    def __init__(self, x, y, z, p, q, r, parent=None, cost=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.p = p
        self.q = q
        self.r = r
        self.parent = parent
        self.cost = cost


class RuntimeRRTStar():

    def __init__(self, robot, taskMapObs, xStart, xGoal, eta=0.3, maxIteration=1000) -> None:
        # robot and workspace
        self.robot = robot
        self.taskMapObs = taskMapObs

        self.xMinRange = -np.pi/2
        self.xMaxRange = np.pi/2
        self.yMinRange = -np.pi/2
        self.yMaxRange = np.pi/2
        self.zMinRange = -np.pi/2
        self.zMaxRange = np.pi/2
        self.pMinRange = -np.pi/2
        self.pMaxRange = np.pi/2
        self.qMinRange = -np.pi/2
        self.qMaxRange = np.pi/2
        self.rMinRange = -np.pi/2
        self.rMaxRange = np.pi/2

        self.probabilityGoalBias = 0.2
        self.xStart = Node(xStart[0, 0], xStart[1, 0], xStart[2, 0], xStart[3, 0], xStart[4, 0], xStart[5, 0])
        self.xGoal = Node(xGoal[0, 0], xGoal[1, 0], xGoal[2, 0], xGoal[3, 0], xGoal[4, 0], xGoal[5, 0])

        # properties of planner
        self.maxIteration = maxIteration
        self.eta = eta
        self.treeVertex = [self.xStart]
        self.XSoln = []


    def planning(self):
        cBest = np.inf
        for itera in range(self.maxIteration):
            print(itera)
            for xSoln in self.XSoln:
                cBest = xSoln.parent.cost + self.cost_line(xSoln.parent, xSoln) + self.cost_line(xSoln, self.xGoal)
                if xSoln.parent.cost + self.cost_line(xSoln.parent, xSoln) + self.cost_line(xSoln, self.xGoal) < cBest:
                    cBest = xSoln.parent.cost + self.cost_line(xSoln.parent, xSoln) + self.cost_line(xSoln, self.xGoal)

            xRand = self.sampling(self.xStart, self.xGoal, cBest)
            # xRand = self.uni_sampling()
            xNearest = self.nearest_node(xRand)
            xNew = self.steer(xNearest, xRand)
            xNew.parent = xNearest
            xNew.cost = xNew.parent.cost + self.cost_line(xNew, xNew.parent)
            if self.is_config_in_collision(xNew) or self.is_connect_config_possible(xNew.parent, xNew):
                continue
            else:
                XNear = self.near(xNew, self.eta)
                xMin = xNew.parent
                cMin = xMin.cost + self.cost_line(xMin, xNew)
                for xNear in XNear:
                    if self.is_connect_config_possible(xNear, xNew):
                        continue

                    cNew = xNear.cost + self.cost_line(xNear, xNew)
                    if cNew < cMin:
                        xMin = xNear
                        cMin = cNew

                xNew.parent = xMin
                xNew.cost = cMin
                self.treeVertex.append(xNew)

                for xNear in XNear:
                    if self.is_connect_config_possible(xNear, xNew):
                        continue
                    cNear = xNear.cost
                    cNew = xNew.cost + self.cost_line(xNew, xNear)
                    if cNew < cNear:
                        xNear.parent = xNew
                        xNear.cost = xNew.cost + self.cost_line(xNew, xNear)

                # in goal region
                if self.ingoal_region(xNew):
                    print("In Goal Config")
                    self.XSoln.append(xNew)

    def search_path(self):
        for xBest in self.XSoln:
            if self.is_connect_config_possible(xBest, self.xGoal):
                continue
            self.xGoal.parent = xBest

            path = [self.xGoal]
            currentNode = self.xGoal
            while currentNode != self.xStart:
                currentNode = currentNode.parent
                path.append(currentNode)
            path.reverse()

            bestPath = path
            cost = sum(i.cost for i in path)
            if cost < sum(j.cost for j in bestPath):
                bestPath = path

        return bestPath

    def sampling(self, xStart, xGoal, cMax):
        if cMax < np.inf:
            cMin = self.cost_line(xStart, xGoal)
            xCenter = np.array([(xStart.x + xGoal.x) / 2,
                                (xStart.y + xGoal.y) / 2,
                                (xStart.z + xGoal.z) / 2,
                                (xStart.p + xGoal.p) / 2,
                                (xStart.q + xGoal.q) / 2,
                                (xStart.r + xGoal.r) / 2,
                                                     0.0]).reshape(7, 1)

            L, C = self.rotation_to_world(xStart, xGoal, cMax, cMin)

            while True:
                xBall = self.unit_ball_sampling()
                xRand = (C@L@xBall) + xCenter
                xRand = Node(xRand[0, 0], xRand[1, 0], xRand[2, 0], xRand[3, 0], xRand[4, 0], xRand[5, 0])
                
                in_range = [(self.xMinRange < xRand.x < self.xMaxRange),
                            (self.yMinRange < xRand.y < self.yMaxRange),
                            (self.zMinRange < xRand.z < self.zMaxRange), 
                            (self.pMinRange < xRand.p < self.pMaxRange),
                            (self.qMinRange < xRand.q < self.qMaxRange),
                            (self.rMinRange < xRand.r < self.rMaxRange)]
                if all(in_range):
                    break
        else:
            # xRand = self.uni_sampling()
            xRand = self.bias_sampling()
        return xRand

    def unit_ball_sampling(self):
        r = np.random.uniform(low=0, high=1)
        theta = np.random.uniform(low=0, high=2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.array([x, y, 0.0, 0.0, 0.0, 0.0, 0.0]).reshape(7, 1)
    
    def uni_sampling(self):
        x = np.random.uniform(low=self.xMinRange, high=self.xMaxRange)
        y = np.random.uniform(low=self.yMinRange, high=self.yMaxRange)
        z = np.random.uniform(low=self.zMinRange, high=self.zMaxRange)
        p = np.random.uniform(low=self.pMinRange, high=self.pMaxRange)
        q = np.random.uniform(low=self.qMinRange, high=self.qMaxRange)
        r = np.random.uniform(low=self.rMinRange, high=self.rMaxRange)
        xRand = Node(x, y, z, p, q, r)
        return xRand
    
    def bias_sampling(self):
        if np.random.uniform(low=0, high=1.0) < self.probabilityGoalBias:
            xRand = Node(self.xGoal.x, self.xGoal.y, self.xGoal.z, self.xGoal.p, self.xGoal.q, self.xGoal.r)
        else:
            xRand = self.uni_sampling()
        return xRand

    def ingoal_region(self, xNew):
        if np.linalg.norm([self.xGoal.x - xNew.x,
                           self.xGoal.y - xNew.y,
                           self.xGoal.z - xNew.z,
                           self.xGoal.p - xNew.p,
                           self.xGoal.q - xNew.q,
                           self.xGoal.r - xNew.r]) <= self.eta:
            return True
        else:
            return False

    def nearest_node(self, xRand):
        vertexList = []

        for eachVertex in self.treeVertex:
            distX = xRand.x - eachVertex.x
            distY = xRand.y - eachVertex.y
            distZ = xRand.z - eachVertex.z
            distP = xRand.p - eachVertex.p
            distQ = xRand.q - eachVertex.q
            distR = xRand.r - eachVertex.r
            dist = np.linalg.norm([distX, distY, distZ, distP, distQ, distR])
            vertexList.append(dist)

        minIndex = np.argmin(vertexList)
        xNear = self.treeVertex[minIndex]

        return xNear

    def steer(self, xNearest, xRand):
        distX = xRand.x - xNearest.x
        distY = xRand.y - xNearest.y
        distZ = xRand.z - xNearest.z
        distP = xRand.p - xNearest.p
        distQ = xRand.q - xNearest.q
        distR = xRand.r - xNearest.r
        dist = np.linalg.norm([distX, distY, distZ, distP, distQ, distR])

        if dist <= self.eta:
            xNew = xRand
        else:
            newX = self.eta * distX + xNearest.x
            newY = self.eta * distY + xNearest.y
            newZ = self.eta * distZ + xNearest.z
            newP = self.eta * distP + xNearest.p
            newQ = self.eta * distQ + xNearest.q
            newR = self.eta * distR + xNearest.r
            xNew = Node(newX, newY, newZ, newP, newQ, newR)
        return xNew

    def near(self, xNew, minStep):
        neighbor = []
        for index, vertex in enumerate(self.treeVertex):
            dist = np.linalg.norm([(xNew.x - vertex.x),
                                   (xNew.y - vertex.y),
                                   (xNew.z - vertex.z),
                                   (xNew.p - vertex.p),
                                   (xNew.q - vertex.q),
                                   (xNew.r - vertex.r)])
            if dist <= minStep:
                neighbor.append(index)
        return [self.treeVertex[i] for i in neighbor]
    
    def cost_line(self, xStart, xEnd):
        return np.linalg.norm([(xStart.x - xEnd.x),
                               (xStart.y - xEnd.y),
                               (xStart.z - xEnd.z),
                               (xStart.p - xEnd.p),
                               (xStart.q - xEnd.q),
                               (xStart.r - xEnd.r)])

    def rotation_to_world(self, xStart, xGoal, cMax, cMin):
        r1 = cMax / 2
        r2to7 = np.sqrt(cMax**2 - cMin**2) / 2
        L = np.diag([r1, r2to7, r2to7, r2to7, r2to7, r2to7, r2to7])
        a1 = np.array([[(xGoal.x - xStart.x) / cMin],
                       [(xGoal.y - xStart.y) / cMin],
                       [(xGoal.z - xStart.z) / cMin],
                       [(xGoal.p - xStart.p) / cMin],
                       [(xGoal.q - xStart.q) / cMin],
                       [(xGoal.r - xStart.r) / cMin],
                       [                        0.0]])
        I1 = np.array([[1.0], [0.0], [0.0], [0.0], [0.0], [0.0], [0.0]])
        M = a1 @ I1.T
        U, _, V_T = np.linalg.svd(M, True, True)
        C = U @ np.diag([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, np.linalg.det(U) * np.linalg.det(V_T.T)]) @ V_T
        return L,C
    
    def is_config_in_collision(self, xNew):
        # theta = np.array([xNew.x, xNew.y, xNew.z]).reshape(3, 1)
        # linkPose = self.robot.forward_kinematic(theta, return_link_pos=True)
        # linkPose = robot.forward_kinematic(theta, return_link_pos=True)
        # linearm1 = ObjLine2D(linkPose[0][0], linkPose[0][1], linkPose[1][0], linkPose[1][1])
        # linearm2 = ObjLine2D(linkPose[1][0], linkPose[1][1], linkPose[2][0], linkPose[2][1])
        # linearm3 = ObjLine2D(linkPose[2][0], linkPose[2][1], linkPose[3][0], linkPose[3][1])

        # for obs in self.taskMapObs:
        #     if intersect_line_v_rectangle(linearm1, obs):
        #         return True
        #     else:
        #         if intersect_line_v_rectangle(linearm2, obs):
        #             return True
        #         else:
        #             if intersect_line_v_rectangle(linearm3, obs):
        #                 return True
        return False

    def is_connect_config_possible(self, xNearest, xNew):  # check if connection between 2 node is possible
        # distX = xNew.x - xNearest.x
        # distY = xNew.y - xNearest.y
        # distZ = xNew.z - xNearest.z
        # desiredStep = 10
        # rateX = distX / desiredStep
        # rateY = distY / desiredStep
        # rateZ = distZ / desiredStep
        # for i in range(1, desiredStep - 1):
        #     newX = xNearest.x + (rateX * i)
        #     newY = xNearest.y + (rateY * i)
        #     newZ = xNearest.z + (rateZ * i)
        #     xNew = Node(newX, newY, newZ)
        #     if self.is_config_in_collision(xNew):
        #         return True
        return False


if __name__ == "__main__":
    np.random.seed(9)
    from robot.planar_rrr import PlanarRRR
    from planner_util.extract_path_class import extract_path_class_6d

    robot = PlanarRRR()

    thetaGoal = np.array([1,0,0,0,0,0]).reshape(6,1)
    thetaInit = np.array([0,0,0,0,0,0]).reshape(6,1)
    obsList = []

    planner = RuntimeRRTStar(robot, obsList, thetaInit, thetaGoal, eta=0.3, maxIteration=1000)
    planner.planning()
    path = planner.search_path()
    path_x, path_y, path_z, path_p, path_q, path_r = extract_path_class_6d(path)
    print(f"==>> path_x: \n{path_x}")
    print(f"==>> path_y: \n{path_y}")
    print(f"==>> path_z: \n{path_z}")
    print(f"==>> path_p: \n{path_p}")
    print(f"==>> path_q: \n{path_q}")
    print(f"==>> path_r: \n{path_r}")
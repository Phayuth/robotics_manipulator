import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

from planner_dev.rrt_component import Node, RRTComponent


class RRTConnectLocalOpt(RRTComponent):

    def __init__(self, xStart, xApp, xGoal, eta, subEta, maxIteration, numDoF, envChoice, nearGoalRadius, rewireRadius, terminationConditionID, print_debug) -> None:
        super().__init__(eta=eta,
                         subEta=subEta,
                         maxIteration=maxIteration,
                         numDoF=numDoF,
                         envChoice=envChoice,
                         nearGoalRadius=nearGoalRadius,
                         rewireRadius=rewireRadius,
                         terminationConditionID=terminationConditionID,
                         print_debug=print_debug)        
        # start, aux, goal node
        self.xStart = Node(xStart)
        self.xGoal = Node(xGoal)
        self.xApp = Node(xApp)

        # planner properties
        self.treeVertexStart = [self.xStart]
        self.treeVertexGoal = [self.xApp]
        self.distGoalToApp = self.distance_between_config(self.xGoal, self.xApp)
        self.treeSwapFlag = True

        # local sampling properties
        self.anchorPath = None
        self.localPath = None
        self.numSegSamplingNode = None

        # solutions
        self.connectNodeStart = None
        self.connectNodeGoal = None
        self.XInGoalRegion = []

    @RRTComponent.catch_key_interrupt
    def start(self):
        for itera in range(self.maxIteration):
            if self.treeSwapFlag is True:
                Ta = self.treeVertexStart
                Tb = self.treeVertexGoal
            elif self.treeSwapFlag is False:
                Ta = self.treeVertexGoal
                Tb = self.treeVertexStart

            xRand = self.uni_sampling()
            xNearest = self.nearest_node(Ta, xRand)
            xNew = self.steer(xNearest, xRand, self.eta)

            if not self.is_collision_and_in_goal_region(xNearest, xNew, self.xGoal, self.distGoalToApp):
                xNew.parent = xNearest
                xNew.cost = xNew.parent.cost + self.cost_line(xNew, xNew.parent)
                xNearest.child.append(xNew)
                Ta.append(xNew)
                xNearestPrime = self.nearest_node(Tb, xNew)
                xNewPrime = self.steer(xNearestPrime, xNew, self.eta)

                if not self.is_collision_and_in_goal_region(xNearestPrime, xNewPrime, self.xGoal, self.distGoalToApp):
                    xNewPrime.parent = xNearestPrime
                    xNewPrime.cost = xNewPrime.parent.cost + self.cost_line(xNewPrime, xNewPrime.parent)
                    xNearestPrime.child.append(xNewPrime)
                    Tb.append(xNewPrime)

                    while True:
                        xNewPPrime = self.steer(xNewPrime, xNew, self.eta)

                        if self.is_collision_and_in_goal_region(xNewPrime, xNewPPrime, self.xGoal, self.distGoalToApp):
                            break

                        if self.distance_between_config(xNewPPrime, xNew) < 1e-3:
                            if self.treeSwapFlag is True:
                                self.connectNodeGoal = xNewPrime
                                self.connectNodeStart = xNew
                            elif self.treeSwapFlag is False:
                                self.connectNodeGoal = xNew
                                self.connectNodeStart = xNewPrime
                            break

                        else:
                            xNewPPrime.parent = xNewPrime
                            xNewPPrime.cost = xNewPPrime.parent.cost + self.cost_line(xNewPPrime, xNewPPrime.parent)
                            xNewPrime.child.append(xNewPPrime)
                            Tb.append(xNewPPrime)
                            xNewPrime = xNewPPrime

                if self.connectNodeGoal is not None and self.connectNodeStart is not None:
                    break

                self.tree_swap_flag()

        # merge tree
        self.reparent_merge_tree(xTobeParent=self.connectNodeStart, xNow=self.connectNodeGoal, treeToAddTo=self.treeVertexStart)

        self.XInGoalRegion.append(self.xApp.parent)  # we know xApp parent is the best node to connect to xApp right now, in case if we cannot find any other, we still have it as parent
        self.localPath = self.search_backtrack_single_directional_path(self.xApp.parent, self.xApp)
        self.numSegSamplingNode = len(self.localPath) - 1
        self.anchorPath = self.segment_interpolation_between_config(self.xStart, self.xApp, self.numSegSamplingNode, includexStart=True)

        for remainItera in range(self.maxIteration - itera):
            _ = self.cbest_single_tree(self.XInGoalRegion, self.xApp, itera+remainItera, self.print_debug)

            xRand = self.local_path_sampling(self.anchorPath, self.localPath, self.numSegSamplingNode)
            xNearest, vertexDistList = self.nearest_node(self.treeVertexStart, xRand, returnDistList=True)
            xNew, xNewIsxRand = self.steer(xNearest, xRand, self.eta, returnxNewIsxRand=True)
            if self.is_collision_and_in_goal_region(xNearest, xNew, self.xGoal, self.distGoalToApp):
                continue
            xNew.parent = xNearest
            xNew.cost = xNew.parent.cost + self.cost_line(xNew, xNew.parent)
            xNearest.child.append(xNew)

            self.star_optimizer(self.treeVertexStart, xNew, self.rewireRadius, xNewIsxRand, vertexDistList)

            # in approach region
            if self.is_config_in_region_of_config(xNew, self.xApp, radius=self.nearGoalRadius):
                self.XInGoalRegion.append(xNew)

    def plot_tree(self, path, ax):
        self.plot_2d_obstacle(ax)
        self.plot_2d_single_tree(self.treeVertexStart, ax)
        self.plot_2d_state_configuration(self.xStart, self.xApp, self.xGoal, ax)
        self.plot_2d_path(path, ax)
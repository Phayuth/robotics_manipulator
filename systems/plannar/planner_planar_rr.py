import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
np.random.seed(9)

# planner
from planner.sampling_based.rrt_plannerapi import RRTPlannerAPI

# environment
from simulator.sim_planar_rr import RobotArm2DSimulator

# joint value
from datasave.joint_value.experiment_paper import Experiment2DArm

sim = RobotArm2DSimulator()

plannarConfigDualTreea = {
    "planner": 25,
    "eta": 0.3,
    "subEta": 0.05,
    "maxIteration": 10000,
    "simulator": sim,
    "nearGoalRadius": None,
    "rewireRadius": None,
    "endIterationID": 1,
    "printDebug": True,
    "localOptEnable": False
}


q = Experiment2DArm.PoseSingle()
# q = Experiment2DArm.PoseMulti()
xStart = q.xStart
xApp = q.xApp
xGoal = q.xGoal

pm = RRTPlannerAPI.init_normal(xStart, xApp, xGoal, plannarConfigDualTreea)
patha = pm.begin_planner()

pm.plot_2d_config_tree()
pm.plot_performance()
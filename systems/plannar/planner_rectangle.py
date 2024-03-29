import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
np.random.seed(9)
import matplotlib.pyplot as plt

# planner
from planner.planner_manipulator import PlannerManipulator
from planner.sampling_based.rrt_plotter import RRTPlotter

# environment
from simulator.sim_rectangle import TaskSpace2DSimulator

# joint value
from datasave.joint_value.experiment_paper import ICRABarnMap

sim = TaskSpace2DSimulator()

plannarConfigSingleTree = {
    "planner": 5,
    "eta": 0.3,
    "subEta": 0.05,
    "maxIteration": 2000,
    "simulator": sim,
    "nearGoalRadius": 0.3,
    "rewireRadius": None,
    "endIterationID": 1,
    "printDebug": True,
    "localOptEnable": True
}


q = ICRABarnMap.PoseSingle()
# q = ICRABarnMap.PoseMulti3()
xStart = q.xStart
xApp = q.xApp
xGoal = q.xGoal

pa = PlannerManipulator(xStart, xApp, xGoal, plannarConfigSingleTree)

patha = pa.planning()
fig, ax = plt.subplots()
ax.set_axis_off()
fig.set_size_inches(w=3.40067, h=3.40067)
fig.tight_layout()
plt.xlim((-np.pi, np.pi))
plt.ylim((-np.pi, np.pi))
# RRTPlotter.plot_2d_config_single_tree(pa.planner, patha, ax)
RRTPlotter.plot_2d_config_dual_tree(pa.planner, patha, ax)

plt.show()

fig, ax = plt.subplots()
RRTPlotter.plot_performance(pa.planner.perfMatrix, ax)
plt.show()
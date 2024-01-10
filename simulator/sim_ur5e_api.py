import sys
import os

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))
sys.path.append("/home/yuth/coppelia/programming/zmqRemoteApi/clients/python")

import numpy as np
import time
from zmqRemoteApi import RemoteAPIClient


class UR5eArmCoppeliaSimAPI:

    def __init__(self, robotChoice="V") -> None:
        # robot choice
        self.robotChoice = {"V": "UR5e_virtual",
                            "D": "UR5e_dynamic",
                            "UR5V": "UR5_virtual",
                            "UR5D": "UR5_dynamic"}
        self.robot = self.robotChoice[robotChoice]

        # limit joint and dof
        self.configLimit = [[-np.pi, np.pi],
                            [-np.pi, np.pi],
                            [-np.pi, np.pi],
                            [-np.pi, np.pi],
                            [-np.pi, np.pi],
                            [-np.pi, np.pi]]
        self.configDoF = len(self.configLimit)

        # coppeliasim
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject('sim')
        self.client.setStepping(True)

        self.robotHeadNames = [self.robot, "UR5e_Goal", "UR5e_Aux", "UR5e_Start"]
        self.jointNames = ['/shoulder_pan_joint',
                           '/shoulder_pan_joint/shoulder_link_resp/shoulder_lift_joint',
                           '/shoulder_pan_joint/shoulder_link_resp/shoulder_lift_joint/upper_arm_link_resp/elbow_joint',
                           '/shoulder_pan_joint/shoulder_link_resp/shoulder_lift_joint/upper_arm_link_resp/elbow_joint/forearm_link_resp/wrist_1_joint',
                           '/shoulder_pan_joint/shoulder_link_resp/shoulder_lift_joint/upper_arm_link_resp/elbow_joint/forearm_link_resp/wrist_1_joint/wrist_1_link_resp/wrist_2_joint',
                           '/shoulder_pan_joint/shoulder_link_resp/shoulder_lift_joint/upper_arm_link_resp/elbow_joint/forearm_link_resp/wrist_1_joint/wrist_1_link_resp/wrist_2_joint/wrist_2_link_resp/wrist_3_joint']

        # arm joint handle
        self.jointHandleList = [self.sim.getObject('/' + self.robotHeadNames[0] + jointName) for jointName in self.jointNames]
        self.jointGoalHandleList = [self.sim.getObject('/' + self.robotHeadNames[1] + jointName) for jointName in self.jointNames]
        self.jointAuxHandleList = [self.sim.getObject('/' + self.robotHeadNames[2] + jointName) for jointName in self.jointNames]
        self.jointStartHandleList = [self.sim.getObject('/' + self.robotHeadNames[3] + jointName) for jointName in self.jointNames]

        # arm collision handle
        self.robotBase = self.sim.getObject(f'/{self.robot}')
        self.collection = self.sim.createCollection(0)
        self.sim.addItemToCollection(self.collection, self.sim.handle_tree, self.robotBase, 0)

    def start_sim(self):
        self.sim.startSimulation()

    def stop_sim(self):
        self.sim.stopSimulation()

    def step_sim(self):
        self.client.step()

    def collision_check(self, jointValue):
        self.set_joint_value(jointValue)
        result, _ = self.sim.checkCollision(self.collection, self.sim.handle_all)
        if result == 1:
            return True
        else:
            return False

    def set_handle_joint_value(self, jointValue, jointHandle):
        if isinstance(jointValue, np.ndarray):
            for i in range(jointValue.shape[0]):
                self.sim.setJointPosition(jointHandle[i], jointValue[i, 0])
        else:
            for i in range(jointValue.config.shape[0]):
                self.sim.setJointPosition(jointHandle[i], jointValue.config[i, 0])

    def set_joint_value(self, jointValue):
        self.set_handle_joint_value(jointValue, self.jointHandleList)

    def set_goal_joint_value(self, jointValue):
        self.set_handle_joint_value(jointValue, self.jointGoalHandleList)

    def set_aux_joint_value(self, jointValue):
        self.set_handle_joint_value(jointValue, self.jointAuxHandleList)

    def set_start_joint_value(self, jointValue):
        self.set_handle_joint_value(jointValue, self.jointStartHandleList)

    def set_joint_target_value(self, jointValue):
        for i in range(jointValue.config.shape[0]):
            self.sim.setJointTargetPosition(self.jointHandleList[i], jointValue.config[i, 0])

    def play_back_path(self, path):
        self.start_sim()
        self.set_start_joint_value(path[0])
        self.set_goal_joint_value(path[-1])
        self.set_aux_joint_value(path[-2])
        for i in range(len(path)):
            self.set_joint_value(path[i])
            time.sleep(0.3)
            # triggers next simulation step
            # client.step()
        self.stop_sim()


if __name__ == "__main__":
    from datasave.joint_value.pre_record_value import SinglePose
    from datasave.joint_value.experiment_paper import URHarvesting

    # View State
    armState = UR5eArmCoppeliaSimAPI()
    # armState.start_sim()
    # jointV = np.array([0.0,0.0,0.0,0.0,0.0,0.0]).reshape(6,1)
    # armState.set_joint_value(jointV)
    # armState.set_goal_joint_value(jointV)
    # armState.set_aux_joint_value(jointV)
    # armState.set_start_joint_value(jointV)

    q = URHarvesting.PoseSingle1()
    qS = q.xStart
    qA = q.xApp
    qG = q.xGoal
    armState.set_goal_joint_value(qG)
    armState.set_aux_joint_value(qA)
    armState.set_start_joint_value(qS)
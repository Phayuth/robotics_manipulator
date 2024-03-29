import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

from spatial_geometry.spatial_transformation import RigidBodyTransformation as rbt

import numpy as np
from icecream import ic


def ik_selectivly_dls():
    e = np.array([1, 3, 5]).reshape(3, 1)
    ic(e)

    Jac = np.array([[3, 4, 5], [1, 3, 2], [3, 6, 1]])
    ic(Jac)

    U, D, VT = np.linalg.svd(Jac)
    V = VT.T
    ic(U)
    ic(D)
    ic(VT)
    ic(V)

    Alpha = U.T @ e
    ic(Alpha)

    N = np.sum(Jac, axis=0)
    ic(N)

    M = np.array([4, 6, 1])
    ic(M)

    vabs = np.abs(V)
    ic(vabs)

    # NdivM = N/M
    # ic(NdivM)

    # gamma = np.minimum(3, NdivM)
    # ic(gamma)


# ik_selectivly_dls()


import json

matrixsamples = np.random.uniform(0, 1, (4, 40)).tolist()
jointsamples = np.random.uniform(-np.pi, np.pi, (10, 6)).tolist()
matrix = np.random.uniform(0, 1, (4, 4)).tolist()
pose = np.random.uniform(0, 1, (1, 7)).tolist()

data = {"Title":"Handeye Calibration Program",
        "Camera Mount Type": "Fixed",
        "Camera Frame": "Camera_color_optical_frame",
        "Object Frame": "calib_board",
        "Robot Base": "base",
        "End Effector Frame": "too0",
        "Matrix Dataset": matrixsamples,
        "Joint Dataset": jointsamples,
        "Result Transformation": "Camera_color_optical_frame to base",
        "Result Matrix": matrix,
        "Result Pose": pose}


with open("/home/yuth/jointsample.json", "w") as f:
    json.dump(data, f, indent=4)

with open("/home/yuth/jointsample.json", "r") as f:
    a = json.load(f)

print(a)
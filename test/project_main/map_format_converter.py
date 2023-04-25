""" Convert costmap from Image format to geometry format """

import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
from collision_check_geometry.collision_class import ObjRec


def mapimg2geo(map, minmax=[], free_space_value=1):
    size_x = map.shape[1]
    size_y = map.shape[0]

    if minmax:
        xval = np.linspace(minmax[0], minmax[1], size_x)
        yval = np.linspace(minmax[0], minmax[1], size_y)
    else:
        xval = np.linspace(-np.pi, np.pi, size_x)
        yval = np.linspace(-np.pi, np.pi, size_y)

    obj = [ObjRec(xval[i], yval[j], xval[i + 1] - xval[i], yval[j + 1] - yval[j], p=free_space_value) for i in range(len(xval) - 1) for j in range(len(yval) - 1) if map[j, i] != free_space_value]

    return obj


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from taskmap_img_format import map_2d_1, map_2d_2, pmap, bmap

    # SECTION - load map in image space
    map = bmap()
    plt.imshow(map)
    plt.show()

    # SECTION - convert from image to geometry format
    obj_list = mapimg2geo(map, minmax=[0, 10], free_space_value=0)
    for obs in obj_list:
        obs.plot()
    plt.show()
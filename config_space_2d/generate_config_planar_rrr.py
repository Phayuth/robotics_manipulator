import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import matplotlib.pyplot as plt
from collision_check_geometry import collision_class
from map.taskmap_geo_format import task_rectangle_obs_3, task_rectangle_obs_6
from robot.planar_rrr import planar_rrr
import numpy as np

def configuration_generate_plannar_rrr(robot, obs_list):

    grid_size = 75
    theta1 = np.linspace(-np.pi, np.pi, grid_size)
    theta2 = np.linspace(-np.pi, np.pi, grid_size)
    theta3 = np.linspace(-np.pi, np.pi, grid_size)

    grid_map = np.zeros((grid_size, grid_size, grid_size))

    for j in range(len(theta1)):
        for k in range(len(theta2)):
            for l in range(len(theta3)):
                print(f"at theta1 {theta1[j]} | at theta2 {theta2[k]} | at theta3 {theta3[l]}")
                theta = np.array([[theta1[j]],[theta2[k]],[theta3[l]]])
                link_pose = robot.forward_kinematic(theta, return_link_pos=True)
                linearm1 = collision_class.obj_line2d(link_pose[0][0], link_pose[0][1], link_pose[1][0], link_pose[1][1])
                linearm2 = collision_class.obj_line2d(link_pose[1][0], link_pose[1][1], link_pose[2][0], link_pose[2][1])
                linearm3 = collision_class.obj_line2d(link_pose[2][0], link_pose[2][1], link_pose[3][0], link_pose[3][1])

                col = []
                for i in obs_list:
                    col1 = collision_class.intersect_line_v_rectangle(linearm1, i)
                    col2 = collision_class.intersect_line_v_rectangle(linearm2, i)
                    col3 = collision_class.intersect_line_v_rectangle(linearm3, i)
                    col.extend((col1,col2,col3))

                if True in col:
                    grid_map[j,k,l] = 1

    return 1 - grid_map

def configuration_generate_plannar_rrr_first_2joints(robot, obs_list):
    
    grid_size = 75
    theta1 = np.linspace(-np.pi, np.pi, grid_size)
    theta2 = np.linspace(-np.pi, np.pi, grid_size)
    theta3 = np.pi

    grid_map = np.zeros((grid_size, grid_size, grid_size))

    for j in range(len(theta1)):
        for k in range(len(theta2)):
                print(f"at theta1 {theta1[j]} | at theta2 {theta2[k]}")
                theta = np.array([[theta1[j]],[theta2[k]],[theta3]])
                link_pose = robot.forward_kinematic(theta, return_link_pos=True)
                linearm1 = collision_class.obj_line2d(link_pose[0][0], link_pose[0][1], link_pose[1][0], link_pose[1][1])
                linearm2 = collision_class.obj_line2d(link_pose[1][0], link_pose[1][1], link_pose[2][0], link_pose[2][1])

                col = []
                for i in obs_list:
                    col1 = collision_class.intersect_line_v_rectangle(linearm1, i)
                    col2 = collision_class.intersect_line_v_rectangle(linearm2, i)
                    col.extend((col1,col2))

                if True in col:
                    grid_map[j,k] = 1

    return 1 - grid_map


if __name__=="__main__":
    r = planar_rrr()
    obs = task_rectangle_obs_6()
    map = configuration_generate_plannar_rrr(r, obs)
    # ax = plt.figure().add_subplot(projection='3d')
    # ax.voxels(map, edgecolor='k')
    # plt.show()

    # plt view of each index slice 3D into 2D image
    plt.imshow(map[0,:,:])
    plt.show()
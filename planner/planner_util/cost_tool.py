import os
import sys
wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

import numpy as np
from node_tool import node
from map.map_value_range import map_val


def distance(q_base, q_far):
    return np.linalg.norm([q_far.x - q_base.x, q_far.y - q_base.y])


def segmented_line(q_base, q_far, num_seg=10):
    x1 = q_base.x
    y1 = q_base.y
    x2 = q_far.x
    y2 = q_far.y

    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    segment_length = distance / (num_seg - 1)
    points = [q_base]
    for i in range(1, num_seg - 1):
        x = x1 + i * segment_length * (q_far.x - q_base.x)/distance
        y = y1 + i * segment_length * (q_far.y - q_base.y)/distance
        point = node(x, y)
        points.append(point)
    points.append(q_far)
    return points


def getcost(map, q, minmax_q = [[-np.pi, np.pi],[-np.pi, np.pi]], return_index_cost=False):

    # if minmax_q[0][0] < q.x < minmax_q[0][1] or minmax_q[1][0] < q.y < minmax_q[1][1]:
    
    cell_size_x = (minmax_q[0][1] - minmax_q[0][0])/map.shape[0]
    cell_size_y = (minmax_q[1][1] - minmax_q[1][0])/map.shape[1]

    ind_x = int(round(q.x/cell_size_x))
    ind_y = int(round(q.y/cell_size_y))

    if return_index_cost:
        return ind_x, ind_y, map[ind_y, ind_x]
    else:
        return map[ind_y, ind_x] # in img format row is y, column is x, spend weeks cause of this

def getc(map, q, return_index_cost=False):

    ind_x = int(round(map_val(q.x, -np.pi, np.pi, 0, map.shape[0])))
    ind_y = int(round(map_val(q.y, -np.pi, np.pi, 0, map.shape[1])))

    if return_index_cost:
        return ind_x, ind_y, map[ind_y, ind_x]
    else:
        return map[ind_y, ind_x] # in img format row is y, column is x, spend weeks cause of this


def setcost(map, q, cost, minmax_q = [[-np.pi, np.pi],[-np.pi, np.pi]]):
    cell_size_x = (minmax_q[0][1] - minmax_q[0][0])/map.shape[0]
    cell_size_y = (minmax_q[1][1] - minmax_q[1][0])/map.shape[1]

    ind_x = int(round(q.x/cell_size_x))
    ind_y = int(round(q.y/cell_size_y))

    map[ind_y, ind_x] = cost


# def obstacle_cost(map, start, end):
#     seg_length = 1
#     seg_point = int(np.ceil(distance(start, end) / seg_length))
#     value = 0
#     if seg_point > 1:
#         v = distance(start, end)/ (seg_point)
#         for i in range(seg_point + 1):
#             seg = np.array([start.x, start.y]) + i * v
#             seg = np.around(seg)
#             if 1 - map[int(seg[0]), int(seg[1])] == 1 :
#                 cost = 1e10
#                 return cost
#             else:
#                 value += 1 - map[int(seg[0]), int(seg[1])]
#         cost = value / (seg_point + 1)
#         return cost
#     else:
#         value = map[int(start.x), int(start.y)] + map[int(end.x), int(end.y)]
#         cost = value / 2
#         return cost


if __name__ == "__main__":
    from map.taskmap_img_format import map_2d_empty, map_2d_1
    import matplotlib.pyplot as plt


    # SECTION - obstacle cost
    map = map_2d_1()
    # q_start = node(5,5)
    # q_end = node(5,10)
    # cost = obstacle_cost(map, q_start, q_end)

    # plt.imshow(np.flip(map, 0), origin="lower")
    # plt.scatter([q_start.x, q_end.x], [q_start.y, q_end.y])
    # plt.plot([q_start.x, q_end.x], [q_start.y, q_end.y])
    # plt.show()


    # SECTION - segmented line
    # q_start = node(1,1)
    # q_end = node(6,8)
    # q_seg = segmented_line(q_start, q_end, num_seg=10)
    # for i in q_seg: plt.scatter(i.x, i.y)
    # plt.show()


    # SECTION - getcost
    # q = node(3.14,2)
    # cell = getcost(map, q, minmax_q = [[-np.pi, np.pi],[-np.pi, np.pi]], return_index_cost=True)
    # plt.imshow(map, origin="lower")
    # plt.scatter(cell[0], cell[1])
    # plt.title(f"cell index and value: {cell}, realgeo value: {q.x, q.y}, map shape: {map.shape}")
    # plt.show()


    # SECTION - getc
    q = node(0,0)
    cell = getc(map, q, return_index_cost=True)
    plt.imshow(map, origin="lower")
    plt.scatter(cell[0], cell[1])
    plt.title(f"cell index and value: {cell}, realgeo value: {q.x, q.y}, map shape: {map.shape}")
    plt.show()
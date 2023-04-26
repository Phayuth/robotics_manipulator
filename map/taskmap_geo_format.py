"""
Taskspace map in geometry format
----

"""

import os
import sys

wd = os.path.abspath(os.getcwd())
sys.path.append(str(wd))

from collision_check_geometry import collision_class


def task_rectangle_obs_1():
    rec1 = collision_class.ObjRec(x=2, y=2, h=2, w=2)
    rec2 = collision_class.ObjRec(x=-4, y=-0.2, h=6, w=3)
    list_obs = [rec1, rec2]
    return list_obs


def task_rectangle_obs_2():
    rec1 = collision_class.ObjRec(50, 50, h=3, w=3)
    rec2 = collision_class.ObjRec(40, 20, h=9, w=1)
    rec3 = collision_class.ObjRec(70, 90, h=5, w=2)
    list_obs = [rec1, rec2, rec3]
    return list_obs


def task_rectangle_obs_3():
    rec1 = collision_class.ObjRec(x=1, y=1, h=0.5, w=0.5)
    rec2 = collision_class.ObjRec(x=0, y=1.5, h=1, w=2)
    rec3 = collision_class.ObjRec(x=-2, y=1, h=1, w=1)
    rec4 = collision_class.ObjRec(x=-1, y=-1, h=0.8, w=4)
    list_obs = [rec1, rec2, rec3, rec4]
    return list_obs


def task_rectangle_obs_4():
    rec1 = collision_class.ObjRec(x=1.5, y=1.56, h=0.2, w=1)
    rec2 = collision_class.ObjRec(x=1.5, y=0.8, h=0.2, w=1)
    rec3 = collision_class.ObjRec(x=-4, y=-0.2, h=6, w=3)
    list_obs = [rec1, rec2, rec3]
    return list_obs


def task_rectangle_obs_5():
    rec1 = collision_class.ObjRec(x=1.5, y=2.3, h=0.2, w=1)
    rec2 = collision_class.ObjRec(x=1.5, y=1.8, h=0.2, w=1)
    list_obs = [rec1, rec2]
    return list_obs


def task_rectangle_obs_6():
    rec1 = collision_class.ObjRec(x=1.5, y=1.25, h=0.2, w=1)
    rec2 = collision_class.ObjRec(x=1.5, y=0.5, h=0.2, w=1)
    list_obs = [rec1, rec2]
    return list_obs


def task_rectangle_obs_7():
    # for my rrtbase
    rec1 = collision_class.ObjRec(x=1, y=1, h=1, w=2)
    rec2 = collision_class.ObjRec(x=5, y=1, h=1, w=2)
    rec3 = collision_class.ObjRec(x=1, y=5, h=1, w=1)
    rec4 = collision_class.ObjRec(x=5, y=5, h=0.8, w=4)
    list_obs = [rec1, rec2, rec3, rec4]
    return list_obs

def task_rectangle_obs_8():
    rec1 = collision_class.ObjRec(x=1.5, y=0.5, h=0.01, w=1)
    return [rec1]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.axes().set_aspect('equal')
    plt.axvline(x=0, c="green")
    plt.axhline(y=0, c="green")

    listTask = [task_rectangle_obs_1(),
                task_rectangle_obs_2(),
                task_rectangle_obs_3(),
                task_rectangle_obs_4(),
                task_rectangle_obs_5(),
                task_rectangle_obs_6(),
                task_rectangle_obs_7(),
                task_rectangle_obs_8()]
    
    for task in listTask:
        for obs in task:
            obs.plot()
    plt.show()
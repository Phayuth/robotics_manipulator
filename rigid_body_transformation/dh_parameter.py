import numpy as np

def dh_transformation(theta,alpha,d,a):
    R = np.array([[np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
                [  np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
                [              0,                np.sin(alpha),                np.cos(alpha),               d],
                [              0,                            0,                            0,               1]])
    return R
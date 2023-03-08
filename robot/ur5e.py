import numpy as np
import matplotlib.pyplot as plt
ax = plt.axes(projection='3d')

class ur5e:
    def __init__(self):
        # DH parameter is from this publication
        # https://www.researchgate.net/publication/347021253_Mathematical_Modelling_and_Simulation_of_Human-Robot_Collaboration
        self.a     = np.array([      [0], [-0.425], [-0.3922],       [0],        [0],      [0]])
        self.alpha = np.array([[np.pi/2],      [0],       [0], [np.pi/2], [-np.pi/2],      [0]])
        self.d     = np.array([ [0.1625],      [0],       [0],  [0.1333],   [0.0997], [0.0996]])

    def dh_transformation(self,theta,alpha,d,a):
        R = np.array([[np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
                      [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
                      [            0,                np.sin(alpha),                np.cos(alpha),               d],
                      [            0,                            0,                            0,               1]])
        return R

    def forward_kinematic(self,theta):

        A1 = self.dh_transformation(theta[0,0],self.alpha[0,0],self.d[0,0],self.a[0,0])
        A2 = self.dh_transformation(theta[1,0],self.alpha[1,0],self.d[1,0],self.a[1,0])
        A3 = self.dh_transformation(theta[2,0],self.alpha[2,0],self.d[2,0],self.a[2,0])
        A4 = self.dh_transformation(theta[3,0],self.alpha[3,0],self.d[3,0],self.a[3,0])
        A5 = self.dh_transformation(theta[4,0],self.alpha[4,0],self.d[4,0],self.a[4,0])
        A6 = self.dh_transformation(theta[5,0],self.alpha[5,0],self.d[5,0],self.a[5,0])

        T06 = A1 @ A2 @ A3 @ A4 @ A5 @ A6

        # https://www.daslhub.org/unlv/courses/me729-sp/week03/lecture/Note_02_Forward_Kinematics.pdf
        # https://robotics.stackexchange.com/questions/8516/getting-pitch-yaw-and-roll-from-rotation-matrix-in-dh-parameter
        # x - y - z sequence
        # tan(roll) = r32/r33
        # tan(pitch)= -r31/(sqrt(r32^2 + r33^2))
        # tan(yaw)  = r21/r11
        # np.arctan2(y, x)
        
        roll = np.arctan2(T06[2,1],T06[2,2])
        pitch= np.arctan2(-T06[2,0],np.sqrt(T06[2,1]*T06[2,1] + T06[2,2]*T06[2,2]))
        yaw  = np.arctan2(T06[1,0],T06[0,0])

        x_current = np.array([[T06[0, 3]],
                              [T06[1, 3]],
                              [T06[2, 3]],
                                   [roll],
                                  [pitch],
                                    [yaw]])

        return x_current

    def jacobian(self,theta):

        A1 = self.dh_transformation(theta[0,0],self.alpha[0,0],self.d[0,0],self.a[0,0])
        A2 = self.dh_transformation(theta[1,0],self.alpha[1,0],self.d[1,0],self.a[1,0])
        A3 = self.dh_transformation(theta[2,0],self.alpha[2,0],self.d[2,0],self.a[2,0])
        A4 = self.dh_transformation(theta[3,0],self.alpha[3,0],self.d[3,0],self.a[3,0])
        A5 = self.dh_transformation(theta[4,0],self.alpha[4,0],self.d[4,0],self.a[4,0])
        A6 = self.dh_transformation(theta[5,0],self.alpha[5,0],self.d[5,0],self.a[5,0])

        T01 = A1
        T02 = A1 @ A2
        T03 = A1 @ A2 @ A3
        T04 = A1 @ A2 @ A3 @ A4
        T05 = A1 @ A2 @ A3 @ A4 @ A5
        T06 = A1 @ A2 @ A3 @ A4 @ A5 @ A6

        Z0 = np.array([[0],
                       [0],
                       [1]])

        Z1 = np.array([[T01[0,2]],
                       [T01[1,2]],
                       [T01[2,2]]])

        Z2 = np.array([[T02[0,2]],
                       [T02[1,2]],
                       [T02[2,2]]])

        Z3 = np.array([[T03[0,2]],
                       [T03[1,2]],
                       [T03[2,2]]])

        Z4 = np.array([[T04[0,2]],
                       [T04[1,2]],
                       [T04[2,2]]])

        Z5 = np.array([[T05[0,2]],
                       [T05[1,2]],
                       [T05[2,2]]])

        O0 = np.array([[0],
                       [0],
                       [0]])

        O1 = np.array([[T01[3,0]],
                       [T01[3,1]],
                       [T01[3,2]]])

        O2 = np.array([[T02[3,0]],
                       [T02[3,1]],
                       [T02[3,2]]])

        O3 = np.array([[T03[3,0]],
                       [T03[3,1]],
                       [T03[3,2]]])

        O4 = np.array([[T04[3,0]],
                       [T04[3,1]],
                       [T04[3,2]]])

        O5 = np.array([[T05[3,0]],
                       [T05[3,1]],
                       [T05[3,2]]])

        O6 = np.array([[T06[3,0]],
                       [T06[3,1]],
                       [T06[3,2]]])

        Jv1 = np.transpose(np.cross(np.transpose(Z0),np.transpose(O6-O0))) 
        Jv2 = np.transpose(np.cross(np.transpose(Z1),np.transpose(O6-O1))) 
        Jv3 = np.transpose(np.cross(np.transpose(Z2),np.transpose(O6-O2))) 
        Jv4 = np.transpose(np.cross(np.transpose(Z3),np.transpose(O6-O3))) 
        Jv5 = np.transpose(np.cross(np.transpose(Z4),np.transpose(O6-O4))) 
        Jv6 = np.transpose(np.cross(np.transpose(Z5),np.transpose(O6-O5)))

        Jw1 = Z0
        Jw2 = Z1
        Jw3 = Z2
        Jw4 = Z3
        Jw5 = Z4
        Jw6 = Z5

        J1 = np.vstack((Jv1,Jw1))
        J2 = np.vstack((Jv2,Jw2))
        J3 = np.vstack((Jv3,Jw3))
        J4 = np.vstack((Jv4,Jw4))
        J5 = np.vstack((Jv5,Jw5))
        J6 = np.vstack((Jv6,Jw6))

        J = np.hstack((J1,J2,J3,J4,J5,J6))

        return J

    def jacobian_analytical(self,theta,roll,pitch,yaw):

        B = np.array([[np.cos(yaw)*np.sin(pitch), -np.sin(yaw), 0],
                      [np.sin(yaw)*np.sin(pitch),  np.cos(yaw), 0],
                      [            np.cos(pitch),            0, 1]])

        Binv = np.linalg.inv(B)

        Ja_mul = np.array([[1, 0, 0,         0,         0,         0],
                           [0, 1, 0,         0,         0,         0],
                           [0, 0, 1,         0,         0,         0],
                           [0, 0, 0, Binv[0,0], Binv[0,1], Binv[0,2]],
                           [0, 0, 0, Binv[1,0], Binv[1,1], Binv[1,2]],
                           [0, 0, 0, Binv[2,0], Binv[2,1], Binv[2,2]]])

        Ja = Ja_mul @ self.jacobian(theta)

        return Ja

    def plot_arm(self,theta):

        A1 = self.dh_transformation(theta[0,0],self.alpha[0,0],self.d[0,0],self.a[0,0])
        A2 = self.dh_transformation(theta[1,0],self.alpha[1,0],self.d[1,0],self.a[1,0])
        A3 = self.dh_transformation(theta[2,0],self.alpha[2,0],self.d[2,0],self.a[2,0])
        A4 = self.dh_transformation(theta[3,0],self.alpha[3,0],self.d[3,0],self.a[3,0])
        A5 = self.dh_transformation(theta[4,0],self.alpha[4,0],self.d[4,0],self.a[4,0])
        A6 = self.dh_transformation(theta[5,0],self.alpha[5,0],self.d[5,0],self.a[5,0])

        T01 = A1
        T02 = A1 @ A2
        T03 = A1 @ A2 @ A3
        T04 = A1 @ A2 @ A3 @ A4
        T05 = A1 @ A2 @ A3 @ A4 @ A5
        T06 = A1 @ A2 @ A3 @ A4 @ A5 @ A6

        plt.figure(figsize=(10,10))
        plt.axes().set_aspect('equal')

        # plot basic axis
        ax.plot3D([0, 0.5], [0, 0], [0, 0], 'red', linewidth=4)
        ax.plot3D([0, 0], [0, 0.5], [0, 0], 'purple', linewidth=4)
        ax.plot3D([0, 0], [0, 0], [0, 0.5], 'gray', linewidth=4)

        ax.plot3D([        0, T01[0, 3]], [        0, T01[1, 3]], [        0, T01[2, 3]], 'blue', linewidth=4)
        ax.plot3D([T01[0, 3], T02[0, 3]], [T01[1, 3], T02[1, 3]], [T01[2, 3], T02[2, 3]], 'orange', linewidth=4)
        ax.plot3D([T02[0, 3], T03[0, 3]], [T02[1, 3], T03[1, 3]], [T02[2, 3], T03[2, 3]], 'brown', linewidth=4)
        ax.plot3D([T03[0, 3], T04[0, 3]], [T03[1, 3], T04[1, 3]], [T03[2, 3], T04[2, 3]], 'pink', linewidth=4)
        ax.plot3D([T04[0, 3], T05[0, 3]], [T04[1, 3], T05[1, 3]], [T04[2, 3], T05[2, 3]], 'green', linewidth=4)
        ax.plot3D([T05[0, 3], T06[0, 3]], [T05[1, 3], T06[1, 3]], [T05[2, 3], T06[2, 3]], 'cyan', linewidth=4)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        # ax.set_xlim(0, 1)
        # ax.set_ylim(0, 1)
        # ax.set_zlim(0, 1)
        
        plt.show()

    def inverse_kinematic_geo(self,desired_transform_matrix):
        # not correct yet/ fix later
        # input as 4x4 transformation matrix
        # https://github.com/yorgoon/ur5_Final_Project/tree/master/inv_kin

        T06 = desired_transform_matrix

        d1 = 0.1625
        d2 = 0
        d3 = 0
        d4 = 0.1333
        d5 = 0.0997
        d6 = 0.0996

        a1 = 0
        a2 = -0.425
        a3 = -0.392
        a4 = 0
        a5 = 0
        a6 = 0

        alpha1 = np.pi/2
        alpha2 = 0
        alpha3 = 0
        alpha4 = np.pi/2
        alpha5 = -np.pi/2
        alpha6 = 0

        # cal theta1
        p05 = (T06 @ np.array([[0], [0], [-d6], [1]])) - np.array([[0], [0], [0], [1]])
        psi = np.arctan2(p05[1,0], p05[0,0])
        phi = np.arccos(d4 / np.sqrt(p05[0,0]**2 + p05[1,0]**2))
        theta1 = np.pi/2 + psi + phi # or pi/2 + psi - phi 

        # cal theta5
        T10 = np.linalg.inv(self.dh_transformation(theta1, alpha1, d1, a1))
        T16 = T10 @ T06
        p16z = T16[2,3]
        theta5 = np.arccos((p16z - d4)/d6) #or -np.arccos((p16z - d4)/d6)

        # cal theta6
        T01 = self.dh_transformation(theta1, alpha1, d1, a1)
        T61 = np.linalg.inv(T06) @ T01
        T61zy = T61[1,2]
        T61zx = T61[0,2]
        theta6 = np.arctan2(-T61zy/np.sin(theta5), T61zx/np.sin(theta5))

        # cal theata3
        T10 = np.linalg.inv(self.dh_transformation(theta1, alpha1, d1, a1))
        T65 = np.linalg.inv(self.dh_transformation(theta6, alpha6, d6, a6))
        T54 = np.linalg.inv(self.dh_transformation(theta5, alpha5, d5, a6))
        T14 = T10 @ T06 @ T65 @ T54
        p13 = T14 @ np.array([[0], [-d4], [0], [1]]) - np.array([[0],[0],[0],[1]])
        p13norm_sq = np.linalg.norm(p13)**2
        theta3 = np.arccos((p13norm_sq - a2*a2 - a3*a3)/(2*a2*a3)) # or -np.arccos((p13norm_sq - a2*a2 - a3*a3)/(2*a2*a3))

        # cal theta2 and theta4
        T10 = np.linalg.inv(self.dh_transformation(theta1, alpha1, d1, a1))
        T65 = np.linalg.inv(self.dh_transformation(theta6, alpha6, d6, a6))
        T54 = np.linalg.inv(self.dh_transformation(theta5, alpha5, d5, a6))
        T14 = T10 @ T06 @ T65 @ T54
        p13 = (T14 @ np.array([[0],[-d4],[0],[0]])) - np.array([[0],[0],[0],[1]])
        p13norm = np.linalg.norm(p13)
        theta2 = -np.arctan2(p13[1,0], p13[0,0]) + np.arcsin(a3*np.sin(theta3)/p13norm)

        T32 = np.linalg.inv(self.dh_transformation(theta3, alpha3, d3, a3))
        T21 = np.linalg.inv(self.dh_transformation(theta2, alpha2, d2, a2))
        T34 = T32 @ T21 @ T14
        theta4 = np.arctan2(T34[1,0], T34[0,0])

        return np.array([[theta1], [theta2], [theta3], [theta4], [theta5], [theta6]])
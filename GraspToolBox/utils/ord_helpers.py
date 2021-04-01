import math
import numpy as np
# get q and x,y,z from config
from scipy.spatial.transform import Rotation as R

from GraspToolBox.config import (ROBOT_START_POINT, ROBOT_START_ROTATION,
                                 pos_kinect, pos_realsense, q_kinect,
                                 q_realsense)


def q_to_matrix(rot):
    qw = rot[0]
    qx = rot[1]
    qy = rot[2]
    qz = rot[3]
    trans_matrix = list()
    trans_matrix.append([
        1 - 2 * qy * qy - 2 * qz * qz, 2 * qx * qy + 2 * qw * qz,
        2 * qx * qz - 2 * qw * qy
    ])
    trans_matrix.append([
        2 * qx * qy - 2 * qw * qz, 1 - 2 * qx * qx - 2 * qz * qz,
        2 * qy * qz + 2 * qw * qx
    ])
    trans_matrix.append([
        2 * qx * qz + 2 * qw * qy, 2 * qy * qz - 2 * qw * qx,
        1 - 2 * qx * qx - 2 * qy * qy
    ])
    trans_matrix = np.array(trans_matrix)
    return trans_matrix


def matrix_to_q(rot):
    r = R.from_matrix(rot)
    quat = r.as_quat()
    return np.array([quat[3], quat[0], quat[1], quat[2]])


def get_trans_matrix(pos, rot):
    # get matrix
    trans_matrix = q_to_matrix(rot)
    inv_matrix = trans_matrix.T
    # get offset
    trans_offset = pos
    return trans_matrix, inv_matrix, trans_offset


# get matrix and offset
trans_matrix_kinect, inv_matrix_kinect, trans_offset_kinect = get_trans_matrix(
    pos_kinect, q_kinect)
trans_matrix_realsense, inv_matrix_realsense, trans_offset_realsense = get_trans_matrix(
    pos_realsense, q_realsense)
trans_matrix_hand, inv_matrix_hand, trans_offset_hand = get_trans_matrix(
    ROBOT_START_POINT, ROBOT_START_ROTATION)
# gripper center offset for realsense
trans_offset_realsense += np.array([0, 0, 0])


def q_to_euler(q):
    # rpy
    sinr = 2.0 * (q[0] * q[1] + q[2] * q[3])
    cosr = 1.0 - 2.0 * (q[1] * q[1] + q[2] * q[2])
    roll = math.atan2(sinr, cosr)

    sinp = 2.0 * (q[0] * q[2] - q[3] * q[1])
    if math.fabs(sinp) >= 1.:
        pitch = math.copysign(np.pi / 2., sinp)
    else:
        pitch = math.asin(sinp)

    siny = 2.0 * (q[0] * q[3] + q[1] * q[2])
    cosy = 1.0 - 2.0 * (q[2] * q[2] + q[3] * q[3])
    yaw = math.atan2(siny, cosy)
    # z x y
    return np.array([roll, pitch, yaw]) * 180 / np.pi


def normalize(q):
    q = np.array(q) / np.linalg.norm(q)
    return q


def euler_to_q(rpy, order='321'):
    rpy = rpy / 180 * np.pi
    qx = (math.cos(rpy[0] / 2.), math.sin(rpy[0] / 2.), 0., 0.)
    qy = (math.cos(rpy[1] / 2.), 0., math.sin(rpy[1] / 2.), 0.)
    qz = (math.cos(rpy[2] / 2.), 0., 0., math.sin(rpy[2] / 2.))
    q = (qx, qy, qz)
    order = (ord(order[0]) - ord('1'), ord(order[1]) - ord('1'),
             ord(order[2]) - ord('1'))
    return normalize(qmul(qmul(q[order[0]], q[order[1]]), q[order[2]]))


def qmul(q0, q1):
    w0, x0, y0, z0 = q0
    w1, x1, y1, z1 = q1
    return np.array([
        -x0 * x1 - y0 * y1 - z0 * z1 + w0 * w1,
        x0 * w1 + y0 * z1 - z0 * y1 + w0 * x1,
        -x0 * z1 + y0 * w1 + z0 * x1 + w0 * y1,
        x0 * y1 - y0 * x1 + z0 * w1 + w0 * z1
    ])


def rot_camera_to_q_base(source, rot_in_camera):
    """transform camera rot to base rot.

    Args:
        source (str): kinect/realsense
        rot_in_camera (np.array): 3*3 rot_matrix

    Returns:
        q_in_base (np.array): quat
    """
    if np.shape(rot_in_camera) != (3.3):
        raise ValueError('Input should be a np.array with shape (3, 3)')
    # origin gripper along x axis
    euler_origin = np.array([-90, 0, -90])
    q_origin = euler_to_q(euler_origin)
    # get q_in camera
    q_in_camera = matrix_to_q(rot_in_camera)
    # rotate to q_in_base
    if source == 'kinect':
        # one steps for kinect
        q_in_base = qmul(matrix_to_q(inv_matrix_kinect), q_in_camera)
    else:
        # two steps for realsense
        q_in_hand = qmul(matrix_to_q(inv_matrix_realsense), q_in_camera)
        q_in_base = qmul(matrix_to_q(inv_matrix_hand), q_in_hand)
    q_in_base = qmul(q_in_base, q_origin)
    # not rotate gripper too much
    euler_in_base = q_to_euler(q_in_base)
    if euler_in_base[2] > 90:
        euler_in_base[2] -= 180
    elif euler_in_base[2] < -90:
        euler_in_base[2] += 180
    q_in_base = euler_to_q(euler_in_base)
    return q_in_base


def ord_camera_to_base(source, ord_in_camera):
    """transform camera ord to base ord.

    Args:
        source (str): kinect/realsense
        ord_in_camera (np.array): x,y,z

    Returns:
        ord_in_base (np.array): x,y,z
    """
    if len(ord_in_camera) != 3:
        raise ValueError('Input should be a np.array with len == 3')
    if source == 'kinect':
        return np.matmul(inv_matrix_kinect,
                         ord_in_camera) + trans_offset_kinect
    return ord_hand_to_base(ord_camera_to_hand(ord_in_camera))


def ord_camera_to_hand(ord_in_camera):
    """transform camera ord to hand ord.

    Args:
        ord_in_camera (np.array): x,y,z

    Returns:
        ord_in_hand (np.array): x,y,z
    """
    if len(ord_in_camera) != 3:
        raise ValueError('Input should be a np.array with len == 3')
    return np.matmul(inv_matrix_realsense,
                     ord_in_camera) + trans_offset_realsense


def ord_hand_to_base(ord_in_hand):
    """transform hand ord to base ord.

    Args:
        ord_in_hand (np.array): x,y,z

    Returns:
        ord_in_base (np.array): x,y,z
    """
    if len(ord_in_hand) != 3:
        raise ValueError('Input should be a np.array with len == 3')
    return np.matmul(inv_matrix_hand, ord_in_hand) + trans_offset_hand


if __name__ == '__main__':
    print(q_to_euler(matrix_to_q(trans_matrix_kinect)))
    # down [-180, 0, 0]
    matrix_in_camera = np.array(
        [[-2.7900429e-02, 2.3445182e-02, 9.9933565e-01],
         [7.6507765e-01, -6.4290589e-01, 3.6443252e-02],
         [6.4333332e-01, 7.6558614e-01, -3.3464833e-08]])
    # heng [-180, 0, 90]
    # matrix_in_camera = np.array([[0.02277477, -0.9989326, -0.04018656],
    #                              [0.49252543, 0.04619145, -0.86907136],
    #                              [0.87, 0., 0.4930517]])
    q_in_camera = matrix_to_q(matrix_in_camera)
    print('q in camera:')
    print(q_in_camera)
    # print(np.matmul(matrix_in_camera, matrix_in_camera.T))
    q_in_base = rot_camera_to_q_base(matrix_in_camera)
    print('q in base:')
    print(q_in_base)
    print(q_to_euler(q_in_base))
    q_in_base = qmul(q_kinect, q_in_camera)
    print('raw ==', q_to_euler(q_in_base))

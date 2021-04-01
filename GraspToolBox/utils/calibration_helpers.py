import numpy as np

from GraspToolBox.config import cx, cy, fx, fy, resolution_x, resolution_y

# inv normalize
cx *= resolution_x
fx *= resolution_x
cy *= resolution_y
fy *= resolution_y


def get_intrinsics_matrix():
    """get intrinsics_matrix according to settings above.

    Returns:
        intrinsics_matrix: 3*3 matrix
    """
    intrinsics_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    return intrinsics_matrix


if __name__ == '__main__':
    print(get_intrinsics_matrix())

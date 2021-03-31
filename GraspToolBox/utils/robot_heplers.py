import time
# get robot ip address
from GraspToolBox.config import IP_ADDRESS, ROBOT_START_POINT, ROBOT_START_ROTATION
# lower api
from GraspToolBox.RTIF.HAPI import HAPI


class RobotController():

    def __init__(self):
        self.controller = HAPI(IP_ADDRESS)

    def get_pos(self):
        return self.controller.GetCurrentEndPos()[0]

    def get_rot(self):
        return self.controller.GetCurrentEndPos()[1]

    def wait_for_movement(self):
        # wait for movement to complete
        while not self.controller.isLastMovementEnd():
            time.sleep(0.5)
        time.sleep(1)

    def reset_robot(self, a=1.2, v=0.05, t=None):
        # move robot
        print('move to start point')
        self.controller.MoveEndPointToPosition(
            pos=ROBOT_START_POINT,
            rotation=ROBOT_START_ROTATION,
            a=a,
            v=v,
            t=t)
        self.wait_for_movement()
        print('move to start point completed')

    def move_robot(self, pos=None, rotation=None, a=1.2, v=0.05, t=None):
        print('move to given point')
        self.wait_for_movement()
        self.controller.MoveEndPointToPosition(
            rotation=rotation, pos=pos, a=a, v=v, t=t)
        self.wait_for_movement()
        print('move to given point completed')

    def set_coordinate_origin(self, ori):
        self.controller.set_coordinate_origin(ori=ori)


if __name__ == '__main__':
    import numpy as np
    from GraspToolBox.utils.ord_helpers import euler_to_q, q_to_euler
    controller = RobotController()
    pos = controller.get_pos()
    q = controller.get_rot()
    print('now_pos ==', pos)
    print('now_rot ==', q)
    euler = q_to_euler(q)
    print(euler)
    euler = np.array([-179.93519185, -4.53879681, -2.04890715])
    q = euler_to_q(euler)
    print(q)
    # controller.reset_robot()
    # base
    # controller.move_robot(rotation=q)
    # ori = [[0.701479089333879, -0.49627869568818056, 0.5928481716284633],
    #        [
    #            0.2830117195130695, -0.6518756969714905, -0.6526927081309741,
    #            0.2625922144101839
    #        ]]
    # controller.set_coordinate_origin(ori=ori)
    # controller.move_robot(
    #     rotation=[0.28687698, 0.63541435, 0.31023961, 0.64629837])

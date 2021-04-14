import time
import numpy as np

# get robot ip address and start pose
from GraspToolBox.config import (IP_ADDRESS, ROBOT_GRASP_END_POINT,
                                 ROBOT_GRASP_END_ROTATION, ROBOT_START_POINT,
                                 ROBOT_START_ROTATION)
# get gripper port
from GraspToolBox.config import GRIPPER_PORT
# lower api
from GraspToolBox.RTIF.HAPI import HAPI
# gripper controller
from GraspToolBox.utils.gripper_helpers import GripperController


class RobotController(GripperController):
    """Ur5e robot with robotiq gripper controller."""

    def __init__(self, defualt_v=0.1, defualt_a=1):
        super().__init__(GRIPPER_PORT)
        self.robot_controller = HAPI(IP_ADDRESS)
        # set default v / a
        self.defualt_v = defualt_v
        self.defualt_a = defualt_a
        # activate fripper
        self.activate_gripper()

    def get_pos(self):
        """get robot pos.

        Returns:
            pos (np.array): (1, 3)
        """
        return self.robot_controller.GetCurrentEndPos()[0]

    def get_rot(self):
        """get robot rot (quaternion)

        Returns:
            rot (np.array): (1, 4)
        """
        return self.robot_controller.GetCurrentEndPos()[1]

    def get_joint_rad(self):
        """get robot joint rad.

        Returns:
            joint_rads (np.array): (1, 6)
        """
        return self.robot_controller.GetCurrentJointRad()

    def wait_for_movement(self):
        # wait for movement to complete
        while not self.robot_controller.isLastMovementEnd():
            time.sleep(0.2)
        time.sleep(0.5)

    def move_robot(self, pos=None, rotation=None, a=None, v=None, t=None):
        """move robot to given pos / rot.

        Args:
            pos (np.array, optional): (1, 3). Defaults to None.
            rotation (np.array, optional): [description]. Defaults to None.
            a (int, optional): robot acceleration . Defaults to None.
            v (int, optional): robot velocity. Defaults to None.
            t (int, optional): robot moving time, with overwrite a / v. Defaults to None.
        """
        # set v / a
        if a is None:
            a = self.defualt_a
        if v is None:
            v = self.defualt_v
        # move
        print(f'move to pos: {pos}, rot: {rotation}')
        self.wait_for_movement()
        self.robot_controller.MoveEndPointToPosition(
            pos=pos, rotation=rotation, a=a, v=v, t=t)
        self.wait_for_movement()
        print('move completed')

    def move_home(self):
        self.move_robot(pos=ROBOT_START_POINT, rotation=ROBOT_START_ROTATION)

    def move_grasp_endpoint(self):
        self.move_robot(
            pos=ROBOT_GRASP_END_POINT, rotation=ROBOT_GRASP_END_ROTATION)

    def get_grasp(self, grasp_pos, grasp_rotation, height_offset=0.4):
        """get grasp on given pos / rot.

        Args:
            grasp_pos (np.array): (1, 3)
            grasp_rotation (np.array): quaternion, (1, 4)
            height_offset (int): moving point height above grasp_pos
        """
        # move above first
        height_offset = np.array([0, 0, height_offset])
        self.move_robot(
            pos=grasp_pos + height_offset, rotation=ROBOT_START_ROTATION)
        # move to get grasp
        self.move_robot(pos=grasp_pos, rotation=grasp_rotation)
        # close gripper
        self.close_gripper()
        # move above first
        self.move_robot(
            pos=grasp_pos + height_offset,
            rotation=ROBOT_START_ROTATION,
        )
        # move to grasp endpoint
        self.move_home()
        # move robot to grasp point
        self.move_grasp_endpoint()
        # wait for sometime
        time.sleep(2)
        # open gripper
        self.open_gripper()
        # reset robot to grasp point
        self.move_home()


if __name__ == '__main__':
    robot_controller = RobotController()

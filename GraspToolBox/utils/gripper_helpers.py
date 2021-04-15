# import gripper
from GraspToolBox.utils.robotiq_2f_85_gripper import Robotiq2FingerGripper


class GripperController(Robotiq2FingerGripper):
    r"""Gripper controller using serial port
    """

    def __init__(self, GRIPPER_PORT):
        super().__init__(comport=GRIPPER_PORT)
        self.sendCommand()
        self.activate_gripper()
        self.sendCommand()

    def open_gripper(self):
        while gripper.getStatus() and gripper.is_moving():
            pass
        self.goto(pos=0.085, vel=0.05, force=10)
        gripper.getStatus()
        print(gripper.get_pos(), gripper.is_ready())
        self.sendCommand()

    def grasp(self):
        while gripper.getStatus() and gripper.is_moving():
            pass
        self.goto(pos=0.03, vel=0.05, force=20)
        gripper.getStatus()
        print(gripper.get_pos(), gripper.is_ready())
        self.sendCommand()


if __name__ == '__main__':
    gripper = GripperController('/dev/ttyUSB0')
    gripper.getStatus()
    print(gripper.get_pos(), gripper.is_ready())
    gripper.open_gripper()
    gripper.grasp()
    # gripper.open_gripper()

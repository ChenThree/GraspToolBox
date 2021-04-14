# import binascii
import serial
import time


class GripperController():
    r"""Gripper controller using serial port

    Register mapping:
        Register       Robot Output / Functionalities         Robot Input / Status
         Byte 0              ACTION REQUEST                      GRIPPER STATUS
         Byte 1              RESERVED                            RESERVED
         Byte 2              RESERVED                            FAULT STATUS
         Byte 3              POSITION REQUEST                    POS REQUEST ECHO
         Byte 4              SPEED                               POSITION
         Byte 5              FORCE                               CURRENT
         Byte 6 to 15        RESERVED                            RESERVED

    """

    def __init__(self, GRIPPER_PORT):
        self.ser = serial.Serial(
            port=GRIPPER_PORT,
            baudrate=115200,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

    def activate_gripper(self):
        # send activate command
        print('activate gripper')
        self.ser.write(
            b'\x09\x10\x03\xE8\x00\x03\x06\x00\x00\x00\x00\x00\x00\x73\x30')
        time.sleep(1)
        # send
        self.ser.write(b'\x09\x03\x07\xD0\x00\x01\x85\xCF')
        time.sleep(1)

    def close_gripper(self):
        # send close command
        print('Close gripper')
        self.ser.write(
            b'\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\xFF\xFF\xFF\x42\x29')
        time.sleep(2)

    def open_gripper(self):
        # send open command
        print('Open gripper')
        self.ser.write(
            b'\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19')
        time.sleep(2)


if __name__ == '__main__':
    gripper = GripperController()
    gripper.activate_gripper()
    gripper.open_gripper()

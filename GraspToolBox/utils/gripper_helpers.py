import binascii
import serial
import time
# get gripper port
from GraspNetToolBox.config import GRIPPER_PORT


class GripperController():

    def __init__(self):
        self.ser = serial.Serial(
            port=GRIPPER_PORT,
            baudrate=115200,
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

    def activate_gripper(self):
        print('activate gripper')
        # send activate command
        self.ser.write(
            b'\x09\x10\x03\xE8\x00\x03\x06\x00\x00\x00\x00\x00\x00\x73\x30')
        data_raw = self.ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print('Response 1 ', data)
        time.sleep(1)
        # send
        self.ser.write(b'\x09\x03\x07\xD0\x00\x01\x85\xCF')
        data_raw = self.ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print('Response 2 ', data)
        time.sleep(1)

    def close_gripper(self):
        # send close command
        print('Close gripper')
        self.ser.write(
            b'\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\xFF\xFF\xFF\x42\x29')
        data_raw = self.ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print('Response 1 ', data)
        time.sleep(2)

    def open_gripper(self):
        # send open command
        print('Open gripper')
        self.ser.write(
            b'\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19')
        data_raw = self.ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print('Response 1 ', data)
        time.sleep(2)


if __name__ == '__main__':
    gripper = GripperController()
    gripper.activate_gripper()
    gripper.close_gripper()

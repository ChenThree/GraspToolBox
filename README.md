# GraspToolBox

GraspToolBox for VCLab of Electronic Engineering, Tsinghua University.  
Experiment environment: UR5e Robot + Rototiq 2f 85 Gripper + Ubuntu18.04 with ROS-melodic.  

## Code Structure

GraspToolBox  
    - RTIF : lower robot controller written by other research group, will be rewritten and deprecated soon  
    - utils : several helpers  
        - calibration_heplers : for getting camera intrinsics matrix, will be upgraded soon  
        - gripper_helpers : Rototiq 2f 85 Gripper serial controller, force controller will be added soon  
        - image_controllers : easily getting rgb and depth picture or pointcloud from Kinect camera or realsense camera  
        - ord_helpers : quaternion calculating functions and coordinate transfrom functions  
        - robot_helpers : robot controller based on RTIF  
    - test : some test scripts  
    - config  

## Linting

Pre-commit is used to lint our codes, you can configure it by editting the config file [.pre-commit-config.yaml](.pre-commit-config.yaml)


## Requirements

- python3
- open3d
- numpy
- Pillow
- serial
- opencv-python
- matplotlib
- pyk4a
- pyrealsense2

### Attention

pyk4a and pyrealsense2 is for kinect camera and realsense camera using, corresponding driver should be installed correctly, you can follow these pages:

[Intel RealSense SDK installation](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)

[Azure Kinect SDK installation](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md)


## Installation

Get the code.

```bash
git clone https://github.com/ChenThree/GraspToolBox.git
git checkout master
python setup.py install # will insatll packages using easy-install
```

Install packages via Pip.

```bash
pip install -r requirements.txt
```

## Usage

Now there is no detailed usage guidance for this toolbox, it will be supplied soon.  
You can follow the code for usage now.

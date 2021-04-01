# robot ip
IP_ADDRESS = '101.6.70.83'
# robot initial status
ROBOT_START_POINT = [-0.07566725, -0.2933787, 0.5278667]
# camera behind
ROBOT_START_ROTATION = [0.11968014, 0.9905304, 0.06719151, 0.00340645]
# camera front
# ROBOT_START_ROTATION = [0.01489975, -0.01462269, 0.9920806, -0.12385556]

# robot grasp status
ROBOT_GRASP_POINT = [0.4, 0, 0.2]
ROBOT_GRASP_ROTATION = [0, -7.07106781e-01, -7.07106781e-01, 0]

# gripper port
GRIPPER_PORT = '/dev/ttyUSB0'

# kinect ord transform matrix
# get on 2021.04.01
# translation:
#   x: 0.685956917353
#   y: -0.540495853856
#   z: 0.609819822525
# rotation:
#   x: -0.661222440978
#   y: -0.65030963348
#   z: 0.249331081736
#   w: 0.278776390375
pos_kinect = [0.685956917353, -0.540495853856, 0.609819822525]
q_kinect = [0.278776390375, -0.661222440978, -0.65030963348, 0.249331081736]

# realsense ord transform matrix
# get on 2021.04.01
# translation:
#   x: 0.0257284392279
#   y: 0.0694205607115
#   z: 0.0218193353845
# rotation:
#   x: 0.00187258682945
#   y: -0.0200717669543
#   z: -0.989155520753
#   w: 0.145481866064
pos_realsense = [0.0257284392279, 0.0694205607115, 0.0218193353845]
q_realsense = [
    0.145481866064, 0.00187258682945, -0.0200717669543, -0.989155520753
]

# kinect raw calibration
cx = 0.49866631627082825  # 1 (order in calibration json paras)
cy = 0.50889438390731812  # 2
fx = 0.47901439666748047  # 3
fy = 0.63846969604492188  # 4
# picture resolution
resolution_x = 1280
resolution_y = 720

# grasp mask
KINECT_MASK_IAMGE_PATH = './utils/kinect_mask.png'
REALSENSE_MASK_IAMGE_PATH = './utils/realsense_mask.png'

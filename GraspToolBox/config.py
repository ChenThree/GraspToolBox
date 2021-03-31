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
pos_kinect = [0.701479089333879, -0.49627869568818056, 0.5928481716284633]
q_kinect = [
    0.2830117195130695, -0.6518756969714905, -0.6526927081309741,
    0.2625922144101839
]

# realsense ord transform matrix
pos_realsense = [
    -0.05033432342198761, -0.0703680686725084, -0.28728621238534285
]
q_realsense = [
    0.9943071048390865, 0.02239446738344697, 0.025408739166783434,
    -0.1010260613459724
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

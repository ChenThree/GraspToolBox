import numpy as np
import open3d as o3d
from graspnetAPI import Grasp, GraspGroup

# transform grasp
g = Grasp()  # simple Grasp
frame = o3d.geometry.TriangleMesh.create_coordinate_frame(0.1)
g = g.to_open3d_geometry()
R = g.get_rotation_matrix_from_xyz((np.pi / 2, 0, np.pi / 2))
print(R)
g.rotate(R, center=(0, 0, 0))
o3d.visualization.draw_geometries([g, frame])

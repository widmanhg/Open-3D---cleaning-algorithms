import open3d as o3d
import numpy as np

def filter_point_cloud(point_cloud, threshold):
    points = np.asarray(point_cloud.points)
    distances = np.linalg.norm(points, axis=1)
    mask = distances <= threshold
    filtered_points = points[mask]
    filtered_point_cloud = o3d.geometry.PointCloud()
    filtered_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    return filtered_point_cloud

point_cloud = o3d.io.read_point_cloud("C:/Users/widma/Desktop/DATABASE/DIRTY/lilshell_pc.ply")
threshold = 50
filtered_point_cloud = filter_point_cloud(point_cloud, threshold)
o3d.visualization.draw_geometries([point_cloud], window_name="Original Point Cloud")
o3d.visualization.draw_geometries([filtered_point_cloud], window_name="Filtered Point Cloud")

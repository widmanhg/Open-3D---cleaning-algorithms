import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

class PointCloudProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.pcd = o3d.io.read_point_cloud(file_path)
        self.points = np.asarray(self.pcd.points)

    def downsample(self, voxel_size=0.01):
        self.downsampled_pcd = self.pcd.voxel_down_sample(voxel_size=voxel_size)
        self.downsampled_points = np.asarray(self.downsampled_pcd.points)

    def normalize_points(self):
        self.scaled_points = StandardScaler().fit_transform(self.downsampled_points)

    def apply_dbscan(self, eps=0.02, min_samples=2):
        self.model = DBSCAN(eps=eps, min_samples=min_samples)
        self.model.fit(self.scaled_points)
        self.labels = self.model.labels_

    def find_densest_cluster(self):
        unique_labels, counts = np.unique(self.labels, return_counts=True)
        densities = counts / np.sum(counts)  
        densest_cluster_label = unique_labels[np.argmax(densities)] 
        self.densest_cluster_indices = np.where(self.labels == densest_cluster_label)[0]
        self.densest_cluster_pcd = self.downsampled_pcd.select_by_index(self.densest_cluster_indices)

    def generate_mesh(self, depth=9):
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.densest_cluster_pcd, depth=depth)
        self.mesh = mesh

    def smooth_mesh(self, iterations=3):
        self.mesh.filter_smooth_laplacian(iterations)

    def visualize_mesh(self):
        o3d.visualization.draw_geometries([self.mesh])

    def save_mesh(self, file_path):
        new_file_path = file_path.replace('_pc', '_mesh')
        o3d.io.write_triangle_mesh(new_file_path, self.mesh)

file_path = "C:/Users/widma/Desktop/DATABASE/DIRTY/lilshell_pc.ply"
processor = PointCloudProcessor(file_path)
processor.downsample()
processor.normalize_points()
processor.apply_dbscan()
processor.find_densest_cluster()  
processor.generate_mesh()
processor.smooth_mesh()
processor.visualize_mesh()
processor.save_mesh(file_path)

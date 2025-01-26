import os
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

    def find_clusters(self):
        self.cluster_indices = []
        unique_labels = np.unique(self.labels)
        for label in unique_labels:
            if label == -1:
                continue
            indices = np.where(self.labels == label)[0]
            self.cluster_indices.append(indices)

    def generate_meshes(self, depth=9):
        self.meshes = []
        for indices in self.cluster_indices:
            cluster_pcd = self.downsampled_pcd.select_by_index(indices)
            mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(cluster_pcd, depth=depth)
            self.meshes.append(mesh)

    def smooth_meshes(self, iterations=3):
        for mesh in self.meshes:
            mesh.filter_smooth_laplacian(iterations)

    def visualize_meshes(self):
        o3d.visualization.draw_geometries(self.meshes)

    def save_meshes(self, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for i, mesh in enumerate(self.meshes):
            output_file_path = os.path.join(output_folder, f"cluster_{i}_mesh.ply")
            o3d.io.write_triangle_mesh(output_file_path, mesh)

file_path = "C:/Users/widma/Desktop/DATABASE/DIRTY/lilshell_pc.ply"
output_folder = "C:/Users/widma/Desktop/DATABASE/cluster_meshes"
processor = PointCloudProcessor(file_path)
processor.downsample()
processor.normalize_points()
processor.apply_dbscan()
processor.find_clusters()
processor.generate_meshes()
processor.smooth_meshes()
processor.visualize_meshes()
processor.save_meshes(output_folder)

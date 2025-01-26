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

    def find_cluster_with_most_colors(self):
        unique_labels = np.unique(self.labels)
        max_colors = -1
        cluster_with_most_colors = None
        
        for label in unique_labels:
            cluster_indices = np.where(self.labels == label)[0]
            cluster_pcd = self.downsampled_pcd.select_by_index(cluster_indices)
            unique_colors = np.unique(np.round(cluster_pcd.colors, decimals=2), axis=0)
            num_colors = len(unique_colors)
            
            if num_colors > max_colors:
                max_colors = num_colors
                cluster_with_most_colors = label
                
        self.cluster_with_most_colors_label = cluster_with_most_colors
        self.cluster_with_most_colors_indices = np.where(self.labels == cluster_with_most_colors)[0]
        self.cluster_with_most_colors_pcd = self.downsampled_pcd.select_by_index(self.cluster_with_most_colors_indices)

    def generate_mesh(self, depth=9):
        self.find_cluster_with_most_colors() 
        mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(self.cluster_with_most_colors_pcd, depth=depth)
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
processor.generate_mesh()
processor.smooth_mesh()
processor.visualize_mesh()
processor.save_mesh(file_path)

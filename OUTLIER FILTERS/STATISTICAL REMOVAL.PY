import open3d as o3d
import numpy as np

class OutlierRemoval:
    def __init__(self, voxel_size=0.2):
        self.voxel_size = voxel_size

    def adaptive_remove_outliers(self, pcd):
        pcd_downsampled = pcd.voxel_down_sample(voxel_size=self.voxel_size)
        points_downsampled = np.asarray(pcd_downsampled.points)

        center = np.mean(points_downsampled, axis=0)
        distances = np.linalg.norm(points_downsampled - center, axis=1)
        std_dev = np.std(distances)
        adaptive_threshold = 7 * std_dev

        mask = distances <= adaptive_threshold
        pcd_filtered = pcd_downsampled.select_by_index(np.where(mask)[0])

        cl, ind = pcd_filtered.remove_statistical_outlier(nb_neighbors=2000, std_ratio=0.01)
        pcd_filtered = pcd_filtered.select_by_index(ind)

        return pcd_filtered

class SurfaceReconstruction:
    def __init__(self, depth=9):
        self.depth = depth

    def poisson_surface_reconstruction(self, pcd_filtered):
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd_filtered, depth=self.depth
            )
        return mesh

    def visualize_and_save_mesh(self, mesh, output_file_path="mesh_result.ply"):
        mesh.paint_uniform_color([1.0, 1.0, 1.0])
        mesh.compute_vertex_normals()
        o3d.io.write_triangle_mesh(output_file_path, mesh)
        o3d.visualization.draw_geometries([mesh])
        print(f'Reconstruction saved to {output_file_path}')

# Uso de las clases
ply_path = "C:/Users/widma/Desktop/plys/0220_01_pc.ply"
pcd = o3d.io.read_point_cloud(ply_path)

outlier_remover = OutlierRemoval()
pcd_filtered = outlier_remover.adaptive_remove_outliers(pcd)

reconstructor = SurfaceReconstruction()
mesh = reconstructor.poisson_surface_reconstruction(pcd_filtered)
reconstructor.visualize_and_save_mesh(mesh, "mesh_result.ply")

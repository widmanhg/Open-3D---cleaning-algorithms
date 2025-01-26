import open3d as o3d
import numpy as np

# Cargar el archivo PLY
file_path = "C:/Users/widma/Desktop/DATABASE/DIRTY/hollowstatue_pc.ply"
pcd = o3d.io.read_point_cloud(file_path)

voxel_size = 0.9  # Tamaño del voxel
downsampled_pcd = pcd.voxel_down_sample(voxel_size)

# Aplicar eliminación de outliers radiales
downsampled_pcd_rad, _ = downsampled_pcd.remove_radius_outlier(nb_points=100, radius=5)

# Aplicar eliminación de outliers estadísticos
downsampled_pcd_stat, _ = downsampled_pcd_rad.remove_statistical_outlier(nb_neighbors=50, std_ratio=0.01)

# Calcular la envolvente convexa de los inliers
convex_hull, _ = downsampled_pcd_stat.compute_convex_hull()

# Expandir la envolvente convexa
expand_factor = 1.03
expanded_convex_hull = convex_hull.scale(expand_factor, center=convex_hull.get_center())

o3d.visualization.draw_geometries([pcd, expanded_convex_hull])

# Filtrar puntos fuera de la envolvente convexa en la nube de puntos original
points = np.asarray(pcd.points)
indices_inside_hull = np.asarray(expanded_convex_hull.select_by_index(pcd).indices)
cropped_points = points[indices_inside_hull]

# Crear una nueva nube de puntos con los puntos dentro de la envolvente convexa
cropped_pcd = o3d.geometry.PointCloud()
cropped_pcd.points = o3d.utility.Vector3dVector(cropped_points)

# Guardar la nube de puntos recortada a un nuevo archivo PCD
output_file_path = "cropped_pcd.ply"
o3d.io.write_point_cloud(output_file_path, cropped_pcd)

# Visualizar la nube de puntos recortada y el convex hull original
o3d.visualization.draw_geometries([cropped_pcd])

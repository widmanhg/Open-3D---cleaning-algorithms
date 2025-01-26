import numpy as np
import open3d as o3d
from sklearn.cluster import  DBSCAN
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

#COLOR CLUSTERING


pcd = o3d.io.read_point_cloud("C:/Users/widma/Desktop/DATABASE/DIRTY/lilshell_pc.ply")

if __name__ == '__main__':
    # Read point cloud:
   
    o3d.visualization.draw_geometries([pcd])
    # Get points and transform it to a numpy array:
    points = np.asarray(pcd.points).copy()

    # Project points on 0XZ plane:
    points[:, 1] = 0
    pcd_projected = o3d.geometry.PointCloud()  # create point cloud object
    pcd_projected.points = o3d.utility.Vector3dVector(points)  # set pcd_np as the point cloud points

    # projection: consider the x and z coordinates:
    points_xz = points[:, [0, 2]]
    # Normalisation:
    scaled_points = StandardScaler().fit_transform(points_xz)
    # Clustering:
    model = DBSCAN(eps=0.01, min_samples=2)
    model.fit(scaled_points)

    # Get labels:
    labels = model.labels_
    # Get the number of colors:
    n_clusters = len(set(labels))

    # Mapping the labels classes to a color map:
    colors = plt.get_cmap("tab20")(labels / (n_clusters if n_clusters > 0 else 1))
    # Attribute to noise the black color:
    colors[labels < 0] = 0
    # Update points colors:
    pcd_projected.colors = o3d.utility.Vector3dVector(colors[:, :3])
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

    # Display:
    o3d.visualization.draw_geometries([pcd_projected])
    o3d.visualization.draw_geometries([pcd])


#DENSITY VISUALIZATION

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9)

print('visualize densities')
densities = np.asarray(densities)
density_colors = plt.get_cmap('plasma')(
    (densities - densities.min()) / (densities.max() - densities.min()))
density_colors = density_colors[:, :3]
density_mesh = o3d.geometry.TriangleMesh()
density_mesh.vertices = mesh.vertices
density_mesh.triangles = mesh.triangles
density_mesh.triangle_normals = mesh.triangle_normals
density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
o3d.visualization.draw_geometries([density_mesh])

#NORMAL VISUALIZATION

o3d.visualization.draw_geometries([pcd], point_show_normal=True)
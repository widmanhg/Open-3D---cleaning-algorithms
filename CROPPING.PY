import open3d as o3d


ply_file = "C:/Users/widma/Desktop/DATABASE/DIRTY/lilshell_pc.ply"

point_cloud = o3d.io.read_point_cloud(ply_file)

center = point_cloud.get_center()

half_extent = 20  
crop_box = o3d.geometry.AxisAlignedBoundingBox(
    min_bound=(center[0] - half_extent, center[1] - half_extent, center[2] - half_extent),
    max_bound=(center[0] + half_extent, center[1] + half_extent, center[2] + half_extent)
)

cropped_point_cloud = point_cloud.crop(crop_box)

o3d.visualization.draw_geometries([point_cloud], window_name="Original Point Cloud")

o3d.visualization.draw_geometries([cropped_point_cloud], window_name="Cropped Point Cloud")

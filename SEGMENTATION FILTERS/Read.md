# 3D Point Cloud Filtering and Processing

This repository provides a set of algorithms for processing 3D point clouds with the primary focus on filtration techniques. The goal is to enhance 3D model data for AI training by cleaning and optimizing the data to improve object recognition and 3D image processing.

## Algorithms Used

This project utilizes Open3D, a powerful library for working with 3D data, alongside various filtration methods to refine point clouds. The following algorithms are implemented:

### Point Cloud Filtration Methods:
- **Cropping**: For cutting out a region of interest from a 3D point cloud.
- **Downsampling**: Reduces the number of points in the cloud while retaining the overall shape.
- **Meshing**: Converts point clouds to meshes for better visualization and processing.
- **Thresholding**: Applies value-based thresholds to filter out irrelevant points.

### Outlier Removal:
- **Radius Removal**: Filters out points based on a specified radius, removing isolated points.
- **Statistical Removal**: Uses statistical methods to eliminate outliers from the point cloud.

### Segmentation:
- **Color Segmentation**: Segments the point cloud based on color.
- **Density Segmentation**: Segments by point density, useful for distinguishing objects.
- **Largest Object Segmentation**: Filters and keeps the largest segmented object from the point cloud.

## How to Use

1. Download the [dirty point cloud](https://drive.google.com/file/d/1QY0G4fUj7WkWQkwW_6f-qLhfpfteE5c_/view?usp=sharing) to test the provided scripts.
2. Explore and run the algorithms in the respective Python files to clean, filter, or downsample the point cloud.
3. Use the visualization scripts to see the results and ensure your point cloud is properly filtered.

## Dependencies

- Open3D
- NumPy
- Matplotlib (for visualization)

You can install the necessary dependencies by running:

```bash
pip install open3d numpy matplotlib

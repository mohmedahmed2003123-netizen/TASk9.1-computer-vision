"""
 3D Point Cloud Viewer using Open3D
this script loads the generated point cloud (.ply) and displays it.
it works on older hardware without requiring heavy GPU drivers.
"""

# import the open3D library for 3D data processing and visualization
import open3d as o3d

#Import os to handle file and folder paths
import os

# import sys to safely exit the script if something goes wrong
import sys


def main():
    """
    main function to load and visualize the 3D point cloud.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    ply_file_path = os.path.join(script_dir, '..', 'outputs', 'pointcloud.ply')
    
    if not os.path.exists(ply_file_path):
        print(f"Error: File not found at {ply_file_path}")
        print("Please make sure you have generated the point cloud first.")
        sys.exit(1)  # stop the program here
    print(f" loading point cloud from: {ply_file_path}")

    point_cloud = o3d.io.read_point_cloud(ply_file_path)
    if point_cloud.is_empty():
        print(" Error: The point cloud is empty or could not be loaded.")
        print("Please check if the PLY file contains valid data.")
        sys.exit(1)
    num_points = len(point_cloud.points)
    print(f"successfully loaded {num_points} points!")
    print("\n  Opening 3D Viewer...")
    print("   - Left click + drag: Rotate the view")
    print("   - Right click + drag: Pan the camera")
    print("   - Scroll wheel: Zoom in / out")
    print("   - Close the window to exit the program.\n")

    o3d.visualization.draw_geometries(
        [point_cloud],  # list of geometries to display 
        window_name="Task 9.1 - 3D Point Cloud",
        width=800,      #initial window width in pixels
        height=600,     # Initial window height in pixels
        point_show_normal=False, 
        mesh_show_wireframe=False 
    )
    print(" viewer closed. Task 9.1 visualization completed.")

if __name__ == "__main__":
    main()
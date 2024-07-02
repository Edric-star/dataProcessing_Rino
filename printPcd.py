import open3d as o3d
import numpy as np

def read_pcd(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    points = np.asarray(pcd.points)
    return points

def count_points_in_pcd(pcd_file):
    points = read_pcd(pcd_file)
    num_points = points.shape[0]
    print(f"PCD文件中点的数量: {num_points}")
    return num_points

# 示例用法
pcd_file_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_third_ann_data/clip_rino_107_10/POINTS/1716882001.499492_1716882001.499987.pcd'
count_points_in_pcd(pcd_file_path)

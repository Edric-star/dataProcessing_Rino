import os
import numpy as np
import open3d as o3d

# 配置路径
# npy_base_path = '/home/edric/dataProcess/kneighborResult_10'
# point_cloud_output_base_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_10/samples_third_ann_data'
# label_output_base_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_10/samples_pointwise_data_bin'

npy_base_path = '/home/edric/dataProcess/kneighborResult'
point_cloud_output_base_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_third_ann_data'
label_output_base_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_pointwise_data_bin'


# 遍历每个子文件夹
for subdir in sorted(os.listdir(npy_base_path)):
    npy_subdir_path = os.path.join(npy_base_path, subdir)
    if not os.path.isdir(npy_subdir_path):
        continue
    
    point_cloud_output_subdir = os.path.join(point_cloud_output_base_path, subdir, 'POINTS')
    label_output_subdir = os.path.join(label_output_base_path, subdir, 'SEG_RESULT')
    
    os.makedirs(point_cloud_output_subdir, exist_ok=True)
    os.makedirs(label_output_subdir, exist_ok=True)

    for npy_file in sorted(os.listdir(npy_subdir_path)):
        if not npy_file.endswith('.npy'):
            continue
        
        npy_filepath = os.path.join(npy_subdir_path, npy_file)
        data = np.load(npy_filepath)
        
        points = data[:, :3]  # xyz坐标
        labels = data[:, 3].astype(np.uint8)  # 标签并转换为uint8
        
        # 检查点云数据和标签长度是否一致
        if points.shape[0] != labels.shape[0]:
            raise ValueError(f"Mismatch between points and labels in file {npy_filepath}")
        
        # 保存点云为PCD文件
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        
        pcd_filename = os.path.splitext(npy_file)[0] + '.pcd'
        pcd_filepath = os.path.join(point_cloud_output_subdir, pcd_filename)
        o3d.io.write_point_cloud(pcd_filepath, pcd)
        print(f"Point cloud saved to {pcd_filepath}")
        
        # 保存标签为uint8格式的bin文件
        bin_filename = os.path.splitext(npy_file)[0] + '.bin'
        bin_filepath = os.path.join(label_output_subdir, bin_filename)
        labels.tofile(bin_filepath)
        print(f"Labels saved to {bin_filepath}")

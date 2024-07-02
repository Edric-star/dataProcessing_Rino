import numpy as np
import pickle
import os
from sklearn.neighbors import KDTree
from scipy.stats import mode
from sklearn import linear_model

def getPlaneModel(ground_points):
    if len(ground_points) < 30:
        return None, None
    ransac = linear_model.RANSACRegressor(
        min_samples=65,
        residual_threshold=0.15,
        max_trials=1000
    )
    X = ground_points[:, :2]
    y = ground_points[:, 2]
    ransac.fit(X, y)
    inlier_mask = ransac.inlier_mask_
    normal = np.array([-ransac.estimator_.coef_[0], -ransac.estimator_.coef_[1], 1.0])
    normal /= np.linalg.norm(normal)
    d = -ransac.estimator_.intercept_
    return normal, d

# 配置路径
# ssc_pred_path = '/home/edric/dataProcess/ssc_pred_ourLabel_10'
# point_cloud_base_path = '/home/edric/dataProcess/clip_rino_107_float32bin_10'
# label_base_path = '/home/edric/dataProcess/clip_rino_107_uint32label_10'
# output_base_path = '/home/edric/dataProcess/kneighborResult_10'

ssc_pred_path = '/home/edric/dataProcess/ssc_pred_ourLabel'
point_cloud_base_path = '/home/edric/dataProcess/clip_rino_107_float32bin'
label_base_path = '/home/edric/dataProcess/clip_rino_107_uint32label'
output_base_path = '/home/edric/dataProcess/kneighborResult'


# 获取子文件夹列表并排序
ssc_pred_subdirs = sorted(os.listdir(ssc_pred_path))
pc_subdirs = sorted(os.listdir(point_cloud_base_path))
label_subdirs = sorted(os.listdir(label_base_path))

# 检查子文件夹数量是否一致
if len(ssc_pred_subdirs) != len(pc_subdirs) or len(ssc_pred_subdirs) != len(label_subdirs):
    raise ValueError("The number of subdirectories in ssc_pred_path, point_cloud_base_path, and label_base_path must be the same.")

# 逐个处理子文件夹
for idx, subdir in enumerate(ssc_pred_subdirs):
    ssc_pred_subdir_path = os.path.join(ssc_pred_path, subdir)
    pc_subdir_path = os.path.join(point_cloud_base_path, pc_subdirs[idx])
    label_subdir_path = os.path.join(label_base_path, label_subdirs[idx])

    ssc_files = sorted(os.listdir(ssc_pred_subdir_path))
    pc_files = sorted(os.listdir(pc_subdir_path))
    label_files = sorted(os.listdir(label_subdir_path))

    # 检查文件数量是否一致
    if len(ssc_files) != len(pc_files) or len(ssc_files) != len(label_files):
        raise ValueError(f"The number of files in {ssc_pred_subdir_path}, {pc_subdir_path}, and {label_base_path} must be the same.")

    for file_idx, ssc_file in enumerate(ssc_files):
        # 读取ssc预测结果
        pkl_filepath = os.path.join(ssc_pred_subdir_path, ssc_file)
        with open(pkl_filepath, 'rb') as handle:
            data = pickle.load(handle)
        ssc_pred = data['ssc_pred']  # 256x256x32的体素预测结果

        voxel_size = 0.2
        vox_origin = np.array([-25.6, -40.0, -3.0])

        # 读取稀疏的点云数据
        pcd_filepath = os.path.join(pc_subdir_path, pc_files[file_idx])
        label_filepath = os.path.join(label_subdir_path, label_files[file_idx])
        
        point_cloud = np.fromfile(pcd_filepath, dtype=np.float32).reshape(-1, 4)  # xyz + intensity
        labels = np.fromfile(label_filepath, dtype=np.uint32)
        assert point_cloud.shape[0] == labels.shape[0], "Point cloud and label file must have the same number of entries"

        # 用原始点云坐标构建 KDTree
        kdtree = KDTree(point_cloud[:, :3])
        print(f"KDTree constructed successfully for subdir {subdir}, file {ssc_file}")

        # 获取ssc_pred标签为0（地面）的点并拟合地面平面模型
        ground_voxel_indices = np.argwhere((ssc_pred == 0))
        ground_voxel_coords = (ground_voxel_indices + 0.5) * voxel_size + vox_origin
        normal, d = getPlaneModel(ground_voxel_coords)

        if normal is not None:
            # 将地面点调整到拟合的平面上
            ground_voxel_coords[:, 2] = (-normal[0] * ground_voxel_coords[:, 0] - normal[1] * ground_voxel_coords[:, 1] - d) / normal[2]

            # 获取非空体素(label 19 为空体素)的索引并计算其中心点坐标转为点云世界坐标
            non_zero_indices = np.argwhere((ssc_pred != 19))
            non_zero_coords = (non_zero_indices + 0.5) * voxel_size + vox_origin

            # 将 non_zero_coords 中的地面点调整到拟合的平面上
            ground_indices = np.argwhere((ssc_pred[non_zero_indices[:, 0], non_zero_indices[:, 1], non_zero_indices[:, 2]] == 0))
            non_zero_coords[ground_indices, 2] = (-normal[0] * non_zero_coords[ground_indices, 0] - normal[1] * non_zero_coords[ground_indices, 1] - d) / normal[2]

            # 计算空体素的索引和中心点坐标
            empty_voxel_indices = np.argwhere((ssc_pred == 19))
            empty_voxel_coords = (empty_voxel_indices + 0.5) * voxel_size + vox_origin

            # 计算空体素到地面平面的距离
            distances_to_plane = np.abs(np.dot(empty_voxel_coords, normal) + d) / np.linalg.norm(normal)
            close_to_ground_indices = empty_voxel_indices[distances_to_plane < 0.1]

            # 合并非空体素和靠近地面0.1m范围内的空体素
            non_zero_indices = np.concatenate((non_zero_indices, close_to_ground_indices))
            non_zero_coords = (non_zero_indices + 0.5) * voxel_size + vox_origin

        # 对非零体素进行近邻查询并获取标签
        k = 1
        distances, indices = kdtree.query(non_zero_coords, k=k)  

        # 获取这些最近邻点在原始点云中的标签
        nearest_labels = labels[indices]
        # 获取最常见的标签
        most_frequent_labels = mode(nearest_labels, axis=1, keepdims=True).mode.flatten()

        # 合并中心点坐标和对应的标签
        non_zero_coords_with_labels = np.hstack((non_zero_coords, most_frequent_labels.reshape(-1, 1)))

        # 获取ssc_pred标签为0（地面）的点并拟合地面平面模型
        ground_indices = np.argwhere((ssc_pred[non_zero_indices[:, 0], non_zero_indices[:, 1], non_zero_indices[:, 2]] == 0))
        ground_coords = non_zero_coords[ground_indices].reshape(-1, 3)
        normal, d = getPlaneModel(ground_coords)

        if normal is not None:
            # 将地面点调整到拟合的平面上
            non_zero_coords_with_labels[ground_indices, 2] = (-normal[0] * non_zero_coords_with_labels[ground_indices, 0] - normal[1] * non_zero_coords_with_labels[ground_indices, 1] - d) / normal[2]

        output_subdir = os.path.join(output_base_path, pc_subdirs[idx])
        os.makedirs(output_subdir, exist_ok=True)
        output_filename = os.path.splitext(pc_files[file_idx])[0] + '.npy'
        print('output_filename :', output_filename)
        output_filepath = os.path.join(output_subdir, output_filename)
        np.save(output_filepath, non_zero_coords_with_labels)
        print(f"Center coordinates with labels saved to {output_filepath}")

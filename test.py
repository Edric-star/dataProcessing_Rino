# import os

# pcd_path = '/media/edric/ac206cf7-4dcf-47a1-b41e-47ae28d8044d/col_car107_0528/collect_1716893237645/_apollo_sensor_lidar_major_PointCloud2_data/1716897009.899780.pcd'

# if os.path.exists(pcd_path):
#     print("File exists and is accessible")
#     try:
#         # 假设有一个函数 load_pcd_file 用于加载 PCD 文件
#         # 例如： load_pcd_file(pcd_path)
#         print("PCD file loaded successfully")
#     except Exception as e:
#         print(f"Error loading PCD file at {pcd_path}: {e}")
# else:
#     print("File does not exist or is not accessible")

# import os

# def check_file_access(pcd_paths):
#     for path in pcd_paths:
#         if os.path.exists(path):
#             print(f"File exists: {path}")
#             if os.access(path, os.R_OK):
#                 print(f"Read permission: Yes")
#             else:
#                 print(f"Read permission: No")
#         else:
#             print(f"File does not exist: {path}")

# pcd_paths = [
#     "/media/edric/ac206cf7-4dcf-47a1-b41e-47ae28d8044d/col_car107_0528/collect_1716893237645/_apollo_sensor_lidar_major_PointCloud2_data/1716897006.499784.pcd",
#     "/media/edric/ac206cf7-4dcf-47a1-b41e-47ae28d8044d/col_car107_0528/collect_1716893237645/_apollo_sensor_lidar_major_PointCloud2_data/1716897006.699784.pcd",
#     "/media/edric/ac206cf7-4dcf-47a1-b41e-47ae28d8044d/col_car107_0528/collect_1716893237645/_apollo_sensor_lidar_major_PointCloud2_data/1716897006.899776.pcd",
#     # 添加其他路径
# ]

# check_file_access(pcd_paths)
# file_path = '/media/edric/ac206cf7-4dcf-47a1-b41e-47ae28d8044d/rino_107_product/rino_107/samples_pointwise_data_bin/clip_rino_107_0/PNT_BIN/1716877140.099504_1716877140.099338.bin'

# with open(file_path, 'rb') as file:
#     binary_data = file.read()

# # 处理读取的二进制数据
# print(binary_data)

#读取pasco环境下的版本信息
# import torch
# print(torch.__version__)
# print(torch.cuda.is_available())
# print(torch.cuda.get_device_name(0))

# ----------------------------------检验bin文件中每个标签多少字节--------------------------------
# import os

# label_bin_file_path = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/others_info/clip_rino_107_11/pnt_instruction/1716882060.699495_1716882060.699996.bin"  # 替换为你的 bin 文件路径

# # 获取文件大小
# file_size = os.path.getsize(label_bin_file_path)
# total_labels = 24486  # 从前面的打印信息中获取

# # 计算每个标签的大小
# size_per_label = file_size / total_labels

# print(f"File size: {file_size} bytes")
# print(f"Size of each label: {size_per_label} bytes")
# ----------------------------------检验bin文件中每个标签多少字节--------------------------------

# # ----------------------------------bin标签在pcd中的可视化--------------------------------
# import open3d as o3d
# import numpy as np

# def read_label_bin_file(file_path):
#     # 读取二进制标签文件
#     labels = np.fromfile(file_path, dtype=np.int8)
#     print(f"Number of labels: {labels.size}")
#     return labels

# def visualize_point_cloud_with_labels(points, labels):
#     # 创建点云对象
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(points)
    
#     # 初始化颜色
#     colors = np.zeros((points.shape[0], 3))
    
#     # 根据标签设置颜色
#     unique_labels = np.unique(labels)
#     color_map = {label: np.random.rand(3) for label in unique_labels}
    
#     for i, label in enumerate(labels):
#         colors[i] = color_map[label]
    
#     pcd.colors = o3d.utility.Vector3dVector(colors)
    
#     # 可视化点云
#     o3d.visualization.draw_geometries([pcd])

# if __name__ == "__main__":
#     pcd_file_path = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_third_ann_data/clip_rino_107_11/POINTS/1716882060.699495_1716882060.699996.pcd"  # pcd 文件路径 24486 labels
#     # label_bin_file_path = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/others_info/clip_rino_107_11/pnt_instruction/1716882060.699495_1716882060.699996.bin"  # bin 文件路径  97947 points
#     label_bin_file_path = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/SEG_RESULT/1716882060.699495_1716882060.699996.bin"  # bin 文件路径  97947 points

#     # 读取 PCD 文件
#     pcd = o3d.io.read_point_cloud(pcd_file_path)
#     points = np.asarray(pcd.points)
#     print(f"Number of points: {points.shape[0]}")
    
#     # 读取标签文件
#     labels = read_label_bin_file(label_bin_file_path)
    
#     # 检查点的数量是否匹配
#     assert len(points) == len(labels), "点数和标签数不匹配"
    
#     # 可视化点云数据和标签
#     visualize_point_cloud_with_labels(points, labels)
# # ----------------------------------bin标签在pcd中的可视化--------------------------------

# # ---------------------------------------查看bin标签分布--------------------------------------
# import numpy as np
# import os
# import matplotlib.pyplot as plt

# def read_label_bin_file(file_path):
#     # 读取二进制标签文件
#     labels = np.fromfile(file_path, dtype=np.int8)
#     print(f"Number of labels: {labels.size}")
#     return labels

# def visualize_label_distribution(labels):
#     # 统计每个标签出现的频率
#     unique_labels, counts = np.unique(labels, return_counts=True)
    
#     # 打印标签和对应的数量
#     for label, count in zip(unique_labels, counts):
#         print(f"Label {label}: {count} points")
    
#     # 绘制标签分布图
#     plt.bar(unique_labels, counts)
#     plt.xlabel('Label')
#     plt.ylabel('Frequency')
#     plt.title('Label Distribution')
#     plt.show()

# if __name__ == "__main__":
#     # label_bin_file_path = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/SEG_RESULT/1716882060.699495_1716882060.699996.bin"  # 替换为你的 bin 文件路径
#     label_bin_file_path = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/PNT_BIN/1716882060.699495_1716882060.699996.bin"  # 替换为你的 bin 文件路径
#     # 读取标签文件
#     labels = read_label_bin_file(label_bin_file_path)
    
#     # 可视化标签分布
#     visualize_label_distribution(labels)
# # ---------------------------------------查看bin标签分布--------------------------------------


# # ---------------------------------------可视化.bin+.label对应的点云--------------------------------------
# import numpy as np
# import open3d as o3d
# import matplotlib.pyplot as plt

# def read_point_cloud_bin_file(file_path):
#     # 读取二进制点云文件
#     points = np.fromfile(file_path, dtype=np.float32)
    
#     # 假设每个点包含 [x, y, z, intensity] 四个值
#     points = points.reshape((-1, 4))[:, :3]  # 忽略 intensity 列
    
#     print(f"Number of points: {points.shape[0]}")
    
#     return points

# def read_label_file(file_path):
#     # 读取标签文件，假设每个标签为 uint32 类型
#     labels = np.fromfile(file_path, dtype=np.uint32)
#     print(f"Number of labels: {labels.size}")
    
#     return labels

# def extract_semantic_labels(labels):
#     # 提取低16位作为语义标签
#     semantic_labels = labels & 0xFFFF
#     return semantic_labels

# def visualize_point_cloud_with_labels(points, labels):
#     # 创建点云对象
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(points)
    
#     # 初始化颜色
#     colors = np.zeros((points.shape[0], 3))
    
#     # 根据标签设置颜色
#     unique_labels = np.unique(labels)
#     color_map = {label: np.random.rand(3) for label in unique_labels}
    
#     for i, label in enumerate(labels):
#         colors[i] = color_map[label]
    
#     pcd.colors = o3d.utility.Vector3dVector(colors)
    
#     # 可视化点云
#     o3d.visualization.draw_geometries([pcd])

# def visualize_label_distribution(labels):
#     # 统计每个标签出现的频率
#     unique_labels, counts = np.unique(labels, return_counts=True)
    
#     # 打印标签和对应的数量
#     for label, count in zip(unique_labels, counts):
#         print(f"Label {label}: {count} points")
    
#     # 绘制标签分布图
#     plt.bar(unique_labels, counts)
#     plt.xlabel('Label')
#     plt.ylabel('Frequency')
#     plt.title('Label Distribution')
#     plt.show()

# if __name__ == "__main__":
#     bin_file_path = "/media/edric/T7 Shield/semanticKitti/data_odometry_velodyne/dataset/sequences/01/velodyne/000000.bin"  # 替换为你的 bin 文件路径
#     label_file_path = "/media/edric/T7 Shield/semanticKitti/data_odometry_velodyne/dataset/sequences/01/labels/000000.label"   # 替换为你的 label 文件路径
    
#     # 读取点云和标签数据
#     points = read_point_cloud_bin_file(bin_file_path)
#     labels = read_label_file(label_file_path)
    
#     # 提取语义标签
#     semantic_labels = extract_semantic_labels(labels)
    
#     # 检查点的数量是否匹配
#     assert len(points) == len(semantic_labels), "点数和标签数不匹配"
    
#     # 可视化标签分布
#     visualize_label_distribution(semantic_labels)
    
#     # 可视化点云数据和标签
#     visualize_point_cloud_with_labels(points, semantic_labels)
# # ---------------------------------------可视化.bin+.label对应的点云--------------------------------------



# import pickle
# import numpy as np
# import open3d as o3d

# def read_bin_file(bin_file):
#     return np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)

# # 定义文件路径
# pkl_file_path = '/home/edric/PaSCo_Edric/gpfsscratch/rech/kvd/uyl37fq/pasco_preprocess/kitti/instance_labels_v2/01/000010_1_1.pkl'
# bin_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000010.bin'

# # 读取 .pkl 文件
# with open(pkl_file_path, 'rb') as f:
#     data = pickle.load(f)

# # 提取 instance_labels 和 semantic_labels
# instance_labels = data['instance_labels']
# semantic_labels = data['semantic_labels']

# # 读取点云 .bin 文件
# points = read_bin_file(bin_file_path)

# # 提取标签信息，将其与点云坐标结合
# colors = []
# for point in points:
#     x, y, z, intensity = point
#     ix, iy, iz = int(x), int(y), int(z)
#     if 0 <= ix < instance_labels.shape[0] and 0 <= iy < instance_labels.shape[1] and 0 <= iz < instance_labels.shape[2]:
#         instance_label = instance_labels[ix, iy, iz]
#         semantic_label = semantic_labels[ix, iy, iz]
#         color = [instance_label / np.max(instance_labels), 0, semantic_label / np.max(semantic_labels)]  # 颜色编码方式
#         colors.append(color)
#     else:
#         colors.append([0, 0, 0])  # 点在标签数据之外时的颜色

# # 将点和颜色转换为 numpy 数组
# points = points[:, :3]  # 只保留 x, y, z 坐标
# colors = np.array(colors)

# # 创建 Open3D 点云对象
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(colors)

# # 可视化点云
# o3d.visualization.draw_geometries([pcd], window_name='3D Point Cloud with Labels')

#测试torch-scatter
# import torch
# from torch_scatter import scatter_max

# src = torch.tensor([[2, 0, 1, 4, 3], [0, 2, 1, 3, 4]])
# index = torch.tensor([[4, 5, 4, 2, 3], [0, 0, 2, 2, 1]])

# out, argmax = scatter_max(src, index, dim=-1)
# print(out)
# # ---------------------------------------bin to label uint32------------------------------------------
import numpy as np
import os

# 读取二进制标签文件
file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels/000000.bin'
labels = np.fromfile(file_path, dtype=np.uint8)

# 生成输出文件路径
output_file_path = os.path.splitext(file_path)[0] + '.label'

# 将标签数据转换为 .label 文件
labels.astype(np.uint32).tofile(output_file_path)

print(f"标签文件已保存到: {output_file_path}")
# ---------------------------------------bin to label uint32------------------------------------------


# import pickle
# import numpy as np

# # 读取pickle文件
# file_path = '/home/edric/PaSCo_Edric/gpfsscratch/rech/kvd/uyl37fq/pasco_preprocess/kitti/instance_labels_v2/01/000000_1_1.pkl'

# def load_data(file_path):
#     with open(file_path, 'rb') as f:
#         data = pickle.load(f)
#     return data

# def print_data_info(data):
#     for key, value in data.items():
#         print(f"Key: {key}")
#         print(f"Shape: {value.shape}")
#         print(f"Data type: {value.dtype}")
#         print()

# # 读取数据
# data = load_data(file_path)

# # 打印数据信息
# print_data_info(data)

#----------------------------------bin voxelize------------------------------------------------------
# import os
# import numpy as np

# def read_bin_file(bin_file):
#     """读取点云bin文件"""
#     point_cloud = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)  # 点云数据格式为 (x, y, z, intensity)
#     return point_cloud

# def read_label_file(label_file):
#     """读取标签文件"""
#     labels = np.fromfile(label_file, dtype=np.uint32)
#     labels = labels.reshape(-1)  # 假设标签为1D数组
#     return labels

# def voxelize(point_cloud, labels, voxel_size, grid_size):
#     """将点云数据进行体素化处理"""
#     assert point_cloud.shape[0] == labels.shape[0], "Point cloud and labels must have the same length"
    
#     # 定义体素栅格的尺寸
#     voxel_grid = np.zeros(grid_size, dtype=np.float32)
#     invalid_grid = np.zeros(grid_size, dtype=np.uint8)
#     label_grid = np.zeros(grid_size, dtype=np.uint16)
#     occluded_grid = np.zeros(grid_size, dtype=np.int32)

#     # 计算点的体素索引
#     voxel_indices = (point_cloud[:, :3] // voxel_size).astype(np.int32)

#     # 确保索引在有效范围内
#     valid_indices = np.all((voxel_indices >= 0) & (voxel_indices < grid_size), axis=1)
#     voxel_indices = voxel_indices[valid_indices]
#     point_cloud = point_cloud[valid_indices]
#     labels = labels[valid_indices]

#     # 填充体素栅格
#     for idx, voxel_index in enumerate(voxel_indices):
#         voxel_grid[tuple(voxel_index)] += 1  # 可以根据需要调整
#         invalid_grid[tuple(voxel_index)] = 0  # 全部点标记为有效
#         label_grid[tuple(voxel_index)] = labels[idx]  # 标签

#     return voxel_grid, invalid_grid, label_grid, occluded_grid

# def save_voxel_grid(voxel_grid, invalid_grid, label_grid, occluded_grid, output_dir, frame_id):
#     """保存体素化结果"""
#     os.makedirs(output_dir, exist_ok=True)
#     voxel_grid.tofile(f"{output_dir}/{frame_id}.bin")
#     invalid_grid.tofile(f"{output_dir}/{frame_id}.invalid")
#     label_grid.tofile(f"{output_dir}/{frame_id}.label")
#     occluded_grid.tofile(f"{output_dir}/{frame_id}.occluded")

# def read_voxel_grid(output_dir, frame_id):
#     """读取并打印体素化结果的维度"""
#     voxel_grid = np.fromfile(f"{output_dir}/{frame_id}.bin", dtype=np.float32).reshape(256, 256, 32)
#     invalid_grid = np.fromfile(f"{output_dir}/{frame_id}.invalid", dtype=np.uint8).reshape(256, 256, 32)
#     label_grid = np.fromfile(f"{output_dir}/{frame_id}.label", dtype=np.uint16).reshape(256, 256, 32)
#     occluded_grid = np.fromfile(f"{output_dir}/{frame_id}.occluded", dtype=np.int32).reshape(256, 256, 32)

#     print("Voxel grid shape:", voxel_grid.shape)
#     print("Invalid grid shape:", invalid_grid.shape)
#     print("Label grid shape:", label_grid.shape)
#     print("Occluded grid shape:", occluded_grid.shape)

# def unpack(compressed):
#     ''' given a bit encoded voxel grid, make a normal voxel grid out of it.  '''
#     uncompressed = np.zeros(compressed.shape[0] * 8, dtype=np.uint8)
#     uncompressed[::8] = compressed[:] >> 7 & 1
#     uncompressed[1::8] = compressed[:] >> 6 & 1
#     uncompressed[2::8] = compressed[:] >> 5 & 1
#     uncompressed[3::8] = compressed[:] >> 4 & 1
#     uncompressed[4::8] = compressed[:] >> 3 & 1
#     uncompressed[5::8] = compressed[:] >> 2 & 1
#     uncompressed[6::8] = compressed[:] >> 1 & 1
#     uncompressed[7::8] = compressed[:] & 1
#     return uncompressed

# def _read_SemKITTI(path, dtype, do_unpack):
#     bin = np.fromfile(path, dtype=dtype)  # Flattened array
#     if do_unpack:
#         bin = unpack(bin)
#     return bin

# def _read_invalid_SemKITTI(path):
#     invalid = _read_SemKITTI(path, dtype=np.uint8, do_unpack=False)
#     print(f"invalid shape:",invalid.shape)
#     return invalid

    

# 示例用法
# def main():
#     bin_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin'
#     label_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels/000000.label'
#     output_dir = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels'
#     frame_id = '000000'

#     point_cloud = read_bin_file(bin_file)
#     labels = read_label_file(label_file)

#     # _read_invalid_SemKITTI(path="/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels/000000.invalid")

#     print(f"Point cloud length: {point_cloud.shape[0]}")
#     print(f"Labels length: {labels.shape[0]}")

#     assert point_cloud.shape[0] == labels.shape[0], "Point cloud and labels must have the same length"

#     voxel_size = 0.2
#     grid_size = (256, 256, 32)

#     voxel_grid, invalid_grid, label_grid, occluded_grid = voxelize(point_cloud, labels, voxel_size, grid_size)

#     # 默认情况下，所有体素都没有遮挡
#     occluded_grid.fill(0)

#     save_voxel_grid(voxel_grid, invalid_grid, label_grid, occluded_grid, output_dir, frame_id)
#     read_voxel_grid(output_dir, frame_id)

# if __name__ == "__main__":
#     main()


#-------------------------------bin voxelize---------------------------------------------------------

# pcd转bin
# import open3d as o3d
# import numpy as np

# def convert_pcd_to_bin_xyz(pcd_file, bin_file):
#     # 读取 PCD 文件
#     pcd = o3d.io.read_point_cloud(pcd_file)
    
#     # 获取点云数据的 x, y, z 坐标
#     points = np.asarray(pcd.points)
    
#     # 将点云数据（x, y, z）保存为 BIN 文件
#     points.astype(np.float32).tofile(bin_file)

# # 示例用法
# convert_pcd_to_bin_xyz("/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_third_ann_data/clip_rino_107_11/POINTS/1716882060.699495_1716882060.699996.pcd",
#                     "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin")


#查看点云bin和label bin匹配
# import numpy as np

# def read_point_cloud_bin(bin_file):
#     """读取点云bin文件，假设数据格式为 (x, y, z, intensity)"""
#     point_cloud = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)
#     return point_cloud

# def read_label_bin(bin_file):
#     """读取标签bin文件"""
#     labels = np.fromfile(bin_file, dtype=np.uint8).reshape(-1)
#     return labels

# def check_point_cloud_and_labels_length(point_cloud_file, label_file):
#     """检查点云和标签数据的长度是否一致"""
#     point_cloud = read_point_cloud_bin(point_cloud_file)
#     labels = read_label_bin(label_file)

#     point_cloud_length = point_cloud.shape[0]
#     labels_length = labels.shape[0]

#     print(f"Point cloud length: {point_cloud_length}")
#     print(f"Labels length: {labels_length}")

#     if point_cloud_length != labels_length:
#         print("Error: Point cloud and labels lengths do not match!")
#     else:
#         print("Success: Point cloud and labels lengths match!")

# # 示例用法
# def main():
#     # point_cloud_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin'
#     # point_cloud_file = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/PNT_BIN/1716882060.699495_1716882060.699996.bin'
#     # label_file = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/SEG_RESULT/1716882060.699495_1716882060.699996.bin'
#     point_cloud_file = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/PNT_BIN/1716882061.099498_1716882061.099996.bin'
#     label_file = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/SEG_RESULT/1716882061.099498_1716882061.099996.bin'
#     check_point_cloud_and_labels_length(point_cloud_file, label_file)

# if __name__ == "__main__":
#     main()

#查看bin的维度和数据
# import numpy as np
# def analyze_bin_file(bin_file, point_dim=4):
#     # 读取 BIN 文件
#     data = np.fromfile(bin_file, dtype=np.float32)
    
#     # 计算点的数量
#     num_points = data.size // point_dim
    
#     # 重新调整数据的形状
#     points = data.reshape((num_points, point_dim))
    
#     # 打印点的数量和每个点的维度
#     print(f"Number of points: {num_points}")
#     print(f"Dimensions of each point: {points.shape[1]}")
    
#     # 打印第一个点的数据
#     print(f"First point data: {points[0]}")
    
#     # 获取第四个维度的数据
#     fourth_dim = points[:, 3]
    
#     # 分析第四个维度的数值范围和特性
#     print(f"Fourth dimension - min: {fourth_dim.min()}, max: {fourth_dim.max()}")
#     print(f"Fourth dimension - mean: {fourth_dim.mean()}, std: {fourth_dim.std()}")
    
#     # 打印前10个第四维度的值
#     print(f"First 10 values of the fourth dimension: {fourth_dim[:10]}")

#     return points

# # 示例用法
# points = analyze_bin_file('/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin')

#uint8转uint32 label
# import numpy as np

# def convert_bin_to_label(input_bin_file, output_label_file):
#     # 读取 uint8 形式的 BIN 文件
#     data_uint8 = np.fromfile(input_bin_file, dtype=np.uint8)
    
#     # 将数据转换为 uint32
#     data_uint32 = data_uint8.astype(np.uint32)
    
#     # 将转换后的数据保存为 .label 文件
#     data_uint32.tofile(output_label_file)
    
#     print(f"Conversion complete. Data saved to {output_label_file}")

# # 示例用法
# convert_bin_to_label("/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/SEG_RESULT/1716882060.699495_1716882060.699996.bin", 
#                         "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels/000000.label")

#点云bin加一列强度0
# import numpy as np

# def add_intensity_to_point_cloud(input_file, output_file):
#     # 读取原始点云数据
#     point_cloud = np.fromfile(input_file, dtype=np.float32).reshape(-1, 3)

#     # 创建全零的intensity特征
#     intensity = np.zeros((point_cloud.shape[0], 1), dtype=np.float32)

#     # 将intensity添加到点云数据
#     point_cloud_with_intensity = np.hstack((point_cloud, intensity))

#     # 将带有intensity的点云数据保存为bin文件
#     point_cloud_with_intensity.tofile(output_file)

#     # 验证数据是否正确
#     loaded_point_cloud = np.fromfile(output_file, dtype=np.float32).reshape(-1, 4)
#     assert np.all(loaded_point_cloud[:, 3] == 0), "Intensity values are not zero!"
#     print("Intensity values are correctly set to zero.")

# # 示例用法
# input_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000-old.bin'
# output_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin'
# add_intensity_to_point_cloud(input_file, output_file)


#————————————————————————————————————————可视化pkl-----------------------------------------
# import os
# import pickle
# import numpy as np
# import open3d as o3d

# def visualize_pkl(filepath):
#     # 读取PKL文件
#     with open(filepath, 'rb') as handle:
#         data = pickle.load(handle)
    
#     # 获取点云数据和场景补全预测
#     xyz = data['xyz']
#     ssc_pred = data['ssc_pred']
    
#     # 打印ssc_pred的形状
#     print("Shape of ssc_pred:", ssc_pred.shape)
    
#     # 可视化点云数据
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(xyz)
#     colors = np.zeros_like(xyz)
#     colors[:, 2] = 1  # 将颜色设置为蓝色
#     pcd.colors = o3d.utility.Vector3dVector(colors)
    
#     # 显示点云
#     o3d.visualization.draw_geometries([pcd], window_name="Point Cloud")

#     # 可视化场景补全数据
#     if ssc_pred.ndim == 4:
#         # 提取第一个三维切片
#         ssc_pred = ssc_pred[0]
#     elif ssc_pred.ndim != 3:
#         raise ValueError("ssc_pred needs to be a 3-dimensional array or convertible to 3D")
    
#     # 创建体素网格
#     voxel_size = 0.1  # 你可以根据需要调整体素大小
#     voxel_centers = []

#     for i in range(ssc_pred.shape[0]):
#         for j in range(ssc_pred.shape[1]):
#             for k in range(ssc_pred.shape[2]):
#                 if ssc_pred[i, j, k] > 0:
#                     voxel_centers.append([i * voxel_size, j * voxel_size, k * voxel_size])

#     # 将体素中心点转换为点云
#     voxel_centers = np.array(voxel_centers)
#     voxel_cloud = o3d.geometry.PointCloud()
#     voxel_cloud.points = o3d.utility.Vector3dVector(voxel_centers)

#     # 创建体素网格
#     voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(voxel_cloud, voxel_size)

#     # 显示体素网格
#     o3d.visualization.draw_geometries([voxel_grid], window_name="Scene Completion")

# filepath = "/home/edric/PaSCo_Edric/output_v1/000000_1.pkl"
# visualize_pkl(filepath)
#————————————————————————————————————————可视化pkl-----------------------------------------

#----可视化bin
# import open3d as o3d
# import numpy as np

# # 读取二进制文件
# bin_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin'
# point_cloud_data = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)

# # 创建Open3D点云对象
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(point_cloud_data[:, :3])  # 只取XYZ坐标

# # 可视化点云
# o3d.visualization.draw_geometries([pcd])

# import open3d as o3d

# # 读取PCD文件
# pcd_file_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_third_ann_data/clip_rino_107_11/POINTS/1716882060.699495_1716882060.699996.pcd'
# pcd = o3d.io.read_point_cloud(pcd_file_path)

# # 可视化点云
# o3d.visualization.draw_geometries([pcd])

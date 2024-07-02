# import numpy as np

# # 读取点云的 .bin 文件
# def load_point_cloud_from_bin(bin_file_path):
#     # 假设每个点包含四个浮点数：x, y, z, intensity
#     point_cloud = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)
#     return point_cloud

# # 计算点云数据的最大值和最小值
# def calculate_extent(point_cloud):
#     min_vals = np.min(point_cloud[:, :3], axis=0)  # 仅计算 x, y, z 的最小值
#     max_vals = np.max(point_cloud[:, :3], axis=0)  # 仅计算 x, y, z 的最大值
#     return min_vals, max_vals


# bin_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01-10/velodyne/000000.bin'
# point_cloud = load_point_cloud_from_bin(bin_file_path)
# min_extent, max_extent = calculate_extent(point_cloud)

# print("Point Cloud Data Range:")
# print(f"X axis: min = {min_extent[0]}, max = {max_extent[0]}")
# print(f"Y axis: min = {min_extent[1]}, max = {max_extent[1]}")
# print(f"Z axis: min = {min_extent[2]}, max = {max_extent[2]}")

# # 定义 max_extent 和 min_extent 参数
# max_extent_tuple = tuple(max_extent)
# min_extent_array = min_extent

# print(f"self.max_extent = {max_extent_tuple}")
# print(f"self.min_extent = np.array({min_extent_array})") #        self.max_extent = (78.84611, 73.6959, 2.9085882) self.min_extent = np.array([-77.91836, -74.92033, -6.454987])

import numpy as np

# 读取点云的 .bin 文件
def load_point_cloud_from_bin(bin_file_path):
    # 假设每个点包含四个浮点数：x, y, z, intensity
    point_cloud = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)
    return point_cloud

# 计算点云数据的范围，去掉前n个最小值和后n个最大值
def calculate_trimmed_extent(point_cloud, trim_count=50):
    x_sorted = np.sort(point_cloud[:, 0])
    y_sorted = np.sort(point_cloud[:, 1])
    z_sorted = np.sort(point_cloud[:, 2])
    
    min_vals = np.array([x_sorted[trim_count], y_sorted[trim_count], z_sorted[trim_count]])
    max_vals = np.array([x_sorted[-trim_count - 1], y_sorted[-trim_count - 1], z_sorted[-trim_count - 1]])
    
    return min_vals, max_vals

# 文件路径
bin_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01-10/velodyne/000000.bin'

# 读取点云数据
point_cloud = load_point_cloud_from_bin(bin_file_path)

# 计算修剪后的范围
min_extent, max_extent = calculate_trimmed_extent(point_cloud)

print("Trimmed Point Cloud Data Range:")
print(f"X axis: min = {min_extent[0]}, max = {max_extent[0]}")
print(f"Y axis: min = {min_extent[1]}, max = {max_extent[1]}")
print(f"Z axis: min = {min_extent[2]}, max = {max_extent[2]}")

# 定义 max_extent 和 min_extent 参数
max_extent_tuple = tuple(max_extent)
min_extent_array = tuple(min_extent)

print(f"self.max_extent = {max_extent_tuple}")
print(f"self.min_extent = np.array({min_extent_array})")

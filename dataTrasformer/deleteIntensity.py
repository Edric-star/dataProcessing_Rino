import os
import numpy as np

def process_bin_file(filepath, output_filepath=None):
    # 读取点云数据
    point_cloud = np.fromfile(filepath, dtype=np.float32).reshape(-1, 4)
    
    # 将强度信息（第四列）设置为0
    point_cloud[:, 3] = 0.0
    
    # 保存修改后的点云数据
    if output_filepath:
        point_cloud.tofile(output_filepath)
    else:
        point_cloud.tofile(filepath)

def process_all_bin_files(input_folder, output_folder=None):
    # 获取文件夹中所有的 .bin 文件
    bin_files = [f for f in os.listdir(input_folder) if f.endswith('.bin')]
    
    for bin_file in bin_files:
        input_filepath = os.path.join(input_folder, bin_file)
        
        if output_folder:
            output_filepath = os.path.join(output_folder, bin_file)
            os.makedirs(output_folder, exist_ok=True)
        else:
            output_filepath = None
        
        print(f"Processing file: {input_filepath}")
        process_bin_file(input_filepath, output_filepath)
        print(f"Finished processing file: {input_filepath}")

# 示例用法
input_folder = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne_withintensity'  # 修改为实际的输入文件夹路径
output_folder = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne'  # 修改为实际的输出文件夹路径，若覆盖原文件则设为 None

# 处理所有 .bin 文件
process_all_bin_files(input_folder, output_folder)

import os
import shutil
import numpy as np

# 原标签映射
original_to_name = {
    0: 'road',
    1: 'sidewalk',
    2: 'building',
    3: 'fence',
    4: 'pole',
    5: 'traffic-sign',
    6: 'vegetation',
    7: 'terrain',
    8: 'car',
    9: 'traffic_cone',
    10: 'truck',
    11: 'bus',
    12: 'bicycle',
    13: 'person',
    14: "construction_vehicle",
    15: "TRICYCLE",
    16: "trailer",
    17: "barrier",
    18: "UNKNOWN",
    19: "free"
}

# 新标签映射
name_to_new = {
    "unlabeled": 0,
    "free": 0,
    "outlier": 1,
    "car": 10,
    "bicycle": 11,
    "bus": 13,
    "motorcycle": 15,
    "TRICYCLE": 15,
    "on-rails": 16,
    "truck": 18,
    "trailer": 18,
    "construction_vehicle": 18,
    "other-vehicle": 20,
    "person": 30,
    "bicyclist": 31,
    "motorcyclist": 32,
    "road": 40,
    "parking": 44,
    "sidewalk": 48,
    "other-ground": 49,
    "building": 50,
    "fence": 51,
    "other-structure": 52,
    "lane-marking": 60,
    "vegetation": 70,
    "trunk": 71,
    "terrain": 72,
    "pole": 80,
    "traffic-sign": 81,
    "UNKNOWN": 99,
    "barrier": 99,
    'traffic_cone': 99,
    "other-object": 99,
    "moving-car": 252,
    "moving-bicyclist": 253,
    "moving-person": 254,
    "moving-motorcyclist": 255,
    "moving-on-rails": 256,
    "moving-bus": 257,
    "moving-truck": 258,
    "moving-other-vehicle": 259
}

# 将原标签映射到新标签的字典
original_to_new = {key: name_to_new[original_to_name[key]] for key in original_to_name}

def read_label_file(file_path):
    # 读取 .label 文件并返回标签数组（uint32）
    labels = np.fromfile(file_path, dtype=np.uint32)
    return labels

def write_label_file(file_path, labels):
    # 将新的标签数组（uint32）写入新的 .label 文件
    labels.tofile(file_path)

def map_labels(labels, mapping, default_value=0):
    # 使用提供的映射字典转换标签，并处理缺失标签
    new_labels = np.vectorize(lambda x: mapping.get(x, default_value))(labels)
    return new_labels.astype(np.uint32)

def rename_and_move_files(input_folder1, input_folder2, output_folder):
    # 获取所有clip文件夹，并按从小到大的顺序排序
    clip_folders = sorted(os.listdir(input_folder1), key=lambda x: int(x.split('_')[-1]))

    for clip_index, clip_folder in enumerate(clip_folders):
        # 新clip文件夹名
        new_clip_name = f"{clip_index:02d}"
        new_clip_folder_velodyne = os.path.join(output_folder, new_clip_name, 'velodyne')
        new_clip_folder_labels = os.path.join(output_folder, new_clip_name, 'labels')

        # 创建新的clip文件夹
        os.makedirs(new_clip_folder_velodyne, exist_ok=True)
        os.makedirs(new_clip_folder_labels, exist_ok=True)

        # 获取当前clip文件夹路径
        current_clip_folder1 = os.path.join(input_folder1, clip_folder)
        current_clip_folder2 = os.path.join(input_folder2, clip_folder)

        # 获取当前clip文件夹中的文件，并按从小到大的顺序排序
        bin_files = sorted(os.listdir(current_clip_folder1))
        label_files = sorted(os.listdir(current_clip_folder2))

        for file_index, (bin_file, label_file) in enumerate(zip(bin_files, label_files)):
            # 新文件名
            new_file_name = f"{file_index:06d}.bin"
            new_label_name = f"{file_index:06d}.label"

            # 构造新文件路径
            new_file_path = os.path.join(new_clip_folder_velodyne, new_file_name)
            new_label_path = os.path.join(new_clip_folder_labels, new_label_name)

            # 复制并重命名bin文件
            shutil.copy2(os.path.join(current_clip_folder1, bin_file), new_file_path)
            
            # 处理label文件并保存
            input_label_path = os.path.join(current_clip_folder2, label_file)
            labels = read_label_file(input_label_path)
            new_labels = map_labels(labels, original_to_new)
            write_label_file(new_label_path, new_labels)

            print(f"Processed and moved {clip_folder} to {new_clip_name}")

# 输入文件夹路径
input_folder1 = "/home/edric/dataProcess/clip_rino_107_float32bin_removeCM"
input_folder2 = "/home/edric/dataProcess/clip_rino_107_uint32label_removeCM"

# 输出文件夹路径
output_folder = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences"

# 运行函数
rename_and_move_files(input_folder1, input_folder2, output_folder)

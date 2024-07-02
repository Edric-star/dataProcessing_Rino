import numpy as np
import os
# def read_label_file(file_path):
#     # 读取文件中的数据
#     labels = np.fromfile(file_path, dtype=np.uint32)
#     return labels

# def extract_labels(labels):
#     # 假设标签存储在每个32位整数的低16位
#     semantic_labels = labels & 0xFFFF
#     return semantic_labels

# def display_labels(labels):
#     unique_labels = np.unique(labels)
#     print("Unique labels in the file:")
#     for label in unique_labels:
#         print(label)

# # 文件路径 000000里面有14种 0-9 12 13 15 18
# label_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels/000000.label'

# # 读取标签文件
# labels = read_label_file(label_file_path)

# # 提取并显示标签
# semantic_labels = extract_labels(labels)
# display_labels(semantic_labels)

# -----------------------------------------------


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

def process_folder(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 处理文件夹中的所有 .label 文件
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.label'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_folder, file)
                labels = read_label_file(input_file_path)
                new_labels = map_labels(labels, original_to_new)
                write_label_file(output_file_path, new_labels)
                print(f"Processed {input_file_path} -> {output_file_path}")

# 文件夹路径
input_folder_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels_original'
output_folder_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels'
process_folder(input_folder_path, output_folder_path)


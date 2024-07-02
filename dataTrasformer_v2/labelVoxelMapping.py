import numpy as np
import pickle
import os

# 原标签映射
original_to_name = {
    0: "empty",  # 空体素
    1: "car",
    2: "bicycle",
    3: "motorcycle",
    4: "truck",
    5: "other-vehicle",
    6: "person",
    7: "bicyclist",
    8: "motorcyclist",
    9: "road",
    10: "parking",
    11: "sidewalk",
    12: "other-ground",
    13: "building",
    14: "fence",
    15: "vegetation",
    16: "trunk",
    17: "terrain",
    18: "pole",
    19: "traffic-sign"
}

# 新标签映射
name_to_new = {
    'road': 0,
    'sidewalk': 1,
    'parking': 1,
    'other-ground': 1,
    'building': 2,
    'fence': 3,
    'pole': 4,
    'traffic-sign': 5,
    'vegetation': 6,
    'trunk': 6,
    'terrain': 7,
    'car': 8,
    'traffic_cone': 9,
    'truck': 10,
    'bus': 11,
    'other-vehicle': 11,
    'bicycle': 12,
    'motorcycle': 12,
    'person': 13,
    'bicyclist': 13,
    'motorcyclist': 13,
    'construction_vehicle': 14,
    'trailer': 16,
    'barrier': 17,
    'UNKNOWN': 18,
    'empty': 19,
    'free': 19  # free
}

input_dir = '/home/edric/new_space/output'
output_dir = '/home/edric/dataProcess/ssc_pred_ourLabel'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 遍历每个序列文件夹（00-26）
for seq_num in range(27):
    seq_dir = os.path.join(input_dir, f'{seq_num:02}')
    output_seq_dir = os.path.join(output_dir, f'{seq_num:02}')
    
    # 确保输出序列目录存在
    os.makedirs(output_seq_dir, exist_ok=True)
    
    # 遍历该序列文件夹中的所有 .pkl 文件
    for filename in os.listdir(seq_dir):
        if filename.endswith('.pkl'):
            input_filepath = os.path.join(seq_dir, filename)
            output_filepath = os.path.join(output_seq_dir, filename)
            
            # 读取SSC预测结果
            with open(input_filepath, 'rb') as handle:
                data = pickle.load(handle)
            ssc_pred = data['ssc_pred'][0]  # 256x256x32的体素预测结果

            # 创建一个新的标签映射数组，初始化为原始标签
            new_ssc_pred = np.copy(ssc_pred)

            # 遍历原标签并进行映射，包括空体素
            for original_label, name in original_to_name.items():
                if name in name_to_new:
                    new_label = name_to_new[name]
                    new_ssc_pred[ssc_pred == original_label] = new_label
                else:
                    # 如果标签名称不在name_to_new字典中将其标签设为255
                    new_ssc_pred[ssc_pred == original_label] = 255

            # 保存新的标签映射结果
            with open(output_filepath, 'wb') as handle:
                pickle.dump({'ssc_pred': new_ssc_pred}, handle)  # 直接保存为数组，而不是列表

            print(f"Processed {input_filepath} and saved to {output_filepath}")

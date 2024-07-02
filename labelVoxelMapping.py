import numpy as np
import pickle

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
    'bicycle': 12,
    'motorcycle': 12,
    'person': 13,
    'bicyclist': 13,
    'motorcyclist': 13,
    'construction_vehicle': 14,
    'other-vehicle': 15,  # tricycle
    'trailer': 16,
    'barrier': 17,
    'parking': 18,  # unknown
    'other-ground': 18,
    'UNKNOWN': 18,
    'free': 19  # free
}

# 读取SSC预测结果
pkl_filepath = '/home/edric/PaSCo_Edric/output_v1/000000_1.pkl'
with open(pkl_filepath, 'rb') as handle:
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
        # 如果标签名称不在name_to_new字典中（例如"empty"），将其标签设为255
        new_ssc_pred[ssc_pred == original_label] = 255

# 打印部分结果以验证映射
print("Original labels in ssc_pred:\n", np.unique(ssc_pred))
print("New labels in new_ssc_pred:\n", np.unique(new_ssc_pred))

# 保存新的标签映射结果
output_filepath = '/home/edric/dataProcess/ssc_pred_ourLabel/000000_1.pkl'
with open(output_filepath, 'wb') as handle:
    pickle.dump({'ssc_pred': new_ssc_pred}, handle)  # 直接保存为数组，而不是列表

print(f"New SSC prediction with updated labels saved to {output_filepath}")

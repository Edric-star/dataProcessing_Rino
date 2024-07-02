import os
import json

def flatten_matrix(matrix):
    """将4x4矩阵的前三行铺平成一行12个数据"""
    return [item for row in matrix[:3] for item in row]

def process_json(json_file, points_folder, output_file):
    # 读取JSON文件
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # 获取POINTS文件夹中的所有.pcd文件名（包括扩展名）
    pcd_files = {f for f in os.listdir(points_folder) if f.endswith('.pcd')}
    
    results = []

    for key, value in data.items():
        if key.startswith("POINTS/") and key.split('/')[-1] in pcd_files:
            matrix = value.get("mtx_4d")
            if matrix:
                flattened = flatten_matrix(matrix)
                results.append(flattened)
    
    # 将结果写入输出文件
    with open(output_file, 'w') as f:
        for result in results:
            f.write(' '.join(map(str, result)) + '\n')

# 文件路径
json_file = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_third_ann_data/clip_rino_107_11/meta/pose_info.json'  # 修改为你的JSON文件路径
points_folder = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_third_ann_data/clip_rino_107_11/POINTS'  # 修改为你的POINTS文件夹路径
output_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/poses.txt'  # 输出文件路径

# 处理文件
process_json(json_file, points_folder, output_file)

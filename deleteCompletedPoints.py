import numpy as np

def read_point_cloud_bin(file_path):
    # 读取包含点云数据的 bin 文件
    point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)  # 假设点云数据每行有4个值 (x, y, z, intensity)
    return point_cloud

def read_label_bin(file_path):
    # 读取Instruction标签 bin 文件
    labels = np.fromfile(file_path, dtype=np.uint8)
    return labels

def read_semantic_label(file_path):
    # 读取语义标签 label 文件
    semantic_labels = np.fromfile(file_path, dtype=np.uint32)
    return semantic_labels

def save_point_cloud_bin(file_path, point_cloud):
    # 将点云数据保存到 bin 文件
    point_cloud.tofile(file_path)

def save_semantic_label(file_path, semantic_labels):
    # 将语义标签数据保存到 label 文件
    semantic_labels.tofile(file_path)

def filter_points_by_labels(point_cloud, labels, semantic_labels, labels_to_remove):
    # 删除标签在 labels_to_remove 中的点
    mask = ~np.isin(labels, labels_to_remove)
    filtered_point_cloud = point_cloud[mask]
    filtered_labels = labels[mask]
    filtered_semantic_labels = semantic_labels[mask]
    return filtered_point_cloud, filtered_labels, filtered_semantic_labels

def main(point_cloud_file_path, label_file_path, semantic_label_file_path, output_point_cloud_file_path, output_semantic_label_file_path, labels_to_remove):
    # 读取点云数据、标签数据和语义标签数据
    point_cloud = read_point_cloud_bin(point_cloud_file_path)
    labels = read_label_bin(label_file_path)
    semantic_labels = read_semantic_label(semantic_label_file_path)
    
    # 检查读取的数据是否匹配
    if point_cloud.shape[0] != labels.shape[0] or point_cloud.shape[0] != semantic_labels.shape[0]:
        raise ValueError("点云数据、标签数据和语义标签数据的点数不匹配")
    
    # 打印删除前的点数
    print(f"删除前的点数: {point_cloud.shape[0]}")
    print(f"删除前语义标签的数量: {semantic_labels.shape[0]}")
    
    # 删除标签在 labels_to_remove 中的点
    filtered_point_cloud, filtered_labels, filtered_semantic_labels = filter_points_by_labels(point_cloud, labels, semantic_labels, labels_to_remove)
    
    # 打印删除后的点数
    print(f"删除后的点数: {filtered_point_cloud.shape[0]}")
    print(f"删除后语义标签的数量: {filtered_semantic_labels.shape[0]}")
    
    # 保存过滤后的点云数据和语义标签数据
    save_point_cloud_bin(output_point_cloud_file_path, filtered_point_cloud)
    save_semantic_label(output_semantic_label_file_path, filtered_semantic_labels)
    print(f"过滤后的点云数据已保存到 {output_point_cloud_file_path}")
    print(f"过滤后的语义标签数据已保存到 {output_semantic_label_file_path}")

# 文件路径
#原始带有补全地面点的点云
point_cloud_file_path = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne_withcm/000000.bin"
#带地面补全的标签
label_file_path = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels_original_bin/1716882060.699495_1716882060.699996.bin"
#原始带有补全地面点的点云的语义标签
semantic_label_file_path = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels_originalwithcm/000000.label"
#输出
#去掉补全点的点云
output_point_cloud_file_path = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin"
#去掉补全点的语义标签
output_semantic_label_file_path = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels_original/000000.label"

# 要删除的标签
labels_to_remove = [7, 9]

# 运行主函数
main(point_cloud_file_path, label_file_path, semantic_label_file_path, output_point_cloud_file_path, output_semantic_label_file_path, labels_to_remove)

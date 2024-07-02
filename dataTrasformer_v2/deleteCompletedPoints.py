import os
import numpy as np

def read_point_cloud_bin(file_path):
    point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    return point_cloud

def read_label_bin(file_path):
    labels = np.fromfile(file_path, dtype=np.uint8)
    return labels

def read_semantic_label(file_path):
    semantic_labels = np.fromfile(file_path, dtype=np.uint32)
    return semantic_labels

def save_point_cloud_bin(file_path, point_cloud):
    point_cloud.tofile(file_path)

def save_semantic_label(file_path, semantic_labels):
    semantic_labels.tofile(file_path)

def filter_points_by_labels(point_cloud, labels, semantic_labels, labels_to_remove):
    mask = ~np.isin(labels, labels_to_remove)
    filtered_point_cloud = point_cloud[mask]
    filtered_labels = labels[mask]
    filtered_semantic_labels = semantic_labels[mask]
    return filtered_point_cloud, filtered_labels, filtered_semantic_labels

def process_files(input_point_cloud_folder, input_label_folder, input_semantic_label_folder, output_point_cloud_folder, output_semantic_label_folder, labels_to_remove):
    if not os.path.exists(output_point_cloud_folder):
        os.makedirs(output_point_cloud_folder)
    if not os.path.exists(output_semantic_label_folder):
        os.makedirs(output_semantic_label_folder)

    for clip_folder in os.listdir(input_point_cloud_folder):
        point_cloud_clip_path = os.path.join(input_point_cloud_folder, clip_folder)
        label_clip_path = os.path.join(input_label_folder, clip_folder, 'pnt_instruction')
        semantic_label_clip_path = os.path.join(input_semantic_label_folder, clip_folder)

        if os.path.isdir(point_cloud_clip_path) and os.path.isdir(label_clip_path) and os.path.isdir(semantic_label_clip_path):
            output_point_cloud_clip_path = os.path.join(output_point_cloud_folder, clip_folder)
            output_semantic_label_clip_path = os.path.join(output_semantic_label_folder, clip_folder)

            if not os.path.exists(output_point_cloud_clip_path):
                os.makedirs(output_point_cloud_clip_path)
            if not os.path.exists(output_semantic_label_clip_path):
                os.makedirs(output_semantic_label_clip_path)

            point_cloud_files = set(os.listdir(point_cloud_clip_path))
            label_files = set(os.listdir(label_clip_path))
            semantic_label_files = set(os.listdir(semantic_label_clip_path))

            # 提取基础文件名（去掉扩展名后的部分）
            point_cloud_basenames = {os.path.splitext(f)[0] for f in point_cloud_files}
            label_basenames = {os.path.splitext(f)[0] for f in label_files}
            semantic_label_basenames = {os.path.splitext(f)[0] for f in semantic_label_files}

            # 找到共有的基础文件名
            common_basenames = point_cloud_basenames.intersection(label_basenames, semantic_label_basenames)

            print(f"在 {clip_folder} 中共找到 {len(common_basenames)} 个共有文件")

            for basename in common_basenames:
                point_cloud_file_path = os.path.join(point_cloud_clip_path, basename + '.bin')
                label_file_path = os.path.join(label_clip_path, basename + '.bin')
                semantic_label_file_path = os.path.join(semantic_label_clip_path, basename + '.label')

                output_point_cloud_file_path = os.path.join(output_point_cloud_clip_path, basename + '.bin')
                output_semantic_label_file_path = os.path.join(output_semantic_label_clip_path, basename + '.label')

                # 读取数据
                print(f"正在处理 {clip_folder} 中的 {basename} ...")
                try:
                    point_cloud = read_point_cloud_bin(point_cloud_file_path)
                    labels = read_label_bin(label_file_path)
                    semantic_labels = read_semantic_label(semantic_label_file_path)
                except Exception as e:
                    print(f"读取文件 {basename} 失败: {e}")
                    continue

                if point_cloud.shape[0] != labels.shape[0] or point_cloud.shape[0] != semantic_labels.shape[0]:
                    print(f"点云数据、标签数据和语义标签数据的点数不匹配: {basename}")
                    continue

                # 打印删除前的点数
                print(f"{basename}: 删除前的点数: {point_cloud.shape[0]}")
                print(f"{basename}: 删除前语义标签的数量: {semantic_labels.shape[0]}")

                # 删除标签在 labels_to_remove 中的点
                filtered_point_cloud, filtered_labels, filtered_semantic_labels = filter_points_by_labels(point_cloud, labels, semantic_labels, labels_to_remove)

                # 打印删除后的点数
                print(f"{basename}: 删除后的点数: {filtered_point_cloud.shape[0]}")
                print(f"{basename}: 删除后语义标签的数量: {filtered_semantic_labels.shape[0]}")

                # 保存过滤后的点云数据和语义标签数据
                save_point_cloud_bin(output_point_cloud_file_path, filtered_point_cloud)
                save_semantic_label(output_semantic_label_file_path, filtered_semantic_labels)
                print(f"{basename}: 过滤后的点云数据已保存到 {output_point_cloud_file_path}")
                print(f"{basename}: 过滤后的语义标签数据已保存到 {output_semantic_label_file_path}")

# 文件夹路径
input_point_cloud_folder = "/home/edric/dataProcess/clip_rino_107_float32bin"
input_label_folder = "/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/others_info"
input_semantic_label_folder = "/home/edric/dataProcess/clip_rino_107_uint32label"
output_point_cloud_folder = "/home/edric/dataProcess/clip_rino_107_float32bin_removeCM"
output_semantic_label_folder = "/home/edric/dataProcess/clip_rino_107_uint32label_removeCM"

# 要删除的标签，打在本车上面的点和补盲雷达的点
labels_to_remove = [0, 3, 7]

# 运行主函数处理文件夹中的所有文件
process_files(input_point_cloud_folder, input_label_folder, input_semantic_label_folder, output_point_cloud_folder, output_semantic_label_folder, labels_to_remove)

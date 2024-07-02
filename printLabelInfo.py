import numpy as np
import os
def read_label_file(file_path):
    # 读取文件中的数据
    # labels = np.fromfile(file_path, dtype=np.uint16)
    labels = np.fromfile(file_path, dtype=np.uint32)
    return labels

def extract_labels(labels):
    # 假设标签存储在每个32位整数的低16位
    # semantic_labels = labels
    semantic_labels = labels & 0xFFFF
    return semantic_labels

def display_labels(labels):
    unique_labels = np.unique(labels)
    print("Unique labels in the file:")
    for label in unique_labels:
        print(label)

# 文件路径 000000里面有14种 0-9 12 13 15 18
# label_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/07/labels/000000.label'
label_file_path = '/home/edric/dataProcess/clip_rino_107_uint32label_removeCM/clip_rino_107_2/1716881340.699492_1716881340.699335.label'
# label_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels/000000.label'
# label_file_path = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01-10/voxels/000000.label'
# label_file_path = '/home/edric/dataProcess/voxel_label_mapped/000000.label'
# 读取标签文件
labels = read_label_file(label_file_path)
unique_labels = np.unique(labels)
print(labels.shape)
print(unique_labels)


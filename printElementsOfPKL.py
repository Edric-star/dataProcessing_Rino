import os
import pickle
import numpy as np
def read_and_print_xyz(filepath):
    # 读取PKL文件
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
    
    # 获取xyz数据
    xyz = data['xyz']
    
    # 打印xyz的数据和元素数量
    print("Shape of xyz:", xyz.shape)
    print("Number of elements in xyz:", xyz.size)



def print_pkl_keys(filepath):
    # 读取PKL文件
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
    
    # 打印所有标签
    print("Keys in the PKL file:", list(data.keys()))

def count_points_in_bin(filepath):
    # 读取bin文件
    point_cloud = np.fromfile(filepath, dtype=np.float32)
    # 每个点包含4个float32数值（x, y, z, intensity）
    point_count = point_cloud.shape[0]/4
    
    # 打印点的数量
    print("Number of points in the bin file:", point_count)

# 打印pkl特定键的元素个数
filepath = "/home/edric/PaSCo_Edric/output_v1/000004_1.pkl"
# filepath = "/home/edric/PaSCo_Edric/output/000000_1.pkl"
read_and_print_xyz(filepath)

# 打印pkl键
# filepath = "/home/edric/PaSCo_Edric/gpfsscratch/rech/kvd/uyl37fq/pasco_preprocess/kitti/waffleiron_v2/sequences/01/seg_feats_tta/000000.pkl"
#Keys in the PKL file: ['embedding', 'coords', 'vote']

# filepath = "/home/edric/PaSCo_Edric/output_v1/000000_1.pkl"
# print_pkl_keys(filepath) 


# bin文件点云数量
# filepath = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01-10/velodyne/000000.bin"
# count_points_in_bin(filepath)

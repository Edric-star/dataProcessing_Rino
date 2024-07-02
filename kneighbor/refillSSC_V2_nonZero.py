import numpy as np
import pickle
from sklearn.neighbors import KDTree
from scipy.stats import mode

# 读取ssc预测结果
pkl_filepath = '/home/edric/dataProcess/ssc_pred_ourLabel/000000_1.pkl'
with open(pkl_filepath, 'rb') as handle:
    data = pickle.load(handle)
ssc_pred = data['ssc_pred']  # 256x256x32的体素预测结果

voxel_size = 0.2
vox_origin = np.array([-25.6, -40.0, -3.0])

# 获取非零体素(标签255)的索引并计算其中心点坐标转为点云世界坐标
non_zero_indices = np.argwhere((ssc_pred != 255))
non_zero_coords = (non_zero_indices + 0.5) * voxel_size + vox_origin

# 保存标签为0的地面体素
ground_label = 0
ground_indices = non_zero_indices[ssc_pred[non_zero_indices[:, 0], 
                                           non_zero_indices[:, 1], non_zero_indices[:, 2]] == ground_label]

# 读取稀疏的点云数据
pcd_filepath = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne/000000.bin'
label_filepath = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels_original/000000.label'
point_cloud = np.fromfile(pcd_filepath, dtype=np.float32).reshape(-1, 4)  # xyz + intensity
labels = np.fromfile(label_filepath, dtype=np.uint32)
assert point_cloud.shape[0] == labels.shape[0], "Point cloud and label file must have the same number of entries"

# 用原始点云坐标构建 KDTree
kdtree = KDTree(point_cloud[:, :3])
print("KDTree constructed successfully")

# 对非零体素进行近邻查询并获取标签
k = 30
distances, indices = kdtree.query(non_zero_coords, k=k)  

# 获取这些最近邻点在原始点云中的标签
nearest_labels = labels[indices]

# 取数量最多的标签
most_frequent_labels = mode(nearest_labels, axis=1).mode.flatten()

# 恢复标签为0的地面体素
for ground_index in ground_indices:
    idx = np.where((non_zero_indices == ground_index).all(axis=1))[0]
    most_frequent_labels[idx] = ground_label

# 合并中心点坐标和对应的标签
non_zero_coords_with_labels = np.hstack((non_zero_coords, most_frequent_labels.reshape(-1, 1)))

output_filepath = '/home/edric/dataProcess/kneighborResult/non_zero_coords_with_labels_withCm_road.npy'
np.save(output_filepath, non_zero_coords_with_labels)
print(f"Center coordinates with labels saved to {output_filepath}")

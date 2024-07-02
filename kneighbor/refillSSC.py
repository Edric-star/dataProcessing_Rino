import numpy as np
import pickle
from sklearn.neighbors import KDTree

# 读取模型预测结果
pkl_filepath = '/home/edric/PaSCo_Edric/output_v1/000000_1.pkl'
with open(pkl_filepath, 'rb') as handle:
    data = pickle.load(handle)
ssc_pred = data['ssc_pred'][0]  # 256x256x32的体素预测结果

# 读取原始标签文件
label_filepath = '/home/edric/dataProcess/voxel_label_mapped/000000.label'
original_labels = np.fromfile(label_filepath, dtype=np.uint16).reshape((256, 256, 32))
print(f"Read {original_labels.size} elements from label file.")

# 创建包含体素空间坐标的三维数组，注意np.indices会返回一个包含每个维度坐标的数组,按高维到低维排列
coords = np.indices((256, 256, 32)).reshape(3, -1).T
# print(coords.shape)

# 计算 KNN
best_k = 5  # 初始K值
best_accuracy = 0
for K in range(9, 11, 2):  # 试验K值=9
# for K in range(3, 9, 2):  # 试验K值从3到8的奇数
    # 尝试不同的 leaf_size
    for leaf_size in [20, 40]:
    # for leaf_size in [10, 20, 40, 60, 80]:
        kdtree = KDTree(coords, leaf_size=leaf_size)
        distances, indices = kdtree.query(coords, k=K)

        # target_labels = {7, 8, 9, 10, 11, 12, 16}
        target_labels = {7, 8, 10, 11, 12, 16}
        corrected_labels = ssc_pred.copy()
        for i in range(len(coords)):
            z, y, x = coords[i]
            if ssc_pred[z, y, x] in target_labels:
                neighbor_labels = original_labels.flatten()[indices[i]]
                bincount = np.bincount(neighbor_labels)
                if bincount.argmax() == 0 and len(bincount) > 1:
                    corrected_labels[z, y, x] = bincount[1:].argmax() + 1
                else:
                    corrected_labels[z, y, x] = bincount.argmax()

        # 保存校正后的结果为 .label 文件
        corrected_label_filepath = f'/home/edric/dataProcess/kneighborResult/knn_k{K}_leaf{leaf_size}.label'
        corrected_labels.astype(np.uint16).tofile(corrected_label_filepath)
        print(f"K={K}, leaf_size={leaf_size}, 校正后的标签已保存到 {corrected_label_filepath}")

        accuracy = np.mean(corrected_labels == original_labels)  # 计算准确率作为评估指标
        print(f"K={K}, leaf_size={leaf_size}, Accuracy={accuracy}")
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_k = K
            best_leaf_size = leaf_size

print(f"最佳K值: {best_k}, 最佳leaf_size: {best_leaf_size}, 对应的准确率: {best_accuracy}")

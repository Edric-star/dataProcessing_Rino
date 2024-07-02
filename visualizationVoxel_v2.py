import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pickle

def get_color_map():
    return {
        0: [0/255, 0/255, 0/255],           # empty (black)
        1: [100/255, 150/255, 245/255],     # car (light blue)
        2: [100/255, 230/255, 245/255],     # bicycle (cyan)
        3: [30/255, 60/255, 150/255],       # motorcycle (dark blue)
        4: [80/255, 30/255, 180/255],       # truck (purple)
        5: [100/255, 80/255, 250/255],      # other-vehicle (light purple)
        6: [255/255, 30/255, 30/255],       # person (red)
        7: [255/255, 40/255, 200/255],      # bicyclist (pink)
        8: [150/255, 30/255, 90/255],       # motorcyclist (dark pink)
        9: [255/255, 0/255, 255/255],       # road (magenta)
        10: [255/255, 150/255, 255/255],    # parking (light magenta)
        11: [75/255, 0/255, 75/255],        # sidewalk (dark magenta)
        12: [175/255, 0/255, 75/255],       # other-ground (dark red)
        13: [255/255, 200/255, 0/255],      # building (yellow)
        14: [255/255, 120/255, 50/255],     # fence (orange)
        15: [0/255, 175/255, 0/255],        # vegetation (green)
        16: [135/255, 60/255, 0/255],       # trunk (brown)
        17: [150/255, 240/255, 80/255],     # terrain (light green)
        18: [255/255, 240/255, 150/255],    # pole (light yellow)
        19: [255/255, 0/255, 0/255]         # traffic-sign (red)
    }

def visualize_voxel_data(voxel_data, grid_size, voxel_size):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color_map = get_color_map()

    x, y, z = np.indices(grid_size)
    x = x.flatten() * voxel_size
    y = y.flatten() * voxel_size
    z = z.flatten() * voxel_size
    voxel_data = voxel_data.flatten()

    mask = voxel_data > 0
    x = x[mask]
    y = y[mask]
    z = z[mask]
    voxel_data = voxel_data[mask]

    colors = np.array([color_map[label] for label in voxel_data])

    ax.scatter(x, y, z, c=colors, marker='s')

    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')

    plt.show()

# 读取 .label 文件
# label_filepath = '/home/edric/dataProcess/voxel_label_mapped/000000.label'
label_filepath = '/home/edric/dataProcess/kneighborResult/knn_k9_leaf40.label'
voxel_data = np.fromfile(label_filepath, dtype=np.uint16).reshape((256, 256, 32))

# 读取模型预测结果
pkl_filepath = '/home/edric/PaSCo_Edric/output_v1/000000_1.pkl'
with open(pkl_filepath, 'rb') as handle:
    data = pickle.load(handle)
ssc_pred = data['ssc_pred'][0]  # 256x256x32的体素预测结果


# 可视化
grid_size = (256, 256, 32)
voxel_size = 0.2
visualize_voxel_data(ssc_pred, grid_size, voxel_size) # 模型预测结果
visualize_voxel_data(voxel_data, grid_size, voxel_size) # 原始voxel或k近邻的结果

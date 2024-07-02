import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d

def get_cmap_semanticKITTI20():
    colors = np.array([
        [0, 0, 0, 255],          # 0.empty (black)
        [100, 150, 245, 255],    # 1.car (light blue)
        [100, 230, 245, 255],    # 2.bicycle (cyan)
        [30, 60, 150, 255],      # 3.motorcycle (dark blue)
        [80, 30, 180, 255],      # 4.truck (purple)
        [100, 80, 250, 255],     # 5.other-vehicle (light purple)
        [255, 30, 30, 255],      # 6.person (red)
        [255, 40, 200, 255],     # 7.bicyclist (pink)
        [150, 30, 90, 255],      # 8.motorcyclist (dark pink)
        [255, 0, 255, 255],      # 9.road (magenta)
        [255, 150, 255, 255],    # 10.parking (light magenta)
        [75, 0, 75, 255],        # 11.sidewalk (dark magenta)
        [175, 0, 75, 255],       # 12.other-ground (dark red)
        [255, 200, 0, 255],      # 13.building (yellow)
        [255, 120, 50, 255],     # 14.fence (orange)
        [0, 175, 0, 255],        # 15.vegetation (green)
        [135, 60, 0, 255],       # 16.trunk (brown)
        [150, 240, 80, 255],     # 17.terrain (light green)
        [255, 240, 150, 255],    # 18.pole (light yellow)
        [255, 0, 0, 255]         # 19.traffic-sign (red)
    ]).astype(np.uint8)
    return colors

def visualize_pkl(filepath, grid_size):
    # 读取PKL文件
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
    
    # 获取点云数据和场景补全预测
    xyz = data['xyz']
    ssc_pred = data['ssc_pred']

    # 打印ssc_pred的形状
    print("Shape of ssc_pred:", ssc_pred.shape)
    
    # 可视化点云数据
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    colors = np.zeros_like(xyz)
    colors[:, 2] = 1  # 将颜色设置为蓝色
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # 显示点云
    o3d.visualization.draw_geometries([pcd], window_name="Point Cloud")

    # 可视化场景补全数据
    if ssc_pred.ndim == 4:
        ssc_pred = ssc_pred[0]
    elif ssc_pred.ndim != 3:
        raise ValueError("ssc_pred needs to be a 3-dimensional array or convertible to 3D")
    
    # 获取颜色映射
    cmap = get_cmap_semanticKITTI20()
    voxel_size = 0.2  # 你可以根据需要调整体素大小
    voxel_centers = []
    voxel_colors = []
    
    label_types = np.unique(ssc_pred)
    num_label_types = len(label_types)
    print(f"Label types: {label_types}")
    print(f"Number of unique label types: {num_label_types}")
    for i in range(ssc_pred.shape[0]):
        for j in range(ssc_pred.shape[1]):
            for k in range(ssc_pred.shape[2]):
                label = ssc_pred[i, j, k]
                if label > 0:
                    voxel_centers.append([(i + 0.5) * voxel_size, (j + 0.5) * voxel_size, (k + 0.5) * voxel_size])
                    voxel_colors.append(cmap[label][:3] / 255.0)  # 颜色值转换到0-1之间

    # 将体素中心点转换为点云
    voxel_centers = np.array(voxel_centers)
    voxel_colors = np.array(voxel_colors)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x, y, z = voxel_centers[:, 0], voxel_centers[:, 1], voxel_centers[:, 2]
    ax.scatter(x, y, z, c=voxel_colors, marker='s')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # ax.set_xlim([0, grid_size[0] * voxel_size])
    # ax.set_ylim([0, grid_size[1] * voxel_size])
    # ax.set_zlim([0, grid_size[2] * voxel_size])
    
    plt.show()

filepath = "/home/edric/PaSCo_Edric/output_v1/000000_1.pkl"
grid_size = (256, 256, 32)
visualize_pkl(filepath, grid_size)

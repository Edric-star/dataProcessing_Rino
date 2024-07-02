import os
import pickle
import numpy as np
import open3d as o3d

def get_cmap_semanticKITTI20():
    colors = np.array([
        [0  , 0  , 0, 255],       # 0.empty (black)
        [100, 150, 245, 255],     # 1.car (light blue)
        [100, 230, 245, 255],     # 2.bicycle (cyan)
        [30, 60, 150, 255],       # 3.motorcycle (dark blue)
        [80, 30, 180, 255],       # 4.truck (purple)
        [100, 80, 250, 255],      # 5.other-vehicle (light purple)
        [255, 30, 30, 255],       # 6.person (red)
        [255, 40, 200, 255],      # 7.bicyclist (pink)
        [150, 30, 90, 255],       # 8.motorcyclist (dark pink)
        # [0  , 0  , 0, 255],
        [255, 0, 255, 255],       # 9.road (magenta)

        # [255, 0, 255, 255],       
        [255, 150, 255, 255],     # 10.parking (light magenta)
      
        [75, 0, 75, 255],         # 11.sidewalk (dark magenta)

        # [255, 0, 255, 255],       
        [175, 0, 75, 255],        # 12.other-ground (dark red)

        [255, 200, 0, 255],       # 13.building (yellow)
        [255, 120, 50, 255],      # 14.fence (orange)
        [0, 175, 0, 255],         # 15.vegetation (green)

        # [0, 175, 0, 255],         
        [135, 60, 0, 255],        # 16.trunk (brown)

        [150, 240, 80, 255],      # 17.terrain (light green)
        [255, 240, 150, 255],     # 18.pole (light yellow)
        [255, 0, 0, 255]          # 19.traffic-sign (red)
    ]).astype(np.uint8)
    return colors

def visualize_pkl(filepath):
    # 读取PKL文件
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
    
    # 获取点云数据和场景补全预测
    # xyz = data['xyz']
    # ssc_pred = data['semantic_label_origin']
    # ssc_pred = data['pred_panoptic_seg']
    # ssc_pred = data['pred_semantic_seg']
    ssc_pred = data['ssc_pred']

    # 打印ssc_pred的形状
    print("Shape of ssc_pred:", ssc_pred.shape)
    
    # # 可视化点云数据
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(xyz)
    # colors = np.zeros_like(xyz)
    # colors[:, 2] = 1  # 将颜色设置为蓝色
    # pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # # 显示点云
    # o3d.visualization.draw_geometries([pcd], window_name="Point Cloud")

    # 可视化场景补全数据
    if ssc_pred.ndim == 4:
        # 提取第一个三维切片
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
                    # voxel_centers.append([i * voxel_size, j * voxel_size, k * voxel_size])
                    voxel_centers.append([(i + 0.5) * voxel_size, (j + 0.5) * voxel_size, (k + 0.5) * voxel_size])
                    voxel_colors.append(cmap[label][:3] / 255.0)  # 颜色值转换到0-1之间

    # 将体素中心点转换为点云
    voxel_centers = np.array(voxel_centers)
    voxel_colors = np.array(voxel_colors)
    voxel_cloud = o3d.geometry.PointCloud()
    voxel_cloud.points = o3d.utility.Vector3dVector(voxel_centers)
    voxel_cloud.colors = o3d.utility.Vector3dVector(voxel_colors)

    # 创建体素网格
    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(voxel_cloud, voxel_size)

    # 显示体素网格
    o3d.visualization.draw_geometries([voxel_grid], window_name="Scene Completion")

filepath = "/home/edric/new_space/output/00/000001_1.pkl"
visualize_pkl(filepath)

# import open3d as o3d
# import numpy as np

# # 定义拾取回调函数
# def pick_points(vis):
#     print("Press 'Shift + left click' to pick points.")
#     picked_points = vis.get_picked_points()
#     for point in picked_points:
#         print(f"Picked point: {point}")

# # 创建点云
# pcd = o3d.io.read_point_cloud("/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_10/samples_third_ann_data/clip_rino_107_10/POINTS_backup/1716882004.899514_1716882004.899992.pcd")

# print(len(pcd.points))
# # 可视化点云并拾取点
# vis = o3d.visualization.VisualizerWithEditing()
# vis.create_window()
# vis.add_geometry(pcd)
# vis.run()  # 使用 Shift + 左键 点击点云中的点来拾取点
# vis.destroy_window()

# # 获取选中的点的索引
# picked_points = vis.get_picked_points()

# # 打印选中的点的坐标
# for idx in picked_points:
#     print(pcd.points[idx])


import numpy as np
import open3d as o3d

def read_bin_file(bin_file_path):
    # 读取 bin 文件
    point_cloud = np.fromfile(bin_file_path, dtype=np.float32)
    # 将数据 reshape 为 Nx4 的形状，每行一个点
    point_cloud = point_cloud.reshape((-1, 4))
    return point_cloud[:,:3]

def visualize_point_cloud(points):
    # 创建 Open3D 点云对象
    pcd = o3d.geometry.PointCloud()
    # 设置点云的坐标
    pcd.points = o3d.utility.Vector3dVector(points)
    # 可视化点云
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    # 指定 bin 文件路径
    bin_file_path = "/home/edric/dataProcess/clip_rino_107_float32bin_removeCM_10/clip_rino_107_10/1716882002.099497_1716882002.099334.bin"
    # 读取点云数据
    points = read_bin_file(bin_file_path)
    
    # 可视化点云
    visualize_point_cloud(points)



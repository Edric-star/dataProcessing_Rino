import os
import numpy as np
import open3d as o3d
from plyfile import PlyData as ply

class PlyManager:
    def __init__(self):
        self.PALETTE = np.array([
            [128, 64, 128],  # 紫色 - 道路 (road)
            [244, 35, 232],  # 粉紫色 - 人行道 (sidewalk)
            [70, 70, 70],    # 深灰色 - 建筑物 (building)
            [102, 102, 156], # 灰蓝色 - 围栏 (fence)
            [190, 153, 153], # 浅褐色
            [153, 153, 153], # 灰色
            [107, 142, 35],  # 橄榄绿 - 植物 (plant)
            [220, 220, 0],   # 黄色 - 地形 (terrain)
            [250, 170, 30],  # 橙黄色 - 车 (car)
            [152, 251, 152], # 浅绿色 (cone)
            [70, 130, 180],  # 蓝色
            [220, 20, 60],   # 红色 - 卡车 (truck)
            [255, 0, 0],     # 亮红色 - 公共汽车 (bus)
            [0, 0, 142],     # 深蓝色 - 火车 (train)
            [0, 0, 70],      # 深灰蓝 - 摩托车 (motorcycle)
            [0, 60, 100],    # 深蓝灰
            [125, 125, 125]  # 中灰色 - 未标注 (free)
        ], np.float32) / 255
        self.code_dict = {}
        for idx, (r, g, b) in enumerate(self.PALETTE):
            self.code_dict[f"{int(r * 255)}_{int(g * 255)}_{int(b * 255)}"] = idx

    def VisualizeColorLableArr(self, in_wrd_arr, in_label_arr):
        labels = in_label_arr.astype(np.uint8)
        labels[np.where(labels >= len(self.PALETTE))] = len(self.PALETTE) - 1
        lables_color = self.PALETTE[labels]
        o3d_pnts = o3d.geometry.PointCloud()
        o3d_pnts.points = o3d.utility.Vector3dVector(in_wrd_arr)
        o3d_pnts.colors = o3d.utility.Vector3dVector(lables_color)
        self.display_point_cloud(o3d_pnts)

    def WritePlyLabelArr(self, in_pnt_arr, in_label_arr, file_pth):
        labels = in_label_arr.astype(np.uint8)
        labels[np.where(labels >= len(self.PALETTE))] = len(self.PALETTE) - 1
        lables_color = self.PALETTE[labels]
        o3d_pnts = o3d.geometry.PointCloud()
        o3d_pnts.points = o3d.utility.Vector3dVector(in_pnt_arr)
        o3d_pnts.colors = o3d.utility.Vector3dVector(lables_color)
        o3d.io.write_point_cloud(file_pth, o3d_pnts)

    def WritePlyArr(self, in_wrd_arr, file_pth):
        o3d_pnts = o3d.geometry.PointCloud()
        o3d_pnts.points = o3d.utility.Vector3dVector(in_wrd_arr)
        o3d.io.write_point_cloud(file_pth, o3d_pnts)

    def LoadPlyAndPcd(self, ply_pth):
        if ply_pth.endswith('.pcd'):
            pcd = o3d.io.read_point_cloud(ply_pth)
            return np.asarray(pcd.points)
        data = ply.read(ply_pth)
        pnt_xs = np.array(data.elements[0]['x'])
        pnt_ys = np.array(data.elements[0]['y'])
        pnt_zs = np.array(data.elements[0]['z'])
        return np.vstack((pnt_xs, pnt_ys, pnt_zs)).transpose(1, 0)

    def LoadPlyAndColorId(self, ply_pth):
        data = ply.read(ply_pth)
        pnt_xs = np.array(data.elements[0]['x'])
        pnt_ys = np.array(data.elements[0]['y'])
        pnt_zs = np.array(data.elements[0]['z'])
        l1 = np.array(data.elements[0]['red'])
        l2 = np.array(data.elements[0]['green'])
        l3 = np.array(data.elements[0]['blue'])
        out = []
        for r, g, b in zip(l1, l2, l3):
            out.append(self.code_dict[f"{r}_{g}_{b}"])
        return np.vstack((pnt_xs, pnt_ys, pnt_zs)).transpose(1, 0), np.array(out)

    def display_point_cloud(self, point_cloud):
        vis = o3d.visualization.VisualizerWithEditing()
        vis.create_window()
        vis.add_geometry(point_cloud)

        def pick_points(vis):
            picked_points = vis.get_picked_points()
            for point in picked_points:
                print(f"Picked point: {point}")
                print(f"Coordinates: {point_cloud.points[point]}")

        vis.run()
        vis.destroy_window()

# 读取保存的非空体素中心点坐标和标签
input_filepath = '/home/edric/dataProcess/kneighborResult/clip_rino_107_35/1716883805.499794_1716883805.499981.npy'
non_zero_coords_with_labels = np.load(input_filepath)

# 分离出坐标和标签
coords = non_zero_coords_with_labels[:, :3]  # 前三列是坐标
labels = non_zero_coords_with_labels[:, 3]   # 第四列是标签

ply_manager = PlyManager()
ply_manager.VisualizeColorLableArr(coords, labels)

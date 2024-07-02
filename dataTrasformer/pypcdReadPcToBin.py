import os
import numpy as np
from pypcd import pypcd

def get_pnts_and_timestamp_intensity(pcd_pth):
    pc = pypcd.PointCloud.from_path(pcd_pth)
    org_pnt = np.stack((pc.pc_data["x"], pc.pc_data["y"], pc.pc_data["z"]), axis=-1)
    intensity = pc.pc_data['label']
    return org_pnt, intensity

def save_bin(file_path, points, intensity):
    data = np.hstack((points, intensity.reshape(-1, 1)))
    data = data.astype(np.float32)
    data.tofile(file_path)

def read_and_print_bin(file_path, num_points=5):
    data = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    print(f'First {num_points} points from {file_path}:')
    print(data[:num_points])
    print(data.shape)

def convert_pcd_to_bin(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.pcd'):
            pcd_path = os.path.join(input_folder, file_name)
            points, intensity = get_pnts_and_timestamp_intensity(pcd_path)
            
            bin_file_name = file_name.replace('.pcd', '.bin')
            bin_path = os.path.join(output_folder, bin_file_name)
            
            save_bin(bin_path, points, intensity)
            print(f'Saved {bin_path}')
            
            read_and_print_bin(bin_path)


input_folder = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_third_ann_data/clip_rino_107_11/POINTS'  # 替换为你的PCD文件夹路径
output_folder = '/home/edric/dataProcess/107_11_pcd_float32bin'  # 替换为你想要保存BIN文件的文件夹路径

convert_pcd_to_bin(input_folder, output_folder)

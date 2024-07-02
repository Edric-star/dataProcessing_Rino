import os
import numpy as np
import open3d as o3d

# pcd文件转float32bin，并清空intensity
def convert_pcd_to_bin(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        if 'POINTS' in dirs:
            points_folder = os.path.join(root, 'POINTS')
            for file_name in os.listdir(points_folder):
                if file_name.endswith('.pcd'):
                    input_path = os.path.join(points_folder, file_name)
                    
                    # 构造输出路径，保持文件夹结构一致，但去掉POINTS部分
                    relative_path = os.path.relpath(input_path, input_folder)
                    # 去掉路径中的POINTS部分
                    relative_path = relative_path.replace('POINTS/', '')
                    output_path = os.path.join(output_folder, relative_path).replace('.pcd', '.bin')
                    output_dir = os.path.dirname(output_path)
                    
                    # 如果输出文件夹不存在，创建它
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    # 读取点云文件
                    pcd = o3d.io.read_point_cloud(input_path)
                    points = np.asarray(pcd.points)
                    if len(points) == 0:
                        print(f"No points found in {input_path}")
                        continue

                    # 初始化激光强度为0
                    intensities = np.zeros((points.shape[0], 1), dtype=np.float32)

                    # 合并点云坐标和激光强度
                    points_with_intensity = np.hstack((points, intensities))

                    # 保存为 float32 类型的 bin 文件
                    points_with_intensity.astype(np.float32).tofile(output_path)
                    
                    print(f'Converted and saved {output_path}')

if __name__ == "__main__":
    input_folder = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_third_ann_data'  # .pcd 文件夹路径
    output_folder = '/home/edric/dataProcess/clip_rino_107_float32bin'  # 保存 bin 文件的文件夹路径
    convert_pcd_to_bin(input_folder, output_folder)

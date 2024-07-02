import os
import numpy as np

def convert_bin_to_label(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.bin'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name.replace('.bin', '.label'))
            
            # 读取 uint8 类型的 bin 标签文件
            labels_uint8 = np.fromfile(input_path, dtype=np.uint8)
            
            # 转换为 uint32 类型
            labels_uint32 = labels_uint8.astype(np.uint32)
            
            # 保存为 uint32 类型的标签文件
            labels_uint32.tofile(output_path)
            
            print(f'Converted and saved {output_path}')


input_folder = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107/samples_pointwise_data_bin/clip_rino_107_11/SEG_RESULT'  # 替换为你的 uint8 标签文件夹路径
output_folder = '/home/edric/dataProcess/107_11_uint32label'  # 替换为你想要保存 uint32 标签文件的文件夹路径
convert_bin_to_label(input_folder, output_folder)

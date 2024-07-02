import os
import numpy as np

def convert_bin_to_label(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        if 'SEG_RESULT' in dirs:
            seg_result_folder = os.path.join(root, 'SEG_RESULT')
            for file_name in os.listdir(seg_result_folder):
                if file_name.endswith('.bin'):
                    input_path = os.path.join(seg_result_folder, file_name)
                    
                    # 构造输出路径，保持文件夹结构一致，但去掉SEG_RESULT部分
                    relative_path = os.path.relpath(input_path, input_folder)
                    # 去掉路径中的SEG_RESULT部分
                    relative_path = relative_path.replace('SEG_RESULT/', '')
                    output_path = os.path.join(output_folder, relative_path).replace('.bin', '.label')
                    output_dir = os.path.dirname(output_path)
                    
                    # 如果输出文件夹不存在，创建它
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    # 读取 uint8 类型的 bin 标签文件
                    labels_uint8 = np.fromfile(input_path, dtype=np.uint8)
                    
                    # 转换为 uint32 类型
                    labels_uint32 = labels_uint8.astype(np.uint32)
                    
                    # 保存为 uint32 类型的标签文件
                    labels_uint32.tofile(output_path)
                    
                    print(f'Converted and saved {output_path}')

input_folder = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_pointwise_data_bin'  #  uint8 标签文件夹路径
output_folder = '/home/edric/dataProcess/clip_rino_107_uint32label'  # 保存 uint32 标签文件的文件夹路径
convert_bin_to_label(input_folder, output_folder)

import os
import shutil

def get_sorted_files(folder):
    """
    获取指定文件夹中的文件列表，并按文件名排序
    """
    files = os.listdir(folder)
    files.sort()
    return files

def rename_and_copy_files(input_folder, output_folder):
    """
    重新命名文件并复制到新的文件夹中
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    files = get_sorted_files(input_folder)
    
    for i, file_name in enumerate(files):
        base, ext = os.path.splitext(file_name)  # 分离文件名和扩展名
        new_name = "{:06d}{}".format(i, ext)  # 生成新的文件名
        src_path = os.path.join(input_folder, file_name)
        dst_path = os.path.join(output_folder, new_name)
        
        print(f"复制 {src_path} 到 {dst_path}")
        shutil.copy2(src_path, dst_path)  # 复制文件并保持原有的元数据

def process_folders(input_folder1, input_folder2, output_folder1, output_folder2):
    """
    处理两个输入文件夹并将结果输出到两个新的文件夹中
    """
    rename_and_copy_files(input_folder1, output_folder1)
    rename_and_copy_files(input_folder2, output_folder2)

# 输入文件夹路径
input_folder1 = "/home/edric/dataProcess/107_11_pcd_float32bin_withoutCm"
input_folder2 = "/home/edric/dataProcess/107_11_uint32label_withoutCm"

# 输出文件夹路径
output_folder1 = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne_withintensity"
output_folder2 = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels_original"

# 处理文件夹
process_folders(input_folder1, input_folder2, output_folder1, output_folder2)

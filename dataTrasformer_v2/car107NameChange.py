import os

def rename_folders(base_path, old_name, new_name):
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            if dir_name == old_name:
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, new_name)
                if os.path.exists(new_path):
                    print(f"Skipping renaming of {old_path} as the target {new_path} already exists.")
                    continue
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed {old_path} to {new_path}")
                except Exception as e:
                    print(f"Failed to rename {old_path} to {new_path}: {e}")

# 配置路径
base_path_samples_pointwise = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_pointwise_data_bin'
base_path_samples_third_ann = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_third_ann_data'

# 先重命名为备份文件夹
rename_folders(base_path_samples_pointwise, 'SEG_RESULT', 'SEG_RESULT_backup')
rename_folders(base_path_samples_third_ann, 'POINTS', 'POINTS_backup')

# 再进行最终重命名
rename_folders(base_path_samples_pointwise, 'SEG_RESULT_2', 'SEG_RESULT')
rename_folders(base_path_samples_third_ann, 'POINTS_2', 'POINTS')

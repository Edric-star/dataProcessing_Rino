import numpy as np

def inspect_label_file(file_path, data_type):
    # 读取二进制文件中的标签数据
    data = np.fromfile(file_path, dtype=data_type)
    
    # 获取唯一标签值
    unique_labels = np.unique(data)
    
    # 打印数据的基本信息
    print(f"Data type: {data_type}")
    print(f"shape of elements: {data.shape}")
    print(f"Unique labels: {unique_labels}")
    
    return unique_labels

def main():
    # 设置文件路径和数据类型
    label_file = '/home/edric/dataProcess/knn.label'  # 修改为实际文件路径
    label_data_type = np.uint16
    
    # 查看标签文件中的数据
    unique_labels = inspect_label_file(label_file, label_data_type)

if __name__ == "__main__":
    main()

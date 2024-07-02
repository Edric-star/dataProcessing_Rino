# import numpy as np

# def read_label_bin(file_path):
#     # 读取标签 bin 文件
#     labels = np.fromfile(file_path, dtype=np.uint32)
#     return labels

# def print_unique_labels_and_count(labels):
#     unique_labels, counts = np.unique(labels, return_counts=True)
#     print("Unique labels and their counts in the bin file:")
#     for label, count in zip(unique_labels, counts):
#         print(f"Label: {label}, Count: {count}")

# # 示例文件路径
# file_path = ""

# # 读取标签文件
# labels = read_label_bin(file_path)

# # 打印唯一标签及其数量
# print_unique_labels_and_count(labels)
# print(labels.shape)


import numpy as np

def inspect_bin_file(file_path, data_type, num_elements=10):
    # 读取二进制文件中的数据
    data = np.fromfile(file_path, dtype=data_type)
    
    # 打印数据的基本信息
    print(f"Data type: {data_type}")
    print(f"Number of elements: {data.size}")
    print(f"First {num_elements} elements: {data[:num_elements]}")
    unique_data = np.unique(data)
    print("Unique elements:",unique_data)
    print(data.shape[0])

def main():
    # 设置文件路径和数据类型
    bin_file = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_pointwise_data_bin/clip_rino_107_10/SEG_RESULT/1716882001.499492_1716882001.499987.bin'
    
    # 根据实际情况设置数据类型
    bin_data_type = np.uint8
    
    # 查看二进制文件中的数据
    inspect_bin_file(bin_file, bin_data_type)

if __name__ == "__main__":
    main()

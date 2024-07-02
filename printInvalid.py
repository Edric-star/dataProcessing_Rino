import numpy as np
import matplotlib.pyplot as plt

def read_invalid_file(invalid_path):
    # 读取 .invalid 文件内容
    INVALID = np.fromfile(invalid_path, dtype=np.uint8)
    return INVALID

def print_value_distribution(values):
    # 打印值的分布
    unique, counts = np.unique(values, return_counts=True)
    for value, count in zip(unique, counts):
        print(f"Value: {value}, Count: {count}")

def plot_value_distribution(values):
    # 绘制值的分布直方图
    plt.hist(values, bins=256, range=(0, 255), edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Value Distribution in .invalid File')
    plt.show()

invalid_path = "/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels/000000.invalid"  # 替换为实际的 .invalid 文件路径
INVALID = read_invalid_file(invalid_path)
print_value_distribution(INVALID)
plot_value_distribution(INVALID)

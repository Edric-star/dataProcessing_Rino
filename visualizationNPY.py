import numpy as np
import matplotlib.pyplot as plt

def visualize_npy_file(file, ax, title):
    image = np.load(file)
    ax.imshow(image, cmap='gray')
    ax.set_title(title)
    ax.axis('off')  # 关闭坐标轴

def visualize_npy_files(file1, file2):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    visualize_npy_file(file1, axes[0], 'File 1')
    visualize_npy_file(file2, axes[1], 'File 2')

    plt.show()

# 示例用法
file1_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_pointwise_data_bin/clip_rino_107_2/OCC2D_19.2X38.4x0x0.1_V3/1716881340.699492_1716881340.699335.npz.npy'
file2_path = '/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino_107_select/samples_pointwise_data_bin/clip_rino_107_2/OCC2D_19.2X38.4x0x0.1_V2/1716881340.699492_1716881340.699335.npz.npy'

visualize_npy_files(file1_path, file2_path)

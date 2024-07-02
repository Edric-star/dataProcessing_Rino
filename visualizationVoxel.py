import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_voxel_data(bin_file, label_file, grid_size):
    voxel_data = np.fromfile(bin_file, dtype=np.float32)
    label_data = np.fromfile(label_file, dtype=np.uint16)
    print(f"Voxel data size: {voxel_data.size}")
    print(f"Label data size: {label_data.size}")
    return voxel_data, label_data

def get_color_map():
    color_map = {
        40: [255/255, 0/255, 255/255],    # road (magenta)
        48: [75/255, 0/255, 75/255],      # sidewalk (dark magenta)
        50: [255/255, 200/255, 0/255],    # building (yellow)
        51: [255/255, 120/255, 50/255],   # fence (orange)
        80: [255/255, 240/255, 150/255],  # pole (light yellow)
        81: [255/255, 0/255, 0/255],      # traffic-sign (red)
        70: [0/255, 175/255, 0/255],      # vegetation (green)
        72: [150/255, 240/255, 80/255],   # terrain (light green)
        10: [100/255, 150/255, 245/255],  # car (light blue)
        99: [0/255, 0/255, 0/255],        # other-object (black)
        18: [80/255, 30/255, 180/255],    # truck (purple)
        13: [100/255, 80/255, 250/255],   # bus (light purple)
        11: [100/255, 230/255, 245/255],  # bicycle (cyan)
        30: [255/255, 30/255, 30/255],    # person (red)
        20: [30/255, 60/255, 150/255],    # other-vehicle (dark blue)
        0: [0/255, 0/255, 0/255]          # unlabeled (black)

        # 0: [0/255, 0/255, 0/255],           # empty (black)
        # 1: [100/255, 150/255, 245/255],     # car (light blue)
        # 2: [100/255, 230/255, 245/255],     # bicycle (cyan)
        # 3: [30/255, 60/255, 150/255],       # motorcycle (dark blue)
        # 4: [80/255, 30/255, 180/255],       # truck (purple)
        # 5: [100/255, 80/255, 250/255],      # other-vehicle (light purple)
        # 6: [255/255, 30/255, 30/255],       # person (red)
        # 7: [255/255, 40/255, 200/255],      # bicyclist (pink)
        # 8: [150/255, 30/255, 90/255],       # motorcyclist (dark pink)
        # 9: [255/255, 0/255, 255/255],       # road (magenta)
        # 10: [255/255, 150/255, 255/255],    # parking (light magenta)
        # 11: [75/255, 0/255, 75/255],        # sidewalk (dark magenta)
        # 12: [175/255, 0/255, 75/255],       # other-ground (dark red)
        # 13: [255/255, 200/255, 0/255],      # building (yellow)
        # 14: [255/255, 120/255, 50/255],     # fence (orange)
        # 15: [0/255, 175/255, 0/255],        # vegetation (green)
        # 16: [135/255, 60/255, 0/255],       # trunk (brown)
        # 17: [150/255, 240/255, 80/255],     # terrain (light green)
        # 18: [255/255, 240/255, 150/255],    # pole (light yellow)
        # 19: [255/255, 0/255, 0/255]         # traffic-sign (red)
    }
    return color_map

def visualize_voxel_data(voxel_data, label_data, grid_size, voxel_size):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color_map = get_color_map()

    x, y, z = np.indices(grid_size)
    x = x.flatten() * voxel_size
    y = y.flatten() * voxel_size
    z = z.flatten() * voxel_size
    voxel_data = voxel_data.flatten()
    label_data = label_data.flatten()

    mask = voxel_data > 0
    x = x[mask]
    y = y[mask]
    z = z[mask]
    label_data = label_data[mask]

    colors = np.array([color_map[label] for label in label_data])

    ax.scatter(x, y, z, c=colors, marker='s')

    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')

    # ax.set_xlim([0, grid_size[0] * voxel_size])
    # ax.set_ylim([0, grid_size[1] * voxel_size])
    # ax.set_zlim([0, grid_size[2] * voxel_size])

    plt.show()

def main():
    bin_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels/000000.bin'
    label_file = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels/000000.label'
    # label_file = '/home/edric/dataProcess/knn.label'
    grid_size = (256, 256, 32)
    voxel_size = 0.2

    voxel_data, label_data = load_voxel_data(bin_file, label_file, grid_size)
    visualize_voxel_data(voxel_data, label_data, grid_size, voxel_size)

if __name__ == "__main__":
    main()
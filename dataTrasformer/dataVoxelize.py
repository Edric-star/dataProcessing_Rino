import os
import numpy as np

def read_bin_file(bin_file):
    """读取点云bin文件"""
    point_cloud = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4)  # 点云数据格式为 (x, y, z, intensity)
    return point_cloud

def read_label_file(label_file):
    """读取标签文件"""
    labels = np.fromfile(label_file, dtype=np.uint32)
    labels = labels.reshape(-1)  # 假设标签为1D数组
    return labels

def voxelize(point_cloud, labels, voxel_size, grid_size, vox_origin):
    """将点云数据进行体素化处理，采用投票机制决定体素的标签"""
    assert point_cloud.shape[0] == labels.shape[0], "Point cloud and labels must have the same length"
    
    # 定义体素栅格的尺寸
    voxel_grid = np.zeros(grid_size, dtype=np.float32)
    invalid_grid = np.zeros(grid_size, dtype=np.uint8)  # 初始化为0全有效
    label_grid = np.zeros(grid_size, dtype=np.uint16)
    occluded_grid = np.zeros(grid_size, dtype=np.int32)
    label_counters = {}

    # 计算点的体素索引
    shifted_points = point_cloud[:, :3] - vox_origin
    voxel_indices = (shifted_points // voxel_size).astype(np.int32)

    # 确保索引在有效范围内
    valid_indices = np.all((voxel_indices >= 0) & (voxel_indices < grid_size), axis=1)
    
    # 记录和打印被过滤的点的信息
    filtered_indices = np.logical_not(valid_indices)
    print(f"Number of points filtered out: {np.sum(filtered_indices)}")
    print(f"Labels of filtered points: {np.unique(labels[filtered_indices])}")

    voxel_indices = voxel_indices[valid_indices]
    point_cloud = point_cloud[valid_indices]
    labels = labels[valid_indices]

    print(f"Remaining point cloud length: {point_cloud.shape[0]}")
    print(f"Remaining labels length: {labels.shape[0]}")
    print(f"Unique labels in remaining points: {np.unique(labels)}")

    # 为每个体素点计数
    for idx, voxel_index in enumerate(voxel_indices):
        index_tuple = tuple(voxel_index)
        if index_tuple not in label_counters:
            label_counters[index_tuple] = {}
        label_count = label_counters[index_tuple]
        label = labels[idx]
        if label in label_count:
            label_count[label] += 1
        else:
            label_count[label] = 1

    # 填充体素网格和标签
    for voxel_index, counts in label_counters.items():
        max_label = max(counts, key=counts.get)  # 选择出现次数最多的标签
        voxel_grid[voxel_index] += 1  # 这里简单统计体素中点的数量
        label_grid[voxel_index] = max_label
        invalid_grid[voxel_index] = 0  # 标记为有效

    return voxel_grid, invalid_grid, label_grid, occluded_grid

def save_voxel_grid(voxel_grid, invalid_grid, label_grid, occluded_grid, output_dir, frame_id):
    """保存体素化结果"""
    os.makedirs(output_dir, exist_ok=True)
    voxel_grid.tofile(f"{output_dir}/{frame_id}.bin")
    invalid_grid.tofile(f"{output_dir}/{frame_id}.invalid")
    label_grid.tofile(f"{output_dir}/{frame_id}.label")
    occluded_grid.tofile(f"{output_dir}/{frame_id}.occluded")

def read_voxel_grid(output_dir, frame_id):
    """读取并打印体素化结果的维度"""
    voxel_grid = np.fromfile(f"{output_dir}/{frame_id}.bin", dtype=np.float32).reshape(256, 256, 32)
    invalid_grid = np.fromfile(f"{output_dir}/{frame_id}.invalid", dtype=np.uint8).reshape(256, 256, 32)
    label_grid = np.fromfile(f"{output_dir}/{frame_id}.label", dtype=np.uint16).reshape(256, 256, 32)
    occluded_grid = np.fromfile(f"{output_dir}/{frame_id}.occluded", dtype=np.int32).reshape(256, 256, 32)

    print("Voxel grid shape:", voxel_grid.shape)
    print("Invalid grid shape:", invalid_grid.shape)
    print("Label grid shape:", label_grid.shape)
    print("Occluded grid shape:", occluded_grid.shape)

def process_all_files(bin_folder, label_folder, output_dir, voxel_size, grid_size, vox_origin):
    """处理文件夹下的所有bin和label文件"""
    bin_files = sorted([f for f in os.listdir(bin_folder) if f.endswith('.bin')])
    label_files = sorted([f for f in os.listdir(label_folder) if f.endswith('.label')])

    for bin_file, label_file in zip(bin_files, label_files):
        bin_file_path = os.path.join(bin_folder, bin_file)
        label_file_path = os.path.join(label_folder, label_file)
        frame_id = os.path.splitext(bin_file)[0]  # 获取文件名，不包括扩展名

        point_cloud = read_bin_file(bin_file_path)
        labels = read_label_file(label_file_path)

        print(f"Processing {bin_file} and {label_file}...")
        assert point_cloud.shape[0] == labels.shape[0], "Point cloud and labels must have the same length"

        voxel_grid, invalid_grid, label_grid, occluded_grid = voxelize(point_cloud, labels, voxel_size, grid_size, vox_origin)

        # 默认情况下，所有体素都没有遮挡
        occluded_grid.fill(0)

        save_voxel_grid(voxel_grid, invalid_grid, label_grid, occluded_grid, output_dir, frame_id)
        read_voxel_grid(output_dir, frame_id)

def main():
    bin_folder = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/velodyne'
    label_folder = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/labels'
    output_dir = '/home/edric/PaSCo_Edric/gpfsdswork/dataset/SemanticKITTI/dataset/sequences/01/voxels'

    voxel_size = 0.2
    grid_size = (256, 256, 32)
    vox_origin = np.array([-25.6, -40.0, -3.0])

    process_all_files(bin_folder, label_folder, output_dir, voxel_size, grid_size, vox_origin)

if __name__ == "__main__":
    main()

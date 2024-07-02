import numpy as np

# 配置路径
npy_filepath = '/home/edric/dataProcess/kneighborResult/clip_rino_107_10/1716882001.499492_1716882001.499987.npy'

# 读取 npy 文件
data = np.load(npy_filepath)

# 打印维度
print(f"The dimensions of the loaded data are: {data.shape}")

import numpy as np

try:
    # 尝试加载为 .npy 文件
    data = np.load('/media/edric/c0aeda71-48a7-463b-9fb2-a7d90e7e1233/rino107_11/samples_pointwise_data_bin/clip_rino_107_11/OCC2D_19.2X38.4x0x0.1_V3/1716882060.699495_1716882060.699996.npz.npy')
    print("Loaded as .npy file:")
    print(data)
    print('------------------------------------------')
    unique_val = np.unique(data)
    print(unique_val)
except ValueError as e:
    print("Failed to load as .npy file:", e)

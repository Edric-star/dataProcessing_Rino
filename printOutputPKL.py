import pickle
import numpy as np

def load_pkl_file(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def compare_data(data1, data2):
    if isinstance(data1, dict) and isinstance(data2, dict):
        return compare_dicts(data1, data2)
    elif isinstance(data1, list) and isinstance(data2, list):
        return compare_lists(data1, data2)
    elif isinstance(data1, np.ndarray) and isinstance(data2, np.ndarray):
        return np.array_equal(data1, data2)
    else:
        return data1 == data2

def compare_dicts(dict1, dict2):
    if dict1.keys() != dict2.keys():
        return False
    for key in dict1:
        if not compare_data(dict1[key], dict2[key]):
            return False
    return True

def compare_lists(list1, list2):
    if len(list1) != len(list2):
        return False
    for item1, item2 in zip(list1, list2):
        if not compare_data(item1, item2):
            return False
    return True

def compare_pkl_files(file1, file2):
    data1 = load_pkl_file(file1)
    data2 = load_pkl_file(file2)
    
    if compare_data(data1, data2):
        print("The two files are identical.")
    else:
        print("The two files are different.")

# 替换成你要比较的文件路径
file_path1 = "/home/edric/new_space/output/0/000000_1.pkl"
file_path2 = "/home/edric/new_space/output/2/000000_1.pkl"

compare_pkl_files(file_path1, file_path2)

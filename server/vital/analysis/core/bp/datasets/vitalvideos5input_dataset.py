import numpy as np
import torch
from torch.utils.data import Dataset
import h5py
import glob


def get_all_data_files(base_directories):
    data_files = []
    for base_directory in base_directories:
        pattern = f"{base_directory}/*.hdf5"
        data_files.extend(glob.glob(pattern))
    return sorted(data_files)


def load_data_from_hdf5(file_name):
    with h5py.File(file_name, 'r') as f:
        rgb = f['rgb'][:]
        ppg = f['ppg'][:]
        hr = f['hr'][()]
        age = f['age'][()]
        gender = f['gender'][:]
        bp = f['bp'][:]

    return rgb.astype(np.float32), ppg.astype(np.float32), hr.astype(np.float32), age.astype(np.float32), gender.astype(
        np.float32), bp.astype(np.float32)


def standardize_ppg(ppg_signals):
    mean = np.mean(ppg_signals)
    std = np.std(ppg_signals)
    standardized_ppg = (ppg_signals - mean) / std
    return standardized_ppg


def min_max_normalize(data):
    min_value = min(data)
    max_value = max(data)
    normalized_data = [(x - min_value) / (max_value - min_value) for x in data]
    return normalized_data


class VitalVideos5input_dataset(Dataset):
    def __init__(self, preprocessed_path):
        self.data_files = get_all_data_files(preprocessed_path)

    def __len__(self):
        return len(self.data_files)

    def __getitem__(self, idx):
        rgb, ppg, hr, age, gender, bp = load_data_from_hdf5(self.data_files[idx])
        ppg = min_max_normalize(ppg)
        # bp = 0.33 * bp[0] + 0.66 * bp[1]
        return (torch.hstack([torch.tensor(rgb, dtype=torch.float32), torch.tensor(ppg, dtype=torch.float32).unsqueeze(1)]),
                torch.tensor(hr, dtype=torch.float32).unsqueeze(0),
                torch.tensor(age, dtype=torch.float32).unsqueeze(0),
                torch.tensor(gender, dtype=torch.float32),
                torch.tensor(bp[0], dtype=torch.float32))

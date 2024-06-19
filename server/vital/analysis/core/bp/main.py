from server.vital.analysis.core.bp.datasets import vitalvideos5input_dataset
from server.vital.analysis.core.bp.trainer import Trainer
from torch.utils.data import DataLoader, random_split
from server.vital.analysis.core.bp.datasets import *
from server.vital.analysis.core.bp.config import load_config

if __name__ == '__main__':
    config = load_config('config.yaml')
    data_loader_dict = {}

    # dataset = vitalvideos_dataset.vitalvideos_dataset(config.DATA.PREPROCESSED_PATH)
    # dataset = vitalvideosag_dataset.VitalVideosAG_dataset(config.DATA.PREPROCESSED_PATH)
    dataset = vitalvideos5input_dataset.VitalVideos5input_dataset(config.DATA.PREPROCESSED_PATH)
    len_dataset = len(dataset)
    len_train_dataset = len_dataset * 0.8
    train_dataset, valid_dataset = random_split(dataset, [int(len_train_dataset), len_dataset - int(len_train_dataset)])
    data_loader_dict['train'] = DataLoader(train_dataset, batch_size=config.TRAIN.BATCH_SIZE, shuffle=True)
    data_loader_dict['valid'] = DataLoader(valid_dataset, batch_size=config.TRAIN.BATCH_SIZE, shuffle=True)

    trainer = Trainer(config, len(data_loader_dict['train']))
    trainer.train(data_loader_dict, 4)

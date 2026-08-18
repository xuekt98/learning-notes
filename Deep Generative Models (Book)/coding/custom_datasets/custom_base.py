import random
import torch
import os
import torchvision.transforms as transforms

from auxilliary.Register import Registers
from custom_datasets.utils import get_image_paths_from_dir, preprocess_dataset_config
from random import random
from torch.utils.data import Dataset
from PIL import Image
from pathlib import Path
from custom_datasets.utils import read_image, transform_image


class ImagePathDataset(Dataset):
    def __init__(self, dataset_config, image_paths, image_paths_cond=None):
        self.image_paths = image_paths
        self.image_paths_cond = image_paths_cond
        self._length = len(image_paths)

        self.dataset_config = dataset_config
        self.flip = self.dataset_config.flip

    def __len__(self):
        if self.flip:
            return self._length * 2
        return self._length

    def __getitem__(self, index):
        if index >= self._length:
            index = index - self._length

        img_path = self.image_paths[index]
        image, image_name = read_image(img_path)

        if self.image_paths_cond is not None:
            cond_img_path = self.image_paths_cond[index]
            cond_image, cond_image_name = read_image(cond_img_path)

            image, cond_image = transform_image(self.dataset_config, image, cond_image)
            return (image, image_name), (cond_image, cond_image_name)
        image = transform_image(self.dataset_config, image)

        return image, image_name


@Registers.datasets.register_with_name('custom_single')
class CustomSingleDataset(Dataset):
    def __init__(self, dataset_config, stage='train'):
        super().__init__()
        self.dataset_config = preprocess_dataset_config(dataset_config, stage)
        image_paths = get_image_paths_from_dir(os.path.join(dataset_config.dataset_path, stage))
        self.imgs = ImagePathDataset(self.dataset_config, image_paths)

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, i):
        return self.imgs[i]


@Registers.datasets.register_with_name('custom_aligned')
class CustomAlignedDataset(Dataset):
    def __init__(self, dataset_config, stage='train'):
        super().__init__()
        image_paths_ori = get_image_paths_from_dir(os.path.join(dataset_config.dataset_path, f'{stage}/B'))
        image_paths_cond = get_image_paths_from_dir(os.path.join(dataset_config.dataset_path, f'{stage}/A'))
        self.dataset_config = preprocess_dataset_config(dataset_config, stage)
        self.imgs = ImagePathDataset(self.dataset_config, image_paths_ori, image_paths_cond)

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, i):
        return self.imgs[i]

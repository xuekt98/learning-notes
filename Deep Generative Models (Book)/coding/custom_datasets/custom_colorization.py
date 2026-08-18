import os
from pathlib import Path

import cv2
import torch
from auxilliary.Register import Registers
from torch.utils.data import Dataset
from custom_datasets.utils import get_image_paths_from_dir, preprocess_dataset_config, read_image, transform_image


@Registers.datasets.register_with_name('custom_colorization_RGB')
class CustomColorizationRGBDataset(Dataset):
    def __init__(self, dataset_config, stage='train'):
        super().__init__()
        self.dataset_config = preprocess_dataset_config(dataset_config, stage)
        self.image_paths = get_image_paths_from_dir(os.path.join(dataset_config.dataset_path, stage))
        self._length = len(self.image_paths)
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

        cond_image = image.convert('L')
        cond_image = cond_image.convert('RGB')

        image, cond_image = transform_image(self.dataset_config, image, cond_image)
        return (image, image_name), (cond_image, image_name)


@Registers.datasets.register_with_name('custom_colorization_LAB')
class CustomColorizationLABDataset(Dataset):
    def __init__(self, dataset_config, stage='train'):
        super().__init__()
        self.dataset_config = preprocess_dataset_config(dataset_config, stage)
        self.image_paths = get_image_paths_from_dir(os.path.join(dataset_config.dataset_path, stage))
        self._length = len(self.image_paths)
        self.flip = self.dataset_config.flip

    def __len__(self):
        if self.flip:
            return self._length * 2
        return self._length

    def __getitem__(self, index):
        p = False
        if index >= self._length:
            index = index - self._length
            p = True

        img_path = self.image_paths[index]
        image_name = Path(img_path).stem
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        image = cv2.flip(image, 1)
        image = cv2.resize(image, self.dataset_config.image_size, interpolation=cv2.INTER_LINEAR)
        image = torch.Tensor(image)
        image = image.permute(2, 0, 1).contiguous()

        if self.dataset_config.to_normal:
            image = ((image - 127.5) / 127.5).clamp_(-1., 1.)

        L = image[0:1, :, :]
        ab = image[1:, :, :]
        # cond_image = torch.cat((L, L, L), dim=0)
        return (ab, image_name), (L, image_name)



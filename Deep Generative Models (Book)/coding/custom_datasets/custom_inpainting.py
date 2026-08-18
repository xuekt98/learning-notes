import os
from pathlib import Path
import math
import numpy as np
import cv2
import torch
import torchvision.transforms as transforms
from random import random, randint
from PIL import Image, ImageDraw
from auxilliary.Register import Registers
from torch.utils.data import Dataset
from custom_datasets.utils import get_image_paths_from_dir, preprocess_dataset_config, read_image, transform_image


def generate_random_mask(height: int = 256,
                         width: int = 256,
                         min_lines: int = 1,
                         max_lines: int = 4,
                         min_vertex: int = 5,
                         max_vertex: int = 13,
                         mean_angle: float = 2/5 * math.pi,
                         angle_range: float = 2/15 * math.pi,
                         min_width: float = 12,
                         max_width: float = 40):
    """
    Generate random mask for GAN. Each pixel of mask
    if 1 or 0, 1 means pixel is masked.

    Parameters
    ----------
    height : int
        Height of mask.
    width : int
        Width of mask.
    min_lines : int
        Miniumal count of lines to draw on mask.
    max_lines : int
        Maximal count of lines to draw on mask.
    min_vertex : int
        Minimal count of vertexes to draw.
    max_vertex : int
        Maximum count of vertexes to draw.
    mean_angle : float
        Mean value of angle between edges.
    angle_range : float
        Maximum absoulte deviation of angle from mean value.
    min_width : int
        Minimal width of edge to draw.
    max_width : int
        Maximum width of edge to draw.
    """

    # init mask and drawing tool
    mask = Image.new('1', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # calculate mean radius to draw lines and count of lines
    num_lines = np.random.randint(min_lines, max_lines)
    average_radius = math.sqrt(height * height + width * width) / 8

    # drawing lines
    for _ in range(num_lines):
        angle_min = mean_angle - np.random.uniform(0, angle_range)
        angle_max = mean_angle + np.random.uniform(0, angle_range)
        num_vertex = np.random.randint(min_vertex, max_vertex)

        # line parameters
        angles = []
        vertex = []

        # generating line angles
        for i in range(num_vertex - 1):
            random_angle = np.random.uniform(angle_min, angle_max)
            if i % 2 == 0:
                random_angle = 2 * np.pi - random_angle
            angles.append(random_angle)

        # start point
        start_x = np.random.randint(0, width)
        start_y = np.random.randint(0, height)
        vertex.append((start_x, start_y))

        # generating next points
        for i in range(num_vertex - 1):
            radius = np.random.normal(loc=average_radius, scale=average_radius / 2)
            radius = np.clip(radius, 0, 2 * average_radius)
            new_x = np.clip(vertex[-1][0] + radius * math.cos(angles[i]), 0, width)
            new_y = np.clip(vertex[-1][1] + radius * math.sin(angles[i]), 0, height)
            vertex.append((int(new_x), int(new_y)))

        # drawing line
        line_width = np.random.uniform(min_width, max_width)
        line_width = int(line_width)
        draw.line(vertex, fill=1, width=line_width)

        # smoothing angles
        for node in vertex:
            x_ul = node[0] - line_width // 2
            x_br = node[0] + line_width // 2
            y_ul = node[1] - line_width // 2
            y_br = node[1] + line_width // 2
            draw.ellipse((x_ul, y_ul, x_br, y_br), fill=1)

    # random vertical flip
    if np.random.normal() > 0:
        mask.transpose(Image.FLIP_LEFT_RIGHT)

    # random horizontal flip
    if np.random.normal() > 0:
        mask.transpose(Image.FLIP_TOP_BOTTOM)

    mask = np.asarray(mask, np.float32)
    return torch.from_numpy(mask)


@Registers.datasets.register_with_name('custom_inpainting')
class CustomInpaintingDataset(Dataset):
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

        transform = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.Resize(self.dataset_config.image_size),
            transforms.ToTensor()
        ])

        img_path = self.image_paths[index]
        image, image_name = read_image(img_path)
        image = transform(image)
        height, width = self.dataset_config.image_size

        crop_type = random()
        if crop_type < self.dataset_config.crop_p1:
            sc_mask = 1. - generate_random_mask(height=height, width=width)
            mask = torch.zeros_like(image)
            mask[:] = sc_mask
            cond_image = image * mask
        else:
            mask = torch.ones_like(image)
            mask[:, height//4:height//4 + height//2, width//4:width//4 + width//2] = 0
            cond_image = image * mask

        if self.dataset_config.to_normal:
            image = ((image - 0.5) * 2.).clamp_(-1., 1.)
            cond_image = ((cond_image - 0.5) * 2.).clamp_(-1., 1.)
        return (image, image_name), (cond_image, image_name), mask


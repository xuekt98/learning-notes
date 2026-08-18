import os
import argparse
from pathlib import Path

from random import random, randint
from PIL import Image
from torchvision.transforms import transforms


def preprocess_dataset_config(dataset_config, stage):
    dataset_config_copy = argparse.Namespace()
    assert dataset_config.__contains__('dataset_path'), f'muse specify dataset path in dataset_config'
    assert dataset_config.dataset_path is not None, f'muse specify dataset path in dataset_config'
    assert dataset_config.__contains__('dataset_name'), f'muse specify dataset name in dataset_config'
    assert dataset_config.dataset_name is not None, f'muse specify dataset name in dataset_config'

    dataset_config_copy.dataset_path = dataset_config.dataset_path
    dataset_config_copy.dataset_name = dataset_config.dataset_name
    dataset_config_copy.image_size = (dataset_config.image_size, dataset_config.image_size) if dataset_config.__contains__('image_size') else (256, 256)
    dataset_config_copy.channels = dataset_config.channels if dataset_config.__contains__('channels') else 3
    dataset_config_copy.flip = dataset_config.flip if dataset_config.__contains__(
        'flip') and stage == 'train' else False
    dataset_config_copy.to_normal = dataset_config.to_normal if dataset_config.__contains__('to_normal') else True
    dataset_config_copy.resize = dataset_config.resize if dataset_config.__contains__(
        'resize') and stage == 'test' else True
    dataset_config_copy.random_crop = dataset_config.random_crop if dataset_config.__contains__(
        'random_crop') and stage != 'test' else False
    dataset_config_copy.crop_p1 = dataset_config.crop_p1 if dataset_config.__contains__('crop_p1') else 1.0
    dataset_config_copy.crop_p2 = dataset_config.crop_p2 if dataset_config.__contains__('crop_p2') else 1.0
    return dataset_config_copy


def get_image_paths_from_dir(fdir):
    flist = os.listdir(fdir)
    flist.sort()
    image_paths = []
    for i in range(0, len(flist)):
        fpath = os.path.join(fdir, flist[i])
        ext = flist[i].split(".")[-1]
        if os.path.isdir(fpath):
            image_paths.extend(get_image_paths_from_dir(fpath))
        elif "." in flist[i] and ext.lower() in ['jpg', 'jpeg', 'png', 'gif']:
            image_paths.append(fpath)
    return image_paths


def read_image(image_path):
    try:
        image = Image.open(image_path)
        image_name = Path(image_path).stem
        if not image.mode == 'RGB':
            image = image.convert('RGB')
        if image is None:
            print('image is None')
            print(image_path)
        if image_name is None:
            print('image_name is None')
            print(image_path)
        return image, image_name
    except FileNotFoundError as e:
        print(image_path)


def transform_image(dataset_config, image, image_cond=None):
    has_cond = True if image_cond is not None else False
    width_image, height_image = image.size
    width_cond, height_cond = image_cond.size if has_cond else image.size
    height_resize, width_resize = dataset_config.image_size

    transform_list = [transforms.ToTensor()]
    if dataset_config.flip:
        transform_list.append(transforms.RandomHorizontalFlip())

    if dataset_config.resize:
        crop_type = random()
        if not dataset_config.random_crop or crop_type < dataset_config.crop_p1:
            transform_list.append(transforms.Resize(dataset_config.image_size))
        else:
            if width_image < width_resize or height_image < height_resize \
                    or width_image != width_cond or height_image != height_cond \
                    or crop_type < dataset_config.crop_p2:
                transform_list.append(transforms.Resize((height_resize * 2, width_resize * 2)))

        transform = transforms.Compose(transform_list)
        image = transform(image)
        image_cond = transform(image_cond) if has_cond else None

        c, h, w = image.shape
        rand_w, rand_h = randint(0, w - width_resize), randint(0, h - height_resize)
        image = image[:, rand_h:rand_h + height_resize, rand_w:rand_w + width_resize]
        image_cond = image_cond[:, rand_h:rand_h + height_resize, rand_w:rand_w + width_resize] if has_cond else None

    if dataset_config.to_normal:
        image = ((image - 0.5) * 2.).clamp_(-1., 1.)
        image_cond = ((image_cond - 0.5) * 2.).clamp_(-1., 1.) if has_cond else None

    if has_cond:
        return image, image_cond
    else:
        return image

import torch
import torch.nn as nn


def get_1d_normalization_layer(normalization, in_channels):
    if normalization == 'batch_norm':
        return nn.BatchNorm1d(num_features=in_channels)
    elif normalization == 'group_norm':
        return nn.GroupNorm(num_groups=32, num_channels=in_channels)
    else:
        raise NotImplementedError


def get_2d_normalization_layer(normalization, in_channels):
    if normalization == 'batch_norm':
        return nn.BatchNorm2d(num_features=in_channels)
    elif normalization == 'group_norm':
        return nn.GroupNorm(num_groups=32, num_channels=in_channels)
    else:
        raise NotImplementedError


def get_activation_layer(activation, *args, **kwargs):
    if activation == 'ReLU':
        return nn.ReLU()
    elif activation == 'LeakyReLU':
        return nn.LeakyReLU()
    elif activation == 'Sigmoid':
        return nn.Sigmoid()
    else:
        raise NotImplementedError
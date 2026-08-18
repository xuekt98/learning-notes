import pdb

import torch
import torch.nn as nn

from model.utils import get_activation_layer, get_1d_normalization_layer


class MLPBaseLayer(nn.Module):
    def __init__(self, n_linear, in_channels, mid_channels, out_channels,
                 normalization='batch_norm', activation='ReLU', dropout=0.):
        super(MLPBaseLayer, self).__init__()

        self.blocks = nn.ModuleList()
        # self.blocks.append(get_1d_normalization_layer(normalization, in_channels))
        self.blocks.append(nn.Sequential(nn.Linear(in_channels, mid_channels),
                                         get_activation_layer(activation),
                                         nn.Dropout(dropout)))
        for i in range(n_linear):
            self.blocks.append(nn.Sequential(nn.Linear(mid_channels, mid_channels),
                                             get_activation_layer(activation),
                                             nn.Dropout(dropout)))
        self.blocks.append(nn.Sequential(nn.Linear(mid_channels, out_channels),
                                         get_activation_layer(activation),
                                         nn.Dropout(dropout)))

    def forward(self, input):
        h = input
        for block in self.blocks:
            h = block(h)
        return h
        # return self.blocks(input)
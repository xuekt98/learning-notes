import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange

from model.DiscriminativeModel.base.MLPBaseLayer import MLPBaseLayer


class DiscriminativeModel(nn.Module):
    def __init__(self, config):
        super(DiscriminativeModel, self).__init__()

        self.config = config
        self.model_params = config.model.params
        self.ch_mult = self.model_params.ch_mult
        self.num_linear_layers = self.model_params.num_linear_layers
        self.in_channels = self.model_params.in_channels
        self.out_channels = self.model_params.out_channels
        self.mid_channels = self.model_params.mid_channels

        self.layers = nn.ModuleList()
        self.layers.append(nn.Flatten())

        channels = [self.in_channels, self.out_channels]
        for i in range(len(self.ch_mult)):
            channels.insert(1, self.ch_mult[i] * self.mid_channels)

        for i in range(len(channels) - 1):
            self.layers.append(MLPBaseLayer(n_linear=self.num_linear_layers,
                                            in_channels=channels[i],
                                            mid_channels=channels[i+1],
                                            out_channels=channels[i+1],
                                            activation=self.model_params.activation,
                                            normalization=self.model_params.normalization,
                                            dropout=self.model_params.dropout))
        # self.layers.append(nn.Softmax(dim=1))

    def forward(self, input):
        h = input
        for module in self.layers:
            h = module(h)
        return h
        # return self.layers(input)


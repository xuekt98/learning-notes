import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange
from tqdm import tqdm

from model.AutoregressiveModel.base.CausalConvLayer import CausalConv1d
from model.utils import get_activation_layer


class AutoregressiveModel(nn.Module):
    def __init__(self, config):
        super(AutoregressiveModel, self).__init__()

        self.config = config
        self.model_params = config.model.params
        self.D = self.model_params.D
        self.in_channels = self.model_params.in_channels
        self.out_channels = self.model_params.out_channels
        self.ch_mult = self.model_params.ch_mult
        self.mid_channels = self.model_params.mid_channels

        self.layers = nn.ModuleList()
        channels = [self.in_channels, self.out_channels]
        for i in range(len(self.ch_mult)):
            channels.insert(1, self.ch_mult[i] * self.mid_channels)

        for i in range(len(channels) - 1):
            self.layers.append(nn.BatchNorm1d(num_features=channels[i]))
            self.layers.append(CausalConv1d(in_channels=channels[i],
                                            out_channels=channels[i+1],
                                            kernel_size=self.model_params.kernel_size,
                                            dilation=1,
                                            A=True if i == 0 else False))
            self.layers.append(get_activation_layer(self.model_params.activation))
        # self.layers.append(nn.Softmax(dim=1))

    def forward(self, input):
        h = input
        for module in self.layers:
            h = module(h)
        return h

    def sample(self, batch_size=4):
        device = self.config.training.device[0]
        sample = torch.zeros((batch_size, 1, self.D)).to(device)
        for d in tqdm(range(self.D), desc='sampling loop', smoothing=0.01):
            p = nn.Softmax(dim=1)(self.forward(sample))
            p = rearrange(p, 'b c d -> b d c')
            sample_new_d = torch.multinomial(p[:, d, :], num_samples=1)
            sample[:, :, d] = sample_new_d
        return rearrange(sample / 255., 'b c (h w) -> b c h w', h=28, w=28)




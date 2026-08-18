import pdb

import torch
import torch.nn as nn
from einops import rearrange

from model.GANModel.base.Discriminator import Discriminator
from model.GANModel.base.Generator import Generator


class GANModel(nn.Module):
    def __init__(self, config):
        super(GANModel, self).__init__()

        self.config = config
        self.generator = Generator(config.model.generator)
        self.discriminator = Discriminator(config.model.discriminator)

        train_batch_size = config.data.train_batch_size
        val_batch_size = config.data.val_batch_size
        test_batch_size = config.data.test_batch_size
        h = w = config.data.dataset_config.image_size
        self.image_channel = c = config.data.dataset_config.channels
        self.image_size = config.data.dataset_config.image_size

        self.train_shape = (train_batch_size, c, h*w)
        self.val_shape = (val_batch_size, c, h*w)
        self.test_shape = (test_batch_size, c, h*w)

        self.device = config.training.device[0]
        self.EPS = 1.e-5

    def forward(self, input, idx=0):
        if idx == 0:
            x_fake = self.generator(input.shape, input.device)
            d_fake = torch.clamp(self.discriminator(x_fake), self.EPS, 1.-self.EPS)
            return (torch.log(1. - d_fake)).mean()
        else:
            x_fake = self.generator(input.shape, input.device)
            d_fake = torch.clamp(self.discriminator(x_fake), self.EPS, 1.-self.EPS)
            d_real = torch.clamp(self.discriminator(input), self.EPS, 1.-self.EPS)
            return -(torch.log(d_real) + torch.log(1. - d_fake)).mean()

    def sample(self):
        sample = self.generator(self.test_shape, self.device)
        sample = rearrange(sample, 'b (c h w) -> b c h w', c=self.image_channel, h=self.image_size, w=self.image_size)
        return sample

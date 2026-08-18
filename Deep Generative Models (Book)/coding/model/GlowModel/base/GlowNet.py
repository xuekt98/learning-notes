import pdb

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from model.GlowModel.base import modules
import model.GlowModel.base.utils as thops


def f(in_channels, out_channels, hidden_channels):
    return nn.Sequential(
        modules.Conv2d(in_channels, hidden_channels), nn.ReLU(inplace=False),
        modules.Conv2d(hidden_channels, hidden_channels, kernel_size=[1, 1]), nn.ReLU(inplace=False),
        modules.Conv2dZeros(hidden_channels, out_channels))


class FlowStep(nn.Module):
    FlowCoupling = ["additive", "affine"]
    FlowPermutation = {
        "reverse": lambda obj, z, logdet, rev: (obj.reverse(z, rev), logdet),
        "shuffle": lambda obj, z, logdet, rev: (obj.shuffle(z, rev), logdet),
        "invconv": lambda obj, z, logdet, rev: obj.invconv(z, logdet, rev)
    }

    def __init__(self, in_channels, hidden_channels,
                 actnorm_scale=1.0,
                 flow_permutation="invconv",
                 flow_coupling="additive",
                 LU_decomposed=False):
        # check configures
        assert flow_coupling in FlowStep.FlowCoupling, \
            "flow_coupling should be in `{}`".format(FlowStep.FlowCoupling)
        assert flow_permutation in FlowStep.FlowPermutation, \
            "float_permutation should be in `{}`".format(
                FlowStep.FlowPermutation.keys())
        super().__init__()
        self.flow_permutation = flow_permutation
        self.flow_coupling = flow_coupling

        # 1. actnorm
        self.actnorm = modules.ActNorm2d(in_channels, actnorm_scale)

        # 2. permute
        if flow_permutation == "invconv":
            self.invconv = modules.InvertibleConv1x1(
                in_channels, LU_decomposed=LU_decomposed)
        elif flow_permutation == "shuffle":
            self.shuffle = modules.Permute2d(in_channels, shuffle=True)
        else:
            self.reverse = modules.Permute2d(in_channels, shuffle=False)

        # 3. coupling
        if flow_coupling == "additive":
            self.f = f(in_channels // 2, in_channels // 2, hidden_channels)
        elif flow_coupling == "affine":
            self.f = f(in_channels // 2, in_channels, hidden_channels)

    def forward(self, input, logdet=None, reverse=False):
        if not reverse:
            return self.normal_flow(input, logdet)
        else:
            return self.reverse_flow(input, logdet)

    def normal_flow(self, input, logdet):
        assert input.size(1) % 2 == 0
        # pdb.set_trace()
        # 1. actnorm
        z, logdet = self.actnorm(input, logdet=logdet, reverse=False)
        # 2. permute
        z, logdet = FlowStep.FlowPermutation[self.flow_permutation](
            self, z, logdet, False)
        # 3. coupling
        z1, z2 = thops.split_feature(z, "split")
        if self.flow_coupling == "additive":
            z2 = z2 + self.f(z1)
        elif self.flow_coupling == "affine":
            h = self.f(z1)
            shift, scale = thops.split_feature(h, "cross")
            scale = torch.sigmoid(scale + 2.)
            z2 = z2 + shift
            z2 = z2 * scale
            logdet = thops.sum(torch.log(scale), dim=[1, 2, 3]) + logdet
        z = thops.cat_feature(z1, z2)
        return z, logdet

    def reverse_flow(self, input, logdet):
        assert input.size(1) % 2 == 0
        # 1.coupling
        z1, z2 = thops.split_feature(input, "split")
        if self.flow_coupling == "additive":
            z2 = z2 - self.f(z1)
        elif self.flow_coupling == "affine":
            h = self.f(z1)
            shift, scale = thops.split_feature(h, "cross")
            scale = torch.sigmoid(scale + 2.)
            z2 = z2 / scale
            z2 = z2 - shift
            logdet = -thops.sum(torch.log(scale), dim=[1, 2, 3]) + logdet
        z = thops.cat_feature(z1, z2)
        # 2. permute
        z, logdet = FlowStep.FlowPermutation[self.flow_permutation](
            self, z, logdet, True)
        # 3. actnorm
        z, logdet = self.actnorm(z, logdet=logdet, reverse=True)
        return z, logdet


class GlowNet(nn.Module):
    def __init__(self, image_shape, hidden_channels, K, L,
                 actnorm_scale=1.0,
                 flow_permutation='invconv',
                 flow_coupling='additive',
                 LU_decomposed=False):
        """
                             K                                      K
        --> [Squeeze] -> [FlowStep] -> [Split] -> [Squeeze] -> [FlowStep]
               ^                           v
               |          (L - 1)          |
               + --------------------------+
        """
        super().__init__()
        self.layers = nn.ModuleList()
        self.output_shapes = []
        self.K = K
        self.L = L
        H, W, C = image_shape
        assert C == 1 or C == 3, ("image_shape should be HWC, like (64, 64, 3)"
                                  "C == 1 or C == 3")
        for i in range(L):
            # 1. Squeeze
            C, H, W = C * 4, H // 2, W // 2
            self.layers.append(modules.SqueezeLayer(factor=2))
            self.output_shapes.append([-1, C, H, W])

            # 2. K FlowStep
            for _ in range(K):
                self.layers.append(
                    FlowStep(in_channels=C,
                             hidden_channels=hidden_channels,
                             actnorm_scale=actnorm_scale,
                             flow_permutation=flow_permutation,
                             flow_coupling=flow_coupling,
                             LU_decomposed=LU_decomposed))
                self.output_shapes.append(
                    [-1, C, H, W])

            # 3. Split2d
            if i < L - 1:
                self.layers.append(modules.Split2d(num_channels=C))
                self.output_shapes.append([-1, C // 2, H, W])
                C = C // 2

    def forward(self, input, logdet=0., reverse=False, eps_std=None):
        if not reverse:
            return self.encode(input, logdet)
        else:
            return self.decode(input, eps_std)

    def encode(self, z, logdet=0.0):
        for layer, shape in zip(self.layers, self.output_shapes):
            z, logdet = layer(z, logdet, reverse=False)
        return z, logdet

    def decode(self, z, eps_std=None):
        for layer in reversed(self.layers):
            if isinstance(layer, modules.Split2d):
                z, logdet = layer(z, logdet=0, reverse=True, eps_std=eps_std)
            else:
                z, logdet = layer(z, logdet=0, reverse=True)
        return z


import pdb

import torch
import torch.nn as nn
import numpy as np
from tqdm import tqdm
import model.GlowModel.base.utils as thops
from model.GlowModel.base import modules
from model.GlowModel.base.GlowNet import GlowNet


class GlowModel(nn.Module):
    BCE = nn.BCEWithLogitsLoss()
    CE = nn.CrossEntropyLoss()

    def __init__(self, config):
        super().__init__()
        self.flow = GlowNet(image_shape=config.model.params.image_shape,
                            hidden_channels=config.model.params.hidden_channels,
                            K=config.model.params.K,
                            L=config.model.params.L,
                            actnorm_scale=config.model.params.actnorm_scale,
                            flow_permutation=config.model.params.flow_permutation,
                            flow_coupling=config.model.params.flow_coupling,
                            LU_decomposed=config.model.params.LU_decomposed)
        self.config = config
        self.y_classes = config.model.params.y_classes
        # for prior
        if config.model.params.learn_top:
            C = self.flow.output_shapes[-1][1]
            self.learn_top = modules.Conv2dZeros(C * 2, C * 2)
        if config.model.params.y_condition:
            C = self.flow.output_shapes[-1][1]
            self.project_ycond = modules.LinearZeros(
                config.model.params.y_classes, 2 * C)
            self.project_class = modules.LinearZeros(
                C, config.model.params.y_classes)

        self.register_parameter(
            "prior_h",
            nn.Parameter(torch.zeros([config.data.train.batch_size,
                                      self.flow.output_shapes[-1][1] * 2,
                                      self.flow.output_shapes[-1][2],
                                      self.flow.output_shapes[-1][3]])))

    def get_parameters(self):
        return self.parameters()

    def prior(self, y_onehot=None):
        B, C = self.prior_h.size(0), self.prior_h.size(1)
        h = self.prior_h.detach().clone()
        assert torch.sum(h) == 0.0
        if self.config.model.params.learn_top:
            h = self.learn_top(h)
        if self.config.model.params.y_condition:
            assert y_onehot is not None
            yp = self.project_ycond(y_onehot).view(B, C, 1, 1)
            h += yp
        return thops.split_feature(h, "split")

    def forward(self, x=None, y_onehot=None, z=None,
                eps_std=None, reverse=False):
        if not reverse:
            return self.normal_flow(x, y_onehot)
        else:
            return self.reverse_flow(z, y_onehot, eps_std)

    def normal_flow(self, x, y_onehot):
        pixels = thops.pixels(x)
        z = x + torch.normal(mean=torch.zeros_like(x),
                             std=torch.ones_like(x) * (1. / 256.))
        logdet = torch.zeros_like(x[:, 0, 0, 0])
        logdet += float(-np.log(256.) * pixels)
        # encode
        # pdb.set_trace()
        z, objective = self.flow(z, logdet=logdet, reverse=False)
        # prior
        mean, logs = self.prior(y_onehot)
        logdet = objective
        prior = modules.GaussianDiag.logp(mean, logs, z)
        objective += prior

        if self.config.model.params.y_condition:
            y_logits = self.project_class(z.mean(2).mean(2))
        else:
            y_logits = None

        # return
        nll = (-objective) / float(np.log(2.) * pixels)

        loss_dict = {
            'loss_logdet': logdet.mean(),
            'loss_prior': prior.mean()
        }

        return z, nll, y_logits, loss_dict

    def reverse_flow(self, z, y_onehot, eps_std):
        with torch.no_grad():
            mean, logs = self.prior(y_onehot)
            if z is None:
                z = modules.GaussianDiag.sample(mean, logs, eps_std)
            x = self.flow(z, eps_std=eps_std, reverse=True)
        return x

    def set_actnorm_init(self, inited=True):
        for name, m in self.named_modules():
            if (m.__class__.__name__.find("ActNorm") >= 0):
                m.inited = inited

    def generate_z(self, img):
        self.eval()
        B = self.config.data.train.batch_size
        x = img.unsqueeze(0).repeat(B, 1, 1, 1).cuda()
        z, _, _ = self(x)
        self.train()
        return z[0].detach().cpu().numpy()

    def generate_attr_deltaz(self, dataset):
        assert "y_onehot" in dataset[0]
        self.eval()
        with torch.no_grad():
            B = self.config.data.train.batch_size
            N = len(dataset)
            attrs_pos_z = [[0, 0] for _ in range(self.y_classes)]
            attrs_neg_z = [[0, 0] for _ in range(self.y_classes)]
            for i in tqdm(range(0, N, B)):
                j = min([i + B, N])
                # generate z for data from i to j
                xs = [dataset[k]["x"] for k in range(i, j)]
                while len(xs) < B:
                    xs.append(dataset[0]["x"])
                xs = torch.stack(xs).cuda()
                zs, _, _ = self(xs)
                for k in range(i, j):
                    z = zs[k - i].detach().cpu().numpy()
                    # append to different attrs
                    y = dataset[k]["y_onehot"]
                    for ai in range(self.y_classes):
                        if y[ai] > 0:
                            attrs_pos_z[ai][0] += z
                            attrs_pos_z[ai][1] += 1
                        else:
                            attrs_neg_z[ai][0] += z
                            attrs_neg_z[ai][1] += 1
                # break
            deltaz = []
            for ai in range(self.y_classes):
                if attrs_pos_z[ai][1] == 0:
                    attrs_pos_z[ai][1] = 1
                if attrs_neg_z[ai][1] == 0:
                    attrs_neg_z[ai][1] = 1
                z_pos = attrs_pos_z[ai][0] / float(attrs_pos_z[ai][1])
                z_neg = attrs_neg_z[ai][0] / float(attrs_neg_z[ai][1])
                deltaz.append(z_pos - z_neg)
        self.train()
        return deltaz

    @staticmethod
    def loss_generative(nll):
        # Generative loss
        return torch.mean(nll)

    @staticmethod
    def loss_multi_classes(y_logits, y_onehot):
        if y_logits is None:
            return 0
        else:
            return GlowModel.BCE(y_logits, y_onehot.float())

    @staticmethod
    def loss_class(y_logits, y):
        if y_logits is None:
            return 0
        else:
            return GlowModel.CE(y_logits, y.long())




import pdb

import torch
from einops import rearrange

from auxilliary.Register import Registers
from model.GANModel.GANModel import GANModel
from runners.BaseRunner import BaseRunner
from runners.utils import get_optimizer, get_image_grid, weights_init


@Registers.runners.register_with_name('GANModelRunner')
class GANModelRunner(BaseRunner):
    def __init__(self, config):
        super().__init__(config)

    def initialize_model(self, config):
        gan = GANModel(config).to(config.training.device[0])
        gan.apply(weights_init)
        return gan

    def initialize_optimizer_scheduler(self, net, config):
        optimizer_g = get_optimizer(config.model.optimizer_g, net.generator.parameters())
        optimizer_d = get_optimizer(config.model.optimizer_d, net.discriminator.parameters())

        return [optimizer_g, optimizer_d], []

    def loss_fn(self, net, batch, epoch, step, opt_idx=0, stage='train', write=True):
        device = self.config.training.device[0]
        img, _ = batch
        img = img.to(device)

        img = rearrange(img, 'b c h w -> b c (h w)')

        if opt_idx == 0:
            loss = net(img, opt_idx)
        else:
            loss = net(img, opt_idx)

        if write:
            self.writer.add_scalar(f'{stage}/loss{opt_idx}', loss, step)
        return loss

    def train_step(self, train_batch, epoch, step):
        self.net.train()

        losses = []
        for i in range(len(self.optimizer)):
            self.optimizer[i].zero_grad()

        loss = self.loss_fn(net=self.net,
                            batch=train_batch,
                            epoch=epoch,
                            step=step,
                            opt_idx=1,
                            stage='train')
        loss.backward(retain_graph=True)
        self.optimizer[1].step()
        losses.append(loss)

        for i in range(len(self.optimizer)):
            self.optimizer[i].zero_grad()

        loss = self.loss_fn(net=self.net,
                            batch=train_batch,
                            epoch=epoch,
                            step=step,
                            opt_idx=0,
                            stage='train')
        loss.backward(retain_graph=True)
        self.optimizer[0].step()
        losses.insert(0, loss)
        return losses

    def sample(self, net, batch, sample_path, stage='train'):
        sample = net.sample()
        img, _ = batch
        if stage == 'val':
            image_grid = get_image_grid(img, grid_size=4, to_normal=self.config.data.dataset_config.to_normal)
            self.writer.add_image(f'sample/gt', image_grid, self.global_step, dataformats='HWC')
            image_grid = get_image_grid(sample, grid_size=4, to_normal=self.config.data.dataset_config.to_normal)
            self.writer.add_image(f'sample/image', image_grid, self.global_step, dataformats='HWC')

    def sample_to_eval(self, net, test_loader, sample_path):
        return









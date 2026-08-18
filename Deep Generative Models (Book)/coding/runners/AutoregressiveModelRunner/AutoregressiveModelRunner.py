import pdb

import torch.nn
import torch.nn.functional as F
from tqdm import tqdm

from auxilliary.Register import Registers
from einops import rearrange
from model.AutoregressiveModel.AutoregressiveModel import AutoregressiveModel
from runners.BaseRunner import BaseRunner
from runners.utils import weights_init, get_optimizer, get_image_grid


@Registers.runners.register_with_name('AutoregressiveModelRunner')
class AutoregressiveModelRunner(BaseRunner):
    def __init__(self, config):
        super().__init__(config)

    def initialize_model(self, config):
        ARMModel = AutoregressiveModel(config)
        ARMModel.apply(weights_init)
        return ARMModel

    def initialize_optimizer_scheduler(self, net, config):
        optimizer = get_optimizer(config.model.optimizer, net.parameters())
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer=optimizer,
                                                               mode='min',
                                                               verbose=True,
                                                               threshold_mode='rel',
                                                               **vars(config.model.scheduler)
                                                               )
        return [optimizer], [scheduler]

    def loss_fn(self, net, batch, epoch, step, opt_idx=0, stage='train', write=True):
        device = self.config.training.device[0]
        img, _ = batch
        img = img.to(device)

        b, c, h, w = img.shape

        input = rearrange(img, 'b c h w -> b c (h w)')
        pred = net(input)
        pred = rearrange(pred, 'b c d -> (b d) c')

        target = (input.permute(0, 2, 1) * 255).long().squeeze(dim=-1)
        target = rearrange(target, 'b c -> (b c)')
        loss = torch.nn.CrossEntropyLoss()(pred, target)

        if write:
            self.writer.add_scalar(f'{stage}/loss', loss, step)
            if stage == 'val_step':
                pred_values, pred_img = torch.topk(pred, k=1, dim=1)
                pred_img = rearrange(pred_img, '(b h w) c -> b c h w', b=b, h=h, w=w) / 255.
                image_grid = get_image_grid(pred_img, grid_size=4, to_normal=False)
                self.writer.add_image(f'val_step/image_rec', image_grid, self.global_step, dataformats='HWC')

                image_grid = get_image_grid(img, grid_size=4, to_normal=False)
                self.writer.add_image(f'val_step/image_gt', image_grid, self.global_step, dataformats='HWC')
        return loss

    def sample(self, net, batch, sample_path, stage='train'):
        img = net.sample()

        if stage == 'val':
            image_grid = get_image_grid(img, grid_size=4, to_normal=self.config.data.dataset_config.to_normal)
            self.writer.add_image(f'sample/image', image_grid, self.global_step, dataformats='HWC')

    def sample_to_eval(self, net, test_loader, sample_path):
        pass



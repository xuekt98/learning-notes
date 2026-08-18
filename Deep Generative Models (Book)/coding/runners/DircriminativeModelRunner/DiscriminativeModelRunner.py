import pdb

import torch.nn
from tqdm import tqdm

from auxilliary.Register import Registers
from model.DiscriminativeModel.DiscriminativeModel import DiscriminativeModel
from runners.BaseRunner import BaseRunner
from runners.utils import weights_init, get_optimizer, get_image_grid


@Registers.runners.register_with_name('DiscriminativeModelRunner')
class DiscriminativeModelRunner(BaseRunner):
    def __init__(self, config):
        super().__init__(config)

    def initialize_model(self, config):
        DiscModel = DiscriminativeModel(config)
        DiscModel.apply(weights_init)
        return DiscModel

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
        img, label = batch
        img = img.to(device)
        label = label.to(device)

        pred = net(img)
        pred_values, pred_indices = torch.topk(pred, k=1, dim=-1)

        loss = torch.nn.CrossEntropyLoss()(pred, label)

        if write:
            self.writer.add_scalar(f'{stage}/loss', loss, step)
            if stage == 'val_step':
                image_grid = get_image_grid(img, grid_size=4, to_normal=self.config.data.dataset_config.to_normal)
                self.writer.add_image(f'{stage}/image', image_grid, self.global_step, dataformats='HWC')
                self.writer.add_text(f'{stage}/predict', str(pred_indices), self.global_step)
        return loss

    def sample(self, net, batch, sample_path, stage='train'):
        device = self.config.training.device[0]
        img, label = batch
        img = img.to(device)
        label = label.to(device)

        pred = net(img)
        pred_values, pred_indices = torch.topk(pred, k=1, dim=-1)

        if stage=='val':
            image_grid = get_image_grid(img, grid_size=4, to_normal=self.config.data.dataset_config.to_normal)
            self.writer.add_image(f'sample/image', image_grid, self.global_step, dataformats='HWC')
            self.writer.add_text(f'sample/predict', str(pred_indices), self.global_step)
            self.writer.add_text(f'sample/gt', str(label), self.global_step)

    def sample_to_eval(self, net, test_loader, sample_path):
        device = self.config.training.device[0]
        pbar = tqdm(test_loader, total=len(test_loader), smoothing=0.01)

        for test_batch in pbar:
            img, label = test_batch
            img = img.to(device)
            label = label.to(device)

            pred = net(img)
            pred_values, pred_indices = torch.topk(pred, k=1, dim=-1)
        return


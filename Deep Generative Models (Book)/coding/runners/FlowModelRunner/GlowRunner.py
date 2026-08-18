import os

import torch
from PIL import Image

from auxilliary.Register import Registers
from model.GlowModel.GlowModel import GlowModel
from model.GlowModel.base import learning_rate_schedule
from runners.FlowModelRunner.FlowBaseRunner import FlowBaseRunner
from runners.utils import weights_init, get_optimizer, get_dataset, make_dir, get_image_grid, save_single_image
from tqdm.autonotebook import tqdm


@Registers.runners.register_with_name('GlowRunner')
class GlowRunner(FlowBaseRunner):
    def __init__(self, config):
        super().__init__(config)

    def initialize_model(self, config):
        glownet = GlowModel(config).to(config.training.device[0])
        return glownet

    def print_model_summary(self, net):
        def get_parameter_number(model):
            total_num = sum(p.numel() for p in model.parameters())
            trainable_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
            return total_num, trainable_num

        total_num, trainable_num = get_parameter_number(net)
        print("Total Number of parameter: %.2fM" % (total_num / 1e6))
        print("Trainable Number of parameter: %.2fM" % (trainable_num / 1e6))

    def initialize_optimizer_scheduler(self, graph, hparams):
        def build_adam(params, args):
            return torch.optim.Adam(params, **args)

        __build_optim_dict = {
            "adam": build_adam
        }

        optim_name = hparams.model.optimizer.name
        optim = __build_optim_dict[optim_name](graph.parameters(), vars(hparams.model.optimizer.args))
        print("[Builder]: Using optimizer `{}`, with args:{}".format(optim_name, hparams.model.optimizer.args))
        # get lrschedule
        schedule_name = "default"
        schedule_args = {}
        if "scheduler" in hparams.model:
            schedule_name = hparams.model.scheduler.name
            schedule_args = vars(hparams.model.scheduler.args)
        if not ("init_lr" in schedule_args):
            schedule_args["init_lr"] = hparams.model.optimizer.args.lr
        assert schedule_args["init_lr"] == hparams.model.optimizer.args.lr, \
            "Optim lr {} != Schedule init_lr {}".format(hparams.model.optimizer.args.lr, schedule_args["init_lr"])
        lrschedule = {
            "func": getattr(learning_rate_schedule, schedule_name),
            "args": schedule_args
        }

        return [optim], [lrschedule]

    def loss_fn(self, net, batch, epoch, step, opt_idx=0, stage='train', write=True):
        (x, x_name), (_, _) = batch
        # x, x_name = batch
        x = x.to(self.config.training.device[0])

        z, nll, y_logits, loss_dict = net(x, y_onehot=None)
        loss = GlowModel.loss_generative(nll)
        if write:
            self.writer.add_scalar(f'{stage}/loss', loss, step)
            for key, value in loss_dict.items():
                self.writer.add_scalar(f'{stage}/{key}', value, step)
        return loss

    def train_step(self, train_batch, epoch, step):
        self.net.train()

        lr = self.scheduler[0]["func"](global_step=self.global_step,
                                       **self.scheduler[0]["args"])
        for param_group in self.optimizer[0].param_groups:
            param_group['lr'] = lr
        self.writer.add_scalar(f'train/lr', lr, self.global_step)

        losses = []
        for i in range(len(self.optimizer)):
            loss = self.loss_fn(net=self.net,
                                batch=train_batch,
                                epoch=epoch,
                                step=step,
                                opt_idx=i,
                                stage='train')

            loss.backward()

            if self.config.training.max_grad_clip is not None and self.config.training.max_grad_clip > 0:
                torch.nn.utils.clip_grad_value_(self.net.parameters(), self.config.training.max_grad_clip)
            if self.config.training.max_grad_norm is not None and self.config.training.max_grad_norm > 0:
                grad_norm = torch.nn.utils.clip_grad_norm_(self.net.parameters(), self.config.training.max_grad_norm)
                if self.global_step % self.config.training.val_step_interval == 0:
                    self.writer.add_scalar("train/grad_norm", grad_norm, self.global_step)

            if step % self.config.training.accumulate_grad_batches == 0:
                self.optimizer[i].step()
                self.optimizer[i].zero_grad()
            losses.append(loss.detach().mean())

        if self.use_ema and self.global_step % (self.update_ema_interval * self.config.training.accumulate_grad_batches) == 0:
            self.step_ema()
        return losses

    def sample(self, net, batch, sample_path, stage='train'):
        sample_path = make_dir(os.path.join(sample_path, f'{stage}_sample'))
        (x, x_name), (_, _) = batch
        x = x.to(self.config.training.device[0])

        x_latent, _, _, _ = net(x, y_onehot=None)
        x_rec = net(z=x_latent, y_onehot=None, eps_std=0.5, reverse=True)
        sample = net(z=None, y_onehot=None, eps_std=0.5, reverse=True)

        grid_size = 4
        gt_grid = get_image_grid(x, grid_size, to_normal=self.config.data.dataset_config.to_normal)
        rec_grid = get_image_grid(x_rec, grid_size, to_normal=self.config.data.dataset_config.to_normal)
        sample_grid = get_image_grid(sample, grid_size, to_normal=self.config.data.dataset_config.to_normal)

        Image.fromarray(gt_grid).save(os.path.join(sample_path, 'ground_truth.png'))
        Image.fromarray(rec_grid).save(os.path.join(sample_path, 'image_rec.png'))
        Image.fromarray(sample_grid).save(os.path.join(sample_path, 'image_sample.png'))
        if stage != 'test':
            self.writer.add_image(f'{stage}_gt', gt_grid, self.global_step, dataformats='HWC')
            self.writer.add_image(f'{stage}_image_rec', rec_grid, self.global_step, dataformats='HWC')
            self.writer.add_image(f'{stage}_image_sample', sample_grid, self.global_step, dataformats='HWC')

    def sample_to_eval(self, net, test_loader, sample_path):
        reverse_result_path = make_dir(os.path.join(sample_path, 'reverse'))
        gt_path = make_dir(os.path.join(sample_path, 'ground_truth'))

        batch_size = self.config.data.test.batch_size
        to_normal = self.config.data.dataset_config.to_normal
        sample_num = self.config.testing.sample_num
        max_count = sample_num // batch_size

        pbar = tqdm(test_loader, total=len(test_loader), smoothing=0.01)
        count = 0
        for test_batch in pbar:
            if count > max_count:
                break
            else:
                count += 1
            (x, x_name), (_, _) = test_batch
            sample = net(z=None, y_onehot=None, eps_std=0.5, reverse=True)
            for j in range(batch_size):
                save_single_image(x[j], gt_path, f'{x_name[j]}.png', to_normal=to_normal)
                save_single_image(sample[j], reverse_result_path, f'{x_name[j]}.png',
                                  to_normal=to_normal)

    def get_checkpoint_states(self, stage='epoch_end'):
        optimizer_state = []
        for i in range(len(self.optimizer)):
            optimizer_state.append(self.optimizer[i].state_dict())

        optimizer_scheduler_states = {
            'optimizer': optimizer_state,
        }

        model_states = {
            'step': self.global_step,
        }

        if self.config.training.use_DDP:
            model_states['model'] = self.net.module.state_dict()
        else:
            model_states['model'] = self.net.state_dict()

        if stage == 'exception':
            model_states['epoch'] = self.global_epoch
        else:
            model_states['epoch'] = self.global_epoch + 1

        if self.use_ema:
            model_states['ema'] = self.ema.shadow
        return model_states, optimizer_scheduler_states

    def load_model_from_checkpoint(self):
        model_states = None
        if self.config.model.__contains__('model_load_path') and self.config.model.model_load_path is not None:
            print(f"load model {self.config.model.model_name} from {self.config.model.model_load_path}")
            model_states = torch.load(self.config.model.model_load_path, map_location='cpu')

            self.global_epoch = model_states['epoch']
            self.global_step = model_states['step']

            # load model
            self.net.load_state_dict(model_states['model'])

            # load ema
            if self.use_ema:
                self.ema.shadow = model_states['ema']
                self.ema.reset_device(self.net)

            # load optimizer and scheduler
            if self.config.args.train:
                if self.config.model.__contains__('optim_sche_load_path') and self.config.model.optim_sche_load_path is not None:
                    optimizer_scheduler_states = torch.load(self.config.model.optim_sche_load_path, map_location='cpu')
                    for i in range(len(self.optimizer)):
                        self.optimizer[i].load_state_dict(optimizer_scheduler_states['optimizer'][i])
        return model_states




import argparse
import datetime
import pdb
import time

import yaml
import os
import traceback

import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torch.nn.parallel import DistributedDataParallel as DDP

from abc import ABC, abstractmethod

from tqdm.autonotebook import tqdm
from runners.auxilliary.EMA import EMA
from runners.utils import make_save_dirs, make_dir, get_dataset, remove_file


class BaseRunner(ABC):
    def __init__(self, config):
        # pdb.set_trace()
        self.net = None  # Neural Network
        self.optimizer = None  # optimizer
        self.scheduler = None  # scheduler
        self.config = config  # config from configuration file

        # set training params
        self.global_epoch = 0  # global epoch
        if config.args.sample_at_start:
            self.global_step = -1  # global step
        else:
            self.global_step = 0

        self.GAN_buffer = {}  # GAN buffer for Generative Adversarial Network
        self.topk_checkpoints = {}  # Top K checkpoints

        # set log and save destination
        self.config.result = argparse.Namespace()
        self.config.result.image_path, \
        self.config.result.ckpt_path, \
        self.config.result.log_path, \
        self.config.result.sample_path, \
        self.config.result.sample_to_eval_path = make_save_dirs(self.config.args,
                                                                prefix=self.config.data.dataset_config.dataset_name,
                                                                suffix=self.config.model.model_name)

        self.save_config()  # save configuration file
        self.writer = SummaryWriter(self.config.result.log_path)  # initialize SummaryWriter

        # initialize model
        self.net, self.optimizer, self.scheduler = self.initialize_model_optimizer_scheduler(self.config)
        # self.net = self.initialize_model(self.config)

        self.print_model_summary(self.net)

        # initialize EMA
        self.use_ema = False if not self.config.model.__contains__('EMA') else self.config.model.EMA.use_ema
        if self.use_ema:
            self.ema = EMA(self.config.model.EMA.ema_decay)
            self.update_ema_interval = self.config.model.EMA.update_ema_interval
            self.start_ema_step = self.config.model.EMA.start_ema_step
            self.ema.register(self.net)

        # load model from checkpoint
        self.load_model_from_checkpoint()

        # initialize DDP
        if self.config.training.use_DDP:
            self.net = DDP(self.net, device_ids=[self.config.training.local_rank], output_device=self.config.training.local_rank)
            # self.optimizer, self.scheduler = self.initialize_optimizer_scheduler(self.net.module, self.config)
        else:
            self.net = self.net.to(self.config.training.device[0])
            # self.optimizer, self.scheduler = self.initialize_optimizer_scheduler(self.net, self.config)
        # self.ema.reset_device(self.net)

    # ------------model initialization part--------------
    def save_config(self):
        """
        save configuration file
        """
        save_path = os.path.join(self.config.result.ckpt_path, 'config.yaml')
        save_config = self.config
        with open(save_path, 'w') as f:
            yaml.dump(save_config, f)

    def print_model_summary(self, net):
        def get_parameter_number(model):
            total_num = sum(p.numel() for p in model.parameters())
            trainable_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
            return total_num, trainable_num

        total_num, trainable_num = get_parameter_number(net)
        print("Total Number of parameter: %.2fM" % (total_num / 1e6))
        print("Trainable Number of parameter: %.2fM" % (trainable_num / 1e6))

    def initialize_model_optimizer_scheduler(self, config, is_test=False):
        """
        initialize model, optimizer, scheduler
        :param args: args
        :param config: config
        :param is_test: is_test
        :return: net: Neural Network, nn.Module;
                 optimizer: a list of optimizers;
                 scheduler: a list of schedulers or None;
        """
        net = self.initialize_model(config)
        optimizer, scheduler = None, None
        if not is_test:
            optimizer, scheduler = self.initialize_optimizer_scheduler(net, config)
        return net, optimizer, scheduler

    # ----------------load and save model part--------------------
    def load_model_from_checkpoint(self):
        """
        load model, EMA, optimizer, scheduler from checkpoint
        :return: loaded model states
        """
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

                    if self.scheduler is not None:
                        for i in range(len(self.optimizer)):
                            self.scheduler[i].load_state_dict(optimizer_scheduler_states['scheduler'][i])
        return model_states

    def get_checkpoint_states(self, stage='epoch_end'):
        """
        get checkpoint states for saving
        :param stage: options {"epoch_end"}
        :return:
        """
        optimizer_state = []
        for i in range(len(self.optimizer)):
            optimizer_state.append(self.optimizer[i].state_dict())

        scheduler_state = []
        if self.scheduler is not None:
            for i in range(len(self.scheduler)):
                scheduler_state.append(self.scheduler[i].state_dict())

        optimizer_scheduler_states = {
            'optimizer': optimizer_state,
            'scheduler': scheduler_state
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

    # ----------------------EMA part----------------------
    def step_ema(self):
        with_decay = False if self.global_step < self.start_ema_step else True
        if self.config.training.use_DDP:
            self.ema.update(self.net.module, with_decay=with_decay)
        else:
            self.ema.update(self.net, with_decay=with_decay)

    def apply_ema(self):
        if self.use_ema:
            if self.config.training.use_DDP:
                self.ema.apply_shadow(self.net.module)
            else:
                self.ema.apply_shadow(self.net)

    def restore_ema(self):
        if self.use_ema:
            if self.config.training.use_DDP:
                self.ema.restore(self.net.module)
            else:
                self.ema.restore(self.net)

    # ---------------------Train, Evaluation and sample part--------------------
    def load_data(self):
        """
        load dataset and create dataloader
        :return: dataloaders and samplers
        """
        train_dataset, val_dataset, test_dataset = get_dataset(self.config.data)
        train_sampler, val_sampler, test_sampler = None, None, None
        if self.config.training.use_DDP:
            train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
            val_sampler = torch.utils.data.distributed.DistributedSampler(val_dataset)
            test_sampler = torch.utils.data.distributed.DistributedSampler(test_dataset)

        train_loader = DataLoader(train_dataset,
                                  batch_size=self.config.data.train_batch_size,
                                  num_workers=self.config.data.num_workers,
                                  shuffle=not self.config.training.use_DDP,
                                  drop_last=True,
                                  sampler=train_sampler)
        val_loader = DataLoader(val_dataset,
                                batch_size=self.config.data.val_batch_size,
                                num_workers=self.config.data.num_workers,
                                shuffle=not self.config.training.use_DDP,
                                drop_last=True,
                                sampler=val_sampler)
        test_loader = DataLoader(test_dataset,
                                 batch_size=self.config.data.test_batch_size,
                                 num_workers=self.config.data.num_workers,
                                 shuffle=False,
                                 drop_last=False,
                                 sampler=test_sampler)
        return train_loader, val_loader, test_loader, train_sampler, val_sampler, test_sampler

    def train_step(self, train_batch, epoch, step):
        """
        training step
        :param train_batch: training batch data
        :param epoch: training epoch number
        :param step: training step number
        :return: loss list
        """
        self.net.train()
        losses = []
        for i in range(len(self.optimizer)):
            loss = self.loss_fn(net=self.net,
                                batch=train_batch,
                                epoch=epoch,
                                step=step,
                                opt_idx=i,
                                stage='train')

            loss.backward()

            if step % self.config.training.accumulate_grad_batches == 0:
                self.optimizer[i].step()
                self.optimizer[i].zero_grad()
                if self.scheduler is not None:
                    self.scheduler[i].step(loss)
            losses.append(loss.detach().mean())

        if self.use_ema and self.global_step % (self.update_ema_interval * self.config.training.accumulate_grad_batches) == 0:
            self.step_ema()
        return losses

    @torch.no_grad()
    def validation_step(self, val_batch, epoch, step):
        """
        validation step
        :param val_batch: validation batch
        :param epoch: training epoch number
        :param step: training step number
        :return:
        """
        self.apply_ema()
        self.net.eval()
        for i in range(len(self.optimizer)):
            loss = self.loss_fn(net=self.net,
                                batch=val_batch,
                                epoch=epoch,
                                step=step,
                                opt_idx=i,
                                stage='val_step')
        self.restore_ema()

    @torch.no_grad()
    def validation_epoch(self, val_loader, epoch):
        """
        validation epoch
        :param val_loader: validation dataloader
        :param epoch: training epoch number
        :return: average loss over validation dataset
        """
        self.apply_ema()
        self.net.eval()

        pbar = tqdm(val_loader, total=len(val_loader), smoothing=0.01)
        step = 0
        loss_sum = 0.
        for val_batch in pbar:
            loss = self.loss_fn(net=self.net,
                                batch=val_batch,
                                epoch=epoch,
                                step=step,
                                opt_idx=0,
                                stage='val',
                                write=False)
            loss_sum += loss
            step += 1
        average_loss = loss_sum / step
        self.writer.add_scalar(f'val_epoch/loss', average_loss, epoch)
        self.restore_ema()
        return average_loss

    @torch.no_grad()
    def sample_step(self, train_batch, val_batch):
        """
        sample step
        :param train_batch: train batch
        :param val_batch: validation batch
        :return:
        """
        self.apply_ema()
        self.net.eval()
        sample_path = make_dir(os.path.join(self.config.result.image_path, str(self.global_step)))
        if self.config.training.use_DDP:
            self.sample(self.net.module, train_batch, sample_path, stage='train')
            self.sample(self.net.module, val_batch, sample_path, stage='val')
        else:
            self.sample(self.net, train_batch, sample_path, stage='train')
            self.sample(self.net, val_batch, sample_path, stage='val')
        self.restore_ema()

    # -----------------abstract methods---------------------
    @abstractmethod
    def initialize_model(self, config):
        """
        initialize model
        :param config: config
        :return: nn.Module
        """
        pass

    @abstractmethod
    def initialize_optimizer_scheduler(self, net, config):
        """
        initialize optimizer and scheduler
        :param net: nn.Module
        :param config: config
        :return: a list of optimizers; a list of schedulers
        """
        pass

    @abstractmethod
    def loss_fn(self, net, batch, epoch, step, opt_idx=0, stage='train', write=True):
        """
        loss function
        :param net: nn.Module
        :param batch: batch
        :param epoch: global epoch
        :param step: global step
        :param opt_idx: optimizer index, default is 0; set it to 1 for GAN discriminator
        :param stage: train, val, test
        :param write: write loss information to SummaryWriter
        :return: a scalar of loss
        """
        pass

    @abstractmethod
    def sample(self, net, batch, sample_path, stage='train'):
        """
        sample a single batch
        :param net: nn.Module
        :param batch: batch
        :param sample_path: path to save samples
        :param stage: train, val, test
        :return:
        """
        pass

    @abstractmethod
    def sample_to_eval(self, net, test_loader, sample_path):
        """
        sample among the test dataset to calculate evaluation metrics
        :param net: nn.Module
        :param test_loader: test dataloader
        :param sample_path: path to save samples
        :return:
        """
        pass

    def on_save_checkpoint(self, net, train_loader, val_loader, epoch, step):
        """
        additional operations whilst saving checkpoint
        :param net: nn.Module
        :param train_loader: train data loader
        :param val_loader: val data loader
        :param epoch: epoch
        :param step: step
        :return:
        """
        pass

    @torch.no_grad()
    def test_every_step_average_loss(self, net, test_loader, save_path):
        """
        test_every_step_average_loss
        :param net: nn.Module
        :param test_loader: test data loader
        :param save_path: save path
        :return:
        """
        pass

    def train(self):
        print(self.__class__.__name__)

        train_loader, val_loader, test_loader, train_sampler, val_sampler, test_sampler = self.load_data()

        epoch_length = len(train_loader)
        start_epoch = self.global_epoch
        print(
            f"start training {self.config.model.model_name} on {self.config.data.dataset_config.dataset_name}, {len(train_loader)} iters per epoch")

        try:
            for epoch in range(start_epoch, self.config.training.n_epochs):
                if self.global_step > self.config.training.n_steps:
                    break

                if self.config.training.use_DDP:
                    train_sampler.set_epoch(epoch)
                    val_sampler.set_epoch(epoch)

                pbar = tqdm(train_loader, total=len(train_loader), smoothing=0.01)
                self.global_epoch = epoch
                start_time = time.time()
                for train_batch in pbar:
                    self.global_step += 1

                    losses = self.train_step(train_batch=train_batch, epoch=self.global_epoch, step=self.global_step)

                    desc = f'Epoch: [{epoch + 1} / {self.config.training.n_epochs}] iter: {self.global_step} '
                    for i in range(len(losses)):
                        desc += f'loss-{i}: {losses[i]:.4f} '
                    pbar.set_description(desc=desc)

                    with torch.no_grad():
                        # val loss step
                        if self.global_step % self.config.training.val_interval_step == 0:
                            val_batch = next(iter(val_loader))
                            self.validation_step(val_batch=val_batch, epoch=epoch, step=self.global_step)

                        # sample step
                        if self.global_step % int(self.config.training.sample_interval * epoch_length) == 0:
                            if not self.config.training.use_DDP or \
                                    (self.config.training.use_DDP and self.config.training.local_rank) == 0:
                                val_batch = next(iter(val_loader))
                                self.sample_step(val_batch=val_batch, train_batch=train_batch)
                                torch.cuda.empty_cache()

                        # save checkpoint step
                        if self.config.training.__contains__('save_interval_step') \
                            and self.global_step % int(self.config.training.save_interval_step) == 0:
                            print(f"{self.global_step} saving latest checkpoint...")
                            self.on_save_checkpoint(self.net, train_loader, val_loader, epoch, self.global_step)
                            model_states, optimizer_scheduler_states = self.get_checkpoint_states(stage='epoch_end')

                            # remove old checkpoint
                            temp = 0
                            while temp < self.global_step // int(self.config.training.save_interval_step):
                                index = temp * int(self.config.training.save_interval_step)
                                remove_file(os.path.join(self.config.result.ckpt_path, f'latest_model_step_{index}.pth'))
                                remove_file(
                                    os.path.join(self.config.result.ckpt_path, f'latest_optim_sche_step_{index}.pth'))
                                temp += 1

                            # save latest checkpoint
                            torch.save(model_states,
                                       os.path.join(self.config.result.ckpt_path,
                                                    f'latest_model_step_{self.global_step}.pth'))
                            torch.save(optimizer_scheduler_states,
                                       os.path.join(self.config.result.ckpt_path,
                                                    f'latest_optim_sche_step_{self.global_step}.pth'))

                end_time = time.time()
                elapsed_rounded = int(round((end_time-start_time)))
                print("training time: " + str(datetime.timedelta(seconds=elapsed_rounded)))

                # save checkpoint
                if (self.config.training.__contains__('save_interval_epoch') and
                        (epoch + 1) % self.config.training.save_interval_epoch == 0) or \
                        (epoch + 1) == self.config.training.n_epochs or \
                        self.global_step > self.config.training.n_steps:

                    if not self.config.training.use_DDP or \
                            (self.config.training.use_DDP and self.config.training.local_rank) == 0:
                        with torch.no_grad():
                            print("epoch end saving latest checkpoint...")
                            self.on_save_checkpoint(self.net, train_loader, val_loader, epoch, self.global_step)
                            model_states, optimizer_scheduler_states = self.get_checkpoint_states(stage='epoch_end')

                            # remove old checkpoint
                            temp = 0
                            remove_file(os.path.join(self.config.result.ckpt_path, f'last_model.pth'))
                            remove_file(os.path.join(self.config.result.ckpt_path, f'last_optim_sche.pth'))
                            while temp < epoch + 1:
                                remove_file(os.path.join(self.config.result.ckpt_path, f'latest_model_{temp}.pth'))
                                remove_file(
                                    os.path.join(self.config.result.ckpt_path, f'latest_optim_sche_{temp}.pth'))
                                temp += 1

                            # save latest checkpoint
                            torch.save(model_states,
                                       os.path.join(self.config.result.ckpt_path,
                                                    f'latest_model_{epoch + 1}.pth'))
                            torch.save(optimizer_scheduler_states,
                                       os.path.join(self.config.result.ckpt_path,
                                                    f'latest_optim_sche_{epoch + 1}.pth'))

                # validation
                if (epoch + 1) % self.config.training.val_interval_epoch == 0 or (
                        epoch + 1) == self.config.training.n_epochs:
                    if not self.config.training.use_DDP or \
                            (self.config.training.use_DDP and self.config.training.local_rank) == 0:
                        with torch.no_grad():
                            print("validating epoch...")
                            average_loss = self.validation_epoch(val_loader, epoch)
                            torch.cuda.empty_cache()
                            print("validating epoch success")

                            if self.config.args.save_top:
                                print("saving top checkpoint...")
                                model_states, optimizer_scheduler_states = self.get_checkpoint_states(stage='epoch_end')

                                # save top_k checkpoints
                                model_ckpt_name = f'top_model_epoch_{epoch + 1}.pth'
                                optim_sche_ckpt_name = f'top_optim_sche_epoch_{epoch + 1}.pth'

                                top_key = 'top'
                                if top_key in self.topk_checkpoints and \
                                        average_loss < self.topk_checkpoints[top_key]["loss"]:
                                    print("remove " + self.topk_checkpoints[top_key]["model_ckpt_name"])
                                    remove_file(os.path.join(self.config.result.ckpt_path,
                                                             self.topk_checkpoints[top_key]['model_ckpt_name']))
                                    remove_file(os.path.join(self.config.result.ckpt_path,
                                                             self.topk_checkpoints[top_key]['optim_sche_ckpt_name']))

                                self.topk_checkpoints[top_key] = {"loss": average_loss,
                                                                  'model_ckpt_name': model_ckpt_name,
                                                                  'optim_sche_ckpt_name': optim_sche_ckpt_name}

                                print(f"saving top checkpoint: average_loss={average_loss} epoch={epoch + 1}")
                                torch.save(model_states,
                                           os.path.join(self.config.result.ckpt_path, model_ckpt_name))
                                torch.save(optimizer_scheduler_states,
                                           os.path.join(self.config.result.ckpt_path, optim_sche_ckpt_name))
        except BaseException as e:
            if not self.config.training.use_DDP or (self.config.training.use_DDP and self.config.training.local_rank) == 0:
                print("exception save model start....")
                print(self.__class__.__name__)
                model_states, optimizer_scheduler_states = self.get_checkpoint_states(stage='exception')
                torch.save(model_states,
                           os.path.join(self.config.result.ckpt_path, f'last_model.pth'))
                torch.save(optimizer_scheduler_states,
                           os.path.join(self.config.result.ckpt_path, f'last_optim_sche.pth'))

                print("exception save model success!")

            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():')
            traceback.print_exc()
            print('traceback.format_exc():\n%s' % traceback.format_exc())

    @torch.no_grad()
    def test(self):
        train_dataset, val_dataset, test_dataset = get_dataset(self.config.data)
        if test_dataset is None:
            test_dataset = val_dataset
        test_sampler=None
        if self.config.training.use_DDP:
            test_sampler = torch.utils.data.distributed.DistributedSampler(test_dataset)
        test_loader = DataLoader(test_dataset,
                                 batch_size=self.config.data.test_batch_size,
                                 shuffle=False,
                                 num_workers=self.config.data.num_workers,
                                 drop_last=True,
                                 sampler=test_sampler)

        if self.use_ema:
            self.apply_ema()

        self.net.eval()
        if self.config.args.sample_to_eval:
            sample_path = self.config.result.sample_to_eval_path
            if self.config.training.use_DDP:
                self.sample_to_eval(self.net.module, test_loader, sample_path)
            else:
                self.sample_to_eval(self.net, test_loader, sample_path)
        else:
            test_iter = iter(test_loader)
            for i in tqdm(range(2), initial=0, dynamic_ncols=True, smoothing=0.01):
                test_batch = next(test_iter)
                sample_path = os.path.join(self.config.result.sample_path, str(i))
                if self.config.training.use_DDP:
                    self.sample(self.net.module, test_batch, sample_path, stage='test')
                else:
                    self.sample(self.net, test_batch, sample_path, stage='test')

        if self.config.args.test_step_loss:
            save_path = self.config.result.ckpt_path
            if self.config.training.use_DDP:
                self.test_every_step_average_loss(self.net.module, test_loader, save_path)
            else:
                self.test_every_step_average_loss(self.net, test_loader, save_path)

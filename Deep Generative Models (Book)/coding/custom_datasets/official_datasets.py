import torchvision
import torchvision.transforms as Transforms
from torch.utils.data import Dataset

from auxilliary.Register import Registers
from custom_datasets.utils import preprocess_dataset_config


@Registers.datasets.register_with_name('official')
class OfficialDataset(Dataset):
    def __init__(self, dataset_config, stage='train'):
        self.dataset_config = preprocess_dataset_config(dataset_config, stage)
        if self.dataset_config.dataset_name == 'MNIST':
            transform_list = [Transforms.ToTensor()]
            if self.dataset_config.to_normal:
                print('dataset MNIST normalization')
                transform_list.append(Transforms.Normalize(mean=(0.1307,), std=(0.3081,)))
            transform_fn = Transforms.Compose(transform_list)
            self.dataset = torchvision.datasets.MNIST(root=self.dataset_config.dataset_path,
                                                      train=True if stage=='train' else False,
                                                      transform=transform_fn,
                                                      download=True)
        else:
            raise NotImplementedError

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        return self.dataset[item]
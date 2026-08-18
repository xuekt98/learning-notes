import torch
import torch.nn as nn
import torch.nn.functional as F


class CausalConv1d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, dilation=1, A=False, **kwargs):
        super(CausalConv1d, self).__init__()

        self.kernel_size = kernel_size
        self.dilation = dilation
        self.A = A

        self.padding = (kernel_size - 1) * dilation + A * 1

        self.conv1d = nn.Conv1d(in_channels, out_channels, kernel_size,
                                stride=1, padding=0, dilation=dilation, **kwargs)

    def forward(self, x):
        x = F.pad(x, (self.padding, 0))
        conv1d_out = self.conv1d(x)
        if self.A:
            return conv1d_out[:, :, :-1]
        else:
            return conv1d_out

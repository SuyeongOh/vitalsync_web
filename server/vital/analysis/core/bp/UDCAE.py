import torch
import torch.nn as nn
import torch.optim as optim


class UDCAE(nn.Module):
    def __init__(self):
        super(UDCAE, self).__init__()

        self.enc_conv1 = nn.Conv1d(1, 32, kernel_size=3, padding=2)
        self.enc_conv2 = nn.Conv1d(32, 64, kernel_size=3, padding=2)
        self.enc_conv3 = nn.Conv1d(64, 128, kernel_size=3, padding=2)
        self.enc_conv4 = nn.Conv1d(128, 256, kernel_size=3, padding=2)

        self.pool = nn.MaxPool1d(2)

        self.dec_conv1 = nn.Conv1d(256, 128, kernel_size=3, padding=2)
        self.dec_conv2 = nn.Conv1d(128, 64, kernel_size=3, padding=2)
        self.dec_conv3 = nn.Conv1d(64, 32, kernel_size=3, padding=2)
        self.dec_conv4 = nn.Conv1d(32, 1, kernel_size=3, padding=2)

        self.upsample = nn.Upsample(scale_factor=2, mode='nearest')

        self.skip_conv1 = nn.Conv1d(128, 128, kernel_size=1)
        self.skip_conv2 = nn.Conv1d(64, 64, kernel_size=1)
        self.skip_conv3 = nn.Conv1d(32, 32, kernel_size=1)

        self.relu = nn.ReLU()

    def forward(self, x):
        x1 = self.relu(self.enc_conv1(x))
        x1_pool = self.pool(x1)
        x2 = self.relu(self.enc_conv2(x1_pool))
        x2_pool = self.pool(x2)
        x3 = self.relu(self.enc_conv3(x2_pool))
        x3_pool = self.pool(x3)
        x4 = self.relu(self.enc_conv4(x3_pool))

        x5 = self.relu(self.dec_conv1(x4))
        x5 = self.upsample(x5)
        x6 = self.relu(self.dec_conv2(torch.cat((x5, self.skip_conv1(x3)), dim=1)))
        x6 = self.upsample(x6)
        x7 = self.relu(self.dec_conv3(torch.cat((x6, self.skip_conv2(x2)), dim=1)))
        x7 = self.upsample(x7)
        x8 = self.dec_conv4(torch.cat((x7, self.skip_conv3(x1)), dim=1))

        return x8


# def count_parameters(model):
#     return sum(p.numel() for p in model.parameters() if p.requires_grad)
#
#
# model = UDCAE()
# print(f'Parameter 수: {count_parameters(model):,}')

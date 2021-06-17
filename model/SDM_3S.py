# -*- coding:utf-8 -*-
import torch
import torch.nn as nn

"""
模型思路
1、提高视野区域:(3区域)√
2、三区域做分组卷积:(减少无用参数和计算)√
3、试用softpool:()
4、试用残差结构:(细粒度信息更多参与决策)√
6、试用多分类:()
7、试用多层VGG:(12层)
"""


class SDM(nn.Module):

    def __init__(self):
        super(SDM, self).__init__()  # 64*64

        self.extract_1 = Sepres_Block(3, 72, 3)  # 32*32
        self.extract_2 = Sepres_Block(72, 144, 3)  # 16*16
        self.extract_3 = Sepres_Block(144, 288, 3)  # 8*8
        self.merge = Sepres_Block(288, 576, 1)  # 4

        self.dense = nn.Sequential(torch.nn.Linear(576 * 4 * 4, 1024),
                                   torch.nn.ReLU(),
                                   torch.nn.Dropout(p=0.5),
                                   torch.nn.Linear(1024, 1024),
                                   torch.nn.ReLU(),
                                   torch.nn.Dropout(p=0.5),
                                   torch.nn.Linear(1024, 1)
                                   )
        self.sigma = nn.Sigmoid()

    def forward(self, x):
        x = self.extract_1(x)
        x = self.extract_2(x)
        x = self.extract_3(x)
        x = self.merge(x)
        x = x.view(x.size(0), -1)
        x = self.dense(x)
        x = self.sigma(x)
        return x


class Sepres_Block(nn.Module):

    def __init__(self, in_channel, out_channel, group_num=3):
        super(Sepres_Block, self).__init__()

        self.scope_extract = torch.nn.Sequential(
            torch.nn.Conv2d(in_channel, out_channel, kernel_size=3, stride=1, padding=1, groups=group_num),
            torch.nn.BatchNorm2d(out_channel),
            torch.nn.ReLU(),
            torch.nn.Conv2d(out_channel, out_channel, kernel_size=3, stride=1, padding=1, groups=group_num),
            torch.nn.BatchNorm2d(out_channel),
            torch.nn.ReLU(),
            torch.nn.Conv2d(out_channel, out_channel, kernel_size=3, stride=1, padding=1, groups=group_num),
            torch.nn.BatchNorm2d(out_channel),
        )

        self.raw_extract = torch.nn.Sequential(
            torch.nn.Conv2d(in_channel, out_channel, kernel_size=1, stride=1, padding=0, groups=group_num),
            torch.nn.BatchNorm2d(out_channel),
        )

        self.relu = torch.nn.ReLU(inplace=True)
        self.maxpool = torch.nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, x):
        out = self.scope_extract(x)
        res = self.raw_extract(x)
        out = out + res
        out = self.relu(out)
        out = self.maxpool(out)
        return out

model=SDM().cuda()
weight=torch.load("weight_100.pkl")
model.load_state_dict(weight)
dummy_input = torch.randn(1, 3, 64, 64, device='cuda')#(b,c,w,h)
output = torch.onnx.export(model, dummy_input, "hello.onnx", verbose=True)
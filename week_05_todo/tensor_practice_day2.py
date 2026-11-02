import torch
import numpy as np

x = torch.arange(5,dtype=torch.float32).reshape(-1,1)
A = torch.tensor([[1.,2.,3.],[4.,5.,6.]])
V = torch.tensor([[1.],[0.],[1.]])

print(x.shape,x[0].shape,x[0,0].shape)
print(A*A)
print(A@V)
# dim = 0 得到每一列的平均值
print(A.mean(dim = 0))

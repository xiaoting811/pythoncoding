import torch
import numpy as np

print(torch.__version__)
a = torch.tensor([[1.,2.],[3.,4.]],dtype=torch.float32)
print(a)
print(a.shape)
print(a.dtype)
print(a.device)
print(a.ndim)
print('*'*30)

a = torch.randint(0,10,(2,3))
print(a)
print(a.shape)
print(a.device)
print(a.ndim)
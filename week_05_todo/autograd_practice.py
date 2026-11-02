import torch
import numpy as np

s = torch.tensor(2.0, requires_grad=True)

z = s*s
# 第一次求导
z.backward()
print(s.grad.item())  # 4.0

# 第二次重新求导 但梯度会相加 所以是8
(s * s).backward()
print(s.grad.item())  # 8.0

# 清空梯度
s.grad.zero_()

# 第三次求导
(s * s).backward()
print(s.grad.item())

# 查看s 本身
print(s.item())


print("-"*30)

# 认识链式求导法则
s = torch.tensor(1.0, requires_grad=True, dtype=torch.float32)
# u = torch.tensor(3.0, requires_grad=True, dtype=torch.float32)
u = 2 * s + 1
loss = u * u
loss.backward()
print(s.grad.item())





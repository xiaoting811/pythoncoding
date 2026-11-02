import torch
import numpy as np
import pandas as pd

x =  torch.arange(5,dtype=torch.float32).reshape(-1,1)
y =  2 * x + 1
w =  torch.tensor(0.0, requires_grad=True)
b =  torch.tensor(0.0, requires_grad=True)
# assert y_pred.shape == y.shape

lr = 0.01
epochs = 10
for epoch in range(epochs):
    y_pred = w * x + b
    assert y_pred.shape == y.shape

    # 损失函数
    loss = (y_pred - y).pow(2).mean()
    print(loss.item())
    # 反向求导
    loss.backward()

    # 参数更新
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
    # 梯度归零
    w.grad.zero_()
    b.grad.zero_()

print(w.item(),b.item())
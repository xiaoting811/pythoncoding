# 第五周：PyTorch 张量、自动求导与线性回归

本周要掌握：看懂张量的形状、类型和设备，理解梯度怎样产生，用手动更新与 SGD 训练同一个线性模型，并保存能够相互核对的损失记录和曲线。

本文按本目录现有代码整理。示例用于解释知识点，不表示示例已全部写入脚本；末尾自测项需要自己验证。这里的人工数据用于学习训练流程，不能代表漏洞检测能力，也不是 Agent 或具身智能系统的评测结果。

## 1. 文件与学习顺序

| 文件 | 对应内容 | 应掌握的知识 |
|---|---|---|
| `tensor_practice-day1.py` | Day 1 | 创建张量，查看 shape、dtype、device、ndim |
| `tensor_practice_day2.py` | Day 2 | reshape、索引、逐元素乘法、矩阵乘法、按维度求均值 |
| `autograd_practice.py` | Day 3 | backward、梯度累加、清零、链式求导 |
| `linear_regression.py` | Day 4 | 线性预测、MSE、反向传播和手动更新；当前运行 10 轮 |
| `linear_regression_day5.py` | Day 5 | 把手动训练封装为 train 函数，返回结果字典 |
| `linear_regression_sgd.py` | Day 6 | 用 torch.optim.SGD 更新参数 |
| `compare_runs.py` | Day 6–7 | 公平对比三组训练，导出 CSV 和损失图 |
| `output/loss_comparison.csv` | 实验记录 | 300 条数据，epoch 从 0 到 299 |
| `output/loss_comparison.png` | 实验图 | 三组训练的 MSE 曲线 |

本周不需要额外建立 data 文件夹。训练数据由各训练函数内部创建，也不使用第一周的任务列表或前几周的成绩 CSV。

## 2. Python 环境与运行方式

“电脑安装了某个库”不等于“当前 Python 可以使用它”。不同解释器、虚拟环境中的库可能不同；PyCharm 与 PowerShell 也可能使用不同解释器。

在 PowerShell 检查当前解释器与依赖：

```powershell
python -c "import sys; print(sys.executable)"
python -m pip --version
python -c "import torch; import matplotlib; print(torch.__version__); print(matplotlib.__version__)"
```

在 PyCharm 运行 `import sys; print(sys.executable)`，可以对比两边路径。版本不同本身不必然报错，但运行所需的库必须安装在实际使用的环境中。

若提示 `ModuleNotFoundError: No module named 'matplotlib'`，表示当前解释器找不到绘图库；可在确认要使用该环境后执行：

```powershell
python -m pip install matplotlib
```

`python -m pip` 让安装操作对应当前 python，避免单独调用 pip 时指向另一个环境。当前几个练习还导入了 NumPy，`linear_regression.py` 还导入了 Pandas；即使未使用，导入时也要求环境中存在这些库。后续整理代码时可删除未使用的导入。

在本周目录运行：

```powershell
python tensor_practice-day1.py
python tensor_practice_day2.py
python autograd_practice.py
python linear_regression.py
python linear_regression_day5.py
python linear_regression_sgd.py
python compare_runs.py
```

文件名中的连字符不影响直接运行，但不能写成普通的 `from tensor_practice-day1 import ...`。以后需要导入该文件时，可统一使用下划线命名。

## 3. Tensor：数值、形状、类型和设备

```python
a = torch.tensor([[1., 2.], [3., 4.]], dtype=torch.float32)
print(a.shape)   # torch.Size([2, 2])
print(a.ndim)    # 2
print(a.dtype)   # torch.float32
print(a.device)  # 当前代码未指定设备，通常为 cpu
```

| 属性 | 含义 | 本例 |
|---|---|---|
| shape | 各维度分别有多少个元素 | 2 行、2 列 |
| ndim | 维度数量 | 二维，不是元素总数 |
| dtype | 元素的数据类型 | 32 位浮点数 |
| device | 张量所在的计算设备 | CPU 或某个 GPU |

`1.` 等价于浮点数 `1.0`。`torch.randint(0, 10, (2, 3))` 创建 2 行 3 列随机整数，包含 0、不包含 10；默认整数类型是 int64。随机值每次可能变化，检查时重点看范围与形状。

训练中的连续参数需要浮点类型。参与同一次运算的张量还需要使用兼容的类型与设备；本周小实验使用 CPU 即可。

## 4. reshape、索引与广播

```python
x = torch.arange(5, dtype=torch.float32).reshape(-1, 1)
```

`arange(5)` 产生 0、1、2、3、4，原形状为 `(5,)`。`reshape(-1, 1)` 指定一列，由 PyTorch 推算行数，结果为 `(5, 1)`。reshape 不改变元素总数，`-1` 只能出现一次。

| 表达式 | 形状 | 含义 |
|---|---|---|
| `x` | `(5, 1)` | 5 个样本，每个样本 1 个输入数值 |
| `x[0]` | `(1,)` | 第一行，仍是一维张量 |
| `x[0, 0]` | `()` | 一个标量，零维张量 |

`.item()` 可以把只有一个元素的张量取成 Python 数值；不能直接用于含多个元素的张量。

**广播不一定报错，所以要主动检查形状。** 若预测形状为 `(5, 1)`、真实值形状为 `(5,)`，相减会广播成 `(5, 5)`，不再是五个样本一一对应的误差。

```python
assert y_pred.shape == y_true.shape
```

当前 Day 4 文件已有这种检查；训练函数里的输入和目标目前也都是 `(5, 1)`。以后换数据时应继续检查，不能只凭 loss 能算出来判断正确。

## 5. 逐元素运算、矩阵乘法与 dim

```python
A = torch.tensor([[1., 2., 3.], [4., 5., 6.]])
V = torch.tensor([[1.], [0.], [1.]])
```

- `A * A`：相同位置分别相乘，得到 `[[1, 4, 9], [16, 25, 36]]`，形状仍为 `(2, 3)`。
- `A @ V`：矩阵乘法，`(2, 3) @ (3, 1)` 得到 `(2, 1)`，数值为 `[[4], [10]]`。
- `A.mean()`：所有元素平均，结果是标量 `3.5`。
- `A.mean(dim=0)`：沿第 0 维聚合，两行合并，得到每列均值 `[2.5, 3.5, 4.5]`。
- `A.mean(dim=1)`：沿第 1 维聚合，三列合并，得到每行均值 `[2, 5]`。

当前 Day 2 已练习 `dim=0`；可自行补 `dim=1` 和不指定 dim 的结果。理解“沿哪个维度做归约”比背“0 是列、1 是行”更可靠，因为更高维张量也使用 dim。

## 6. 自动求导：backward 只计算梯度

```python
s = torch.tensor(2.0, requires_grad=True)
z = s * s
z.backward()
print(s.grad.item())  # 4.0
print(s.item())       # 2.0
```

`requires_grad=True` 让涉及这个参数的运算被自动求导记录。对于 `z=s²`，导数为 `2s`，所以 s=2 时梯度是 4。

- `s` 保存参数本身，`s.grad` 保存计算得到的梯度。
- `backward()` 从这个标量结果反向计算梯度，不会自动把 s 改小。
- 当前例子和训练中的 MSE 都是标量，因此可以直接调用无参数的 `backward()`。
- `.item()` 用于打印和记录；不要先把训练 loss 转成 Python 数值，再对它调用 backward。

### 梯度默认累加

```python
(s * s).backward()
print(s.grad.item())  # 原来为 4，再加 4，得到 8
s.grad.zero_()
(s * s).backward()
print(s.grad.item())  # 清零后重新得到 4
```

`zero_()` 的末尾下划线表示原地修改。在这个例子中清零的是梯度，不是参数 s。

每次 `(s * s)` 都进行了新的前向计算。默认反向传播后，旧图中用于求导的中间结果会被释放；不要把这里误改成对同一个 z 连续调用两次 backward。本周无需使用 retain_graph。

### 链式求导

令 s=1，`u=2*s+1`，`loss=u*u`。此时 u=3、loss=9，梯度为 `2*u * 2 = 12`。

梯度与损失值是不同的量：loss 为 9 不意味着梯度也为 9。自动求导沿着计算关系应用链式法则。

## 7. 线性回归、参数与 MSE

本周数据：

```python
x = torch.arange(5, dtype=torch.float32).reshape(-1, 1)
y_true = 2 * x + 1
w = torch.tensor(0.0, requires_grad=True)
b = torch.tensor(0.0, requires_grad=True)
y_pred = w * x + b
loss = (y_true - y_pred).pow(2).mean()
```

| 名称 | 含义 |
|---|---|
| x | 输入：0、1、2、3、4 |
| y_true | 已知目标：1、3、5、7、9 |
| y_pred | 用当前 w、b 算出的预测 |
| w | 斜率，训练希望逐渐接近 2 |
| b | 截距，训练希望逐渐接近 1 |
| loss | 预测误差的均方值，MSE |

`.pow(2)` 等价于平方，`.mean()` 再对这些平方求平均。两者顺序不能交换；先求平均再平方可能让正负误差抵消。

初始 w=b=0 时，预测全为 0，MSE 为 `(1+9+25+49+81)/5 = 33`。此时 w 的梯度为 -28，b 的梯度为 -10。

学习率 0.01 下更新一次：w=0.28，b=0.1；使用更新后的参数重新计算，MSE 约为 24.7524。

这是连续数值预测，所以用 MSE；第四周的 Precision、Recall、F1、Accuracy 用于分类任务，不能直接套到这些小数预测上。

## 8. 手动训练循环的顺序

当前手动 train 函数每轮执行：

```python
y_pred = w * x + b                    # 前向预测
loss = (y_true - y_pred).pow(2).mean() # 计算误差
losses.append(loss.item())            # 记录本轮更新前的损失
loss.backward()                      # 计算梯度
with torch.no_grad():
    w -= lr * w.grad                 # 参数沿梯度反方向移动
    b -= lr * b.grad
w.grad.zero_()                       # 清掉本轮梯度
b.grad.zero_()
```

- `lr` 是学习率，决定每次更新的步长；它不是模型学出来的 w 或 b。
- `epochs` 是训练轮数。当前每轮处理全部 5 个样本并更新一次参数。
- 梯度为负时，减去负数会让参数增大，属于正常更新。
- `torch.no_grad()` 让参数更新不被记录进求导图，不是让参数从此失去求导能力。
- 不清零会把不同轮次的梯度累加，改变当前想实现的普通梯度下降过程。
- 每轮都要重新计算预测和 loss，使梯度对应当前参数。

训练结束后重新计算 `final_loss`，它对应最后一次参数更新之后的模型。不要把 `losses[-1]` 必然当成更新后的最终损失。

## 9. SGD 优化器与手动更新的对应关系

```python
optimizer = torch.optim.SGD([w, b], lr=lr)
for epoch in range(epochs):
    optimizer.zero_grad()
    y_pred = w * x + b
    loss = (y_true - y_pred).pow(2).mean()
    losses.append(loss.item())
    loss.backward()
    optimizer.step()
```

| SGD 代码 | 作用 | 对应手动版 |
|---|---|---|
| `SGD([w, b], lr=lr)` | 登记要更新的参数及学习率 | 明确更新 w 和 b |
| `optimizer.zero_grad()` | 清除旧梯度 | 对各参数梯度调用 zero_ |
| `loss.backward()` | 计算梯度 | 相同 |
| `optimizer.step()` | 根据梯度更新登记的参数 | 在 no_grad 中减去学习率乘梯度 |

优化器不会替你计算预测、loss 或调用 backward。当前 SGD 没有设置动量等额外选项，与手动更新采用相同更新规则；数据、初值、学习率、轮数都相同时，结果应接近，曲线可能完全重合。

`optimizer.zero_grad()` 在一些版本/配置下把梯度设为 None，而不是零张量；对本例每轮都重新计算的参数梯度，仍能达到不累加旧梯度的目的。

虽然类名叫 SGD，本例每轮使用全量 5 个样本，没有随机抽样或 DataLoader。不要把“调用了 SGD”理解成“已经实现随机小批量训练”。

## 10. 函数封装、返回字典与入口保护

两个训练文件都定义 `train(lr, epochs)`。参数没有默认值，因此调用时必须传学习率和轮数，例如：

```python
result = train(lr=0.05, epochs=300)
print(result["w"], result["b"], result["final_loss"])
```

函数内部重新创建 x、w、b、losses。每次调用都从 w=b=0 开始，避免第二组实验接着第一组训练后的参数继续跑。

返回字典中的 `w`、`b`、`final_loss` 是 Python 数值，`losses` 是每轮损失组成的列表。多个值放进字典后，调用者可以按键取出，不必复制训练代码。

```python
from linear_regression_day5 import train as train_manual
from linear_regression_sgd import train as train_sgd
```

`as` 给同名函数起不同的本地名字，便于同时调用两个版本。

`if __name__ == "__main__":` 下的代码只在直接运行该文件时执行。被 compare_runs 导入时，不会顺便执行那里的演示训练。

**当前两个训练文件单独运行均使用 `train(0.05, 500)`；compare_runs 显式传入 300 轮。** 这不是冲突，但比较结果时必须说明轮数，不能把 500 轮和 300 轮当作同一配置。

## 11. 三组实验、CSV 与绘图

当前 compare_runs 的配置：

| 名称 | 方法 | 学习率 | 轮数 | 初始参数 |
|---|---|---:|---:|---|
| manual_005 | 手动更新 | 0.05 | 300 | w=b=0 |
| sgd_005 | SGD | 0.05 | 300 | w=b=0 |
| sgd_001 | SGD | 0.01 | 300 | w=b=0 |

比较手动版与 SGD 时保持其他条件一致；比较学习率时只改变学习率。这个例子中 0.05 收敛更快，不代表任何任务里学习率越大越好；过大可能使损失振荡或发散。

### 字典与列表表达式

```python
for name, result in runs.items():
    print(name, result["w"])
writer.writerow(["epoch", *runs.keys()])
writer.writerow([epoch] + [r["losses"][epoch] for r in runs.values()])
```

- `.items()` 每次提供一个实验名称与对应结果字典。
- `*runs.keys()` 把三个名称展开到表头列表。
- 列表推导式从每组结果取出同一轮的 loss，再与 `[epoch]` 拼接。
- 当前 keys 与 values 都来自同一个未修改的 runs 字典，因此表头与数值顺序一致。
- `newline=""` 配合 csv.writer，避免 Windows 下出现多余空行。
- 文件以 `"w"` 模式打开，每次运行会覆盖同名结果。

### 损失记录的时间点

CSV 有 300 条数据，加上表头共 301 行。epoch=0 是第一次更新前的初始损失 33，epoch=299 是第 300 次更新前的损失；终端打印的 final_loss 是第 300 次更新后的损失，所以末行与 final_loss 不要求完全相同。

当前保存的 CSV 中，epoch=1 的三组值约为 3.61、3.61、24.7524；epoch=299 时两组 0.05 的值约为 3.19e-10，0.01 的值约为 6.60e-4。这些是该记录的数值，不是通用验收常数；浮点结果可能有微小差异。

### 绘图

- `plt.plot(..., label=name)` 为每组画线并指定图例名称。
- `plt.yscale("log")` 使用对数纵轴，便于同时看很大和很小的正损失；不会改变 CSV 中的数据，也不改变训练。
- 对数轴不能正常表示 0 或负数；若以后训练出现精确零损失，应调整展示方法，不要篡改原始记录。
- `legend()` 显示图例；`tight_layout()` 调整边距；`savefig(..., dpi=150)` 保存图片。
- `show()` 显示窗口，在常见桌面运行方式下会等待关闭窗口；这不一定是程序卡住。
- `close()` 释放图形资源。

两个 0.05 的曲线重合是符合预期的。需要核对 CSV 的列，而不能因为只看到两条明显曲线就认为漏跑了一组。

## 12. 路径可靠性与 Day 7 独立重跑

```python
out = Path(__file__).resolve().parent / "output"
out.mkdir(parents=True, exist_ok=True)
```

`__file__` 指当前脚本，`resolve()` 解析为绝对路径，`.parent` 取脚本所在文件夹，`/` 用来拼接子路径。输出位置因此由脚本位置确定，不依赖终端当前目录。

`parents=True` 允许创建缺失的上级目录，`exist_ok=True` 允许目录已经存在。

用包含所需依赖的 Python，在另一个目录启动：

```powershell
Set-Location "E:\ai\job"
python "E:\ai\job\week_05_todo\compare_runs.py"
```

输出仍应进入 `E:\ai\job\week_05_todo\output`。若报缺少 matplotlib，应先核对解释器和安装依赖；这个错误发生在导入阶段，尚未证明输出路径有问题。

额外关系检查示例，可放在手动训练文件的主入口中：

```python
result = train(lr=0.05, epochs=300)
prediction = result["w"] * 5 + result["b"]
print(prediction)  # 应接近 11
```

这里使用训练得到的参数。x=5 没有用于这次训练，但只是根据已知人工规律进行的一次额外检查，不构成完整独立测试，更不能据此宣称泛化能力或漏洞检测效果。

## 13. 论文记录与当前待补知识

本周目录尚未发现单独的论文卡文件。若记录在其他位置，可补一个链接或文件位置；未完成时不要写成已经阅读完成。

论文卡建议记录：题目和来源、研究问题、输入输出、方法流程、数据与划分、比较基线、指标的定义和分母、主要结果、局限、仍不理解的术语。

联系当前研究方向时，先判断论文是在“用 Agent 检测软件漏洞”，还是“测试 Agent/具身系统自身的安全性”。模型产生的文字、提出的工具调用、实际执行的动作和最终环境结果不一定相同；评测要明确自己测的是哪一步。

当前练习打下的是张量、梯度、训练与实验记录基础。Dataset、DataLoader、nn.Module、训练/验证划分属于后续学习内容，本周代码尚未实现这些部分。

## 14. 本周自测清单

- [ ] 能查出终端和 PyCharm 使用的解释器，解释为什么一个环境有库、另一个没有。
- [ ] 能区分 `(5,)`、`(5, 1)`、`(1,)` 与标量 `()`。
- [ ] 能手算 A*A、A@V、mean(dim=0) 和 mean(dim=1)。
- [ ] 能解释梯度为什么依次为 4、8、4，而 s 本身仍是 2。
- [ ] 能手算链式求导例子的 loss=9、梯度=12。
- [ ] 能算出初始 MSE=33，以及学习率 0.01 下第一步的 w=0.28、b=0.1。
- [ ] 不看代码说出预测、损失、反向传播、更新、清梯度的顺序与作用。
- [ ] 能解释 no_grad、item、optimizer.zero_grad 和 optimizer.step。
- [ ] 每组实验重新初始化参数；比较时确认数据、学习率、轮数一致。
- [ ] 能说明 500 轮单独演示与 300 轮对比实验的区别。
- [ ] 核对 CSV 的 300 条记录与图的横轴，说明末行 loss 与 final_loss 的区别。
- [ ] 从另一个目录运行 compare_runs，确认输出位置正确。
- [ ] 用训练后的参数计算 x=5，说明接近 11 能检查什么、不能证明什么。
- [ ] 整理一张论文卡，并写下仍不理解的问题。

完成练习不只看程序是否退出成功，还要能够解释每一步为什么这样写，并让参数配置、输出记录和自己的结论对应起来。

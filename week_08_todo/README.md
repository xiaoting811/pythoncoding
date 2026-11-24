# 第八周 PyTorch 模型训练、保存与加载验证

本周用一个二分类练习串起完整流程。从 CSV 读取样本，用 PyTorch 训练小型神经网络，把模型参数和验证集预测保存到磁盘，再重新加载模型，检查能否复现原来的预测。

## 本周代码

| 文件 | 用途 |
| --- | --- |
| `data/samples.csv` | 练习数据。每条样本含 `sample_id`、两个特征 `x1` 和 `x2`、真实标签 `label` 及数据划分 `split` |
| `dataset.py`、`inspect_data.py` | 按训练集和验证集划分读取数据，查看样本张量和标签 |
| `model.py`、`inspect_weights.py` | 定义 `SmallMLP`，查看各层参数的名称、形状和元素数量 |
| `train_classifier.py`、`train_and_save.py` | 实现批量训练与评估，保存 `lr_001` 实验的模型和预测 |
| `load_one.py` | 加载模型并预测第一条验证样本 |
| `load_and_check.py`、`check_comparison.py` | 核对整个验证集的重载结果，并测试比较函数 |

## 1. 从 CSV 到张量

- `csv.DictReader` 用第一行作表头，逐行读成字典。原始标签是字符串，因此构建张量或比较标签时用 `int()` 转换。
- `ToyDataset("train")` 有 160 条样本，`ToyDataset("val")` 有 40 条。验证集的 `ds.x` 形状是 `(40, 2)`，数据类型是 `torch.float32`。标签张量的形状是 `(40,)`，数据类型是 `torch.long`。
- `x, y = ds[0]` 会调用 `__getitem__`，把返回的特征和标签解包。用 `x.tolist()` 得到特征列表，用 `y.item()` 取出单个标签值。
- `ds.x[:1]` 取第一条样本并保留批次维度，形状为 `(1, 2)`。模型随即输出形状为 `(1, 2)` 的类别分数，`scores.argmax(dim=1).item()` 取出分数最高的类别下标。

## 2. 看懂模型参数

`SmallMLP` 在 `nn.Sequential` 里依次执行 `Linear(2, 8)`、`ReLU()`、`Linear(8, 2)`。第一层的每个输出都按 `w1 * x1 + w2 * x2 + b` 计算。PyTorch 把线性层权重存成 `(输出数, 输入数)`。

| 参数名 | 形状 | 元素数 |
| --- | --- | ---: |
| `net.0.weight` | `(8, 2)` | 16 |
| `net.0.bias` | `(8,)` | 8 |
| `net.2.weight` | `(2, 8)` | 16 |
| `net.2.bias` | `(2,)` | 2 |

`ReLU` 把负值置零，保留正值，无需训练参数。遍历 `model.state_dict().items()` 时，每次得到一个参数名和对应的张量。用 `tensor.numel()` 统计元素个数，这个模型共 42 个参数。

## 3. 训练与保存

`train_and_save.py` 使用 SGD、交叉熵损失、学习率 `0.01`、批量大小 `16` 和 `60` 个 epoch。种子 `44` 用于模型初始化，种子 `43` 用于训练批次的打乱。验证集按原顺序读取，方便将预测与样本 ID 对齐。

| `output/lr_001/` 下的文件 | 内容 |
| --- | --- |
| `model.pt` | 最后一轮的模型参数，由 `torch.save(model.state_dict(), ...)` 写入 |
| `val_predictions.csv` | 最后一轮的验证集预测，含 `sample_id`、`y_true`、`y_pred` |
| `history.csv` | 每轮训练过程中的批次损失汇总，以及每轮结束后重新评估得到的训练损失、验证损失和验证准确率 |
| `config.json` | 超参数、随机种子、样本数、数据 SHA-256 和运行环境 |

保存后，用 `SmallMLP()` 先建立模型结构，再用 `torch.load(..., map_location="cpu", weights_only=True)` 读取参数字典。接着调用 `model.load_state_dict(state)` 按名称装入参数。评估时用 `model.eval()` 切换模式，用 `torch.no_grad()` 让前向计算跳过梯度记录。

## 4. 验证重新加载的模型

`ref` 和 `actual` 都是 `{样本 ID: 预测类别}`。两者使用同一套训练参数，分别在保存前和加载后计算。

- `ref` 用 `read_reference()` 从 CSV 读取 `sample_id` 和 `y_pred`。
- `actual` 用加载后的模型重新预测。`zip(ids, preds)` 产出一对对 `(ID, 类别)`，`dict()` 用每对的第一项作键、第二项作值。
- `diff = compare(ref, actual)` 先检查两组 ID 是否相同，再列出保存前后预测类别有变化的 ID。
- `wrong` 列出预测类别和 CSV 原始标签不同的 ID。比如 `s171` 的真实标签是 `1`，两次预测都是 `0`，所以它计入 `matched`，同时出现在 `wrong` 中。

`check_comparison.py` 用两条断言测试 `compare()`。复制 `ref` 后故意翻转 `s171` 的预测，结果应该是 `["s171"]`。把 `ref` 和内容相同的副本比较，结果应该是 `[]`。断言失败时，Python 在对应行抛出 `AssertionError`。

## 5. 运行与结果

在本地第八周目录下，使用已安装 PyTorch 的 Python。保存的实验配置记录了 Python `3.9.13` 和 PyTorch `2.8.0+cpu`。

```text
python inspect_data.py
python inspect_weights.py
python train_and_save.py
python load_one.py
python load_and_check.py
python check_comparison.py
```

`train_and_save.py` 会重新生成 `output/lr_001/` 下的实验文件。已有保存产物时，可以直接运行后面三个脚本。

当前保存的模型在最后一轮的验证损失约为 `0.2768`，验证准确率为 `97.5%`。加载并核对后的输出如下。

```text
matched: 40 / 40 []
correct: 39 / 40 ['s171']
```

比较函数测试输出 `changed IDS: ['s171']`，两条断言均通过。

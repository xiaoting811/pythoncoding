# 第六周：Dataset、DataLoader、MLP 分类与实验结果导出

本周要掌握：自己生成带标签的数据，固定训练/验证划分；用 Dataset 读取样本、DataLoader 组织批次、nn.Module 定义模型；写训练与验证循环，保存配置、逐轮损失和逐样本预测，再读取 CSV 画图。

本文按本目录实际文件整理。知识点、自测项与已实现功能分开描述，不表示所有自测均已完成。数据是人工坐标，不是漏洞数据；本周结果用于检查训练流程和代码理解。

## 1. 每个文件负责什么

| 文件 | 用途 |
|---|---|
| `check.py` | 查看解释器路径、Python、PyTorch、Matplotlib 版本 |
| `prepare_data.py` | 生成 200 条样本、标签和固定划分，写入数据 CSV |
| `dataset.py` | 定义 ToyDataset，读取指定划分；主入口演示取一个批次 |
| `model.py` | 定义 SmallMLP；主入口用临时数据检查形状、损失和参数数目 |
| `train_classifier.py` | 定义训练、验证、导出函数；主入口训练 60 轮并写入结果 |
| `plot-history.py` | 读取 history.csv，保存损失曲线 |
| `data/samples.csv` | 人工坐标、真实标签、训练/验证标记 |
| `output/history.csv` | 每一轮训练损失、验证损失、验证准确率 |
| `output/val_predictions.csv` | 最后一轮模型对验证集的预测与真实标签 |
| `output/config.json` | 学习率、轮数、种子、样本数、版本等配置 |
| `output/loss_curve.png` | 从 history.csv 画出的两条损失曲线 |
| `paper_notes_06.md` | 论文卡记录位置；整理本 README 时文件为空，待补 |

所有 Python 文件在本周目录同级，data 和 output 是子目录。新建模型时使用 model.py；Day 4-6 训练、验证与导出继续修改 train_classifier.py；画图另建 plot-history.py。

本目录实际画图文件名带连字符，运行命令以它为准。直接运行可以使用连字符；以后若要普通 import 这个模块，应改用下划线命名并更新相关引用。

## 2. 环境与运行顺序

本周已确认可运行的解释器是 `E:\anacanda\python.exe`。此前检查输出为 Python 3.9.13、PyTorch 2.8.0+cpu、Matplotlib 3.5.2；以重新运行 check.py 的实际输出为准。

PowerShell 中裸写 python 曾指向另一个 Python 3.13 环境，因此先明确使用同一个解释器：

```powershell
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\check.py"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\prepare_data.py"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\dataset.py"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\model.py"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\train_classifier.py"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\plot-history.py"
```

`&` 是 PowerShell 的调用运算符；第一个路径指定解释器，第二个指定脚本。上述命令写在终端，不写入 .py 文件。在 PyCharm 选择同一解释器后，右键运行也可以。

第一次先生成数据，再检查读取和模型，最后训练、画图。固定好数据后，重复训练可跳过生成步骤。训练会覆盖同名输出；生成脚本会覆盖同名输入 CSV，应保留实验配置与数据版本。

## 3. 人工样本、特征、标签与划分

一个样本就是一对数字 `(x1, x2)`，标签规则：

```python
label = 1 if x1 + x2 > 0 else 0
```

例如 `(0.6, -0.2)` 的标签是 1，`(-0.8, 0.3)` 的标签是 0。0、1 只是类别编号，不表示无漏洞、有漏洞。

| 字段 | 作用 | 是否送进模型 |
|---|---|---|
| sample_id | 样本编号，方便追溯 | 否 |
| x1、x2 | 两个输入特征 | 是 |
| label | 正确答案，用于计算损失和核对结果 | 不作为输入特征 |
| split | train 或 val，决定样本用途 | 否 |

训练中需要使用 label 计算损失，但输入只含 x1、x2。把答案放进输入会造成标签泄漏；split 也不是数值特征。

## 4. 批量生成数据的代码

```python
a = torch.linspace(-0.95, 0.95, 20)
b = torch.linspace(-0.9, 0.9, 10)
x = torch.cartesian_prod(a, b)
y = (x.sum(dim=1) > 0).long()
```

- linspace 包含两端，生成指定数量的等间隔数。
- cartesian_prod 将每个 a 与每个 b 配对，得到 20×10=200 个点，x 形状为 `(200, 2)`。
- sum(dim=1) 对每行的两个特征求和，结果为 `(200,)`。
- 与 0 比较得到布尔张量；long() 转为 int64 的 0/1 类别标签。
- 当前坐标取值下两类各 100 条；不需要画点才能生成数据，也不用手工输入 200 行。

### 编号与数值转换

```python
f"s{i:03d}"
x[i, 0].item()
```

`03d` 把整数至少显示为三位、不足补零，例如 s000、s009、s199。`.item()` 将一个元素的张量取成 Python 数值，便于写入 CSV。

## 5. 固定分层划分与随机种子

```python
g = torch.Generator().manual_seed(42)
train_ids = set()
for label in (0, 1):
    ids = torch.where(y == label)[0]
    order = torch.randperm(len(ids), generator=g)
    train_ids.update(ids[order[:80]].tolist())
```

- `where(...)[0]` 在这个一维条件中取出满足标签条件的位置编号。
- `randperm(n)` 生成 0 到 n-1 的随机排列，每个编号出现一次。
- `order[:80]` 选择前 80 个位置；`ids[...]` 再取出它们对应的原始样本编号。
- `tolist()` 转成 Python 列表；集合的 update 加入这些编号。
- `i in train_ids` 决定写 train 还是 val。

每类分别取 80 条训练、20 条验证，因此是保持类别比例的划分：

| 划分 | 标签 0 | 标签 1 | 总数 |
|---|---:|---:|---:|
| train | 80 | 80 | 160 |
| val | 20 | 20 | 40 |

训练集与验证集编号不能重叠。split 保存在 CSV 后，后面的每轮训练读取同一划分，不重新分组。

种子 42 控制划分，43 控制正式训练 DataLoader 的打乱顺序，44 在建模前控制参数初始化。固定种子便于同环境复核，不保证不同版本、设备都逐位一致。

## 6. CSV 读取与 Dataset 类

```python
self.rows = [r for r in csv.DictReader(file) if r["split"] == split]
self.x = torch.tensor(
    [[float(r["x1"]), float(r["x2"])] for r in self.rows],
    dtype=torch.float32,
)
self.y = torch.tensor(
    [int(r["label"]) for r in self.rows], dtype=torch.long,
)
```

DictReader 将每一行读成以表头为键的字典，字段值原本是字符串。必须转换 float/int 后才能构造训练张量。列表推导式先按 split 过滤，再构造特征与标签。

Dataset 管理样本，当前 ToyDataset 继承 PyTorch 的 Dataset：

```python
def __len__(self):
    return len(self.y)

def __getitem__(self, index):
    return self.x[index], self.y[index]
```

- `len(ds)` 调用 __len__，返回样本数。
- `ds[0]` 调用 __getitem__(0)，返回一条样本的特征和标签。
- 单个特征形状 `(2,)`，单个标签是零维标量 `()`。
- train 数据整体形状为 x `(160,2)`、y `(160,)`；val 为 x `(40,2)`、y `(40,)`。
- self.rows 保留编号等原始字段，供后面按同一顺序导出。

当前只检查 split 是否为 train/val。若将来读取外部数据，需要另加文件、列、数值、空数据、标签范围与ID重复检查。不能假设任意 CSV 都满足本例约束。

## 7. DataLoader：样本变成批次

```python
train_loader = DataLoader(
    train_ds, batch_size=16, shuffle=True, num_workers=0,
    generator=torch.Generator().manual_seed(43),
)
val_loader = DataLoader(
    val_ds, batch_size=16, shuffle=False, num_workers=0,
)
```

| 内容 | 训练集 | 验证集 |
|---|---|---|
| 样本数 | 160 | 40 |
| batch_size | 16 | 16 |
| 批次数 | 10 | 3，分别为 16、16、8 |
| shuffle | True | False |

`len(ds)` 是样本数，`len(loader)` 是批次数。`xb, yb = next(iter(loader))` 获取一个批次，常见形状为 xb `(16,2)`、yb `(16,)`。

打乱训练顺序不会改变 train/val 身份；同一批的特征和标签仍对应。验证不打乱，便于让 predictions 顺序与 val_ds.rows 对齐。

当前 dataset.py 演示入口用了 num_workers=2，正式训练用了 0。前者会启用两个数据加载工作进程；Windows 下需要正确的主入口保护。小数据初学阶段建议设 0，便于排错；2 不是 batch_size，也不是类别数。

## 8. nn.Module、MLP 与模型参数

```python
class SmallMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 2),
        )

    def forward(self, x):
        return self.net(x)
```

- nn.Module 是模型的基类，super().__init__() 初始化父类功能。
- 把层赋给 self.net，可以让框架管理层和参数；Sequential 按顺序执行各层。
- Linear(2,8) 将每条样本的 2 个特征映射到 8 个数；ReLU 将负数置零；Linear(8,2) 输出两类分数。
- 对 batch B，形状依次为 `(B,2) → (B,8) → (B,8) → (B,2)`。
- `model(x)` 会通过 Module 的调用机制执行 forward；平时使用这种写法。

参数数目为：第一层 2×8+8=24，第二层 8×2+2=18，共 42。`sum(p.numel() for p in model.parameters())` 统计的是可枚举参数张量中的元素数量；此模型参数均参与训练。

model.py 主入口用 4 条全零输入和临时标签检查接口，不读取 CSV，也不进行训练。当前人工分类边界是线性的，选择 MLP 是为了学习模型接口，并不意味着该任务必须用多层网络。

## 9. logits、argmax 与交叉熵

```python
logits = model(xb)
loss = nn.CrossEntropyLoss()(logits, yb)
pred = logits.argmax(dim=1)
```

| 变量 | 形状与类型 | 含义 |
|---|---|---|
| xb | `(B,2)` float32 | 输入特征 |
| logits | `(B,2)` 浮点数 | 每个样本的两个原始分数 |
| yb | `(B,)` long | 真实类别编号 0/1 |
| loss | 标量 | 这个批次的平均交叉熵 |
| pred | `(B,)` 整数 | 每行分数最大位置对应的类别 |

例如一条 logits 为 `[-0.3, 1.2]`，预测类别为 1。分数不是概率，可为负数，也不要求和为 1。

CrossEntropyLoss 使用原始 logits 和类别编号；本例不先做 softmax，也不把 argmax 后的类别送去算训练损失。argmax 用于判断预测类别，不能替代可求导的损失输入。本例标签无需 one-hot。

交叉熵与第五周 MSE 的含义、量纲不同，不能直接比较谁的数值小来判断任务做得更好。第四周的分类指标可在下一周接入本周真实预测。

## 10. 训练一轮与梯度更新

```python
model.train()
for xb, yb in loader:
    optimizer.zero_grad()
    logits = model(xb)
    loss = loss_fn(logits, yb)
    loss.backward()
    optimizer.step()
```

这与第五周训练步骤对应：清梯度 → 前向预测 → 计算损失 → 反向传播 → 更新参数。优化器初始化为 `SGD(model.parameters(), lr=0.1)`，直接管理网络中的全部参数。

一个 epoch 遍历全部训练批次；本例每轮 10 个批次，因此更新 10 次，60 轮共 600 次。optimizer 不应每轮重新初始化，模型也不应每轮重新创建。

```python
n = len(yb)
total_loss += loss.item() * n
count += n
return total_loss / count
```

默认损失是批次均值。先乘样本数得到该批损失总和，再除总样本数，是按样本加权的均值。若最后不足一批，不能直接平均各批均值；验证集 16、16、8 这个例子尤其需要注意。

`.item()` 取出数值用于日志；backward 调用的仍是原 loss 张量。返回值要求 loader 非空，换数据时应先检查，避免 count=0。

## 11. 验证：模式、梯度与准确率

```python
model.eval()
with torch.no_grad():
    for xb, yb in loader:
        logits = model(xb)
        pred = logits.argmax(dim=1)
        correct += (pred == yb).sum().item()
        predictions.extend(pred.tolist())
```

- eval() 切换 Dropout、BatchNorm 等层的行为，不自动关闭求导。
- no_grad() 关闭这段计算的梯度记录，不自动切换层模式。
- 当前网络没有 Dropout/BatchNorm，但保留这两个步骤，方便以后扩展。
- 验证不 backward、不 optimizer.step，不用验证数据更新参数。
- 下一轮训练函数先执行 model.train()，恢复训练模式。
- `(pred == yb)` 是逐样本布尔结果；求和得到正确条数，再除 count 得准确率。
- extend 把一个批次的预测逐项加入总列表；append 会加入一个整批列表，结构不同。

evaluate 返回三个值：平均验证损失、验证准确率、全部预测列表，调用处按相同顺序接收。40 条验证数据下，准确率的变化步长为 1/40=0.025。

训练和验证数据用途不同；当前没有独立测试集。以后用验证集调整方法后，不能再把它称为最终独立测试成绩。

## 12. 60 轮主入口与日志口径

主入口先固定模型种子、读取两组数据、构建 DataLoader、模型、损失函数和优化器；训练前 evaluate 一次，然后循环训练与验证，最后导出。

`range(1,61)` 产生 1 到 60。history 每轮追加一条字典，字段为 epoch、train_loss、val_loss、val_accuracy。`epoch == 1 or epoch % 10 == 0` 只控制终端打印，不会跳过中间轮次的训练或记录。

训练 loss 是这一轮各批更新时的平均，期间参数在变化；验证 loss 是本轮训练结束后用固定参数算的平均。所以两条曲线的高低差不能单独证明过拟合，应结合趋势、数据和实验条件分析。

本次已有文件的最后一行（epoch=60）：

```text
train_loss = 0.06892157755792142
val_loss = 0.02784869186580181
val_accuracy = 1.0
```

保存的预测对应 40/40 正确。这是简单人工数据上的结果，不代表真实漏洞检出能力。其他环境可能出现浮点差异，不必追求所有小数位完全相同。

## 13. val_predictions.csv 到底在哪里写入

写入发生在 train_classifier.py 的 export_results 中：

```python
rows = []
for row, pred in zip(val_ds.rows, predictions):
    rows.append({
        "sample_id": row["sample_id"],
        "y_true": int(row["label"]),
        "y_pred": pred,
    })
write_csv(out / "val_predictions.csv", rows)
```

先用 evaluate 得到预测；再配对原始验证记录与预测；最后调用 write_csv 保存。这个流程依赖 val_loader 的 shuffle=False 以及 Dataset 当前按原行顺序取样。

`assert len(predictions) == len(val_ds)` 检查数量一致，但不能单独证明顺序一致。zip 默认按较短序列停止，所以长度检查仍然必要。

| 输出 | 写入位置 | 数据来源 |
|---|---|---|
| history.csv | export_results → write_csv | 60 轮 history |
| val_predictions.csv | export_results → write_csv | 最后一轮验证预测与 val_ds.rows |
| config.json | export_results → json.dump | 主入口中的配置字典 |
| loss_curve.png | plot-history.py → savefig | history.csv 的两列损失 |

主入口中的 `export_results(history, val_ds, predictions, config)` 放在训练循环之后、与 for 同级缩进，执行一次，保存最后一轮的结果。

write_csv 用第一条字典的键作为表头，writeheader 写表头、writerows 写记录。当前 history 和验证记录都非空；若扩展为通用工具，应检查空列表。`newline=""` 避免 Windows CSV 多余空行，`"w"` 会覆盖旧文件。

当前配置中的 `"loss": "CrossEntropyloss"` 是说明字符串，大小写与真实类名 `CrossEntropyLoss` 不一致，不影响当前训练；后续整理可改正。当前 json.dump 未格式化，仍是合法 JSON。为便于阅读，可使用 UTF-8、ensure_ascii=False、indent=2；这属于建议，不表示脚本已改。

## 14. pathlib 路径、绘图与复盘

```python
BASEDIR = Path(__file__).resolve().parent
out = BASEDIR / "output"
```

__file__ 指当前脚本，resolve 解析路径，parent 取脚本目录，`/` 拼接路径。输出因此不依赖终端当前工作目录。mkdir(parents=True, exist_ok=True) 创建缺少的目录并允许它已存在。

绘图脚本读 CSV 时把 epoch 转 int、两列 loss 转 float，再画两条线。legend 显示名称，xlabel/ylabel 标轴，tight_layout 调整边距，savefig 保存图片，close 释放图形资源。

当前未调用 show()，所以不弹窗是正常的。打开 output/loss_curve.png 查看图片即可。每次重跑训练会更新 CSV；随后重跑画图才能让图片跟这次结果对应。

可从另一目录运行检查路径：

```powershell
Set-Location "E:\ai\job"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\train_classifier.py"
& "E:\anacanda\python.exe" "E:\ai\job\week_06_todo\plot-history.py"
```

建议完成的自测：

- [ ] 能从零说明 200 个点如何产生，以及为什么划分为 160/40。
- [ ] 能解释特征、标签、split，检查标签未被混入模型输入。
- [ ] 能解释 Dataset 两个特殊方法、DataLoader 与最后一批大小。
- [ ] 能逐层说明形状，手算参数总数 42。
- [ ] 能区分 logits、预测类别、交叉熵和准确率。
- [ ] 能不看参考说出训练顺序，解释 eval 与 no_grad 的不同作用。
- [ ] 验证前后参数值不变，训练与验证编号无交集。
- [ ] 能找到每个输出的写入位置，说明为何导出要在训练循环后。
- [ ] CSV 共 60 条历史和 40 条预测，准确率与逐样本核对一致。
- [ ] 能从另一个目录运行，确认文件仍写入本周 output。
- [ ] 能说明本例没有独立测试集，结果不能直接推广到漏洞检测。
- [ ] 补完 paper_notes_06.md，记录研究对象、输入输出、工具、验证证据、指标与疑问。

下周在这条可重跑基线上练习学习率对照、分类指标与错误分析；保留数据划分，避免同时改模型、数据和优化器。

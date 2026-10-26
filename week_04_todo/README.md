# 第四周：漏洞检测指标、数据校验与评测结果导出

本周要掌握：区分真实标签与预测标签，统计 TP/FP/TN/FN，计算分类指标，校验预测 CSV，调用其他文件中的函数，并导出可核对的结果。

本文按当前目录中的代码整理。标为“建议补充”或“后续任务”的内容是需要掌握的要求，不表示脚本已经实现。当前代码到 Day 4；论文对比和漏洞案例属于后续学习项。

## 1. 文件与运行方式

| 文件 | 用途 |
|---|---|
| `practice.py` | 计数函数、零分母处理、指标计算和示例入口 |
| `evaluate_predictions.py` | 读取预测文件、检查数据、调用函数、导出结果 |
| `day1_notes.md` | 手算与概念记录，目前已有混淆矩阵 |
| `data/predictions_practices.csv` | 人工真实标签和模拟预测，共 10 条 |
| `output/metrics.json` | 样本数、四种计数和指标 |
| `output/error_samples.csv` | 真实标签与预测标签不同的记录 |

在本目录终端运行：

```powershell
python practice.py
python evaluate_predictions.py
```

本目录实际输入名是 `predictions_practices.csv`，比计划示例多一个 `s`。名字可以不同，但代码与文件名必须一致。

数据是人为构造的练习，没有实际漏洞代码，不能用这些数字说明真实模型的检测水平。

## 2. 真实标签、预测标签与正负类

```python
y_true = [1, 1, 0, 0, 1, 0, 0, 0, 1, 0]
y_pred = [1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
```

- `y_true` 是真实答案，`y_pred` 是预测结果；相同位置对应同一个样本。
- 本练习约定 `1` 为有漏洞，即正类；`0` 为无漏洞，即负类。
- “正类”指研究中重点识别的类别，不表示好事或正确判断。
- 真实研究先看数据说明，不能假设所有数据集标签意义相同。
- 不要把两列分别删缺失后再配对，否则可能让不同样本的标签错位。

## 3. TP、FP、TN、FN 与混淆矩阵

| 真实标签 | 预测标签 | 类别 | 含义 |
|---:|---:|---|---|
| 1 | 1 | TP | 有漏洞，预测有漏洞，正确检出 |
| 0 | 1 | FP | 无漏洞，预测有漏洞，误报 |
| 0 | 0 | TN | 无漏洞，预测无漏洞，正确排除 |
| 1 | 0 | FN | 有漏洞，预测无漏洞，漏报 |

T/F 表示判断是否正确，P/N 表示预测是正类还是负类。理解每行对应的真实和预测值比背缩写重要。

本练习约定矩阵的行是真实标签、列是预测标签，顺序均为 0、1：

| 真实情况 / 预测结果 | 预测无漏洞（0） | 预测有漏洞（1） |
|---|---:|---:|
| 真实无漏洞（0） | TN=4 | FP=2 |
| 真实有漏洞（1） | FN=1 | TP=3 |

写成二维列表为 `[[4, 2], [1, 3]]`。不同工具和论文的排列方式可能不同，先看行列标签。

### 逐样本核对

| 编号 | 真实 | 预测 | 分类 |
|---|---:|---:|---|
| s01 | 1 | 1 | TP |
| s02 | 1 | 0 | FN |
| s03 | 0 | 0 | TN |
| s04 | 0 | 1 | FP |
| s05 | 1 | 1 | TP |
| s06 | 0 | 0 | TN |
| s07 | 0 | 0 | TN |
| s08 | 0 | 1 | FP |
| s09 | 1 | 1 | TP |
| s10 | 0 | 0 | TN |

合法输入必须满足：`tp + fp + tn + fn == len(y_true)`。不满足时可能漏计了样本。

## 4. 用函数统计计数

```python
counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}

for i in range(len(y_true)):
    if y_true[i] == 1 and y_pred[i] == 1:
        counts["tp"] += 1
    # 其他三种情况分别累加对应键
```

- `range(len(y_true))` 产生从 0 到长度减 1 的下标。
- `counts["tp"] += 1` 等价于把原计数加 1 后重新赋值。
- `and` 表示两个条件同时成立；比较两边的括号不是必须的。
- `return counts` 返回整个计数字典，不能写在循环内部，否则可能只处理一个样本。

### 输入检查先于统计

```python
if len(y_true) != len(y_pred):
    raise ValueError("真实列表和预测列表长度不相同")
if len(y_true) == 0:
    raise ValueError("列表为空")

for label in y_true:
    if label not in (0, 1):
        raise ValueError("真实标签只能为 0 或 1")
```

`y_pred` 也要检查。当前代码使用 `label != 0 and label != 1`，与这里的标签范围判断等价。

不要对错误输入返回一句字符串而对正常输入返回字典；调用者难以按统一格式处理。`raise ValueError(...)` 用于明确报告无效数据，异常可以在调用处捕获。

### `zip` 的可选写法

```python
for actual, predicted in zip(y_true, y_pred):
    print(actual, predicted)
```

每轮取出同位置的一对值，不需要手动下标。`zip` 默认在较短序列结束时停止，因此即使换用它，也必须先检查长度。当前使用下标的方式正确，不要求为了简短而重写。

## 5. Precision、Recall、F1 和 Accuracy

| 指标 | 公式 | 回答的问题 | 本例 |
|---|---|---|---:|
| Precision | TP / (TP+FP) | 报告的漏洞中，多少是真的？ | 0.6 |
| Recall | TP / (TP+FN) | 真实漏洞中，找出了多少？ | 0.75 |
| F1 | 2TP / (2TP+FP+FN) | Precision 和 Recall 的综合表现 | 约 0.6667 |
| Accuracy | (TP+TN) / 总样本数 | 所有样本中，总体判断对了多少？ | 0.7 |

这些是正类为漏洞时的二分类指标。F1 不是 Precision 与 Recall 的普通算术平均。

例如 100 个样本中只有 5 个漏洞，全部预测无漏洞，会得到 Accuracy=95%，但 Recall=0%。高准确率不一定意味着找到了漏洞。

### 零分母与空数据

```python
def safe_division(numerator, denominator):
    if denominator == 0:
        return 0.0
    return numerator / denominator
```

- `numerator` 是分子，`denominator` 是分母。
- 执行 `return 0.0` 后函数立即结束，不再继续除法。
- 分母为零时记 0 是本练习约定，不是数学上认为除以零等于零。
- 全部计数之和为 0 表示没有样本，`calculate_metrics` 应抛出 `ValueError`，不能给出“0 分评测”。
- 当前代码保留单项零分母提示，再调用 `safe_division`，存在重复保护但不影响结果。

| 真实 / 预测 | Precision | Recall | F1 | Accuracy |
|---|---:|---:|---:|---:|
| `[1,0]` / `[1,0]` | 1 | 1 | 1 | 1 |
| `[1,0]` / `[0,0]` | 0（约定） | 0 | 0 | 0.5 |
| `[0,0]` / `[0,0]` | 0（约定） | 0（约定） | 0（约定） | 1 |

最后一组没有真实漏洞，不能证明检测系统会发现漏洞。

## 6. 返回字典、遍历与格式化

```python
metrics = {
    "precision": 0.6,
    "recall": 0.75,
    "f1": 2 / 3,
    "accuracy": 0.7,
}

for name, value in metrics.items():
    print(f"{name}: {value:.4f}")
```

`items()` 提供每一组键和值，分别交给 `name`、`value`；这两个名字可自行命名。输出例如 `precision: 0.6000`。

- f-string 把大括号中的值插入字符串。
- `.4f` 显示小数点后 4 位，必要时补零或四舍五入。
- 这只改变显示，不会改写 `metrics` 中的原始浮点数。
- 内部计算保留精度，避免先把 Precision、Recall 四舍五入再计算 F1。
- 当前函数内部的 `Recall`、`F1`、`Accuracy` 命名能运行，后续可统一小写；返回字典键已是小写。

## 7. 文件导入与程序入口

```python
from practice import confusion_counts, calculate_metrics
```

这是从同目录的 `practice.py` 导入两个函数，模块名不写 `.py`。导入后可以直接调用，不需要复制实现。不是从文件名相似的其他周目录读取函数。

```python
if __name__ == "__main__":
    # 在这里运行示例
    result = confusion_counts(y_true, y_pred)
```

直接运行 `practice.py` 时会进入这里；被 `evaluate_predictions.py` 导入时，不会执行示例。函数定义在入口外，以便导入复用。当前代码已加入口保护。

## 8. 读取预测 CSV 与数据校验

```python
BASE_DIR = Path(__file__).resolve().parent
input_path = BASE_DIR / "data" / "predictions_practices.csv"
df = pd.read_csv(input_path)

required_columns = {"sample_id", "y_true", "y_pred"}
missing_columns = required_columns - set(df.columns)
```

- 花括号这里表示集合；集合差集找出“要求存在，但实际没有”的列名。
- `df.empty` 判断表格是否为空；只有表头没有数据也属于空表。
- 完全空文件可能在 `read_csv` 时就抛 `pd.errors.EmptyDataError`，还没执行到 `df.empty`。该异常属于 `ValueError`，当前 `except ValueError` 可以捕获。

### `any()` 与 `all()`

```python
df["sample_id"].isnull().any()
df["sample_id"].duplicated().any()
df["y_true"].isin([0, 1]).all()
```

| 表达式 | 含义 |
|---|---|
| `isnull().any()` | 是否至少有一个缺失值 |
| `duplicated().any()` | 是否至少有一个重复记录 |
| `isin([0,1]).all()` | 是否每个值都属于 0 或 1 |
| `not ...all()` | 是否存在不合要求的值 |

遍历 DataFrame 时默认得到列名：

```python
for column in df[["y_true", "y_pred"]]:
    print(column)  # 分别为 y_true、y_pred
```

不是直接遍历每一行；随后 `df[column]` 才取出相应 Series。

### 样本编号与空白字符串

当前脚本已检查编号缺失和重复，但没有剔除两端空格后检查。`"   "` 不一定是 Pandas 缺失值。

建议补充的知识点示例：

```python
if df["sample_id"].isnull().any():
    raise ValueError("样本编号缺失")
ids = df["sample_id"].astype(str).str.strip()
if ids.eq("").any():
    raise ValueError("样本编号不能为空白")
if ids.duplicated().any():
    raise ValueError("样本编号重复")
```

这里 `astype(str)` 转字符串，`.str.strip()` 对整列文本去两端空白，`.eq("")` 逐项比较是否为空字符串。先检查缺失，再转普通字符串，避免把缺失值变成文字后漏查。

### Series 与列表

当前 `check()` 返回 `df["y_true"], df["y_pred"]`，它们是两个 Series，不是整个 DataFrame；注释可据此理解。

CSV 默认读取产生从 0 开始的行索引，当前下标计数方式可以使用。若以后先筛选、去重，索引可能不连续；建议在调用计数函数前使用 `.tolist()` 转成列表，或用按值遍历的 `zip`，不要把 Series 的标签索引误当作位置。

## 9. 异常处理要给出真实原因并停止

```python
try:
    y_true, y_pred = check(input_path)
except (FileNotFoundError, ValueError) as error:
    print(f"无法评测：{error}")
    raise SystemExit(1)
```

上面是建议采用的提示写法。`as error` 保存异常对象，保留“列缺失、标签错误、ID 重复”等实际原因。

- `raise` 抛出异常，交给调用者处理。
- `except` 捕获指定异常，不等于自动重新读取成功。
- `raise SystemExit(1)` 结束当前脚本，1 表示非正常退出。
- 读取失败后继续计算，会使用尚未创建的 `y_true`、`y_pred`，引发新错误。
- 当前代码已经停止失败流程，但把所有捕获到的错误都打印成“输入文件不存在”，需要掌握上面这种保留原因的方式。
- `OSError` 还可涉及权限或磁盘等文件问题；只有成功写完文件才能声称保存成功。

## 10. JSON 导出与错误样本筛选

```python
result = {
    "sample_count": len(y_true),
    "confusion_matrix": counts,
    "metrics": metrics,
}

with open(output_dir / "metrics.json", "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=2)
```

外层字典包含嵌套字典。`sample_count` 是记录数，不包含表头。当前 `confusion_matrix` 字段保存四种计数字典，不是二维数组，读取时以实际结构为准。

```python
error_samples = df[df["y_true"] != df["y_pred"]]
error_samples.to_csv(
    output_dir / "error_samples.csv",
    index=False,
    encoding="utf-8-sig",
)
```

- 比较产生布尔 Series，保留 True 对应的行。
- 本例错误行是 s02、s04、s08，其中 s02 漏报，另两条误报。
- 当前代码从同一输入重新读取 df 再筛选，也能得到预期结果；后续可让检查函数返回同一个 df，避免重复读取及潜在数据不一致。
- 直接向 `to_csv` 传路径，让 Pandas 处理打开、编码和换行。若自己 `open` 文本文件，应设置正确编码及 `newline=""`，不能指望 `to_csv` 改变已打开文件的编码。
- `mkdir(exist_ok=True)` 允许已有目录；`parents=True` 才会递归创建缺少的上级目录。
- 默认写文件会覆盖同名输出，校验必须先完成，原始 CSV 应保留。

## 11. Day 5、Day 6 需要继续掌握的内容

以下是本周后续学习目标，不代表目前目录已经有相关成果。

### 论文阅读与比较

第二篇论文先整理：任务与目标语言、输入输出、检测粒度、数据来源、标签、划分、模型、基线、指标和局限。

比较论文时先核对数据与口径。不同测试集、不同粒度、不同阈值下的 F1 不能简单按大小排序。未找到的信息如实标注，不自行猜测。

建议交付 `paper_notes_02.md` 与 `paper_compare.md`。若第一篇记录放在其他文件夹，可记录位置，不需要重复复制全文。

### 漏洞与修复案例

每例解释：输入来源、危险操作、成立前提、根因、修改语句、修复机制、剩余限制和来源。使用教学例时注明它不是已确认的真实项目漏洞。

例如数据库参数绑定用于分离查询结构与数据，但不能替代权限检查；工具告警、编译通过、模型自评也不能单独证明漏洞成立或已经修复。

## 12. 自测与本周待补项

- [ ] 不看表格解释 TP/FP/TN/FN，能逐样本分类。
- [ ] 四项计数之和等于样本数，指标与手算一致。
- [ ] 解释为什么准确率高仍可能漏掉全部漏洞。
- [ ] 解释空数据报错与单项零分母记 0 的区别。
- [ ] 能说明实参、返回字典、`.items()`、`.4f` 和入口保护。
- [ ] 检查列、样本数、编号、标签，错误时停止并显示真实原因。
- [ ] 理解只含空格的 ID 需要另外检查。
- [ ] JSON 和错误样本 CSV 可读，原始输入没有被覆盖。
- [ ] 在 `day1_notes.md` 补逐样本表与准确率反例解释。
- [ ] 完成第二篇论文比较和两个漏洞案例说明。

当前已实现的正常流程与本例数值一致；不要把此 README 的知识点或待办写成所有要求都已验收通过。

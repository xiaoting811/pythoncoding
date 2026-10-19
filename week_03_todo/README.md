# 第三周：NumPy、Pandas 与数据可视化

本周学习：数组索引与运算、表格读取与筛选、缺失值与重复检查、函数拆分、统计图导出。
本文根据本目录当前代码整理；标为“建议”的示例用于补充学习，不表示脚本已经实现。

## 1. 文件与运行方式

| 文件 | 用途 |
|---|---|
| numpy_practice.py | 数组属性、索引、切片、统计和筛选 |
| pandas_practice.py | 成绩表读取、筛选、增加总分和平均分、导出 |
| practice.py | 缺失值、重复行、标签和项目分布练习 |
| analyze_data.py | 用函数组织数据检查和两张统计图生成 |
| scores.csv | 姓名、Python、数学成绩 |
| data/sample_practice.csv | 人为构造的数据检查练习，不是真实漏洞数据集 |
| data/clean_df.csv | practice.py 生成的去重数据 |
| data/clean_sample_practice.csv | analyze_data.py 生成的去重数据 |
| output/score_analysis.csv | 成绩统计结果 |
| output/label_distribution.png | 去重后标签数量柱状图 |
| output/code_length_distribution.png | 去重后代码长度直方图 |

在本目录终端运行相应文件：

```powershell
python numpy_practice.py
python pandas_practice.py
python practice.py
python analyze_data.py
```

需要的第三方库：

```powershell
python -m pip install numpy pandas matplotlib
```

部分早期练习被注释，不会执行；取消注释时注意变量名和运行顺序。

## 2. 导入与路径

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
input_path = BASE_DIR / "data" / "sample_practice.csv"
output_dir = BASE_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)
```

- `as` 给模块起别名；`plt` 对应 `matplotlib.pyplot`，不能仅导入 `matplotlib as plt` 后调用 pyplot 的方法。
- `__file__` 是当前 Python 文件路径；`Path()` 转成路径对象。
- `resolve()` 得到绝对路径并解析符号链接等；`parent` 取所在目录。
- 路径对象的 `/` 用来拼接路径，不是做除法。
- `mkdir()` 创建文件夹；`parents=True` 连同缺少的父目录一起创建。
- `exist_ok=True` 允许目标文件夹已经存在，不会清空其内容。
- 拼接路径本身不会创建文件；保存 CSV、PNG 前要保证父文件夹存在。
- `BASE_DIR`、`BASEDIR` 都是自定义变量名，使用时要保持一致。

## 3. NumPy：创建数组和查看属性

```python
scores = np.array([
    [85, 90],
    [78, 88],
    [92, 95],
    [60, 70],
])

print(scores.shape)  # (4, 2)：4 个学生、2 门课程
print(scores.ndim)   # 2：二维数组
print(scores.dtype)  # 元素的数据类型，当前数据为整数类型
```

`shape`、`ndim`、`dtype` 是属性，不加调用括号。

### 索引、切片和修改

```python
scores[2]       # 第三个学生：[92, 95]
scores[:, 1]    # 所有学生的第二科：[90, 88, 95, 70]
scores[:2]      # 前两个学生；切片包含起点，不包含终点
scores[3, 0] = 65
```

下标从 0 开始。二维索引写成 `[行, 列]`；`:` 表示该方向全选。
`scores[3][0] = 65` 在本例也可用，但 NumPy 更常写成 `scores[3, 0] = 65`。
以下统计例子以原始成绩为准；如果先修改成绩，结果会相应改变。

### axis、求和、平均与最大值

```python
scores.mean(axis=0)  # 各科平均分：[78.75, 85.75]
scores.mean(axis=1)  # 各学生平均分：[87.5, 83, 93.5, 65]
scores.sum(axis=1)   # 各学生总分：[175, 166, 187, 130]
scores.max(axis=0)   # 各科最高分：[92, 95]
```

对于本例的“学生 × 课程”二维数组：

- `axis=0`：消去行方向，得到每列的统计结果。
- `axis=1`：消去列方向，得到每行的统计结果。
- 不指定 axis 时，这些方法默认对整个数组统计。

### 布尔筛选

```python
scores[scores[:, 0] >= 80]
scores[scores.mean(axis=1) >= 85]
```

先计算每行条件，得到 True/False 数组，再保留 True 对应的行。
第二句选出第一、第三个学生，返回他们的两科成绩，不只是平均分。

### 广播与数组、列表的乘法

```python
bonus = np.array([2, 3])
adjusted_scores = scores + bonus
```

`(4, 2)` 数组与长度为 2 的数组相加，按最后一个维度对齐：每行第一科加 2、第二科加 3。
形状不兼容时可能报 ValueError；广播不是任意大小的数组都能相加。

```python
scores * 2       # 每个数乘以 2
[85, 90] * 2     # 列表重复：[85, 90, 85, 90]
```

## 4. Pandas：读取和查看表格

```python
df = pd.read_csv(BASE_DIR / "scores.csv")
print(df.head())
print(df.shape)
print(df.columns)
print(df.dtypes)
```

| 用法 | 含义 |
|---|---|
| DataFrame | 带行索引、列名的二维表格 |
| Series | 一维带索引的数据，常见于单列和统计结果 |
| head() / head(2) | 前 5 行 / 前 2 行 |
| shape | `(行数, 列数)`，不含 CSV 表头 |
| shape[0] / shape[1] | 行数 / 列数 |
| columns | 列名索引 |
| dtypes | 每列的数据类型 |

Pandas 会推断 CSV 的列类型；当前成绩为整数。若混入文本或缺失值，推断结果可能不同。
`name` 在当前环境显示 `object`，表示该列使用对象类型存储，不表示姓名不是字符串。

```python
df["name"].dtype             # 整列存储类型，当前环境为 object
type(df.loc[0, "name"])     # 索引为 0 的姓名值类型：str
```

不同 Pandas 版本或配置也可能使用专门的字符串 dtype，不必要求所有环境显示相同名称。

### 选列、筛选与新增列

```python
df["math"]                       # Series
df[["name", "math"]]             # DataFrame：外层选列、内层是列名列表
df[df["python"] >= 80]           # 筛选符合条件的学生

df["total"] = df["python"] + df["math"]
df["average"] = df["total"] / 2
print(df)
```

列运算按索引对齐，本例对应同一学生的两科相加，不需要手动循环。
给不存在的列赋值会新增列，给已有列赋值会替换该列。
赋值不会自动打印；之前的 print 不会随之后的数据变化而更新。
筛选后的行索引默认保留，看到 0、2 而非 0、1 是正常的。

组合多个条件时使用 `&`（且）、`|`（或），每个条件加括号：

```python
df[(df["python"] >= 80) & (df["math"] >= 80)]
```

### 保存 CSV

```python
df.to_csv(output_dir / "score_analysis.csv",
          index=False, encoding="utf-8-sig")
```

- `index=False`：不把行索引额外写成一列，不是删除内存中的索引。
- `utf-8-sig`：带 BOM 的 UTF-8，方便 Excel 识别中文。
- 默认写入表头，同名目标文件会被覆盖。
- 修改 DataFrame 不会自动更新原始文件，调用 to_csv 才保存。
- 输入、输出采用不同文件名，保留原始数据。

当前成绩验收：张三 175 / 87.5，李四 166 / 83，王五 187 / 93.5，赵六 130 / 65。

## 5. 练习数据含义与数据检查

`data/sample_practice.csv` 是人工构造的练习数据，不能用于评价漏洞检测模型。

| 字段 | 含义 |
|---|---|
| sample_id | 样本编号 |
| project | 来源项目 |
| label | 本例约定 0 为无漏洞、1 为有漏洞；缺失表示未知 |
| code_lines | 代码行数，长度单位为行 |

真实数据中的标签含义以数据说明为准，不能直接套用本例约定。

### 缺失值

```python
df.isnull()                         # 每个单元格是否缺失
# isna() 和 isnull() 在这里等价
df.isnull().sum()                   # 每列缺失数量
df.isnull().sum().sum()             # 缺失单元格总数，不是含缺失的行数
df[df["label"].isnull()]            # 找到标签缺失的记录
df[df["code_lines"].isnull()]       # 找到长度缺失的记录
lengths = df["code_lines"].dropna()  # 取非缺失长度，不修改原表
```

True 求和按 1、False 按 0 计算。空 CSV 字段读取后通常是 NaN；NaN 不是 0，也不是字符串 "NaN"。
不要把未知标签自动填为 0；不要把缺失长度默认当作 0 行。
含缺失的整数列在当前读取方式下可能显示为浮点数，如 1.0、0.0。

### 重复行

```python
df.duplicated()                      # 第一次出现为 False，后续完全相同行为 True
df.duplicated().sum()                # 多余重复行数
duplicates = df[df.duplicated()]     # 多余的重复记录
df[df.duplicated(keep=False)]        # 重复组中的全部记录，含第一次出现
clean_df = df.drop_duplicates()      # 默认保留第一次，返回新的 DataFrame
```

默认比较所有列的值。去重和筛选保留原行索引：s09 左侧的 9 是原表索引，不是记录数量。
原始 df 和输入 CSV 不会因为上述默认调用而被改写。

建议补充重复记录导出；当前 practice.py 只生成了 duplicates 对应变量，尚未导出它：

```python
duplicates.to_csv(output_dir / "duplicate_records.csv",
                  index=False, encoding="utf-8-sig")
```

### 标签与项目分布

```python
clean_df["label"].value_counts()                 # 默认不计缺失，按数量降序
clean_df["label"].value_counts(dropna=False)     # 缺失也统计
clean_df["project"].value_counts(dropna=False)   # 各项目数量
clean_df.groupby("project").size()              # 按项目分组，统计每组行数
```

统计原始数据还是去重数据要标明，避免终端报告与图表口径不同。
`groupby(...).size()` 统计组内行数，本例中即使 label 或 code_lines 缺失也计入所属项目。

### reindex 与 to_numpy

```python
label_counts = clean_df["label"].value_counts()
label_counts = label_counts.reindex([0, 1], fill_value=0)
values = label_counts.to_numpy()
```

`value_counts()` 返回 Series：索引是标签，值是数量。
`reindex([0, 1])` 固定输出标签和顺序，新补出的索引对应数量填 0。
例如仅有标签 0 共 5 条时，结果为“0: 5，1: 0”。填的是数量，不会把原始缺失标签改为 0。
如果有标签 2，此 reindex 会排除它，所以真实数据需先检查标签范围。
`fill_value` 用于新补出的项，不是通用的已有缺失值填充操作。
`to_numpy()` 取出数量数组，不带原 Series 的索引，例如 `[4, 4]`。

### 本例核对结果

| 指标 | 预期 |
|---|---:|
| 原始行数 | 10 |
| 多余完全重复行 | 1 |
| 去重后行数 | 9 |
| 去重前标签 1 / 0 | 5 / 4 |
| 去重后标签 1 / 0 | 4 / 4 |
| 去重后缺失标签 | 1 |
| 去重后缺失长度 | 1 |
| 去重后有效长度 | 8 |
| 去重后 alpha / beta / gamma | 各 3 |

## 6. Matplotlib：创建、绘制和保存

```python
fig, ax = plt.subplots()
```

`fig` 是整张图，`ax` 是绘图区。绘制两张独立图时分别创建画布，避免 bar 和 hist 画到同一个 ax 上。

### 标签数量柱状图

```python
fig, ax = plt.subplots()
ax.bar(["0", "1"], label_counts.to_numpy())
ax.set_xlabel("Label")
ax.set_ylabel("Sample Count")
ax.set_title("Label Distribution")
fig.tight_layout()
fig.savefig(output_dir / "label_distribution.png", dpi=150)
```

横轴是类别、纵轴是数量；bar 按位置配对，不会根据 Series 索引自动匹配。
先 reindex 再转数组，才能确保第一根柱子是标签 0、第二根是标签 1。
缺失标签不进入这两个柱子，应单独打印其数量。

### 代码长度直方图

```python
lengths = clean_df["code_lines"].dropna()
fig, ax = plt.subplots()
ax.hist(lengths, bins=5, edgecolor="black")
ax.set_xlabel("Code Length (lines)")
ax.set_ylabel("Sample Count")
ax.set_title("Code Length Distribution")
fig.tight_layout()
fig.savefig(output_dir / "code_length_distribution.png", dpi=150)
```

- hist 统计数值落入各区间的次数；横轴为长度区间，纵轴为样本数量。
- bins=5 表示分为 5 个等宽区间，不是每组 5 条数据，也不是区间宽度为 5。
- 默认根据数据范围确定边界；区间左闭右开，最后一个也包含右端点。
- edgecolor 设置柱子边框颜色，不是填充颜色。
- 本例有效长度为 12、8、20、15、9、30、18、11。
- 范围 8～30，区间边界为 8、12.4、16.8、21.2、25.6、30，数量依次 4、1、2、0、1。
- 缺少标签但有长度的 s09 可以参与长度图；缺少长度但有标签的 s07 可以参与标签图。

### 布局、保存、显示与关闭

| 用法 | 含义 |
|---|---|
| set_xlabel / set_ylabel | 横轴 / 纵轴名称 |
| set_title | 图标题 |
| fig.tight_layout() | 自动调整布局，减少文字被遮挡 |
| fig.savefig(path, dpi=150) | 保存图片，扩展名决定格式；dpi 是分辨率参数 |
| plt.show() | 显示当前打开的图，脚本中通常等待窗口关闭 |
| plt.close(fig) | 关闭指定图并释放资源，已保存文件仍保留 |

只保存时可以 savefig 后立即 close；需要显示时应在 show 前保持图打开。
两张图推荐使用 fig1/ax1、fig2/ax2，再在 show 后分别 close。
当前代码覆盖 fig、ax 变量名不会覆盖已保存图片，两个图仍是不同图对象。
先用英文标题和坐标轴，避免中文字体配置打断练习。

## 7. 函数组织与程序入口

```python
def load_data(file_path):
    return pd.read_csv(file_path)

def main():
    df = load_data(input_path)
    clean_df = inspect_data(df)
    make_plots(clean_df, output_dir)

if __name__ == "__main__":
    main()
```

上面的 main 是调用顺序示意，input_path 和 output_dir 需要先按第 2 节定义。

- 参数接收调用者传入的数据；函数中和调用处的变量名不必一致。
- return 把结果交给调用者；只有 print 不会把数据返回。
- 没有 return 的函数默认返回 None；绘图函数可以只负责生成文件。
- 定义函数不会自动执行，需要调用。
- 三引号文本是函数说明；pass 仅占位，不执行实际处理。
- 入口判断使直接运行文件时调用 main，被其他脚本导入时不自动运行整条流程。
- f"样本数量: {df.shape[0]}" 是 f-string，把表达式结果插入字符串。
- print("-" * 40) 是把短横线重复 40 次，用来分隔终端输出。

当前脚本分工：load_data 返回原表；inspect_data 打印原始统计并返回去重表；make_plots 使用去重表绘图。

## 8. 本周复盘与后续补充

1. 当前 analyze_data.py 已创建输出目录，并分别保存、显示两张图。
2. missing_labels 和 missing_lengths 已计算，建议打印，明确图中排除了多少缺失值。
3. 当前 inspect_data 打印的是去重前标签分布，建议增加去重后数量，并用 dropna=False 报告缺失标签。
4. shape[1] 是“列数”，本例包含 ID、项目和标签，全部称为“模型特征数量”不够准确。
5. practice.py 的 Day 3 注释示例使用 df，但文件实际变量是 df1、df2；取消注释前需改成正确变量名。
6. clean_df.csv 和 clean_sample_practice.csv 都是去重结果，分别由两个练习产生，可在后续整理时统一输出位置。
7. 本周计划还包含 paper_notes.md：记录论文任务、输入输出、数据、方法、实验和不理解的问题，代码练习不能替代论文阅读。
8. 运行脚本会覆盖同名结果文件；原始 CSV 应继续保留，不要把缺失标签直接当作 0。

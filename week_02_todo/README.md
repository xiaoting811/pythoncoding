# 第二周：文件读写、JSON 与 CSV 数据处理

本周需要掌握：定位文件、选择读写模式、把 Python 数据保存与恢复、读取并校验 CSV、将处理步骤拆成函数，并在异常时作出清楚的处理。

本文根据当前目录代码与第二周任务整理。标为“建议”的示例用于补齐知识点，不表示现有脚本已经实现；待办程序的保存和加载扩展仍保存在第一周 `main.py` 中。

## 1. 文件与运行方式

| 文件 | 用途 |
|---|---|
| file-.py | 写入、追加、读取 notes.txt 的练习 |
| notes.txt | 学习记录文本 |
| practice_json.py | 将任务列表保存到 practice.json |
| practice.json | JSON 写入练习结果 |
| score_stats.py | 读取成绩、检查数值、计算个人总分与平均分、导出 |
| scores.csv | 原始成绩表，包含 name、python、math |
| summary.csv | 每个人的总分和平均分 |
| ../week_01_todo/main.py | 待办程序及 JSON 保存、加载扩展 |

在本目录终端运行：

```powershell
python file-.py
python practice_json.py
python score_stats.py
```

本周代码使用标准库，无需安装第三方包。`file-.py` 这个文件名可以直接运行，但短横线不适合常规 `import` 模块名；以后需要跨文件导入时，宜使用 `file_practice.py` 等名称。运行写入程序会覆盖对应结果，练习前区分原始数据和输出数据。

## 2. pathlib：文件到底在哪里

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "notes.txt"
```

| 写法 | 作用 |
|---|---|
| __file__ | 当前 Python 文件的路径 |
| Path(...) | 创建路径对象 |
| resolve() | 得到解析后的绝对路径 |
| parent | 取上一级目录，是属性，不加括号 |
| BASE_DIR / "notes.txt" | 在脚本所在目录拼接文件名 |
| path.exists() | 判断该路径是否存在 |

`Path` 和 `path` 不是同一个名称，大小写要一致。`Path(__file__).resolve().parent()` 多写一对括号会出错。

只写 `open("notes.txt")` 时，相对路径通常以当前工作目录为起点；它不一定等于脚本目录。以 `BASE_DIR` 拼接后，从其他工作目录启动脚本，也能定位同一个数据文件。拼接路径不会自动创建文件或文件夹。

```python
# 建议：需要输出目录时先创建
output_dir = BASE_DIR / "output"
output_dir.mkdir(parents=True, exist_ok=True)
```

`parents=True` 连同缺失的父目录创建；`exist_ok=True` 允许目录已经存在，不清空已有文件。

## 3. open、with 和读写模式

```python
with open(file_path, "w", encoding="utf-8") as file:
    file.write("今天学习文件\n")

with open(file_path, "a", encoding="utf-8") as file:
    file.write("明天学习 JSON\n")

with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

- `file_path` 决定打开哪个文件。
- `as file` 把打开后的文件对象交给变量 `file`；它与路径不是同一对象。
- `with` 管理文件资源，正常结束或出现异常时会关闭文件，但不会自动吞掉异常。
- `write()` 写字符串；`\n` 是换行符，不会因为调用多次 write 自动换行。
- `read()` 返回读取到的字符串，不会自动打印。

| 模式 | 已存在文件 | 不存在文件 |
|---|---|---|
| "r" | 读取，不修改内容 | 抛出 FileNotFoundError |
| "w" | 打开时清空原内容，再写入 | 创建文件，父目录需存在 |
| "a" | 在末尾追加 | 创建文件，父目录需存在 |

当前 `file-.py` 每次先用 `"w"` 写第一条，再用 `"a"` 追加。因此重跑会重新生成四条记录，而不是无限追加。注释“追加写入三条”不改变第一步实际使用 `"w"` 的行为。

### 编码与换行

`encoding="utf-8"` 明确文本编码，读写双方要匹配。`utf-8-sig` 是带 UTF-8 签名的编码，常用于让 Excel 更容易识别中文 CSV；它不是加密。

CSV 文本句柄建议使用 `newline=""`，把 CSV 的换行处理交给 csv 模块，避免 Windows 上出现多余空行。普通 TXT 练习不必机械增加这个参数。

## 4. JSON：把列表和字典保存下来

```python
import json

tasks = [
    {"id": 1, "title": "学习文件读写", "done": True},
    {"id": 2, "title": "学习 JSON", "done": False},
]

with open(BASE_DIR / "practice.json", "w", encoding="utf-8") as file:
    json.dump(tasks, file, ensure_ascii=False, indent=2)
```

| 参数或结果 | 含义 |
|---|---|
| tasks | 要保存的 Python 对象 |
| file | 已打开的输出文件对象 |
| ensure_ascii=False | 中文直接显示，不写成 \uXXXX 转义形式 |
| indent=2 | 每一级缩进两个空格，便于阅读 |
| Python 的 True / False / None | 保存为 JSON 的 true / false / null |

JSON 是文本格式，保存数据而不是保存正在运行的 Python 变量本身。适合此练习的列表、字典、字符串、数值、布尔值和 None；任意自定义对象不一定能直接保存。

### 读取 JSON

```python
with open(BASE_DIR / "practice.json", "r", encoding="utf-8") as file:
    loaded_tasks = json.load(file)

print(loaded_tasks[0]["title"])
```

`load()` 从文件读取并解析，返回 Python 对象。读取之后才能操作列表和字典；直接 `file.read()` 得到的只是字符串。

| 函数 | 输入与输出 |
|---|---|
| json.dump(obj, file) | Python 对象写入文件 |
| json.load(file) | 从文件解析为 Python 对象 |
| json.dumps(obj) | Python 对象转为 JSON 字符串，末尾 s 表示字符串方向 |
| json.loads(text) | JSON 字符串解析为 Python 对象 |

本周主要掌握 dump/load。不要对完整 JSON 文件反复用 `"a"` 追加多个列表；`[...][...]` 不是一个合法的 JSON 文档。

## 5. 保存与加载函数的职责

第一周待办程序中的扩展：

```python
def save_tasks(tasks, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)

def load_tasks(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
```

- 保存需要“已有任务列表”和“文件路径”两个参数。
- 加载只需要文件路径，从文件获取列表，并把它作为返回值交给调用者。
- `tasks = load_tasks(file_path)` 中等号左侧接收返回值。
- 当前 `practice_json.py` 只演示写入；上面的读取和恢复流程在待办程序中使用。

要区分不同异常：

| 情况 | 处理思路 |
|---|---|
| 第一次运行，任务文件不存在 | 可以返回空列表，开始新建任务 |
| 文件存在但不是合法 JSON | 提示格式问题并停止，保留原文件 |
| 保存时权限不足、目录不可用等 | 报告保存失败，说明内存修改未必已写入磁盘 |
| 合法 JSON 但不是预期任务结构 | 需要进一步检查类型、键与值；当前代码未完整实现 |

当前 main.py 在主函数中捕获 `json.JSONDecodeError`。不要把所有错误都当成“空列表”，否则之后保存可能覆盖原数据。

## 6. CSV DictReader：按表头读字典

原始表格示例：

```csv
name,python,math
张三,85,90
李四,78,88
```

```python
import csv

with open(BASE_DIR / "scores.csv", "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)
```

默认把第一行作为列名，后面每一行变成一个字典：

```python
{"name": "张三", "python": "85", "math": "90"}
```

`"85"` 是字符串，计算前需要转换：

```python
python_score = float(row["python"])
math_score = float(row["math"])
```

`float()` 允许小数；`float("abc")`、`float("")` 会抛出 `ValueError`。CSV 表头不含预期键时可能产生 `KeyError`；一行列数不足时也可能得到 None。当前脚本未覆盖全部结构错误，应先检查表头与记录完整性，而不是只依赖数值转换。

## 7. 数据校验、continue 与列表积累

```python
results = []
for row in reader:
    try:
        python_score = float(row["python"])
        math_score = float(row["math"])
    except ValueError:
        print("成绩不是有效数字")
        continue

    if 0 <= python_score <= 100 and 0 <= math_score <= 100:
        results.append({
            "name": row["name"],
            "python": python_score,
            "math": math_score,
        })
    else:
        print("成绩超出范围")
```

- 每次循环处理一条记录。
- 转换失败时 `continue` 跳过本行，后续学生仍继续处理。
- `0 <= score <= 100` 包含边界 0 和 100。
- `and` 要求两科都有效。
- 每条有效记录创建独立字典，再 append 到结果列表。
- `results` 要放在循环外初始化；若每轮重新赋值为空列表，前面的记录会丢失。

建议在提示中增加原始行号和姓名，方便定位问题。不要把无法识别的成绩直接改为 0，因为“缺失”和“真实零分”含义不同。

## 8. 总分、平均分与函数分工

当前 `score_stats.py` 的数据流：

```python
scores = load_scores(file_path)
summary = calculate_summary(scores)
save_summary(summary, BASE_DIR / "summary.csv")
```

| 函数 | 接收什么 | 交付什么 |
|---|---|---|
| load_scores | CSV 路径 | 有效成绩字典组成的列表 |
| calculate_summary | 有效成绩列表 | 姓名、总分、平均分的列表 |
| save_summary | 结果列表、输出路径 | 写入结果文件，当前默认返回 None |

```python
total = record["python"] + record["math"]
average = total / 2
```

两科总分除以 2 得到个人平均分，不是除以学生人数。输入列表与结果列表职责不同，不要因变量都叫 results 就认为是同一个列表。

### 建议补齐：班级统计与空数据

原任务还要求班级每科平均分、Python 最高分和及格人数，当前脚本尚未实现。可先理解：

```python
if not scores:
    print("没有有效成绩，无法统计班级结果")
else:
    python_values = [record["python"] for record in scores]
    class_average = sum(python_values) / len(python_values)
    highest = max(python_values)
    passed = sum(score >= 60 for score in python_values)
```

先检查非空，避免除以 0 或对空序列求 max。最后一行把满足条件的 True 按 1 累加，计算及格人数；及格边界包含 60 分。

## 9. DictWriter：按指定列输出

```python
with open(BASE_DIR / "summary.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "total", "average"])
    writer.writeheader()
    writer.writerows(summary)
```

- `fieldnames` 指定输出列名和顺序。
- `writeheader()` 写表头，不会自动写数据。
- `writerow(record)` 写一个字典；`writerows(records)` 写多条字典。
- 默认情况下，字典出现未列入 fieldnames 的额外键会报错；输出前核对数据结构。
- 传入 csv writer 的是已打开文件对象，不是只传路径。
- 当前代码使用 `utf-8`；需要方便 Excel 识别中文时可考虑 `utf-8-sig`，但应在打开文件时统一选择。
- 写入 summary.csv 不会修改输入 scores.csv。

## 10. 异常与程序入口

```python
if __name__ == "__main__":
    try:
        scores = load_scores(file_path)
        summary = calculate_summary(scores)
        save_summary(summary, BASE_DIR / "summary.csv")
    except OSError as error:
        print(f"文件操作错误：{error}")
```

当前脚本捕获 `OSError` 但未显示异常详情，上例是建议写法。`FileNotFoundError` 属于 OSError 的子类；数字转换错误 ValueError、表头缺失 KeyError 则不属于 OSError，需要按实际职责处理。

`except` 只处理对应异常；异常处理结束后，程序通常会继续执行后面的语句，除非明确 return、重新抛出异常或退出。因此不要在读取失败后继续使用尚未创建的变量。

## 11. 核对结果与本周自查

若使用原计划的四个学生：张三 85/90、李四 78/88、王五 92/95、赵六 60/70，应得到：

| 学生 | 总分 | 平均分 |
|---|---:|---:|
| 张三 | 175 | 87.5 |
| 李四 | 166 | 83 |
| 王五 | 187 | 93.5 |
| 赵六 | 130 | 65 |

班级统计建议结果：Python 平均分 78.75、数学平均分 85.75、Python 最高分 92、Python 及格人数 4。数据变化后结果也要重新计算，不能套用答案。

- [ ] 能解释 Path、resolve()、parent 和路径拼接。
- [ ] 能说明 r、w、a 对已有文件的区别。
- [ ] 能用 with 写入、追加、读取中文文本。
- [ ] 能解释 JSON dump/load 的参数与返回结果。
- [ ] 能区分文件不存在、JSON 损坏、结构错误和保存失败。
- [ ] 知道 CSV 读取的数值通常是字符串，需转换后计算。
- [ ] 能校验成绩范围并跳过错误记录，保留原始数据。
- [ ] 能解释个人平均分与全班平均分的不同分母。
- [ ] 能在没有有效记录时停止班级统计。
- [ ] 能说明 DictWriter、fieldnames、writeheader、writerows、newline。
- [ ] 能独立组织“读取、检查、计算、保存”的处理流程。

当前代码已实现文件读写、JSON 写入、个人成绩处理及导出；班级统计、错误行号提示、完整表头与记录检查仍是需要补齐的学习项。待办持久化在第一周项目继续维护，无需在本目录复制另一份主程序。

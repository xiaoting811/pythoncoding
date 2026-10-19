# Python 学习记录

按周整理的 Python 练习。前两周使用 Python 标准库，第三周增加 NumPy、Pandas 和 Matplotlib。

## 第一周：命令行待办事项

目录：`week_01_todo`

添加、查看、完成和删除任务，使用 JSON 保存数据。

运行：`python week_01_todo/main.py`

## 第二周：文件读写与成绩统计

目录：`week_02_todo`

练习文本读写、JSON 保存、CSV 读取、成绩范围检查，以及总分和平均分导出。

运行：`python week_02_todo/score_stats.py`

输入为该目录下的 `scores.csv`，输出为 `summary.csv`。

各周目录中的 README.md 保留学习笔记。
## 第三周：NumPy、Pandas 与数据可视化

目录：`week_03_todo`

数组运算、表格筛选、缺失值与重复数据检查、标签数量柱状图和代码长度直方图。

依赖安装：`python -m pip install numpy pandas matplotlib`

运行：`python week_03_todo/analyze_data.py`

输入为 `data/sample_practice.csv`，属于人工构造的练习数据；两张统计图保存在 `output` 中。
详细用法和示例见 [第三周学习笔记](week_03_todo/README.md)。

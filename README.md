# Python 学习记录

按周整理的 Python 与 AI 基础学习记录。前两周练习 Python 标准库，第三周学习 NumPy、Pandas 和 Matplotlib，第四周学习二分类检测指标与批量评测。

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

## 第四周：检测指标与批量评测

目录：`week_04_todo`

练习混淆矩阵、Precision、Recall、F1、Accuracy、零分母处理，以及预测文件的字段、标签和样本编号检查。

运行指标练习：`python week_04_todo/practice.py`

运行 CSV 评测：`python week_04_todo/evaluate_predictions.py`

输入为 `data/predictions_practices.csv`，汇总指标保存在 `output/metrics.json`，误判样本保存在 `output/error_samples.csv`。数据用于学习练习，不代表真实漏洞检测效果。

各周 README.md 已按需要掌握的知识点整理，包含示例、易错点和自查内容。

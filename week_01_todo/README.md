# 命令行待办事项程序

## 功能
- 添加任务
- 查看任务
- 标记任务完成
- 删除任务

## 运行方式
python main.py

## 数据结构
使用列表存放任务，每个任务包含 id、title、done。

## 当前限制
任务保存在内存中，关闭程序后不会保留。

## 遇到的问题
with open :
    "w"  重新创建写入
    "a"  追加写入

# 导包 import json
# 把python数据写入以json的形式写入文件
json.dump(tasks,file,ensure_ascii=False,indent=2)   
ensure_ascii=False  # 让中文直接显示
indent=2 # 缩进

# 从打开的文件中读取数据 并转换成python形式
tasks = json.load(file) 

from pathlib import path
BASE_DIR = Path(__file__).resolve().parent()



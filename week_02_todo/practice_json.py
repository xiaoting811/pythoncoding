

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "practice.json"


tasks = [
    {"id": 1, "title": "学习文件读写", "done": True},
    {"id": 2, "title": "学习 JSON", "done": False},
]

# 将 tasks 列表写入 practice.json 文件
with open(file_path,"w",encoding="utf-8") as file:
    # ensure_ascii=False 保留中文
    # indent=2 缩进
    json.dump(tasks,file,ensure_ascii=False,indent=2)
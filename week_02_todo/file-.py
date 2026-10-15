from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "notes.txt"

# 1. 追加写入三条学习记录
with open(file_path,"w",encoding="utf-8") as file:
    file.write("今天学习读")

with open(file_path,"a",encoding="utf-8") as file:
    file.write("\n今天学习写")

with open(file_path,"a",encoding="utf-8") as file:
    file.write("\n今天学习玩")

# 2. 追加第四条
with open(file_path,"a",encoding="utf-8") as file:
    file.write("\n明天学习json")

# 3. 读取并打印
with open(file_path,"r",encoding="utf-8") as file:
    print(file.read())

# 4. 再次使用w 观察原内容的变化
# with open(file_path,"w",encoding="utf-8") as file:
#     file.write("第二次写入")




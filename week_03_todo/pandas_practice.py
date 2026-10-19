from pathlib import Path
import pandas as pd

BASEDIR = Path(__file__).resolve().parent
file_path = BASEDIR / "scores.csv"

df = pd.read_csv(file_path)

# 1. 只显示姓名和数学成绩
print(df[["name","math"]])
print('-'*40)

# 2. 筛选python成绩不低于80的学生
print(df[df["python"] >= 80])
print('-'*40)

# 3.增加total和average两列
df["total"] = df["python"] + df["math"]
df["average"] = df["total"] / 2
# 不会修改csv文件
print(df)


# 创建输出文件夹
output_dir = BASEDIR / "output"
output_dir.mkdir(parents=True,exist_ok=True)

output_path = output_dir / "score_analysis.csv"
# index = False 不会把左侧的索引列写入csv文件
df.to_csv(output_path,index=False,encoding="utf-8-sig")



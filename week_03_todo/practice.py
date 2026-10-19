from pathlib import Path
import pandas as pd

BASEDIR = Path(__file__).resolve().parent
file_path = BASEDIR/"scores.csv"
file_path2 = BASEDIR/"data"/"sample_practice.csv"

df1 = pd.read_csv(file_path)
df2 = pd.read_csv(file_path2)

# day3 练习
# print(df.head())      # 默认前五行数据
# print(df.shape)      # 数据形状
# print(df.columns)    # 列名
# print(df.dtypes)     # 列数据类型

# day4 练习
# # 1. 统计每列缺失值数量
# print(df2.isnull().sum())
# print('-'*40)
# # 2. 统计多余的重复行
# print(df2.duplicated().sum())
# print('-'*40)
# # 3.去掉重复行
# clean_df = df2.drop_duplicates()
# print(clean_df.duplicated().sum())
# print('-'*40)
# # 4. 筛选缺失数据的记录
# print(clean_df[clean_df["label"].isnull()])
# print('-'*40)
# # 5.统计标签列表中 每种值出现了多少次  dropna=False 表示：缺失值也统计进去
# print(clean_df["label"].value_counts(dropna=False))

# day4 核验
# 1. 统计原始的行数
print(df2.shape[0])
print('-'*40)

# 2.找出重复行 并保存一份重复记录
df2_duplicated = df2[df2.duplicated()]
print('-'*40)

# 3. 去掉重复行得到应该新的DataFrame
file_path3 = BASEDIR/"data"/"clean_df.csv"
output_df = df2.drop_duplicates()
output_df.to_csv(file_path3, index=False)
print('-'*40)

# 4.缺失的“label”记录
print(output_df[output_df["label"].isnull()])
print('-'*40)

# 5.缺失的codeline记录
print(output_df[output_df["code_lines"].isnull()])
print('-'*40)

# 6.统计去重后的标签分布和项目分布
print(output_df["label"].value_counts(dropna=False))
print('-'*40)
print(output_df["project"].value_counts(dropna=False))

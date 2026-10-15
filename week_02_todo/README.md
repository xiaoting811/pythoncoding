# import csv
# 它默认把第一行表头作为字典的键 后续每行作为具体的值
reader = csv.DictReader(file)

writer = csv.DictWriter(
    file,
    fieldnames=["name","total","average"]   # 指定字典中要使用的键 以及顺序
)
writer.writeheader()        # 写入表头
writer.writerows(records)   # 把字典逐行写入
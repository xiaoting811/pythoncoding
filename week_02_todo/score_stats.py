import csv
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "scores.csv"

# results = []

# day4
# with open(file_path,"r",encoding="utf-8") as file:
#     # 把每一行变成字典
#     reader = csv.DictReader(file)
#     for row in reader:
#         row["python"]=float(row["python"])
#         row["math"]=float(row["math"])
#         print(f'{row["name"]}的总分为{row["python"] + row["math"]:.2f}，平均分为{(row["python"] + row["math"]) / 2:.2f}')
#         # 存入列表
#         result = {
#             "name": row["name"],
#             "python": row["python"],
#             "math": row["math"],
#             "total": row["python"] + row["math"],
#             "average": (row["python"] + row["math"]) / 2
#         }
#         results.append(result)
#     print(results)

# day5
# 加载数据
def load_scores(file_path):
    results = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row["python"] = float(row["python"])
                row["math"] = float(row["math"])
            except ValueError:
                print("数据的输入有问题")
                continue
            if (0<=row["python"]<=100 and 0<=row["math"]<=100):
                result = {
                    "name": row["name"],
                    "python": row["python"],
                    "math": row["math"],
                }
                results.append(result)
            else:
                print("数据的输入超出范围")
        return results

# 计算每个人的总分和平均分
def calculate_summary(records):
    results = []
    for record in records:
        total_score = record["python"] + record["math"]
        average_score = total_score / 2
        result = {
            "name": record["name"],
            "total": total_score,
            "average": average_score
        }
        results.append(result)
    return results


# 导出每个人的总分和平均分
def save_summary(records,file_path):
    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "total", "average"]
        )
        writer.writeheader()
        writer.writerows(records)

if __name__ == "__main__":
    try:
        scores = load_scores(file_path)
        summary = calculate_summary(scores)
        save_summary(summary, BASE_DIR / "summary.csv")
    except OSError:
        print("文件操作错误")


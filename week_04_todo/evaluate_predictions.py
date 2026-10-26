from pathlib import Path
import json
import pandas as pd
# 调用之前写过的方法
from practice import confusion_counts,calculate_metrics

# 检查输入文件是否符合要求
def check(input_file):
    df = pd.read_csv(input_file)
    required_columns = {"sample_id","y_true","y_pred"}
    missing_columns = required_columns - set(df.columns)
    # 如果存在缺失的列，则抛出异常
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")
    if  df.empty:
        raise ValueError("没有样本数据")
    # 检查样本ID是否存在重复
    if df["sample_id"].duplicated().any():
        raise ValueError("存在重复的样本ID")
    # 检查样本ID是否存在空值
    if df["sample_id"].isnull().any():
        raise ValueError("存在空值的样本ID")
    # 检查y_true和y_pred列是否存在空值或标签不为0或1的样本
    for column in df[["y_true","y_pred"]]:
        if df[column].isnull().any():
            raise ValueError(f"存在空值")
        if not df[column].isin([0,1]).all():
            raise ValueError(f"存在标签不为0或者1的样本")

    # 返回包含y_true和y_pred列的DataFrame
    return df["y_true"],df["y_pred"]


if __name__ == "__main__":
    BASEDIR = Path(__file__).resolve().parent
    INPUT =  BASEDIR / "data" / "predictions_practices.csv"
    OUTPUT = BASEDIR/"output"
    OUTPUT.mkdir(exist_ok=True)
    try :
        y_true,y_pred = check(INPUT)
    except (FileNotFoundError, ValueError):
        print("输入文件不存在")
        raise SystemExit(1)
    confusion_matrix = confusion_counts(y_true,y_pred)
    metrics = calculate_metrics(confusion_matrix)
    result = {
              "sample_count":len(y_true),
              "confusion_matrix":confusion_matrix,
              "metrics":metrics
              }
    with open(OUTPUT/"metrics.json","w",encoding="utf-8") as file:
        json.dump(result,file,ensure_ascii=False,indent=2)
    # 保存错误样本
    df = pd.read_csv(INPUT)
    error_samples = df[y_true != y_pred]
    error_samples.to_csv(
        OUTPUT / "error_samples.csv",
        index=False,
        encoding="utf-8-sig"
    )



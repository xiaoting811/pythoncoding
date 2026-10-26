
def confusion_counts(y_true,y_pred):
    counts = {"tp":0,"fp":0,"tn":0,"fn":0}
    if len(y_true) != len(y_pred):
        raise ValueError("真实列表和预测列表长度不相同")
    if len(y_true) == 0:
        raise ValueError("列表为空")
    # 增加标签检查
    for label in y_true:
        if label != 0 and label != 1:
            raise ValueError("标签必须是0或1")
    for label in y_pred:
        if label != 0 and label != 1:
            raise ValueError("标签必须是0或1")

    for i in range(len(y_true)):
        if (y_true[i]==1) and (y_pred[i] ==1):
            counts["tp"] += 1
        elif (y_true[i]==0) and (y_pred[i] ==1):
            counts["fp"] += 1
        elif (y_true[i]==0) and (y_pred[i] ==0):
            counts["tn"] += 1
        elif (y_true[i]==1) and (y_pred[i] ==0):
            counts["fn"] += 1
    return counts


def safe_division(numerator, denominator):
    if denominator == 0:
        return 0.0
    else:
        return numerator / denominator

# 计算 precision, recall, f1, accuracy
def calculate_metrics(counts):
    total = counts["tp"] + counts["fp"] + counts["tn"] + counts["fn"]
    if total == 0:
        raise ValueError("总样本数为0")
    if (counts["tp"] + counts["fp"]) == 0:
        print("Precision的分母为0")
        precision = 0.0
    else :
        precision = safe_division(counts["tp"], (counts["tp"] + counts["fp"]))

    if (counts["tp"] + counts["fn"]) == 0:
        print("Recall的分母为0")
        Recall = 0.0
    else :
        Recall = safe_division(counts["tp"], (counts["tp"] + counts["fn"]))

    if (counts["tp"] * 2 + counts["fp"] + counts["fn"]) == 0:
        print("F1的分母为0")
        F1 = 0.0
    else :
        F1 = safe_division((counts["tp"] * 2), (counts["tp"] * 2 + counts["fp"] + counts["fn"]))

    Accuracy = safe_division((counts["tp"] + counts["tn"]), total)

    return {"precision": precision, "recall": Recall, "f1": F1, "accuracy": Accuracy}

if __name__ == "__main__":
    y_true = [1, 1, 0, 0, 1, 0, 0, 0, 1, 0]
    y_pred = [1, 0, 0, 1, 1, 0, 0, 1, 1, 0]

    result = confusion_counts(y_true,y_pred)
    metrics = calculate_metrics(result)

    # metrics.items() 提供字典中的每一组“键和值”。循环时，分别交给 name 和 value：
    for name, value in metrics.items():
        print(f"{name}: {value:.4f}")


from os import name
from pathlib import Path
import csv
from metrics import confusion_counts,calculate_metrics

BASEDIR = Path(__file__).resolve().parent
RUNS = {"lr_010","lr_001"}

def read_csv(path):
    with open(path,"r",encoding="utf-8",newline="") as file:
        return [r for r in csv.DictReader(file)]

def analyze_results(name,val):
    folder = BASEDIR / "output" / name
    rows = read_csv(folder/"val_predictions.csv")
    ids = [r["sample_id"] for r in rows]
    if len(ids) != len(set(ids)) or  set(ids) != set(val):
        raise ValueError("Validation IDs do not match")
    y_true = [int(r["y_true"]) for r in rows]
    y_pred = [int(r["y_pred"]) for r in rows]
    for r in rows:
        if int(r["y_true"]) != int(val[r["sample_id"]]["label"]):
            raise ValueError("Validation labels do not match")
    counts = confusion_counts(y_true,y_pred)
    scores = calculate_metrics(counts)
    last = read_csv(folder/"history.csv")[-1]
    assert abs(scores["accuracy"] - float(last["val_acc"])) < 1e-9
    summary = {"run":name,"sample_count":len(rows),**counts,**scores,
               "val_loss":float(last["val_loss"])}
    errors = []
    for r ,actual,predicted in zip(rows,y_true,y_pred):
        if actual != predicted:
            errors.append({"sample_id":r["sample_id"],
                          "y_true":actual,
                          "y_pred":predicted,
                          "error_type":"FP" if actual == 0 else "FN"})
    return summary ,errors

if __name__ == "__main__":
    data = read_csv(BASEDIR/"data" / "samples.csv")
    val_rows = [r for r in data if r["split"] == "val"]
    val = {r["sample_id"]:r for r in val_rows}
    assert len(val) == len(val_rows) == 40
    summaries = []
    errors = []
    for name in RUNS:
        summary ,error = analyze_results(name,val)
        summaries.append(summary)
        errors.extend(error)
        print(summary)
    out = BASEDIR / "output"
    jobs = [("comparison.csv",summaries,list(summaries[0])),
            ("errors.csv",errors,["run","sample_id","y_true","y_pred","error_type","x1","x2"])]
    for filename,rows,fields in jobs:
        with open (out/filename,"w",encoding="utf-8",newline="") as file:
            writer = csv.DictWriter(file,fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)



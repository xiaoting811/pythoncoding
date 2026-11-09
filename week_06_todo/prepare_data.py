import torch
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent

def make_row():
    a = torch.linspace(-0.95,0.95,20)
    b = torch.linspace(-0.9,0.9,10)
    x = torch.cartesian_prod(a,b)
    y = (x.sum(dim=1)>0).long()
    # 创建一个随机数生成器 随机种子为42
    g = torch.Generator().manual_seed(42)
    train_ids = set()
    for label in (0,1):
        ids = torch.where(y == label)[0]
        # torch.randperm(n) 生成 0～n-1 的随机排列，每个数字恰好出现一次。
        order = torch.randperm(len(ids),generator=g)
        train_ids.update(ids[order[:80]].tolist())
    rows = []
    for i in range(len(x)):
        rows.append(
            {
                "sample_id":f"s{i:03d}",
                "x1": x[i,0].item(),
                "x2": x[i,1].item(),
                "label": y[i].item(),
                "split": "train" if i in train_ids else "val"
            }
        )
    return rows

if __name__ == "__main__":
    rows = make_row()
    BASEDIR = Path(__file__).resolve().parent
    folder = BASEDIR/"data"
    folder.mkdir(parents=True,exist_ok=True)
    with open(folder/"samples.csv","w",newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for split in ("train","val"):
        labels = [r["label"] for r in rows if r["split"] == split ]
        print(split,len(labels),labels.count(0),labels.count(1))
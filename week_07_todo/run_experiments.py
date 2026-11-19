from csv import DictWriter
from pathlib import Path
import csv
import json
import hashlib
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import ToyDataset
from model import SmallMLP
from train_classifier import  train_one_epoch,evaluate


BASEDIR = Path(__file__).resolve().parent
RUNS = {"lr_010":0.1,"lr_001":0.01}

def write_csv(path,rows):
    if not rows:
        raise ValueError("rows cannot be empty")
    with open (path,"w",newline="",encoding="utf-8") as file:
        writer = csv.DictWriter(file,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def run_one(name,lr):
    torch.manual_seed(44)
    train_ds = ToyDataset("train")
    val_ds = ToyDataset("val")
    train_loader = DataLoader(train_ds,batch_size=16,shuffle=True,num_workers=0,
                              generator=torch.Generator().manual_seed(43))
    train_eval_loader = DataLoader(train_ds,batch_size=16,shuffle=False,num_workers=0)
    val_loader = DataLoader(val_ds,batch_size=16,shuffle=False,num_workers=0)
    model = SmallMLP()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(),lr=lr)
    initial_loss , initial_accuracy , predictions = evaluate(model,val_loader,loss_fn)
    history = []
    for epoch in range(1,61):
        online_loss = train_one_epoch(model,train_loader,loss_fn,optimizer)
        train_loss,_,_ = evaluate(model,train_eval_loader,loss_fn)
        val_loss,val_acc,predictions = evaluate(model,val_loader,loss_fn)
        history.append({"epoch":epoch,
                        "train_loss":train_loss,
                        "val_loss":val_loss,
                        "val_acc":val_acc,
                        "online_loss":online_loss})
    save_run(name,lr,history,val_ds,predictions,initial_loss)
    print(name,history[-1])

def save_run(name,lr,history,val_ds,predictions,initial_loss):
    out = BASEDIR / "output" /name
    out.mkdir(parents=True,exist_ok=True)
    write_csv(out / "history.csv",history)
    assert  len(predictions) == len(val_ds)
    rows = [{"sample_id":row["sample_id"],
             "y_true": int(row["label"]),
             "y_pred": pred} for row , pred in zip(val_ds.rows,predictions)]
    write_csv(out/"val_predictions.csv",rows)
    data_hash = hashlib.sha256((BASEDIR/"data/samples.csv").read_bytes()).hexdigest()
    config = {
        "lr":lr,"epochs":60,"batch_size":16,
        "loader_seed":43,"model_seed":44,
        "model":"2-8-2 ReLU","optimizer":"SGD",
        "loss":"CrossEntropyLoss","device":"cpu",
        "train_count":160,"val_count":40,
        "data_sha256":data_hash,
        "initial_val_loss":initial_loss,
        "python":sys.version,"torch":torch.__version__
    }
    with open(out/"config.json","w",encoding="utf-8") as f:
        json.dump(config,f,ensure_ascii=False,indent=2)

if __name__ == "__main__":
    for name,lr in RUNS.items():
        run_one(name,lr)

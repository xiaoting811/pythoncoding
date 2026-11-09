import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import ToyDataset
from model import SmallMLP
from pathlib import Path
import csv
import json
import sys

def write_csv(path,rows):
    with open(path,"w",newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def export_results(history,val_ds,predictions,config):
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(parents=True,exist_ok=True)
    write_csv(out / "history.csv",history)
    assert len(predictions) == len(val_ds)
    rows = []
    for row , pred in zip(val_ds.rows,predictions):
        rows.append({"sample_id":row["sample_id"],
                     "y_true": int(row["label"]),
                     "y_pred": pred})
    write_csv(out / "val_predictions.csv",rows)
    with open(out / "config.json","w") as f:
        json.dump(config,f)



def train_one_epoch(model,loader,loss_fn,optimizer):
    model.train()
    total_loss = 0.0
    count = 0
    for xb,yb in loader:
        optimizer.zero_grad()
        logits = model(xb)
        loss = loss_fn(logits,yb)
        loss.backward()
        optimizer.step()
        n = len(yb)
        total_loss = total_loss + loss.item()*n
        count += n
    return total_loss / count

def evaluate(model,loader,loss_fn):
    model.eval()
    total_loss = 0.0
    correct = 0
    count = 0
    predictions = []
    with torch.no_grad():
        for xb,yb in loader:
            logits = model(xb)
            loss = loss_fn(logits,yb)
            pred = logits.argmax(dim=1)
            n = len(yb)
            total_loss = total_loss + loss.item()*n
            correct += (pred == yb).sum().item()
            count += n
            predictions.extend(pred.tolist())
    return total_loss / count, correct / count, predictions


if __name__ == "__main__":
    torch.manual_seed(44)
    train_ds = ToyDataset("train")
    val_ds = ToyDataset("val")
    train_loader = DataLoader(train_ds,batch_size=16,shuffle=True,num_workers=0,
                              generator=torch.Generator().manual_seed(43))
    val_loader = DataLoader(val_ds,batch_size=16,shuffle=False,num_workers=0,)
    model = SmallMLP()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(),lr=0.1)
    initial_loss , initial_accuracy, predictions = evaluate(model,val_loader,loss_fn)
    print("initial loss:",initial_loss,"initial accuracy:",initial_accuracy)
    history = []
    for epoch in range(1,61):
        train_loss = train_one_epoch(model,train_loader,loss_fn,optimizer)
        val_loss, val_accuracy, predictions = evaluate(model,val_loader,loss_fn)
        history.append({"epoch":epoch,"train_loss":train_loss,"val_loss":val_loss,"val_accuracy":val_accuracy})
        if epoch==1 or epoch%10==0:
            print(f"epoch:{epoch}, train_loss:{train_loss}, val_loss:{val_loss}, val_accuracy:{val_accuracy}")
    config = {
        "data_seed":42,"loader_seed":43,"model_seed":44,
        "batch_size":16,"epochs":60,"lr":0.1,
        "train_count":len(train_ds),"val_count":len(val_ds),
        "device":"cpu","model":"2-8-2 ReLU",
        "loss":"CrossEntropyloss","optimizer":"SGD",
        "python":sys.version,"torch":torch.__version__
    }
    export_results(history, val_ds, predictions, config)




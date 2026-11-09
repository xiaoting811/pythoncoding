import csv
import  torch
from torch.utils.data import Dataset
from pathlib import Path


BASEDIR = Path(__file__).resolve().parent

class ToyDataset(Dataset):
    def __init__(self,split):
        if split not in ("train","val"):
            raise ValueError("split must be train or val")
        with open (BASEDIR/"data/samples.csv",newline="",encoding="utf-8") as file:
            self.rows = [r for r in csv.DictReader(file) if r ["split"] == split]
        self.x = torch.tensor([[float(r["x1"]),float(r["x2"])] for r in self.rows],dtype=torch.float32)
        self.y = torch.tensor([int(r["label"]) for r in self.rows],dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self,index):
        return self.x[index],self.y[index]

if __name__ == "__main__":
    from torch.utils.data import DataLoader
    ds = ToyDataset("train")
    print(ds.rows)
    loader = DataLoader(ds,batch_size=16,shuffle=False,num_workers=2)
    xb, yb = next(iter(loader))
    print(len(ds),len(loader),ds[0])
    print(xb.shape,yb.shape,xb.dtype,yb.dtype)
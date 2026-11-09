import torch
from torch import nn

class SmallMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2,8),
            nn.ReLU(),
            nn.Linear(8,2),
        )
    def forward(self,x):
        return self.net(x)

if __name__ == "__main__":
    torch.manual_seed(44)
    model = SmallMLP()
    xb = torch.zeros(4,2)
    yb = torch.tensor([0,1,0,1],dtype=torch.long)
    logits = model(xb)
    loss = nn.CrossEntropyLoss()(logits,yb)
    print(logits.shape,loss.item())
    print(logits)
    # argmax 找出每行最大值所在的位置
    print(logits.argmax(dim=1))
    print(sum(p.numel() for p in model.parameters()))
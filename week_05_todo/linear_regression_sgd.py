import torch

def train(lr ,epochs):
    x = torch.arange(5,dtype=torch.float32).reshape(-1,1)
    w = torch.tensor(0.0,requires_grad=True)
    b = torch.tensor(0.0,requires_grad=True)
    y_true = 2 * x + 1
    optimizer = torch.optim.SGD([w,b],lr=lr)
    losses = []
    for epoch in range(epochs):
        optimizer.zero_grad()
        y_pred = w * x + b
        loss = (y_true - y_pred).pow(2).mean()
        losses.append(loss.item())
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        final_loss = ((w*x+b-y_true)**2).mean().item()
    return {"w":w.item(),"b":b.item(),"losses":losses,"final_loss":final_loss}

if __name__ == "__main__":
    result = train(0.05,500)
    print(result["final_loss"],result["w"],result["b"])

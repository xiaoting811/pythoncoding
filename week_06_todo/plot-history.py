from pathlib import Path
import csv
import matplotlib.pyplot as plt


BASEDIR = Path(__file__).resolve().parent

if  __name__ == "__main__":
    out = BASEDIR / "output"
    with open(out / "history.csv", "r",encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    epochs  = [int(row["epoch"]) for row in rows]
    train_loss = [float(row["train_loss"]) for row in rows]
    val_loss = [float(row["val_loss"]) for row in rows]
    plt.plot(epochs, train_loss, label="train online loss")
    plt.plot(epochs, val_loss, label="validation loss")
    plt.xlabel("epochs")
    plt.ylabel("cross entropy loss")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "loss_curve.png",dpi = 150)
    plt.close()
    print(out/"loss_curve.png")

from pathlib import Path
import csv
import matplotlib.pyplot as plt

BASEDIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    out = BASEDIR/"output"
    for name in ("lr_010","lr_001"):
        with open(out/name/"history.csv",encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
            epochs = [int(row["epoch"]) for row in rows]
            plt.plot(epochs,[float(row["train_loss"]) for row in rows],
                     label = name + " train eval")
            plt.plot(epochs,[float(row["val_loss"]) for row in rows],
                     linestyle="--",label = name + " val eval")
    plt.xlabel("epoch")
    plt.ylabel("cross entropy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/"loss_comparison.png",dpi=150)
    plt.close()

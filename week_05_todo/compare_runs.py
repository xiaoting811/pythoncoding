from pathlib import Path
import csv
import matplotlib.pyplot as plt
from linear_regression_day5 import train as train_manual
from linear_regression_sgd import train as train_sgd

if __name__ == "__main__":
    out = Path(__file__).resolve().parent/"output"
    out.mkdir(parents=True,exist_ok=True)
    runs = {"manual_005":train_manual(0.05,300),
            "sgd_005":train_sgd(0.05,300),
            "sgd_001":train_sgd(0.01,300)
            }
    for name ,result in runs.items():
        print(name,result["w"],result["b"],result["final_loss"])
        # 画出某次变化的损失曲线变化 横轴是轮次 纵轴是损失
        plt.plot(range(300),result["losses"],label=name)
    with open(out/"loss_comparison.csv","w",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["epoch",*runs.keys()])
        for epoch in range(300):
            writer.writerow([epoch] + [r["losses"][epoch] for r in runs.values()])
    plt.xlabel("epoch(loss before update)")
    plt.ylabel("MSE")
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/"loss_comparison.png",dpi=150)
    plt.show()
    plt.close()
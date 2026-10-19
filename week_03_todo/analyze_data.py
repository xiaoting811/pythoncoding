import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt



def load_data(file_path):
    """读取数据。"""
    return pd.read_csv(file_path)

def inspect_data(df):
    """统计样本、缺失值、重复与标签分布。"""
    print(f"样本数量: {df.shape[0]}")
    print(f"特征数量: {df.shape[1]}")
    print(f"缺失值: {df.isnull().sum().sum()}")
    print(f"重复值: {df.duplicated().sum()}")
    print(f"标签分布: {df['label'].value_counts()}")
    df2 = df.drop_duplicates()
    return df2


def make_plots(df, output_dir):
    """生成统计图。"""
    # 1. 第一张图需要的数据
    label_counts = df['label'].value_counts()
    label_counts = label_counts.reindex(index=[0, 1],fill_value=0)
    # 1.1缺失标签单独统计
    missing_labels = df['label'].isnull().sum()

    # 2. 第二张图需要的数据
    lengths = df["code_lines"].dropna()
    # 2.1 缺失的行单独统计
    missing_lengths = df["code_lines"].isnull().sum()

    # 3. 创建画布和坐标区域
    fig, ax = plt.subplots()

    # 4. 柱状图
    ax.bar(["0", "1"], label_counts.to_numpy())
    ax.set_xlabel("Label")
    ax.set_ylabel("Sample Count")
    ax.set_title("Label Distribution")

    fig.tight_layout()
    fig.savefig(output_dir / "label_distribution.png",dpi=150)



    # 5. 直方图
    fig,ax = plt.subplots()
    ax.hist(lengths, bins=5,edgecolor = 'black')
    ax.set_xlabel("Code Length(lines)")
    ax.set_ylabel("Sample Count")
    ax.set_title("Code Length Distribution")

    fig.tight_layout()
    fig.savefig(output_dir / "code_length_distribution.png", dpi=150)

    plt.show()




def main():
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / "data"
    # 确定输入和输出路径
    input_path = Path(__file__).resolve().parent / "data" / "sample_practice.csv"
    output_path = Path(__file__).resolve().parent / "output"
    output_path.mkdir(parents=True, exist_ok=True)
    # 读取数据
    df = load_data(input_path)
    # 检查数据
    clean_df = inspect_data(df)
    # 将去重结果保存到输入路径
    clean_df.to_csv(file_path/"clean_sample_practice.csv", index=False, encoding='utf-8-sig')
    # 生成图表
    make_plots(clean_df, output_path)


if __name__ == "__main__":
    main()


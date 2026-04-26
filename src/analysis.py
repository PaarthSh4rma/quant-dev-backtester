from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from config import DATA_DIR


INPUT_FILE = DATA_DIR / "multi_asset_parameter_sweep.csv"
PLOTS_DIR = Path("plots/analysis")
PLOTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_csv(INPUT_FILE)
    return df


# ---------------------------
# 1. Heatmap (Trend Strategy)
# ---------------------------
def plot_trend_heatmap(df: pd.DataFrame, ticker: str):
    subset = df[
        (df["ticker"] == ticker) &
        (df["strategy"] == "sma_trend")
    ]

    pivot = subset.pivot_table(
        values="sharpe",
        index="sma_window",
        aggfunc="mean"
    )

    plt.figure()
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label="Sharpe Ratio")

    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xticks([])

    plt.title(f"{ticker} SMA Trend Sharpe Heatmap")
    plt.ylabel("SMA Window")

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / f"{ticker}_trend_heatmap.png")
    plt.close()


# ---------------------------
# 2. Heatmap (Crossover)
# ---------------------------
def plot_crossover_heatmap(df: pd.DataFrame, ticker: str):
    subset = df[
        (df["ticker"] == ticker) &
        (df["strategy"] == "sma_crossover")
    ]

    pivot = subset.pivot_table(
        values="sharpe",
        index="short_window",
        columns="long_window"
    )

    plt.figure()
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label="Sharpe Ratio")

    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xticks(range(len(pivot.columns)), pivot.columns)

    plt.xlabel("Long Window")
    plt.ylabel("Short Window")
    plt.title(f"{ticker} SMA Crossover Sharpe Heatmap")

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / f"{ticker}_crossover_heatmap.png")
    plt.close()


# ---------------------------
# 3. Best Strategy per Asset
# ---------------------------
def plot_best_strategies(df: pd.DataFrame):
    best = (
        df.sort_values(by="sharpe", ascending=False)
        .groupby("ticker")
        .head(1)
    )

    plt.figure()
    plt.bar(best["ticker"], best["sharpe"])

    plt.title("Best Strategy Sharpe by Asset")
    plt.ylabel("Sharpe Ratio")
    plt.xlabel("Ticker")

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "best_strategy_sharpe.png")
    plt.close()


# ---------------------------
# MAIN
# ---------------------------
def main():
    df = load_data()

    tickers = df["ticker"].unique()

    for ticker in tickers:
        print(f"Generating plots for {ticker}...")
        plot_trend_heatmap(df, ticker)
        plot_crossover_heatmap(df, ticker)

    plot_best_strategies(df)

    print(f"\nSaved plots to {PLOTS_DIR}")


if __name__ == "__main__":
    main()
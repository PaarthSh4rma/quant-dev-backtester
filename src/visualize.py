from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def load_data(backtest_file: Path) -> pd.DataFrame:
    df = pd.read_csv(backtest_file)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def compute_drawdown(series: pd.Series) -> pd.Series:
    running_max = series.cummax()
    return (series / running_max) - 1.0


def plot_price_and_sma(
    df: pd.DataFrame,
    plots_dir: Path,
    ticker: str,
    sma_window: int,
) -> None:
    plots_dir.mkdir(exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["close"], label="Close")
    plt.plot(df["date"], df[f"sma_{sma_window}"], label=f"SMA {sma_window}")
    plt.title(f"{ticker} Price vs {sma_window}-Day SMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / "price_vs_sma.png")
    plt.show()


def plot_cumulative_returns(
    df: pd.DataFrame,
    plots_dir: Path,
    strategy_name: str,
) -> None:
    plots_dir.mkdir(exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["cum_market"], label="Buy and Hold")
    plt.plot(df["date"], df["cum_strategy"], label=strategy_name)
    plt.title("Cumulative Returns: Strategy vs Buy-and-Hold")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / "cumulative_returns.png")
    plt.show()


def plot_drawdown(
    df: pd.DataFrame,
    plots_dir: Path,
    strategy_name: str,
) -> None:
    plots_dir.mkdir(exist_ok=True)

    df = df.copy()
    df["strategy_drawdown"] = compute_drawdown(df["cum_strategy"])
    df["market_drawdown"] = compute_drawdown(df["cum_market"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["market_drawdown"], label="Market Drawdown")
    plt.plot(df["date"], df["strategy_drawdown"], label=f"{strategy_name} Drawdown")
    plt.title("Drawdown: Strategy vs Market")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plots_dir / "drawdown.png")
    plt.show()
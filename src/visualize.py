import matplotlib.pyplot as plt
import pandas as pd

from config import BACKTEST_FILE, PLOTS_DIR, SMA_WINDOW


def load_data() -> pd.DataFrame:
    df = pd.read_csv(BACKTEST_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def compute_drawdown(series: pd.Series) -> pd.Series:
    running_max = series.cummax()
    return (series / running_max) - 1.0


def print_sanity_checks(df: pd.DataFrame) -> None:
    days_in_market = int((df["position"] == 1).sum())
    total_days = len(df)

    strategy_final = df["cum_strategy"].dropna().iloc[-1]
    market_final = df["cum_market"].dropna().iloc[-1]

    print("\nSanity checks:")
    print(f"Total rows: {total_days}")
    print(f"Days in market: {days_in_market}")
    print(f"Pct days in market: {days_in_market / total_days:.2%}")
    print(f"Final cumulative market return: {market_final:.4f}")
    print(f"Final cumulative strategy return: {strategy_final:.4f}")


def plot_price_and_sma(df: pd.DataFrame) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["close"], label="Close")
    plt.plot(df["date"], df[f"sma_{SMA_WINDOW}"], label=f"SMA {SMA_WINDOW}")
    plt.title(f"AAPL Price vs {SMA_WINDOW}-Day SMA")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "price_vs_sma.png")
    plt.show()


def plot_cumulative_returns(df: pd.DataFrame) -> None:
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["cum_market"], label="Buy and Hold")
    plt.plot(df["date"], df["cum_strategy"], label="Strategy")
    plt.title("Cumulative Returns: Strategy vs Buy-and-Hold")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "cumulative_returns.png")
    plt.show()


def plot_drawdown(df: pd.DataFrame) -> None:
    df = df.copy()
    df["strategy_drawdown"] = compute_drawdown(df["cum_strategy"])
    df["market_drawdown"] = compute_drawdown(df["cum_market"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["market_drawdown"], label="Market Drawdown")
    plt.plot(df["date"], df["strategy_drawdown"], label="Strategy Drawdown")
    plt.title("Drawdown: Strategy vs Market")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "drawdown.png")
    plt.show()
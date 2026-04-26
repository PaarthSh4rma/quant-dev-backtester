from itertools import product
from pathlib import Path

import pandas as pd

from data_loader import download_stock_data, save_raw_data
from strategy import build_signals, load_price_data, select_signal
from backtester import (
    compute_returns,
    compute_positions,
    compute_strategy_returns,
    compute_cumulative_returns,
)
from metrics import calculate_metrics
from config import DATA_DIR
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

def run_single_backtest(
    ticker: str,
    start_date: str,
    strategy: str,
    sma_window: int,
    short_window: int,
    long_window: int,
) -> dict:
    raw_file = DATA_DIR / f"{ticker.lower()}_temp.csv"

    # Download once per run (can optimize later)
    df = download_stock_data(ticker=ticker, start=start_date)
    save_raw_data(df, raw_file)

    df = load_price_data(raw_file)

    df = build_signals(
        df,
        sma_window=sma_window,
        short_window=short_window,
        long_window=long_window,
    )

    df = select_signal(df, strategy_name=strategy)

    df = compute_returns(df)
    df = compute_positions(df)
    df = compute_strategy_returns(df)
    df = compute_cumulative_returns(df)

    metrics = calculate_metrics(
        daily_returns=df["strategy_returns"],
        cumulative_returns=df["cum_strategy"],
        label=strategy,
    )

    return {
        "strategy": strategy,
        "sma_window": sma_window,
        "short_window": short_window,
        "long_window": long_window,
        "total_return": metrics["total_return"],
        "annual_return": metrics["annualized_return"],
        "volatility": metrics["annualized_volatility"],
        "sharpe": metrics["sharpe_ratio"],
        "max_drawdown": metrics["max_drawdown"],
    }


def run_sma_trend_sweep(ticker: str, start_date: str) -> pd.DataFrame:
    results = []

    sma_windows = [10, 20, 30, 50, 100]

    for sma in sma_windows:
        print(f"Testing SMA Trend ({sma})")

        result = run_single_backtest(
            ticker=ticker,
            start_date=start_date,
            strategy="sma_trend",
            sma_window=sma,
            short_window=10,
            long_window=50,
        )

        results.append(result)

    return pd.DataFrame(results)


def run_sma_crossover_sweep(ticker: str, start_date: str) -> pd.DataFrame:
    results = []

    short_windows = [5, 10, 20]
    long_windows = [30, 50, 100]

    for short, long in product(short_windows, long_windows):
        if short >= long:
            continue

        print(f"Testing SMA Crossover ({short}, {long})")

        result = run_single_backtest(
            ticker=ticker,
            start_date=start_date,
            strategy="sma_crossover",
            sma_window=20,
            short_window=short,
            long_window=long,
        )

        results.append(result)

    return pd.DataFrame(results)


def main():
    ticker = "AAPL"
    start_date = "2020-01-01"

    print("\n=== Running SMA Trend Sweep ===")
    trend_df = run_sma_trend_sweep(ticker, start_date)

    print("\n=== Running SMA Crossover Sweep ===")
    crossover_df = run_sma_crossover_sweep(ticker, start_date)

    all_results = pd.concat([trend_df, crossover_df], ignore_index=True)

    # Sort by Sharpe (most important)
    all_results = all_results.sort_values(by="sharpe", ascending=False)

    print("\n=== Top Strategies by Sharpe ===")
    print(all_results.head(10))

    output_file = DATA_DIR / f"{ticker.lower()}_parameter_sweep.csv"
    all_results.to_csv(output_file, index=False)

    print(f"\nSaved results to {output_file}")


if __name__ == "__main__":
    main()
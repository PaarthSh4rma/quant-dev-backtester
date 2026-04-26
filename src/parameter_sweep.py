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
pd.set_option("display.width", 160)
pd.set_option("display.max_rows", 100)


def run_single_backtest(
    ticker: str,
    raw_file: Path,
    strategy: str,
    sma_window: int,
    short_window: int,
    long_window: int,
) -> dict:
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
        "ticker": ticker,
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


def run_sma_trend_sweep(ticker: str, raw_file: Path) -> pd.DataFrame:
    results = []
    sma_windows = [10, 20, 30, 50, 100]

    for sma in sma_windows:
        print(f"Testing {ticker} SMA Trend ({sma})")

        result = run_single_backtest(
            ticker=ticker,
            raw_file=raw_file,
            strategy="sma_trend",
            sma_window=sma,
            short_window=10,
            long_window=50,
        )

        results.append(result)

    return pd.DataFrame(results)


def run_sma_crossover_sweep(ticker: str, raw_file: Path) -> pd.DataFrame:
    results = []

    short_windows = [5, 10, 20]
    long_windows = [30, 50, 100]

    for short, long in product(short_windows, long_windows):
        if short >= long:
            continue

        print(f"Testing {ticker} SMA Crossover ({short}, {long})")

        result = run_single_backtest(
            ticker=ticker,
            raw_file=raw_file,
            strategy="sma_crossover",
            sma_window=20,
            short_window=short,
            long_window=long,
        )

        results.append(result)

    return pd.DataFrame(results)


def run_sweep_for_ticker(ticker: str, start_date: str) -> pd.DataFrame:
    print(f"\n==============================")
    print(f"Running sweep for {ticker}")
    print(f"==============================")

    raw_file = DATA_DIR / f"{ticker.lower()}_cached.csv"

    print(f"Downloading data for {ticker} once...")
    raw_df = download_stock_data(ticker=ticker, start=start_date)
    save_raw_data(raw_df, raw_file)

    print("\n=== Running SMA Trend Sweep ===")
    trend_df = run_sma_trend_sweep(ticker, raw_file)

    print("\n=== Running SMA Crossover Sweep ===")
    crossover_df = run_sma_crossover_sweep(ticker, raw_file)

    results = pd.concat([trend_df, crossover_df], ignore_index=True)
    return results


def print_top_results(all_results: pd.DataFrame) -> None:
    print("\n=== Top 15 Strategies by Sharpe ===")
    print(
        all_results.head(15)[
            [
                "rank",
                "ticker",
                "strategy",
                "sma_window",
                "short_window",
                "long_window",
                "annual_return",
                "volatility",
                "sharpe",
                "max_drawdown",
            ]
        ]
    )


def print_best_by_ticker(all_results: pd.DataFrame) -> None:
    print("\n=== Best Strategy Per Ticker ===")

    best_by_ticker = (
        all_results.sort_values(by="sharpe", ascending=False)
        .groupby("ticker")
        .head(1)
        .sort_values(by="sharpe", ascending=False)
    )

    print(
        best_by_ticker[
            [
                "ticker",
                "strategy",
                "sma_window",
                "short_window",
                "long_window",
                "annual_return",
                "volatility",
                "sharpe",
                "max_drawdown",
            ]
        ]
    )


def print_best_overall(all_results: pd.DataFrame) -> None:
    best = all_results.iloc[0]

    print("\n=== BEST OVERALL STRATEGY ===")
    print(f"Ticker: {best['ticker']}")
    print(f"Strategy: {best['strategy']}")
    print(f"SMA Window: {best['sma_window']}")
    print(f"Short/Long: {best['short_window']}/{best['long_window']}")
    print(f"Sharpe: {best['sharpe']:.4f}")
    print(f"Annual Return: {best['annual_return']:.2%}")
    print(f"Volatility: {best['volatility']:.2%}")
    print(f"Max Drawdown: {best['max_drawdown']:.2%}")


def main() -> None:
    tickers = ["AAPL", "MSFT", "GOOG", "SPY"]
    start_date = "2020-01-01"

    all_ticker_results = []

    for ticker in tickers:
        ticker_results = run_sweep_for_ticker(ticker, start_date)
        all_ticker_results.append(ticker_results)

    all_results = pd.concat(all_ticker_results, ignore_index=True)

    all_results = all_results.sort_values(by="sharpe", ascending=False).reset_index(drop=True)
    all_results["rank"] = range(1, len(all_results) + 1)

    print_top_results(all_results)
    print_best_by_ticker(all_results)
    print_best_overall(all_results)

    output_file = DATA_DIR / "multi_asset_parameter_sweep.csv"
    all_results.round(4).to_csv(output_file, index=False)

    print(f"\nSaved results to {output_file}")


if __name__ == "__main__":
    main()
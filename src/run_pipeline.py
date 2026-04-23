import argparse
from pathlib import Path

from config import (
    DATA_DIR,
    PLOTS_DIR,
    DEFAULT_LONG_SMA_WINDOW,
    DEFAULT_SHORT_SMA_WINDOW,
    DEFAULT_SMA_WINDOW,
    DEFAULT_START_DATE,
    DEFAULT_STRATEGY_NAME,
    DEFAULT_TICKER,
)
from data_loader import download_stock_data, save_raw_data
from strategy import build_signals, load_price_data, save_signals, select_signal
from backtester import (
    compute_cumulative_returns,
    compute_positions,
    compute_returns,
    compute_strategy_returns,
    load_signal_data,
    save_backtest,
)
from metrics import calculate_metrics, load_backtest_data, print_metrics_table
from visualize import load_data, plot_cumulative_returns, plot_drawdown, plot_price_and_sma


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run quant backtesting pipeline")

    parser.add_argument("--ticker", type=str, default=DEFAULT_TICKER)
    parser.add_argument("--start-date", type=str, default=DEFAULT_START_DATE)
    parser.add_argument(
        "--strategy",
        type=str,
        default=DEFAULT_STRATEGY_NAME,
        choices=["sma_trend", "sma_crossover"],
    )
    parser.add_argument("--sma-window", type=int, default=DEFAULT_SMA_WINDOW)
    parser.add_argument("--short-window", type=int, default=DEFAULT_SHORT_SMA_WINDOW)
    parser.add_argument("--long-window", type=int, default=DEFAULT_LONG_SMA_WINDOW)

    return parser.parse_args()


def build_file_paths(ticker: str) -> dict:
    ticker_lower = ticker.lower()
    return {
        "raw_data_file": DATA_DIR / f"{ticker_lower}_historical_data.csv",
        "signals_file": DATA_DIR / f"{ticker_lower}_signals.csv",
        "backtest_file": DATA_DIR / f"{ticker_lower}_backtest.csv",
        "plots_dir": PLOTS_DIR / ticker_lower,
    }


def validate_args(args: argparse.Namespace) -> None:
    if args.sma_window <= 0:
        raise ValueError("--sma-window must be > 0")

    if args.short_window <= 0 or args.long_window <= 0:
        raise ValueError("--short-window and --long-window must be > 0")

    if args.short_window >= args.long_window:
        raise ValueError("--short-window must be less than --long-window for crossover strategy")


def main() -> None:
    args = parse_args()
    validate_args(args)

    file_paths = build_file_paths(args.ticker)

    print("Configuration:")
    print(f"  ticker={args.ticker}")
    print(f"  start_date={args.start_date}")
    print(f"  strategy={args.strategy}")
    print(f"  sma_window={args.sma_window}")
    print(f"  short_window={args.short_window}")
    print(f"  long_window={args.long_window}")

    print("\nStep 1: Downloading raw market data...")
    raw_df = download_stock_data(ticker=args.ticker, start=args.start_date)
    save_raw_data(raw_df, file_paths["raw_data_file"])

    print("Step 2: Generating strategy signals...")
    signal_df = load_price_data(file_paths["raw_data_file"])
    signal_df = build_signals(
        signal_df,
        sma_window=args.sma_window,
        short_window=args.short_window,
        long_window=args.long_window,
    )
    signal_df = select_signal(signal_df, strategy_name=args.strategy)
    save_signals(signal_df, file_paths["signals_file"])

    print("Step 3: Running backtest...")
    backtest_df = load_signal_data(file_paths["signals_file"])
    backtest_df = compute_returns(backtest_df)
    backtest_df = compute_positions(backtest_df)
    backtest_df = compute_strategy_returns(backtest_df)
    backtest_df = compute_cumulative_returns(backtest_df)
    save_backtest(backtest_df, file_paths["backtest_file"])

    print("Step 4: Calculating performance metrics...")
    results_df = load_backtest_data(file_paths["backtest_file"])

    market_metrics = calculate_metrics(
        daily_returns=results_df["returns"],
        cumulative_returns=results_df["cum_market"],
        label="Buy & Hold",
    )

    strategy_label = args.strategy
    if args.strategy == "sma_trend":
        strategy_label = f"sma_trend({args.sma_window})"
    elif args.strategy == "sma_crossover":
        strategy_label = f"sma_crossover({args.short_window},{args.long_window})"

    strategy_metrics = calculate_metrics(
        daily_returns=results_df["strategy_returns"],
        cumulative_returns=results_df["cum_strategy"],
        label=strategy_label,
    )

    print_metrics_table([market_metrics, strategy_metrics])

    print("Step 5: Generating plots...")
    plot_df = load_data(file_paths["backtest_file"])
    plot_price_and_sma(
        plot_df,
        plots_dir=file_paths["plots_dir"],
        ticker=args.ticker,
        sma_window=args.sma_window,
    )
    plot_cumulative_returns(
        plot_df,
        plots_dir=file_paths["plots_dir"],
        strategy_name=strategy_label,
    )
    plot_drawdown(
        plot_df,
        plots_dir=file_paths["plots_dir"],
        strategy_name=strategy_label,
    )

    print(f"\nPipeline complete. Backtest output saved to {file_paths['backtest_file']}")
    print(f"Plots saved to {file_paths['plots_dir']}")


if __name__ == "__main__":
    main()
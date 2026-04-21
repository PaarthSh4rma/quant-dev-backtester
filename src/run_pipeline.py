from data_loader import download_stock_data, save_raw_data
from strategy import add_moving_average, add_signal, load_price_data, save_signals
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
from config import BACKTEST_FILE, RISK_FREE_RATE, SMA_WINDOW, START_DATE, TICKER


def main() -> None:
    print("Step 1: Downloading raw market data...")
    raw_df = download_stock_data(ticker=TICKER, start=START_DATE)
    save_raw_data(raw_df)

    print("Step 2: Generating strategy signals...")
    signal_df = load_price_data()
    signal_df = add_moving_average(signal_df, window=SMA_WINDOW)
    signal_df = add_signal(signal_df, ma_column=f"sma_{SMA_WINDOW}")
    save_signals(signal_df)

    print("Step 3: Running backtest...")
    backtest_df = load_signal_data()
    backtest_df = compute_returns(backtest_df)
    backtest_df = compute_positions(backtest_df)
    backtest_df = compute_strategy_returns(backtest_df)
    backtest_df = compute_cumulative_returns(backtest_df)
    save_backtest(backtest_df)

    print("Step 4: Calculating performance metrics...")
    results_df = load_backtest_data()

    market_metrics = calculate_metrics(
        daily_returns=results_df["returns"],
        cumulative_returns=results_df["cum_market"],
        label="Buy & Hold",
    )

    strategy_metrics = calculate_metrics(
        daily_returns=results_df["strategy_returns"],
        cumulative_returns=results_df["cum_strategy"],
        label="SMA Strategy",
    )

    print_metrics_table([market_metrics, strategy_metrics])

    print("Step 5: Generating plots...")
    plot_df = load_data()
    plot_price_and_sma(plot_df)
    plot_cumulative_returns(plot_df)
    plot_drawdown(plot_df)

    print(f"\nPipeline complete. Backtest output saved to {BACKTEST_FILE}")


if __name__ == "__main__":
    main()